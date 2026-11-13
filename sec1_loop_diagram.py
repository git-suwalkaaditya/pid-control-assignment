
from common import plt, save
from matplotlib.patches import FancyBboxPatch, Circle

fig, ax = plt.subplots(figsize=(7.4, 2.5))
ax.set_xlim(0, 10.6); ax.set_ylim(0, 3.2); ax.axis("off")

def box(x, y, w, h, text, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                fc=color, ec="k", lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9.5)

def arrow(x1, y1, x2, y2, label=None, dy=0.18):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color="k"))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + dy, label, ha="center", fontsize=8.5)

ax.text(0.45, 2.15, "Target\nr (setpoint)", ha="center", va="center", fontsize=9)
ax.add_patch(Circle((1.9, 2.15), 0.22, fc="w", ec="k", lw=1.2))
ax.text(1.9, 2.15, "Σ", ha="center", va="center", fontsize=11)
ax.text(1.62, 2.42, "+", fontsize=10); ax.text(1.95, 1.72, "−", fontsize=12)
arrow(1.05, 2.15, 1.68, 2.15)
box(3.4, 1.75, 1.8, 0.8, "Controller\n(PID)", "#ffe3c4")
arrow(2.12, 2.15, 3.4, 2.15, "error\ne = r − y")
box(6.3, 1.75, 2.0, 0.8, "Machine (plant)\nblock + spring", "#d6e9ff")
arrow(5.25, 2.15, 6.3, 2.15, "force\nu (N)")
arrow(8.35, 2.15, 10.4, 2.15, "position y (m)")
box(6.3, 0.25, 2.0, 0.7, "Sensor", "#dff5dc")
ax.plot([9.3, 9.3], [2.15, 0.6], color="k", lw=1.3)
arrow(9.3, 0.6, 8.35, 0.6)
ax.plot([6.3, 1.9], [0.6, 0.6], color="k", lw=1.3)
arrow(1.9, 0.6, 1.9, 1.93)
ax.text(4.1, 0.75, "measured y (fed back)", ha="center", fontsize=8.5)
ax.set_title("Closed feedback loop: measure, compare with target, correct, repeat")
save(fig, "fig01_loop.png")
