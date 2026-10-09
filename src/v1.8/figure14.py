import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerPatch
import matplotlib.patches as mpatches
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# --- Configuration ---
# Enable LaTeX rendering for professional fonts (Computer Modern)
#import os

#os.environ["PATH"] += os.pathsep + "/Library/TeX/texbin"
#plt.rcParams['text.usetex'] = True
#plt.rcParams['font.family'] = 'serif'
#plt.rcParams['font.serif'] = ['Computer Modern Roman']
#plt.rcParams['mathtext.fontset'] = 'custom'

# --- 1. Setup ---
fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111, projection='3d')

# --- 2. CRITICAL: Remove ALL Backgrounds and Boxes ---
# 1. Make the figure background white (or transparent)
fig.patch.set_facecolor('white')

# 2. Make the axes background transparent
ax.set_facecolor('none')

# 3. Remove the axis panes (the "walls" of the coordinate box)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('none')
ax.yaxis.pane.set_edgecolor('none')
ax.zaxis.pane.set_edgecolor('none')

# 4. Remove the grid lines from the axes (we draw our own)
ax.grid(False)

# 5. Hide ticks and labels (we will use native labels which auto-rotate)
ax.tick_params(axis='both', which='both', labelbottom=False, labelleft=False,
               labeltop=False, labelright=False)
ax.tick_params(axis='z', which='both', labelbottom=False, labelleft=False,
               labeltop=False, labelright=False)

# 6. Enable Native Labels (These auto-rotate correctly!)
ax.set_xlabel('$x$ (Space)', fontsize=14)
ax.set_ylabel('$y$ (Space)', fontsize=14)
ax.set_zlabel('$z$ (Space)', fontsize=14)

# --- 3. Define Boundaries ---
x_min, x_max = 0, 6
y_min, y_max = 0, 6
z_min, z_max = 0, 6

# --- 4. Draw Custom Walls (Bottom, Back, Left only) ---
clean_verts = [
    [[x_min, y_min, z_min], [x_max, y_min, z_min], [x_max, y_max, z_min],
         [x_min, y_max, z_min]],  # Bottom
    [[x_min, y_max, z_min], [x_max, y_max, z_min], [x_max, y_max, z_max],
         [x_min, y_max, z_max]],  # Back
    [[x_min, y_min, z_min], [x_min, y_min, z_max], [x_min, y_max, z_max],
         [x_min, y_max, z_min]]   # Left
    ]
# No edges on custom walls
wall_collection = Poly3DCollection(clean_verts, alpha=0.15, facecolors='lightgray',
                edgecolors='none', linewidths=0)
ax.add_collection3d(wall_collection)

# --- 5. Draw Grid (Manual) ---
grid_color = 'gray'; grid_alpha = 0.5; grid_linewidth = 0.5
# Bottom Grid
for y in np.linspace(y_min, y_max, 7): ax.plot([x_min, x_max], [y, y],
            [z_min, z_min], color=grid_color, linewidth=grid_linewidth,
            alpha=grid_alpha)
for x in np.linspace(x_min, x_max, 7): ax.plot([x, x], [y_min, y_max],
            [z_min, z_min], color=grid_color, linewidth=grid_linewidth,
            alpha=grid_alpha)
        # redraw custom ticks
ax.text(-2.6, -2.4, 2, '0')
ax.text(-1.8, -2.4, 2, '1')
ax.text(-0.9, -2.4, 2, '2')
ax.text(0, -2.4, 2, '3')
ax.text(1, -2.4, 2, '4')
ax.text(2.8, -2.4, 2, '6')
# Back Grid
for z in np.linspace(z_min, z_max, 7): ax.plot([x_min, x_max], [y_max,
            y_max], [z, z], color=grid_color, linewidth=grid_linewidth,
            alpha=grid_alpha)
for x in np.linspace(x_min, x_max, 7): ax.plot([x, x], [y_max, y_max],
            [z_min, z_max], color=grid_color, linewidth=grid_linewidth,
            alpha=grid_alpha)
        # redraw custom ticks
ax.text(-1.15, 5, 0.5, '0')
ax.text(-1.3, 5, 1.8, '1')
ax.text(-1.3, 5, 2.75, '2')
ax.text(-1.3, 5, 3.75, '3')
ax.text(-1.3, 5, 4.7, '4')
ax.text(-1.3, 5, 6.6, '6')
# Left Grid
for z in np.linspace(z_min, z_max, 7): ax.plot([x_min, x_min], [y_min,
            y_max], [z, z], color=grid_color, linewidth=grid_linewidth,
            alpha=grid_alpha)
for y in np.linspace(y_min, y_max, 7): ax.plot([x_min, x_min], [y, y],
            [z_min, z_max], color=grid_color, linewidth=grid_linewidth,
            alpha=grid_alpha)
        # redraw custom ticks
ax.text(-1, 4.3, 0.4, '1')
ax.text(-1, 3.3, 0.4, '2')
ax.text(-1, 2.4, 0.4, '3')
ax.text(-1, 1.4, 0.4, '4')
ax.text(-1, -0.6, 0.4, '6')
# --- 6. Draw Main Axes (Thick Black Lines) ---
ax.plot([x_max+0.15, 0], [x_max, x_max], [-0.1, -0.1], color='black', linewidth=2)
ax.plot([y_min, 0.1], [y_max, 0], [0.1, 0], color='black', linewidth=2)
ax.plot([0.1, 0.1], [z_max, z_max], [0, z_max], color='black', linewidth=2)
         # progression of space
ax.quiver(3, -1.25, 1, 1, 0, 0, color='black')
ax.quiver(-4.1, -2.1, 3, 1, 0, -0.8, color='black')
ax.quiver(-5, 1.15, 7.5, 0, 0, 1, color='black')

# --- 7. Draw Time Axes (Red Lines) ---
ax.plot([x_max, -2], [x_max, x_max], [0, 0], color='red', linewidth=2)

ax.plot([y_min, 0], [8, 0], [0, 0], color='red', linewidth=2)
ax.plot([0, 0], [z_max, z_max], [-1, z_max], color='red', linewidth=2)
        # progression of time
ax.quiver(4, -1.5, 1, -1, 0, 0, color='red') 
ax.quiver(-4.3, -3, 2.9, -1, 0, 0.8, color='red')
ax.quiver(-3.05, 3.3, 7.2, 0, 0, -1, color='red')

# --- 8. Spacetime Data: Cyan = present, Green = past, Blue = future ---
ax.plot([x_max+0.3, 0], [x_max, x_max], [-0.2, -0.2], color='green', linewidth=2,
        linestyle='--')
ax.plot([y_min, 0.2], [y_max, 0], [0.2, 0], color='green', linewidth=2,
        linestyle='--')
ax.plot([0.2, 0.2], [z_max, z_max], [0, z_max], color='green', linewidth=2,
        linestyle='--')

ax.plot([-2, 0], [x_max, x_max], [-0.1, -0.1], color='blue', linewidth=2,
        linestyle='--')
ax.plot([y_min, 0.1], [6, 8], [0.1, 0], color='blue', linewidth=2,
        linestyle='--')
ax.plot([0.1, 0.1], [z_max, z_max], [0, -1], color='blue', linewidth=2,
        linestyle='--')

ax.scatter([x_min], [x_max], [0], color='cyan', s=200, zorder=10)

# --- 9. Limits & View ---
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_zlim(z_min, z_max)
ax.view_init(elev=20, azim=220)

# --- 10. Legend ---
    # create arrows for legend
class HandlerArrow(HandlerPatch):
    def create_artists(
        self, legend, orig_handle,
        xdescent, ydescent, width, height, fontsize, trans
    ):
        y = ydescent + height / 2

        if getattr(orig_handle, 'reverse', False):
            start = (xdescent + width, y)
            end = (xdescent, y)
        else:
            start = (xdescent, y)
            end = (xdescent + width, y)

        arrow = mpatches.FancyArrowPatch(
            start,
            end,
            arrowstyle="->",
            mutation_scale=fontsize,
            color=orig_handle.get_edgecolor(),
            linewidth=orig_handle.get_linewidth()
        )
        arrow.set_transform(trans)
        return [arrow]

# Legend-only arrows
space_arrow = mpatches.FancyArrowPatch(
    (0, 0), (1, 0),
    color='black',
    linewidth=2,
    label='Progression of space'
)

time_arrow = mpatches.FancyArrowPatch(
    (1, 0), (0, 0),
    color='red',
    linewidth=2,
    label='Progression of time'
)
time_arrow.reverse = True
# Other normal legend entries
space_line = Line2D(
    [0], [0],
    color='black',
    linewidth=2,
    label='Spatial axes'
)
time_line = Line2D(
    [0], [0],
    color='red',
    linewidth=2,
    label='Temporal axes'
)
past_line = Line2D(
    [0], [0],
    color='green',
    linestyle='--',
    linewidth=2,
    label='Green Ray: The Past (Created)'
)
present_dot = Line2D(
    [0], [0],
    color='cyan',
    marker='o',
    linestyle='None',
    linewidth=2,
    label='The Present (Now)'
)
future_line = Line2D(
    [0], [0],
    color='blue',
    linestyle='--',
    linewidth=2,
    label='Blue Ray (Empty Space): The Future (Not yet created)'
)
ax.legend(
    handles=[space_line, time_line, space_arrow, time_arrow, past_line,
            present_dot, future_line],
            handler_map={mpatches.FancyArrowPatch: HandlerArrow()}, fontsize=14
)

text_content = (
    "Time enters the spacetime with the opposite sign to the\n spatial "
    "coordinates. Consequently, spacetime interval does\n not obey the "
    "ordinary Euclidean, or strictly Pythagorean,\n distance formula:\n"
    r"$s^2 = -c^2 \Delta t^2 + \Delta x^2 + \Delta y^2 + \Delta z^2$   or:" "\n"
    r"$s^2 = c^2 \Delta t^2 - \left(\Delta x^2 + \Delta y^2 + \Delta z^2\right)$")
ax.text(2.05, 2.5, 7.2, text_content, 
        fontsize=14, 
        verticalalignment='top', 
        bbox=dict(boxstyle='round', facecolor='cyan', alpha=0.5))

# --- 11. Save/Show ---
plt.tight_layout()
plt.title('Spacetime: Past - Present - Future', fontsize=24)
plt.savefig('figure14.png', dpi=300, bbox_inches='tight')
plt.show()
