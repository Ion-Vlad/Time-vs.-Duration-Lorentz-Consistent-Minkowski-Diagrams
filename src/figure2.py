import numpy as np
import matplotlib.pyplot as plt

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

# --- Lorentz transform ---
def lorentz_transform(x, ct):
    t = ct / c
    t_prime = gamma * (t - v * x / c**2)
    x_prime = gamma * (x - v * t)
    return x_prime, c * t_prime

# --- Plot setup ---
fig, ax = plt.subplots(figsize=(7,7))

# --- Limits ---
limit=16
x_vals = np.linspace(-16, 16, 400)

# --- S grid (grey) ---
for x in np.arange(-10, 11, 1):
    ax.plot([x, x], [-10, 10], color='lightgrey', linewidth=0.5)
for ct in np.arange(-10, 11, 1):
    ax.plot([-10, 10], [ct, ct], color='lightgrey', linewidth=0.5)

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

k_vals = np.arange(-8, 9, 1)
# constant ct' lines: ct - v x = k/gamma → ct = v x + k/gamma
for k in k_vals:
    ct_line = v * x_vals + k / gamma
    ax.plot(x_vals, ct_line, color='pink', linewidth=0.5)

# constant x' lines: x - v ct = k/gamma → ct = (x - k/gamma)/v
for k in k_vals:
    ct_line = (x_vals - k / gamma) / v
    ax.plot(x_vals, ct_line, color='pink', linewidth=0.5)


# --- Draw ct' = 5 line (correct) ---
# ct - v x = 5/gamma
ct_line_5 = v * x_vals + 5 / gamma
ax.plot(x_vals, ct_line_5, color='cyan', linestyle='--', linewidth=2, label="Simultaneity line for T'; projection \n onto $ct$ axis")

# --- Line of simultaneity through Blue point ---
ct_sim = v * x_vals + 3 / gamma
ax.plot(x_vals, ct_sim, color='blue', linestyle='--', linewidth=2,
        label="Simultaneity line from S' - incorrect \n projection onto $ct$ axis")

# --- Mark intersection of ct'=5 and x'=4 ---
# Solve system:
# ct - v x = 5/gamma
# x - v ct = 4/gamma

A = np.array([[ -v, 1],
              [ 1, -v]])
b = np.array([5/gamma, 4/gamma])

solution = np.linalg.solve(A, b)
x_int, ct_int = solution

# --- Event in S ---
x0, ct0 = 4, 5
ax.scatter(x0, ct0, color='blue', zorder=5, label="T - turnaround in S: ($x=4, ct=5$) \n P' - projection of T onto S' \n ($x'=0, ct'=3$) ")
ax.text(x0 + 0.5, ct0 - 0.5,'T', color='blue', fontweight='bold')
ax.text(x0 - 0.2, ct0 - 1.1,"P'", color='blue', fontweight='bold')

# --- Compute its S' coordinates ---
xp, ctp = lorentz_transform(x0, ct0)
# --- Event in S' ---
ax.scatter(x_int, ct_int, color='red', zorder=6, label="T' - turnaround in S': ($x'=4, ct'=5$)")
ax.text(x_int - 0.3, ct_int + 0.5, "T'", color='red', fontweight='bold')

# Green point (turnaround in S')

# Its projection onto ct' axis (green point)
# (this is the actual (x'=0, ct'=3) event in S coordinates)
x_green = 0  # on ct' axis → x' = 0
ct_green = 3 / gamma / (1 - v**2)  # DON'T do this manually

ax.scatter(x_green, ctp, color='green', zorder=6, label="P - projection of T' onto $ct$ axis: \n ($x=0, ct=3$)")
ax.text(-1.2, ct_green - 2, 'P', color='green', fontweight='bold')

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
    r"$\bullet$ T - event in S" "\n"
    r"$\bullet$ T' - identical numerical" "\n" "coordinates from S, but assigned in S'" "\n"
    r"$\bullet$ P — same event as T'," "\n" "projected onto the $ct$ axis. (S)" "\n"
    r"$\bullet$ P' — same event as T," "\n" "projected onto the $ct'$ axis. (S')" "\n"  "\n"
    r"$\bullet$ The same event apears on" "\n" "different simultaneity lines." "\n" "That concludes the 'simultaneity lines'" "\n"
    "are in fact "
    r"$\mathbf{observational\ hypersurface}$"
    )
ax.text(0.53, 0.02, text_content, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6, pad=0.5),
        fontfamily='serif') # Optional: force serif font for consistency

# Save and Show
plt.tight_layout()
plt.savefig('figure2.png', dpi=300, bbox_inches='tight')
plt.title("Lorentz-Consistent Minkowski Diagram ($v = 0.8c$)")
plt.show()
