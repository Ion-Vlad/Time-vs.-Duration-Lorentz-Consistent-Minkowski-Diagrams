import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.widgets import Button

# --- Configuration ---
# Enable LaTeX rendering for professional fonts (Computer Modern)
# THIS WILL SLOW DOWN THE SLIDERS!!!

#import os

#os.environ["PATH"] += os.pathsep + "/Library/TeX/texbin"
#plt.rcParams['text.usetex'] = True
#plt.rcParams['font.family'] = 'serif'
#plt.rcParams['font.serif'] = ['Computer Modern Roman']
#plt.rcParams['mathtext.fontset'] = 'custom'

# --- Parameters ---
c = 1.0
v = 0.8
gamma = 1 / np.sqrt(1 - v**2)

# --- Slider setup ---
Ax = 5   # event A(5, ct)
Act = 3  # event A(x, 3)
Bx = 6   # event B(6, ct)
Bct = 4  # event B(x, 4)

# --- Lorentz transform ---
def lorentz_transform(x, ct):
    t = ct / c
    t_prime = gamma * (t - v * x / c**2)
    x_prime = gamma * (x - v * t)
    return x_prime, c * t_prime

# --- Plot setup ---
fig, ax = plt.subplots(figsize=(7,7))
title = plt.title("Non-Simultaneity_in_Minkowski_diagram") 
plt.subplots_adjust(bottom=0.25)

def save_figure(event):
    fig.savefig(f"{title.get_text()}.png", dpi=300, bbox_inches='tight')
    print (f"{title.get_text()}.png")
    
# --- create sliders ---
ax_Ax = plt.axes([0.12, 0.15, 0.3, 0.03])
ax_Act = plt.axes([0.12, 0.1, 0.3, 0.03])
ax_Bx = plt.axes([0.6, 0.15, 0.3, 0.03])
ax_Bct = plt.axes([0.6, 0.1, 0.3, 0.03])

slider_Ax = Slider(ax_Ax, 'Ax', -6, 7, valinit=Ax, valstep=1)
slider_Act = Slider(ax_Act, 'Act', -6, 5, valinit=Act, valstep=1)
slider_Bx = Slider(ax_Bx, 'Bx', -6, 8, valinit=Bx, valstep=1)
slider_Bct = Slider(ax_Bct, 'Bct', -6, 5, valinit=Bct, valstep=1)

# --- Limits ---
limit=20
x_vals = np.linspace(-20, 20, 400)

# --- S grid (grey) ---
for x in np.arange(-20, 21, 1):
    ax.plot([x, x], [-20, 20], color='lightgrey', linewidth=0.5)
for ct in np.arange(-20, 21, 1):
    ax.plot([-20, 20], [ct, ct], color='lightgrey', linewidth=0.5)

# --- S axes ct vertical ---
ax.axhline(0, color='black')
ax.axvline(0, color='black')

# --- S' axes ---
# ct' axis: x = vt → ct = x/v
ct_axis = (1/v) * x_vals
ax.plot(x_vals, ct_axis, color='red', linewidth=2, label="$ct'$")

# x' axis: ct = v x
x_axis = v * x_vals
ax.plot(x_vals, x_axis, color='red', linestyle='dotted', linewidth=2, label="$x'$")

# --- S' grid (correct Lorentz construction) ---
k_vals = np.arange(-8, 9, 1)
# constant ct' lines: ct - v x = k/gamma → ct = v x + k/gamma
for k in k_vals:
    ct_line = v * x_vals + k / gamma
    ax.plot(x_vals, ct_line, color='pink', linewidth=0.5)

# constant x' lines: x - v ct = k/gamma → ct = (x - k/gamma)/v
for k in k_vals:
    ct_line = (x_vals - k / gamma) / v
    ax.plot(x_vals, ct_line, color='pink', linewidth=0.5)

# --- Update sliders ---
def update(val):
    Ax = slider_Ax.val
    Act = slider_Act.val
    Bx = slider_Bx.val
    Bct = slider_Bct.val

    # Update A
    point_A.set_data([Ax], [Act])
    label_A.set_position((Ax - 1, Act - 1.5))
    label_A.set_text(f"A({Ax:.0f}, {Act:.0f})")

    # Update B
    point_B.set_data([Bx], [Bct])
    label_B.set_position((Bx - 1, Bct - 1.5))
    label_B.set_text(f"B({Bx:.0f}, {Bct:.0f})")

    # Transform A → A'
    xAp, ctAp = solve_event(v, gamma, Act, Ax)
    point_Ap.set_data([xAp], [ctAp])
    label_Ap.set_position((xAp - 1, ctAp - 1.5))
    label_Ap.set_text(f"A'({Ax:.0f}, {Act:.0f})")

    # Transform B → B'
    xBp, ctBp = solve_event(v, gamma, Bct, Bx)
    point_Bp.set_data([xBp], [ctBp])
    label_Bp.set_position((xBp - 1, ctBp - 1.5))
    label_Bp.set_text(f"B'({Bx:.0f}, {Bct:.0f})")

    # Update simultaneity line
    ct_line_sim = v * x_vals + Act / gamma
    ct_line_sim_plot.set_data(x_vals, ct_line_sim)

    # show ONLY if Act == Bct → simultaneity
    if abs(Act - Bct) < 1e-6:   # robust float comparison
        ct_line_sim_plot.set_visible(True)
        title.set_text("Simultaneity_in_Minkowski_diagram")
    else:
        ct_line_sim_plot.set_visible(False)
        title.set_text("Non-Simultaneity_in_Minkowski_diagram")
fig.canvas.draw()

# --- Draw simultaneity line ---
ct_line_sim_plot, = ax.plot([], [], color='cyan', linestyle='--', linewidth=2, label="Simultaneity line")

# --- Initial plot objects (will be updated) ---
point_A, = ax.plot(Ax, Act, 'bo')
label_A = ax.text(Ax, Act, "")

point_B, = ax.plot(Bx, Bct, 'bo')
label_B = ax.text(Bx, Bct, "")

point_Ap, = ax.plot([], [], 'ro')
label_Ap = ax.text(0, 0, "")

point_Bp, = ax.plot([], [], 'ro')
label_Bp = ax.text(0, 0, "")


def solve_event(v, gamma, ct_prime, x_prime):
    A = np.array([[-v, 1],
                  [ 1, -v]])
    
    b = np.array([ct_prime / gamma, x_prime / gamma])
    
    solution = np.linalg.solve(A, b)
    x, ct = solution
    return x, ct

# --- Formatting ---
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_aspect('equal')
ax.set_xlabel("x")
ax.set_ylabel("ct")
ax.legend()

#--- Textbox ----
text_content = (
    r"Key Features:" "\n"
    r"$\bullet$ Event A($x, ct$) in S" "\n"
    r"$\bullet$ Event B($x, ct$) in S" "\n"
    r"$\bullet$ Event A'($x', ct'$) in S'" "\n"
    r"$\bullet$ Event B'($x', ct'$) in S'" "\n\n" 
    r"$\bullet$ When A($ct$) = B($ct$), the" "\n" "events are simultaneous")
ax.text(0.02, 0.6, text_content, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6, pad=0.5),
        fontfamily='serif') # Optional: force serif font for consistency

# --- Save button ---
ax_save = plt.axes([0.47, 0.09, 0.07, 0.05])
btn_save = Button(ax_save, 'Save')
btn_save.on_clicked(save_figure)

# --- Connect sliders -----
slider_Ax.on_changed(update)
slider_Act.on_changed(update)
slider_Bx.on_changed(update)
slider_Bct.on_changed(update)

# --- Show ---
plt.tight_layout()
update(None)
plt.show(block=True)
