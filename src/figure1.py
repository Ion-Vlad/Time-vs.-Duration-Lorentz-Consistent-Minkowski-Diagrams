import matplotlib.pyplot as plt
import numpy as np

# --- Configuration ---
# Enable LaTeX rendering for professional fonts (Computer Modern)
import os

os.environ["PATH"] += os.pathsep + "/Library/TeX/texbin"
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Computer Modern Roman']
plt.rcParams['mathtext.fontset'] = 'custom'

# --- Parameters ---
v = 0.8
gamma = 1 / np.sqrt(1 - v**2)
L_rest = 4.0
t_earth_out = L_rest / v
t_earth_total = 2 * t_earth_out
tau_leg = t_earth_out / gamma
tau_total = 2 * tau_leg


# --- Setup Plot ---
fig, ax = plt.subplots(figsize=(14, 6))
ax.set_aspect('equal')
plt.title("Classical Spacetime Diagram: Twin paradox ($v = 0.8c$)")
limit = 10
ct_max = 9
ct_min = -limit + 5
x_vals = np.linspace(-limit + 5, limit-2, 400)
k_vals = np.arange(-8, 9, 1)

# --- Grey grid (S frame) ---
for x in range(-limit, limit+1):
    ax.plot([x, x], [-limit, limit], color='lightgrey', linewidth=0.5)

for ct in range(-limit, limit+1):
    ax.plot([-limit, limit], [ct, ct], color='lightgrey', linewidth=0.5)

# --- Pink grid (S' frame) ---

# 1. Lines through x = k, parallel to ct'
for k in k_vals:
    ct_line = (1/v) * (x_vals - k)
    
    mask = (ct_line >= ct_min) & (ct_line <= ct_max)
    ax.plot(x_vals[mask], ct_line[mask], color='pink', linewidth=0.8)

# 2. Lines through ct = k, parallel to x'
for k in k_vals:
    ct_line = v * x_vals + k
    
    mask = (ct_line >= ct_min) & (ct_line <= ct_max)
    ax.plot(x_vals[mask], ct_line[mask], color='pink', linewidth=0.8)

# --- 1. Draw Inertial Frame Axes (Earth) ---
ax.axvline(0, color='black', linewidth=2.5, label=r'Inertial Frame ($S$): $ct$')
ax.axhline(0, color='black', linewidth=2.5, label=r'Inertial Frame ($S$): $x$')

# --- 2. Draw Moving Frame Axes (Traveler) ---
slope_ct_prime = 1/v
slope_x_prime = v

# Plot ct' axis (Outbound)
x_ct_prime = np.linspace(-2, 6, 100)
y_ct_prime = slope_ct_prime * x_ct_prime
ax.plot(x_ct_prime, y_ct_prime, 'r-', linewidth=2, label=r'Moving Frame ($S^{\prime}$): $ct^{\prime}$')

# Plot x' axis (Outbound)
x_x_prime = np.linspace(-2, 6, 100)
y_x_prime = slope_x_prime * x_x_prime
ax.plot(x_x_prime, y_x_prime, 'r--', linewidth=2, label=r'Moving Frame ($S^{\prime}$): $x^{\prime}$')

# --- 3. Draw Traveler's Path (Twin Paradox) ---
path_x = [0, L_rest, 0]
path_ct = [0, t_earth_out, t_earth_total]
ax.plot(path_x, path_ct, 'b-o', linewidth=3, markersize=14, label='Traveler Path', zorder=5)

# Mark Turnaround Event
ax.scatter([L_rest], [t_earth_out], color='darkorange', s=200, zorder=6, marker='*', label='Turnaround Event')
ax.text(L_rest + 0.4, t_earth_out - 0.1, r'Turnaround ($\tau=3, t=5$)', fontsize=12, fontweight='bold', color='blue')

# --- 4. Draw Simultaneity Lines (The "Jump") ---
# Line 1: Outbound Simultaneity
y_out = slope_x_prime * (x_x_prime - L_rest) + t_earth_out
ax.plot(x_x_prime, y_out, 'g:', linewidth=2, alpha=0.8, label=r'Outbound Simultaneity ($t^{\prime}=3$)')
ax.scatter([0], [1.8], color='green', s=80, zorder=6)
ax.text(-3, 1.65, r'$t=1.8$', color='green', fontsize=11, fontweight='bold')

# Line 2: Inbound Simultaneity
y_in = -slope_x_prime * (x_x_prime - L_rest) + t_earth_out
ax.plot(x_x_prime, y_in, 'm:', linewidth=2, alpha=0.8, label=r'Return Simultaneity ($t^{\prime}=3$)')
ax.scatter([0], [8.2], color='magenta', s=80, zorder=6)
ax.text(-3, 8, r'$t=8.2$', color='magenta', fontsize=11, fontweight='bold')

# --- 5. Annotations & Formatting ---
ax.scatter([0], [t_earth_total], color='black', s=100, zorder=6, marker='o')
ax.text(0.5, t_earth_total-0.1, r'Earth Arrival ($t=10$)', fontsize=12, fontweight='bold')

# --- Legend: Outside Right ---
ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize=11, frameon=True, shadow=True)

# --- Text Box: Moved Outside (Bottom Right) ---
text_content = (
    r"Key Features:" "\n"
    r"$\bullet$ Speed: $v$ = 0.8c" "\n"
    r"$\bullet$ Distance (Earth to star, rest): 4 light-years" "\n"
    r"$\bullet$ Round-trip distance ($L_0$): 8 light-years" "\n"
    r"$\bullet$ Blue: Traveler path ($\tau=6$ yr)" "\n"
    r"$\bullet$ Green: Outbound 'Now' ($t=1.8$)" "\n"
    r"$\bullet$ Magenta: Return 'Now' ($t=8.2$)" "\n"
)

ax.text(1.05, 0.05, text_content, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6, pad=0.5),
        fontfamily='serif') # Optional: force serif font for consistency

# Save and Show
plt.tight_layout()
plt.savefig('figure1.png', dpi=300, bbox_inches='tight')
plt.show()
