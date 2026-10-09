import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

v  = 0.8
g  = 1/np.sqrt(1-v**2)      # γ = 5/3
sp = 1/g                    # γ lives ONLY here (grid spacing)

T = (4, 5)                  # turnaround = origin of S''

fig, ax = plt.subplots(figsize=(9,9))
plt.subplots_adjust(bottom=0.12)
ax.set_xlim(-2, 11); ax.set_ylim(-2, 11); ax.set_aspect('equal')
ax.set_xticks(range(-2, 12)); ax.set_yticks(range(-2, 12))
ax.grid(True, ls='-', color='gray', alpha=0.35)
ax.axhline(0, color='k', lw=1.5); ax.axvline(0, color='k', lw=1.5)  # x, ct axes
title = plt.title("Twin paradox, $v=±0.8c, Round trip")

turnaround_dot = ax.plot(*T, 'ko', ms=9, zorder=5,label= "Turnaround:"
                         "\n $T(4, 5) = T'(0, 3) = T''(0, 0)$")[0]
xs = np.linspace(-2, 11, 300)

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

def draw_sprime(vis=True):
    arts = []
    arts += ax.plot(xs, xs/v, 'r-', label="$ct'$", lw=1.5, visible=vis)
    arts += ax.plot(xs, v*xs, 'r--', label="$x'$", lw=1.5, visible=vis)
    for k in range(-20, 21):
        arts += ax.plot(xs, v*xs + k*sp, 'orange', alpha=0.2, lw=0.5, visible=vis)
        arts += ax.plot(xs, (xs - k*sp)/v, 'pink', alpha=0.2, lw=0.5, visible=vis)

    # 1-year and 2-year marks in S':
    # grid lines parallel to x' intersect the ct' axis at ct'=1 and ct'=2.
    xdot, ydot = v*g, g
    arts += ax.plot(xdot, ydot, 'o', markerfacecolor='white',
                    markeredgecolor='red', ms=6, zorder=6,
                    label="First year in frame S'", visible=vis)
    xdot, ydot = 2*v*g, 2*g
    arts += ax.plot(xdot, ydot, 'o', markerfacecolor='cyan',
                    markeredgecolor='red', ms=6, zorder=6,
                    label="Second year in frame S'", visible=vis)

    arts.append(ax.annotate("$T(4, 5) = T'(0, 3)$", xy=T, xytext=(0.9, 5.1),
                 color='k', visible=vis))
    return arts

def draw_s2prime(vis=False):
    """S'' grid: origin AT T(4,5), v=-0.8 — traveler's RETURN frame"""
    arts, vo = [], -0.8
    xt, ctt = T
    arts += ax.plot(xt + vo*(xs - ctt), xs, 'g-', label=r"$ct^{\prime\prime}$",
                    lw=1.5, visible=vis)   # ct'' axis (return worldline → (0,10))
    arts += ax.plot(xs, ctt + vo*(xs - xt), 'g--', label=r"$x^{\prime\prime}$",
                    lw=1.5, visible=vis)   # x'' axis (simult. slice → ct=8.2)
    arts.append(ax.annotate(r"$T(4, 5) = T^{\prime\prime}(0, "
                             "0)$", xy=T, xytext=(0.9, 4.5),
                 color='k', visible=vis))
    # ORIGINS OFFSET
    arts.append(ax.annotate(r"$\mathbf{O(0,0) = O^{\prime\prime}"
                r"(-13.33,\, -13.67)}$", xy=(0, 0), xytext=(0.2, 4), color='k',
                fontweight='bold'))
    arts += ax.plot(0, 10, 'go', ms=9, zorder=5,label=r"Return: $R(0, 10)"
                r"= R^{\prime\prime}(0, 3)$", visible=vis)
    arts.append(ax.annotate(r"$R(0, 10) = R^{\prime\prime}(0, "
                "3)$", xy=T, xytext=(0.5, 10), color='k', visible=vis))
    for k in range(-20, 21):
        b = k*sp
        arts += ax.plot(xt + vo*(xs - ctt) + b, xs, 'teal', alpha=0.2,
                lw=0.5, visible=vis)  # x''=const
        arts += ax.plot(xs, ctt + vo*(xs - xt) + b, 'blue', alpha=0.2,
                lw=0.5, visible=vis) # ct''=const

    # 1-year and 2-year marks in S'':
    # grid lines parallel to x'' intersect the ct'' axis at ct''=1 and ct''=2.
    xdot, ydot = xt + vo*g, ctt + g
    arts += ax.plot(xdot, ydot, 'o', markerfacecolor='white',
                    markeredgecolor='green', ms=6, zorder=6,
                    label="First year in frame S''", visible=vis)
    xdot, ydot = xt + 2*vo*g, ctt + 2*g
    arts += ax.plot(xdot, ydot, 'o', markerfacecolor='cyan',
                    markeredgecolor='green', ms=6, zorder=6,
                    label="Second year in frame S''", visible=vis)

    return arts

grp1 = draw_sprime(True)
grp2 = draw_s2prime(True)

legend = ax.legend(loc='upper right', shadow=True)


def update_legend():
    # Map stage number to legend label
    STAGE_LEGEND_LABELS = {
        0: "Turnaround: $T(4, 5) = T'(0, 3)$",
        1: "Turnaround: $T(4, 5) = T''(0, 0)$",
        2: "Turnaround: \n $T(4, 5) = T'(0, 3) = T''(0, 0)$"
    }
    
    handles = []
    labels = []
    
    # Show coordinates for turnaround in legend
    handles.append(turnaround_dot)
    labels.append(STAGE_LEGEND_LABELS[stage])
    
    handles, labels, seen = [turnaround_dot], labels, set()

    if stage == 2:
        groups = [grp1, grp2]        # Round trip: entries from both grids
    elif stage == 0:
        groups = [grp1]
    else:
        groups = [grp2]

    for group in groups:
        for artist in group:
            lbl = artist.get_label()
            if (lbl and not lbl.startswith('_')
                    and artist.get_visible()          # only what's on screen
                    and lbl not in seen):             # no duplicates       
                handles.append(artist)
                labels.append(lbl)
                seen.add(lbl)

    if handles:
        ax.legend(handles, labels, loc='upper right', shadow=True)

# --- Toggle button: S' ↔ S'' ---
stage = 0 

STAGE_TITLES = [
    "Twin paradox, $v=\\pm 0.8c$, Outbound leg",
    "Twin paradox, $v=\\pm 0.8c$, Inbound leg",
    "Twin paradox, $v=\\pm 0.8c$, Round trip",
]

STAGE_BUTTONS = [
    r"Show Inbound leg ($S^{\prime\prime}$)",   # label = what clicking does NEXT
    "Show Round trip",
    "Show Outbound leg ($S'$)",
]

ax_btn = plt.axes([0.3, 0.02, 0.2, 0.05]) 
btn = Button(ax_btn, STAGE_BUTTONS[0])

def apply_stage():
    for a in grp1:
        a.set_visible(stage in (0, 2))   # S' grid: outbound + round trip
    for a in grp2:
        a.set_visible(stage in (1, 2))   # S'' grid: inbound + round trip
    ax.set_title(STAGE_TITLES[stage])
    btn.label.set_text(STAGE_BUTTONS[stage])
    update_legend()
    fig.canvas.draw_idle()

def toggle(event):
    global stage
    stage = (stage + 1) % 3
    apply_stage()

# Show popup message after save image
save_message = ax.text(0.5, 0.1, "", transform=ax.transAxes, zorder=100,
            fontsize=11, color="blue", ha="center", va="bottom",
            bbox=dict(boxstyle="round", facecolor="white", alpha=1))
save_message.set_visible(False)

# --- Save button ---
ax_save = plt.axes([0.6, 0.02, 0.1, 0.05])
btn_save = Button(ax_save, 'Save')
btn_save.on_clicked(save_figure)
btn.on_clicked(toggle)
ax.set_xlabel('x'); ax.set_ylabel('ct')
plt.show()
