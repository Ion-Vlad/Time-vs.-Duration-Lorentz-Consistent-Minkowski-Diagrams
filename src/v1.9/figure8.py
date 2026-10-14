import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

# --- Configuration ---
# Enable LaTeX rendering for professional fonts (Computer Modern)
import os

os.environ["PATH"] += os.pathsep + "/Library/TeX/texbin"
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Computer Modern Roman']
plt.rcParams['mathtext.fontset'] = 'custom'

# --- Parameters ---
c = 1.0
v = 0.8
gamma = 1 / np.sqrt(1 - v**2)

# --- Plot setup ---
fig, ax = plt.subplots(figsize=(6.6, 6.6))

# --- Limits ---
limit=16
x_vals = np.linspace(-2, limit, 400)
ax.set_xticks(range(-2, limit)); ax.set_yticks(range(-2, limit))

# --- S grid (grey) ---
for x in np.arange(-2, limit, 1):
    ax.plot([x, x], [-2, limit], color='lightgrey', linewidth=0.5)
for ct in np.arange(-2, limit, 1):
    ax.plot([-2, limit], [ct, ct], color='lightgrey', linewidth=0.5)

# --- S axes ---
ax.axhline(0, color='black')
ax.axvline(0, color='black')

# --- S' axes ---
# ct' axis: x = vt → ct = x/v
ct_axis = (1/v) * x_vals
ax.plot(x_vals, ct_axis, color='red', linewidth=2, label="$ct$'")

# x' axis: ct = v x
x_axis = v * x_vals
ax.plot(x_vals, x_axis, color='red', linestyle='dotted', linewidth=2, label="$x'$")

# --- S' grid (correct Lorentz construction) ---

k_vals = np.arange(-30, 30, 1)
# constant ct' lines: ct - v x = k/gamma → ct = v x + k/gamma
for k in k_vals:
    ct_line = v * x_vals + k / gamma
    ax.plot(x_vals, ct_line, color='pink', linewidth=0.5)

# constant x' lines: x - v ct = k/gamma → ct = (x - k/gamma)/v
for k in k_vals:
    ct_line = (x_vals - k / gamma) / v
    ax.plot(x_vals, ct_line, color='teal', linewidth=0.5)

# --- Events in S ---
ax.plot(5, 0, 'o', color='blue', ms=8, zorder=5, label='Garage in the rest frame')
ax.text(4.9,  -0.8,r"$\mathbf{G}$", color='blue')
ax.plot(6, 0, 'o', color='red', ms=8, zorder=6, label='Ladder in the rest frame')
ax.text(5.7, -0.8,r"$\mathbf{L}$", color='red')

# --- Events in S' ---
#ax.plot(5, 4, 'o', markerfacecolor='white', markeredgecolor='blue', ms=8,
#        markeredgewidth=2, zorder=5, label='Garage in the moving frame')
#ax.text(5.5,  3.8, r"$\mathbf{G'(x' = 3, ct' = 0)}$", color='blue')
ax.plot(10, 8, 'o', markerfacecolor='white', markeredgecolor='red', ms=8,
        markeredgewidth=2, zorder=6, label='Ladder in the moving frame')
ax.text(10.3, 7.3,r"$\mathbf{L'(x'=6, ct'=0)}$", color='red')
        #path_effects=[pe.withStroke(linewidth=1, foreground='k')])

# --- Projections ---
#ax.plot(3, 0, 'o', markerfacecolor='cyan', markeredgecolor='blue',
#    markeredgewidth=2, ms=8, zorder=5, label="Projection of G' onto the $x$ axis")
#ax.text(2.8,  -0.6,"$G'_P$", color='blue', fontweight='bold')
ax.plot(3.6, 0, 'o', markerfacecolor='cyan', markeredgecolor='red',
    markeredgewidth=2, ms=8, zorder=6, label="Projection of L' onto the $x$ axis")
ax.text(3.15, -0.8,r"$\mathbf{L'_P}$", color='red')
#ax.text(1, -1.2,r"$\mathbf{raw L'_P(x=3.6, ct=0)}$", color='red')
#ax.text(1, -1.8,r"$\mathbf{L'_P(x=6, ct=0)\ after\ correction}$", color='red')
# --- Formatting ---
ax.set_xlim(-2, limit)
ax.set_ylim(-2, limit)
ax.set_aspect('equal')
ax.set_xlabel("x")
ax.set_ylabel("ct")
ax.legend(loc='lower right', framealpha=0.9, shadow=True, fancybox=True)

text_content = (
    r"$\mathbf{Coordinates\ in\ frame\ S:}$" "\n"
    r"$\bullet$ G (x = 5, ct = 0) $\leftrightarrow$ (x' = 8.35, ct' = 0)" "\n"
    r"$\bullet$ L (x = 6, ct = 0) $\leftrightarrow$ (x' = 10, ct' = 0)" "\n"
    r"Raw projections need to be corrected as follows: the projection of "  
    r"$L'_P$ onto the" "\n" "$x$-axis is equal to the raw $x$-value multiplied by "
    r"$\gamma$, because the Lorentz factor is" "\n" "embedded only in frame S'."
    r"$\quad$ $\displaystyle \gamma = \frac{5}{3} \approx 1.67$" "\n"
#    r"$\bullet$ $G'_P$ $(x = 3 \times \gamma = 5)$" "\n"
    r"$\bullet$ $L'_{P(corrected)}$ $(x = 3.6 \times 1.67 = 6)$" "\n" "\n"
    r"$\mathbf{Note:}$ All coordinates are given in units (grid divisions). "
    r"Unprimed units refer to " "\n" "frame S, and primed units to frame S'. " 
    r"These are two different systems and are " "\n" "not interchangeable. "
    r"Coordinates from different frames cannot be compared without " "\n" "a Lorentz "
    r"transformation."
    )
ax.text(0.02, 0.635, text_content, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=1, pad=0.5),
        fontfamily='serif') # Optional: force serif font for consistency

# Save and Show
plt.tight_layout()
plt.title("Ladder paradox in a Lorentz-Consistent Minkowski Diagram ($v = 0.8c$)")
plt.savefig('figure8.png', dpi=300, bbox_inches='tight')
plt.show()
