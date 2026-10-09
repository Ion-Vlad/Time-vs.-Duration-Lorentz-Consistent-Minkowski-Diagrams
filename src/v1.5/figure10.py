import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# --- Configuration ---
# Enable LaTeX rendering for professional fonts (Computer Modern)
import os

os.environ["PATH"] += os.pathsep + "/Library/TeX/texbin"
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Computer Modern Roman']
plt.rcParams['mathtext.fontset'] = 'custom'

# Create the figure and 3D axis
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Set the range for the axes
limit = 5
offset = 0.3  # Small offset to place the blue line close to the red one

# --- 1. Draw Spatial Axes (x, y, z) in Black ---
ax.plot([-limit, limit], [0, 0], [0, 0], color='black', linewidth=2, label='$x$')
#--- and Time axis (t) in Red ---
ax.plot([-limit, limit], [0, 0], [offset, offset], color='red', linewidth=2)
ax.plot([0, 0], [-limit, limit], [0, 0], color='black', linewidth=2, label='$y$')
#--- and Time axis (t) in Red ---
ax.plot([offset, offset], [-limit, limit], [0, 0], color='red', linewidth=2)

ax.plot([0, 0], [0, 0], [-limit, limit], color='black', linewidth=2, label='$z$')
#--- and Time axis (t) in Red ---
ax.plot([offset, offset], [0, 0], [-limit, limit], color='red', linewidth=2, label=r'$t$ (Time)')

# --- 2. Labels and Formatting ---
ax.set_xlabel('$x$', fontsize=12)
ax.set_ylabel('$y$', fontsize=12)
ax.set_zlabel('$z$', fontsize=12)
ax.set_title('3D Spacetime', fontsize=14)

# Set limits
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_zlim(-limit, limit)

# Add a legend
ax.legend(loc='upper left', fontsize=10)

# Set a nice viewing angle
ax.view_init(elev=20, azim=-60)

# Save and Show
plt.tight_layout()
plt.savefig('figure9.png', dpi=300, bbox_inches='tight')
print("Saved as figure9.png")
plt.show()
