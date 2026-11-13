
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pidlab import PID, MassSpringDamper, ThirdOrderLag, simulate, step_metrics, fmt_row

# ---- Test system (given in the assignment)
M, C, K = 1.0, 10.0, 20.0          # kg, N*s/m, N/m
TARGET = 1.0                       # m
DT = 0.001                         # s, simulation and default controller step

# ---- Gains chosen in Section 6 (ideal motor, no force limit)
KP, KI, KD = 300.0, 200.0, 20.0
# ---- Gains used in Section 9 (real motor: 30 N limit + anti-windup)
KP9, KI9, KD9 = 300.0, 600.0, 20.0
U_MAX = 30.0                       # N
NOISE = 0.001                      # m (+/- 1 mm)
D_TAU = 0.01                       # s, D-filter time constant

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams.update({
    "figure.figsize": (7.0, 3.6), "figure.dpi": 110, "savefig.dpi": 200,
    "axes.grid": True, "grid.alpha": 0.3, "axes.titlesize": 11,
    "axes.labelsize": 10, "legend.fontsize": 8.5, "font.size": 9.5,
    "axes.spines.top": False, "axes.spines.right": False,
})


def plant():
    return MassSpringDamper(M, C, K)


def save(fig, name):
    fig.tight_layout()
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print("saved", path)


def target_line(ax, r=TARGET, label="Target (1 m)"):
    ax.axhline(r, color="k", ls="--", lw=0.9, label=label)
