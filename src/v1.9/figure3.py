import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D

v  = 0.8
g  = 1/np.sqrt(1-v**2)
sp = 1/g

def to_prime(x, ct):
    return g*(x - v*ct), g*(ct - v*x)

def to_unprimed(xp, ctp):
    return g*(xp + v*ctp), g*(ctp + v*xp)

A, B = (2.0, 5.0), (4.0, 5.0)
Cp, Dp, Ep = (-2.0, 4.0), (2.0, 4.0), (-1.25, 4)
Ap, Bp = to_prime(*A), to_prime(*B)
C,  D, E  = to_unprimed(*Cp), to_unprimed(*Dp), to_unprimed(*Ep)

fig, ax = plt.subplots(figsize=(9,9))
ax.set_xlim(-10,10); ax.set_ylim(-10,10); ax.set_aspect('equal')
ax.set_xticks(range(-10,11)); ax.set_yticks(range(-10,11))
ax.grid(True, ls='-', color='gray', alpha=0.35)
ax.axhline(0, color='k', lw=1.5); ax.axvline(0, color='k', lw=1.5)

xs = np.linspace(-10,10,200)

# S' axes + calibrated grid
ct_prime = ax.plot(xs, xs/v, 'r-', lw=1.5)[0]
x_prime = ax.plot(xs, v*xs, 'r--', lw=1.5)[0]
for k in range(-18,19):
    ax.plot(xs, v*xs + k*sp, 'purple', alpha=0.2, lw=0.5)
    ax.plot(xs, (xs - k*sp)/v, 'blue',  alpha=0.2, lw=0.5)

# --- Simultaneity slices ---
ln_A = ax.plot(xs, np.full_like(xs, A[1]), 'orange', lw=1.5, alpha=0.7)[0]
ln_C = ax.plot(xs, v*xs + Cp[1]*sp, 'teal', lw=1.5, alpha=0.8)[0]

# --- Event markers: plain dots, NO text on the diagram ---
mk = dict(ms=9, zorder=5, ls='None')
pt_A = ax.plot(*A,  'o', color='darkorange', **mk)[0]
ax.text(1.3, 5.3,"A=A'", color='darkorange', fontweight='bold')
pt_B = ax.plot(*B,  'o', color='darkorange', ms=9, zorder=5)[0]
ax.text(4.7, 5.2,"B=B'", color='darkorange', fontweight='bold')
pt_C = ax.plot(*C,  'o', color='teal', ms=9, zorder=5)[0]
ax.text(0.8, 4.1,"C'=C", color='teal', fontweight='bold')
pt_D = ax.plot(*D,  'o', color='teal', ms=9, zorder=5)[0]
ax.text(8.83, 8.5,"D'=D", color='teal', fontweight='bold')


pt_E = ax.plot(*E,  'o', color='teal', ms=9, zorder=5,
        path_effects=[pe.withStroke(linewidth=5, foreground='orange')])[0]
ax.text(2.6, 5.3,"E'=E", color='teal', fontweight='bold')

# PROJECTIONS:
# 1. Projecting A and B onto S' grid
""" NOTE:   The coordinates of projected events A and B onto S' are:
        A_project(A[0]/g, A[1]/g) and B_project(B[0]/g, B[1]/g). However,
        we have to use the function 'to_unprimed()' in order to represent
        the point correctly on the diagram. This is because we plot everything
        on the S grid, and the S grid does not have the Lorentz factor built into it.
            Similar for E. """
    
A_project = to_unprimed(A[0]/g, A[1]/g)
B_project = to_unprimed(B[0]/g, B[1]/g)
E_project = to_unprimed(E[0]/g, E[1]/g)

ax.plot(A_project[0], A_project[1],  'o', color='blue', **mk)[0]
ax.text(6.2, 6.2,"Ap", color='blue', fontweight='bold')
ax.plot(B_project[0], B_project[1], 'o', color='blue', ms=9, zorder=5)[0]
ax.text(8.2, 7.5,"Bp", color='blue', fontweight='bold')
ax.plot(E_project[0], E_project[1], 'o', color='blue', ms=9, zorder=5)[0]
ax.text(7.2, 7,"Ep", color='blue', fontweight='bold')
# simultaneity line blue
x1, y1 = A_project
x2, y2 = B_project
slope = (y2 - y1) / (x2 - x1)
y_line = slope * (xs - x1) + y1
ax.plot(xs, y_line, color='blue', lw=1.5, zorder=4)

# 2. Projecting C', D' and E' onto S grid
pt_Cp_p = ax.plot(*Cp/g, *Cp/g,  'o', color='cyan', ms=9, zorder=5)[0]
ax.text(-2, 1.6, "C'p", color='cyan', fontweight='bold',
    path_effects=[pe.withStroke(linewidth=2, foreground='k')])
pt_Dp_p = ax.plot(*Dp/g, *Dp/g,  'o', color='cyan', ms=9, zorder=5)[0]
ax.text(0.3, 1.6, "D'p", color='cyan', fontweight='bold',
    path_effects=[pe.withStroke(linewidth=2, foreground='k')])
pt_Ep_p = ax.plot(*Ep/g, *Ep/g,  'o', color='cyan', ms=9, zorder=5)[0]
ax.text(-1, 3, "E'p", color='cyan', fontweight='bold',
    path_effects=[pe.withStroke(linewidth=2, foreground='k')])

# simultaneity line cyan
ax.plot(xs, np.full_like(xs, Cp[1]/g), 'cyan', lw=1.5, alpha=0.7)[0]

## --- Legend: coordinates computed at runtime, formatted identically ---
ax.legend(
    handles=[pt_A, pt_B, pt_C, pt_D, pt_E, ln_A, ln_C, ct_prime, x_prime],
    labels=[
        f"$A(x={A[0]:.1f}, ct={A[1]:.1f}) = A'(x'={Ap[0]:.1f}, ct'={Ap[1]:.1f})$",
        f"$B(x={B[0]:.1f}, ct={B[1]:.1f}) = B'(x'={Bp[0]:.1f}, ct'={Bp[1]:.1f})$",
        f"$C'(x'={Cp[0]:.1f}, ct'={Cp[1]:.1f}) = C(x={C[0]:.1f}, ct={C[1]:.1f})$",
        f"$D'(x'={Dp[0]:.1f}, ct'={Dp[1]:.1f}) = D(x={D[0]:.1f}, ct={D[1]:.1f})$",
        f"$E'(x'={Ep[0]:.1f}, ct'={Ep[1]:.1f}) = E(x={E[0]:.1f}, ct={E[1]:.1f})$",
        f"$ct = {A[1]:.1f}$ slice (S-simultaneous)",
        f"$ct' = {Cp[1]:.1f}$ slice (S'-simultaneous)",
        f"$ct' axis$",
        f"$x' axis$"
    ],
    loc='upper left', fontsize=9, framealpha=0.9)

# Projections text box
text_projections = (r"     Projections: $X(x,ct) \; → \; Xp(x/\gamma, ct/\gamma)$" "\n\n"
        f"       $ct'={A[1]/g:.1f}$ slice for projected coordinates" "\n"
        f"       $ct={Cp[1]/g:.1f}$ slice for projected coordinates" "\n"
        f"A onto S' frame → $Ap(x'= {A[0]/g:.1f}, ct'={A[1]/g:.1f})$" "\n"
        f"B onto S' frame → $Bp(x'= {B[0]/g:.1f}, ct'={B[1]/g:.1f})$" "\n"
        f"E onto S' frame → $Ep(x'= {E[0]/g:.1f}, ct'={E[1]/g:.1f})$" "\n"        
        f"C' onto S frame → $C'p(x= {Cp[0]/g:.1f}, ct={Cp[1]/g:.1f})$" "\n"
        f"D' onto S frame → $D'p(x= {Dp[0]/g:.1f}, ct={Dp[1]/g:.1f})$" "\n"
        f"E' onto S frame → $E'p(x= {Ep[0]/g:.1f}, ct={Ep[1]/g:.1f})$" "\n"
        )
ax.text(0.54, 0.02, text_projections, fontsize=10,
        transform=ax.transAxes, verticalalignment='bottom',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6, pad=0.5),
        fontfamily='serif')
# add labels
ax.plot(
    [0.54, 0.57],       # x coordinates (length)
    [0.23, 0.23],       # y coordinates
    color='blue', linewidth=2, transform=ax.transAxes, solid_capstyle='round',
    zorder=10)
ax.plot([0.54, 0.57], [0.21, 0.21], color='cyan', linewidth=2,
    transform=ax.transAxes, solid_capstyle='round', zorder=10)

ax.set_xlabel('x'); ax.set_ylabel('ct')
ax.set_title(f"v=0.8c, ABE sim. in S, C'D'E' sim. in S'")
plt.savefig('figure3.png', dpi=300, bbox_inches='tight')
plt.show()
