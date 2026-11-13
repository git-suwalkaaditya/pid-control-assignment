
from common import *

cases = [("P   (Kp=300)", PID(KP)),
         ("PI  (Kp=300, Ki=200)", PID(KP, KI)),
         ("PD  (Kp=300, Kd=20)", PID(KP, 0, KD)),
         ("PID (Kp=300, Ki=200, Kd=20)", PID(KP, KI, KD))]
fig, ax = plt.subplots()
rows = []
for name, c in cases:
    s = simulate(plant(), c, T=5)
    m = step_metrics(s["t"], s["y"])
    ax.plot(s["t"], s["y"], lw=1.8 if "PID" in name else 1.4, label=name)
    rows.append(fmt_row(name, m))
target_line(ax)
ax.set_xlim(0, 1.5)
ax.set_xlabel("Time (s)"); ax.set_ylabel("Position (m)")
ax.set_title("P, PI, PD and PID on the block (ideal motor, no force limit)")
ax.legend(loc="lower right")
save(fig, "fig06_compare.png")
open(os.path.join(FIG_DIR, "sec6_results.txt"), "w").write("\n".join(rows) + "\n")
print("\n".join(rows))
