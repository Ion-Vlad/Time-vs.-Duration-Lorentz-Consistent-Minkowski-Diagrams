#######################################################
#   Copyright 2026 Ion Vlad     contact@ionvlad.com   #
# Licensed under the Creative Commons Attribution 4.0 #
#        International License (CC BY 4.0)            #
# https://creativecommons.org/licenses/by/4.0/        #
#######################################################
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.transforms import Affine2D

# --- Configuration ---
# Enable LaTeX rendering for professional fonts (Computer Modern)
# THIS MAY SLOW DOWN THE DRAGGING!!!

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

# --- Horizontal shear angle ---
# Shear LEFT by 38.7° so the ct' axis becomes vertical
# For a horizontal shear x' = x + k y, verticalizing the ct' axis
# requires k = -1/m where m = 1/v.
shear_angle_deg = 38.7
shear_factor = -v
shear_enabled = False
shear_title = ""
dragging_text = False

# --- Event coordinates ---
x_A = 5   # event A(5, ct)
ct_A = 3  # event A(x, 3)
x_B = 3   # event B(3, ct)
ct_B = 1  # event B(x, 1)

# --- Lorentz transform ---
def lorentz_transform(x, ct):
    t = ct / c
    t_prime = gamma * (t - v * x / c**2)
    x_prime = gamma * (x - v * t)
    return x_prime, c * t_prime

# --- Plot setup ---
fig, ax = plt.subplots(figsize=(11, 8))
title = plt.title("Non-Simultaneity in Minkowski diagram")
plt.subplots_adjust(left=0.07, right=0.72, bottom=0.14, top=0.92)

# --- Shear transform ---
shear_transform = Affine2D().from_values(1, 0, shear_factor, 1, 0, 0)
normal_transform = Affine2D()

# Keep references to all artists that should be transformed
transformable_artists = []

def apply_current_transform():
    """Apply either the normal or sheared transform."""
    current_transform = (
        shear_transform + ax.transData
        if shear_enabled
        else normal_transform + ax.transData
    )
    for artist in transformable_artists:
        artist.set_transform(current_transform)

    fig.canvas.draw_idle()

def toggle_shear(event):
    global shear_enabled, shear_title
    shear_enabled = not shear_enabled
    if shear_enabled:
        shear_title = " - Shear: 38.7° ($v=0.8c$)"
        textbox_sim.set_visible(True)
        btn_shear.label.set_text('Normal View')
    else:
        shear_title = ""
        textbox_sim.set_visible(False)
        btn_shear.label.set_text('Sheared View')
        
    apply_current_transform()
    update(None)

def save_figure(event):
    filename = f"{title.get_text()}.png"
    fig.savefig(filename, dpi=300, bbox_inches="tight")

    save_message.set_text(f"Image saved as: {filename}")
    save_message.set_visible(True)
    fig.canvas.draw_idle()

    timer = fig.canvas.new_timer(interval=3000)

    def hide_message():
        save_message.set_visible(False)
        fig.canvas.draw_idle()
        timer.stop()

    timer.add_callback(hide_message)
    timer.start()
    
# --- Mouse dragging support ---
dragging_point = None

def get_distance(x1, y1, x2, y2):
    return np.hypot(x1 - x2, y1 - y2)

def on_press(event):
    global dragging_point
    global dragging_text

    dragging_point = None
    dragging_text = False

    if event.inaxes != ax:
        return

    contains, _ = star_message.contains(event)
    if contains:
        dragging_text = True
        return

    if event.xdata is None or event.ydata is None:
        return

    dA = get_distance(event.xdata, event.ydata, x_A, ct_A)
    dB = get_distance(event.xdata, event.ydata, x_B, ct_B)

    threshold = 1.0

    if dA < threshold:
        dragging_point = "A"
    elif dB < threshold:
        dragging_point = "B"
        
def on_motion(event):
    global x_A, ct_A, x_B, ct_B

    if event.inaxes != ax:
        return
    if event.xdata is None or event.ydata is None:
        return

    if dragging_text:
        x_axes, y_axes = ax.transAxes.inverted().transform((event.x, event.y))
        star_message.set_position((x_axes, y_axes))
        fig.canvas.draw_idle()
        return

    if dragging_point is None:
        return

    raw_x = round(event.xdata)
    raw_y = round(event.ydata)

    if not (-9 <= raw_x <= 9):
        warning_text.set_text("x_A and x_B must stay between -9 and 9")
        fig.canvas.draw_idle()
        return

    if not (-9 <= raw_y <= 9):
        warning_text.set_text("ct_A and ct_B must stay between -9 and 9")
        fig.canvas.draw_idle()
        return

    # Transformed coordinates
    x_Ap, ct_Ap = solve_event(v, gamma, raw_y, raw_x)
    margin = 2   # make sure the coordinate label stays inside the diagram
    inside_square = (
        -limit + margin <= x_Ap <= limit - margin and
        -limit + margin <= ct_Ap <= limit - margin
    )
    if inside_square:
        warning_text.set_text("")
        if dragging_point == 'A':
            x_A = raw_x
            ct_A = raw_y
        elif dragging_point == 'B':
            x_B = raw_x
            ct_B = raw_y

        update(None)
    else:
        warning_text.set_text("A' and B' must remain inside the diagram")

    fig.canvas.draw_idle()

def solve_event(v, gamma, ct_prime, x_prime):
    A = np.array([[-v, 1], [ 1, -v]])

    b = np.array([ct_prime / gamma, x_prime / gamma])
    
    solution = np.linalg.solve(A, b)
    x, ct = solution
    return x, ct

def on_release(event):
    global dragging_point
    global dragging_text
    dragging_point = None
    dragging_text = False
    
# --- Connect mouse events ---
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

# --- Limits ---
limit = 20
x_vals = np.linspace(-limit, limit, 400)

# --- S grid (grey) ---
for x in np.arange(-limit, limit +1, 1):
    line, = ax.plot([x, x], [-limit, limit], color='lightgrey', linewidth=0.5)
    transformable_artists.append(line)

for ct in np.arange(-limit, limit, 1):
    line, = ax.plot([-limit, limit], [ct, ct], color='lightgrey', linewidth=0.5)
    transformable_artists.append(line)

# --- S axes ct vertical ---
# we use limit +/- 3 to avoid overlapping with textbox when shear_enabled is true
line, = ax.plot([0, 0], [-limit + 3, limit - 3], color='black', label="$ct$")
transformable_artists.append(line)
# keep symmetry with ct axis
line, = ax.plot([-limit + 3, limit - 3], [0, 0], color='black', linestyle='dotted',
                label="$x$")
transformable_artists.append(line)

# --- S' axes ---
# ct' axis: x = vt → ct = x/v
ct_axis = (1/v) * x_vals
line_ctp, = ax.plot(x_vals, ct_axis, color='red', linewidth=2, label="$ct'$")
transformable_artists.append(line_ctp)

# x' axis: ct = v x
x_axis = v * x_vals
line_xp, = ax.plot(x_vals, x_axis, color='red', linestyle='dotted', linewidth=2,
                label="$x'$")
transformable_artists.append(line_xp)

# --- S' grid (correct Lorentz construction) ---
k_vals = np.arange(-8, 9, 1)

# constant ct' lines: ct - v x = k/gamma → ct = v x + k/gamma
for k in k_vals:
    ct_line = v * x_vals + k / gamma
    line, = ax.plot(x_vals, ct_line, color='pink', linewidth=0.5)
    transformable_artists.append(line)

# constant x' lines: x - v ct = k/gamma → ct = (x - k/gamma)/v
for k in k_vals:
    ct_line = (x_vals - k / gamma) / v
    line, = ax.plot(x_vals, ct_line, color='pink', linewidth=0.5)
    transformable_artists.append(line)

# --- Update points A, B, A' and B' ---
def update(val):
    global x_A, ct_A, x_B, ct_B
    # Update A
    point_A.set_data([x_A], [ct_A])
    label_A.set_position((x_A - 0.5, ct_A - 1))
    label_A.set_text(f"A({x_A:.0f}, {ct_A:.0f})")
    # Update B
    point_B.set_data([x_B], [ct_B])
    label_B.set_position((x_B - 0.5, ct_B - 1))
    label_B.set_text(f"B({x_B:.0f}, {ct_B:.0f})")
    # Transform A → A' (Ap short for A')
    
    # The draggable coordinates are defined on the transformed S' grid. We therefore
    # use solve_event(...) to convert them into the underlying Matplotlib plotting
    # coordinates used to place A' and B'.
    x_Ap, ct_Ap = solve_event(v, gamma, ct_A, x_A)
    point_Ap.set_data([x_Ap], [ct_Ap])
    label_Ap.set_position((x_Ap - 0.5, ct_Ap - 1))
    # The labels use the coordinates of A' and B' in the transformed S' grid.
    # The variables x_A and x_B are grid coordinates, while x_Ap and x_Bp are
    # the corresponding plotting coordinates.
    label_Ap.set_text(f"A'({x_A:.0f}, {ct_A:.0f})")

    # Transform B → B' (Bp short for B')
    x_Bp, ct_Bp = solve_event(v, gamma, ct_B, x_B)
    point_Bp.set_data([x_Bp], [ct_Bp])
    label_Bp.set_position((x_Bp - 0.5, ct_Bp - 1))
    label_Bp.set_text(f"B'({x_B:.0f}, {ct_B:.0f})")
    # Update simultaneity lines
    # 1. Simultaneity line in S'
    ct_line_sim = v * x_vals + ct_A / gamma
    ct_line_sim_plot.set_data(x_vals, ct_line_sim)
    
    # show ONLY if ct_A == ct_B → simultaneity
    if abs(ct_A - ct_B) < 1e-6:   # robust float comparison
        ct_P = ct_A / gamma
        """Since point of intersection (P) resides in S but represents the
            projection of point A' or B', whose Lorentz transformation is already
            embedded in the grid, and since the script applies shearing
            globally, we must recalculate the ct_P coordinate when
            shear_enabled is true (undo Lorentz transformation). Alternatively,
            we can simply use the ct or ct' coordinates of A, B, A', or B', since
            they are all equal, so ct_P = ct_A / gamma  becomes ct_P = ct_A."""
        x_P = 0  # intersection point always on ct-axis
        if shear_enabled:
            ct_P = ct_A
            point_ct_intersection_b.set_data([x_P], [ct_P])
            point_ct_intersection.set_data([x_P], [ct_P])
            label_ct_intersection.set_position((-5.4, ct_P - 1))
            label_ct_intersection.set_text(f"P(0, {ct_P:.1f})")
        else: # ct_intersection coordinate unchanged
            point_ct_intersection_b.set_data([x_P], [ct_P])
            point_ct_intersection.set_data([x_P], [ct_P])
            label_ct_intersection.set_position((-4.5, ct_P - 1))
            label_ct_intersection.set_text(f"P(0, {ct_P:.1f})")

        point_ct_intersection.set_visible(True)
        point_ct_intersection_b.set_visible(True)
        label_ct_intersection.set_visible(True)
        
        star_message.set_position(default_textbox_pos)
        star_message.set_visible(True)
        star_message.set_text("The temporal coordinate of the intersection point "
                "$P$ is identical to" "\n" " the temporal coordinate of $A'$ or $B'$."
                " Because the Lorentz" "\n" "transformation is embedded in the "
                "$S'$ grid but is not applied to the " "\n" "$S$ grid, $P$ appears "
                "on the $ct$-axis with coordinate "
                rf"${{ct_P}} = \frac{{ct'_{{A'}}}}{{\gamma}} = {ct_A/gamma:.1f}$. "
                "\n" rf"$P$(0, {ct_A/gamma:.1f}) instead of $P$(0, {ct_A:.1f})."
                "\n" "(The temporal coordinate shown here is rounded to one decimal "
                "place.)" "\n" "Therefore, a correction must be applied to the $ct$ "
                "coordinate. " "\n" "This correction becomes apparent after shearing"
                rf" $P$(0, {ct_A:.1f})." "\n"
                r"$\mathbf{You\ can\ drag\ this\ text\ box\ to\ a\ more\ "
                r"convenient\ place.}$")
        ct_line_sim_plot.set_visible(True)
        title.set_text("Simultaneity in Minkowski diagram" + shear_title)
    else:
        point_ct_intersection.set_visible(False)
        point_ct_intersection_b.set_visible(False)
        label_ct_intersection.set_visible(False)
        star_message.set_visible(False)
        star_message.set_text("")
        ct_line_sim_plot.set_visible(False)
        title.set_text("Non-Simultaneity in Minkowski diagram" + shear_title)
    # 2. Simultaneity line in S
    # Show ONLY if ct_A == ct_E, ct_B == ct_E or ct_A == ct_B → simultaneity
    if ct_A == 4 or ct_B == 4 or ct_A == ct_B:
        if ct_B == 4:  # ct_B == ct_E
            line_sim_ABE.set_data([-limit, limit], [ct_B, ct_B])
        else:   # ct_A == ct_E or ct_A == ct_B
            line_sim_ABE.set_data([-limit, limit], [ct_A, ct_A])
        line_sim_ABE.set_visible(True)
    else:
        line_sim_ABE.set_visible(False)

    fig.canvas.draw_idle()

# --- Draw simultaneity lines ---
# 1. Simultaneity line in S
line_sim, = ax.plot([-limit, limit], [9, 9], color='lightgreen', linestyle='--',
            linewidth=2, label="Simultaneity line in S")
transformable_artists.append(line_sim)
# 2. Simultaneity line in S'
ct_line_sim_plot, = ax.plot([], [], color='cyan', linestyle='--', linewidth=2,
            label="Simultaneity line in S'")

transformable_artists.append(ct_line_sim_plot)
# 3. Events in S: C and D are simultaneous, while E is not
# simultaneity line in S for event A, B and E
line_sim_ABE, = ax.plot([], [], color='lightgreen', linestyle='--', linewidth=2)
transformable_artists.append(line_sim_ABE)

point_C, = ax.plot(1, 9, 'o', color='lightgreen')
transformable_artists.append(point_C)
label_C = ax.text(0.5, 8, "C(1, 9)")
transformable_artists.append(label_C)
point_D, = ax.plot(13, 9, 'o', color='lightgreen')
transformable_artists.append(point_D)
label_D = ax.text(12.5, 8, "D(13, 9)")
transformable_artists.append(label_D)
point_E, = ax.plot(14, 4, 'o', color='cyan')
transformable_artists.append(point_E)
label_E = ax.text(13.5, 3, "E(14, 4)")
transformable_artists.append(label_E)

# --- Initial plot objects (will be updated) ---
point_A, = ax.plot(x_A, ct_A, 'bo') # A in S
transformable_artists.append(point_A)
label_A = ax.text(x_A, ct_A, "")
transformable_artists.append(label_A)

point_B, = ax.plot(x_B, ct_B, 'bo') # B in S
transformable_artists.append(point_B)
label_B = ax.text(x_B, ct_B, "")
transformable_artists.append(label_B)

point_Ap, = ax.plot([], [], 'ro') # A' in S'
transformable_artists.append(point_Ap)
label_Ap = ax.text(0, 0, "")
transformable_artists.append(label_Ap)

point_Bp, = ax.plot([], [], 'ro') # B' in S'
transformable_artists.append(point_Bp)
label_Bp = ax.text(0, 0, "")
transformable_artists.append(label_Bp)

# --- Intersection of simultaneity line (A'B') with ct-axis ---
# first we draw a black background for star
point_ct_intersection_b, = ax.plot([], [], color='black', marker='o', markersize=12)
# the star
point_ct_intersection, = ax.plot([], [], color='orange', marker='*', markersize=10)
transformable_artists.append(point_ct_intersection_b)
transformable_artists.append(point_ct_intersection)
label_ct_intersection = ax.text(0, 0, "")
transformable_artists.append(label_ct_intersection)

# --- Formatting ---
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_aspect('equal')

# --- Legend ---
ax.legend(bbox_to_anchor=(1.01, 1), fontsize=11, frameon=True, shadow=True)

# Show popup message after save image
save_message = ax.text(0.5, 0.1, "", transform=ax.transAxes, zorder=100, fontsize=11,
            color="blue", ha="center", va="bottom", bbox=dict(boxstyle="round",
            facecolor="white", alpha=1))
save_message.set_visible(False)

# Show message when point of intersection (orange star) is visible
star_message = ax.text(0.5, 0.1, "", transform=ax.transAxes, zorder=10,
        fontsize=12, color="black", ha="center", va="bottom",
        bbox=dict(boxstyle="round", facecolor="cyan", alpha=0.8))
default_textbox_pos = (0.5, 0.1)
star_message.set_visible(False)

# --- Warning Textbox for A and B ---
warning_text = ax.text(0.5, 0.985, "", transform=ax.transAxes, fontsize=11,
    color='red', ha='center', va='top', bbox=dict(boxstyle='round',
    facecolor='white', alpha=0.8))

# --- Textbox ----
text_key_content = (
    r"Key features:" "\n"
    r"$\bullet$ $\mathbf{Drag\ point\ A\ or\ B\ with\ the\ mouse}$" "\n"
    r"          (only in Normal View mode)" "\n" "\n"
    r"$\bullet$ A($x, ct$) - an event in S" "\n"
    r"$\bullet$ B($x, ct$) - an event in S" "\n"
    r"$\bullet$ A'($x', ct'$) - an event in S'" "\n"
    r"$\bullet$ B'($x', ct'$) - an event in S'" "\n\n"
    r"$\bullet$ C and D - simultaneous events in S" "\n"
    r"$\bullet$ E - an arbitrary event in S" "\n\n"
    r"$\bullet$ When $ct_A$ = $ct_B$, the events" "\n" "are simultaneous." "\n"
    r"$\bullet$ Orange star (P): projection of the $ct'$" "\n"
                "coordinate onto the $ct$-axis")

textbox_key = ax.text(1.03, 0.2, text_key_content, transform=ax.transAxes,
    fontsize=10, verticalalignment='bottom', bbox=dict(boxstyle='round',
    facecolor='wheat', alpha=0.6, pad=0.5), fontfamily='serif')

# Simultaneity textbox
text_sim_content = (r"Simultaneity is preserved after shearing. The simultaneity "
                r"lines are, in fact, $\mathbf{observational\ hypersurfaces}$." "\n" 
                r"The $\mathbf{simultaneity\ frame}$ is preserved across reference "
                r"frames. $\mathbf{The\ two\ should\ not\ be\ conflated.}$")
textbox_sim = ax.text(0.015, 0.02, text_sim_content, transform=ax.transAxes, fontsize=8,
        horizontalalignment='left', bbox=dict(boxstyle='round',
        facecolor='lightblue', alpha=0.4))
textbox_sim.set_visible(False)
# --- Save button ---
ax_save = plt.axes([0.85, 0.15, 0.07, 0.05])
btn_save = Button(ax_save, 'Save')
btn_save.on_clicked(save_figure)

# --- Shear toggle button ---
ax_shear = plt.axes([0.7, 0.15, 0.14, 0.05])
btn_shear = Button(ax_shear, 'Sheared View')
btn_shear.on_clicked(toggle_shear)

# --- Apply initial transform ---
apply_current_transform()

# --- Show ---
update(None)
plt.show(block=True)
