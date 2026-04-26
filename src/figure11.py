import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# --- Configuration ---
# Enable LaTeX rendering for professional fonts (Computer Modern)
#import os

#os.environ["PATH"] += os.pathsep + "/Library/TeX/texbin"
#plt.rcParams['text.usetex'] = True
#plt.rcParams['font.family'] = 'serif'
#plt.rcParams['font.serif'] = ['Computer Modern Roman']
#plt.rcParams['mathtext.fontset'] = 'custom'

# Create the figure and 3D axis
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Set the range
limit = 5
offset = -0.2

# --- 1. Draw Spatial Axes (x, y, z) ---
ax.plot([-limit, limit], [0, 0], [0, 0], color='black', linewidth=2, label='$x$')
ax.plot([0, 0], [-limit, limit], [0, 0], color='black', linewidth=2, label='$y$')
ax.plot([0, 0], [0, 0], [0, limit], color='black', linewidth=2, label='$z$')
# ---- and Time axes (t) ----
ax.plot([-limit, limit], [0.3, 0.3], [0, 0], color='red', linewidth=2, label='time')
ax.plot([0.2, 0.2], [-limit, limit], [0, 0], color='red', linewidth=2)
ax.plot([0, 0], [0.3, 0.3], [-limit, limit], color='red', linewidth=2)
ax.plot([offset-0.1, offset-0.1], [0.3, 0.3], [-limit, 0], color='blue', linewidth=2, linestyle='--')

# --- 2 Draw the "Observer" at the Present (z=0)
ax.scatter([0], [0], [0], color='darkorange', s=200, zorder=10, label='The Present (Now)')

# --- 3. Draw Parallel Path ---
ax.plot([offset, offset], [0, 0], [0, limit], color='green', linewidth=2, alpha=0.6, linestyle='--')

# --- 4. Labels and Formatting ---
ax.set_xlabel('$x$ (Space)', fontsize=12)
ax.set_ylabel('$y$ (Space)', fontsize=12)
ax.set_zlabel('$z$ (Space)', fontsize=12)
ax.set_title('3D Spacetime: Present & Past Only (Future Not Created)', fontsize=14)

# Set limits
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_zlim(0, limit) 

# Add a legend
ax.legend(loc='upper left', fontsize=10)

# Set a nice viewing angle
ax.view_init(elev=20, azim=-60)

#--- Text box location ---
text_x, text_y, text_z = 0, 0, 7.4 
text_str = (
    "Philosophy: Presentism\n"
    "- Green Ray: The Past (Created)\n"
    "- Orange Dot: The Present (Now)\n"
    "- Blue Ray (Empty Space): The Future (Not yet created)"
)

# Correct syntax for 3D text: ax.text(x, y, z, string, ...)
ax.text(text_x, text_y, text_z, text_str, 
        fontsize=9, 
        verticalalignment='top', 
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Save and Show
plt.tight_layout()
plt.savefig('figure11.png', dpi=300, bbox_inches='tight')
print("Saved as figure10.png")
plt.show()
