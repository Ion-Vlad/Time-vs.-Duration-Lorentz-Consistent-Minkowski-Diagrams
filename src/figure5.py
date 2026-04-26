import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
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

# Shear parameters
shear_factor = v

# --- Shear Transformation Function ---
def shear_point(x, y, shear_factor):
    """
    Apply horizontal shear: x shifts left as y increases.
    x_new = x - y * shear_factor
    y_new = y
    """
    x_new = x - y * shear_factor
    y_new = y
    return x_new, y_new

# --- Lorentz transform ---
def lorentz_transform(x, ct):
    t = ct / c
    t_prime = gamma * (t - v * x / c**2)
    x_prime = gamma * (x - v * t)
    return x_prime, c * t_prime

# --- Plot setup ---
fig, ax = plt.subplots(figsize=(7,7))

# Define original coordinate bounds
x_min_orig, x_max_orig = -2, 8
y_min_orig, y_max_orig = -1, 10
# --- Limits ---
limit = 16
x_vals = np.linspace(-16, 16, 400)

# --- S Grid (Grey) - FULLY SHEARED ---
# Vertical lines (x = constant)
for x in np.arange(-10, 11, 1):
    y_vals = np.linspace(-10, 10, 100)
    x_s, y_s = shear_point(np.full_like(y_vals, x), y_vals, shear_factor)
    ax.plot(x_s, y_s, color='lightgrey', linewidth=0.5)

# Horizontal lines (ct = constant)
for ct in np.arange(-10, 11, 1):
    if ct == 0:
        # EXCEPT x-axis (ct=0): Keep it straight and unsheared
        ax.plot([-10, 10], [ct, ct], color='lightgrey', linewidth=0.5)
    else:
        # Apply shear to horizontal grid lines
        x_start, ct_start = -10, ct
        x_end, ct_end = 10, ct
        
        x_start_s, ct_start_s = shear_point(x_start, ct_start, shear_factor)
        x_end_s, ct_end_s = shear_point(x_end, ct_end, shear_factor)
        
        ax.plot([x_start_s, x_end_s], [ct_start_s, ct_end_s], color='lightgrey', linewidth=0.5)

# --- S axes ---
ax.axhline(0, color='black', linewidth=1.5)  # x-axis (UNsheared - preserved)
ax.axvline(0, color='black', linewidth=1.5)  # ct-axis (will be sheared below)

# Shear the ct-axis (vertical line at x=0)
#ct_axis_vals = np.linspace(-10, 10, 100)   ORIGINAL ct line length
ct_axis_vals = np.linspace(-6, 6, 100)  # NEW ct line shortened to avoid legend overlap
x_ct, ct_ct = 0, ct_axis_vals
x_ct_s, ct_ct_s = shear_point(x_ct, ct_ct, shear_factor)
ax.plot(x_ct_s, ct_ct_s, color='black', linewidth=1.5)

# --- S' axes ---
# ct' axis: x = vt → ct = x/v
ct_axis = (1/v) * x_vals
# Apply shear to ct' axis
x_s, ct_s = shear_point(x_vals, ct_axis, shear_factor)
ax.plot(x_s, ct_s, color='red', linewidth=2, label="$ct'$")

# x' axis: ct = v x
# Apply shear to x' axis
x_axis = v * x_vals
x_s_prime, ct_s_prime = shear_point(x_vals, x_axis, shear_factor)
ax.plot(x_s_prime, ct_s_prime, color='red', linestyle='dotted', linewidth=2, label="$x'$")

# --- S' grid (correct Lorentz construction) ---
k_vals = np.arange(-8, 9, 1)

# constant ct' lines
for k in k_vals:
    ct_line = v * x_vals + k / gamma
    x_s, ct_s = shear_point(x_vals, ct_line, shear_factor)
    ax.plot(x_s, ct_s, color='pink', linewidth=0.5)

# constant x' lines
for k in k_vals:
    ct_line = (x_vals - k / gamma) / v
    x_s, ct_s = shear_point(x_vals, ct_line, shear_factor)
    ax.plot(x_s, ct_s, color='pink', linewidth=0.5)

# --- Draw ct' = 5 line ---
ct_line_5 = v * x_vals + 5 / gamma
x_s, ct_s = shear_point(x_vals, ct_line_5, shear_factor)
ax.plot(x_s, ct_s, color='cyan', linestyle='--', linewidth=2, label="Simultaneity line for T'")

# --- Line of simultaneity through Blue point ---
ct_sim = v * x_vals + 3 / gamma
x_s, ct_s = shear_point(x_vals, ct_sim, shear_factor)
ax.plot(x_s, ct_s, color='blue', linestyle='--', linewidth=2, label="Simultaneity line from S' - incorrect \n projection onto $ct$ axis")

# --- Intersection calculation ---
A = np.array([[ -v, 1], [ 1, -v]])
b = np.array([5/gamma, 4/gamma])
solution = np.linalg.solve(A, b)
x_int, ct_int = solution

# Apply shear to intersection point
x_int_s, ct_int_s = shear_point(x_int, ct_int, shear_factor)

# --- Event in S ---
x0, ct0 = 4, 5
x0_s, ct0_s = shear_point(x0, ct0, shear_factor)
ax.scatter(x0_s, ct0_s, color='blue', zorder=5, label="T - turnaround in S: ($x=4, ct=5$)" "\n" "P' - projection of T onto $ct'$ axis:" "\n" "($x'=0, ct'=3$)")
ax.text(x0_s + 0.5, ct0_s - 0.2, 'T', color='blue', fontweight='bold')
ax.text(x0_s + 0.4, ct0_s - 1, "P'", color='blue', fontweight='bold')

# --- Event in S' ---
ax.scatter(x_int_s, ct_int_s, color='red', zorder=6, label="T' - turnaround in S': ($x'=4, ct'=5$)")
ax.text(x_int_s + 0.5, ct_int_s - 0.2, "T'", color='red', fontweight='bold')

# --- Green point ---
x_green = 0
ct_green = 3 / gamma / (1 - v**2)
x_green_s, ct_green_s = shear_point(x_green, ct_green, shear_factor)
ax.scatter(x_green_s, ct_green_s, color='green', zorder=6, label="P - projection of T' onto $ct$ axis: \n ($x=0, ct=3$)")
ax.text(x_green_s - 0.3, ct_green_s - 1, 'P', color='green', fontweight='bold')

# --- Formatting ---
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_aspect('equal')
ax.set_xlabel("x")
ax.set_ylabel("ct")
ax.legend(loc='upper left')

#--- Textbox ----
text_content = (
    r"Key Features:" "\n"
    r"$\bullet$ T - event in S" "\n"
    r"$\bullet$ T' - identical numerical" "\n" "coordinates from S, but assigned in S'" "\n"
    r"$\bullet$ P - projection of T' onto the $ct$ axis:" "\n" "($x=0, ct=3$)" "\n"
    r"$\bullet$ P' - projection of T onto the $ct'$ axis:" "\n" "($x'=0, ct'=3$)" "\n" "\n"
    r"$\bullet$ P, P' and T are on the same" "\n" " horizontal line: "
    r"$\mathbf{simultaneity\ line}$"
    )
ax.text(0.59, 0.02, text_content, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6, pad=0.5),
        fontfamily='serif')

# Add annotation explaining the coordinate system
props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.8)
max_shift = y_max_orig * shear_factor
ax.text(0.02, 0.02, 
        f'Shear Factor: {shear_factor:.2f} ($v={v}c$)\n'
        f'x-axis UNCHANGED\n'
        f'Shift = 38.7°  left\n'
        f'Events: Shown at sheared positions with \n original coordinates',
        transform=ax.transAxes, fontsize=10, verticalalignment='bottom',
        bbox=props)

plt.tight_layout()
plt.savefig('figure5.png', dpi=300, bbox_inches='tight')
plt.title("Lorentz-Consistent Minkowski Diagram 38.7° Shear ($v = 0.8c$)")
plt.show()
