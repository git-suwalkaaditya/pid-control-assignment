
import numpy as np
from common import *

lines = []
# ---------------- P only ----------------
kps = [20, 50, 100, 300]
fig, ax = plt.subplots()
lines.append("P only: theory vs simulation")
for kp in kps:
    s = simulate(plant(), PID(kp), T=1.5)
    m = step_metrics(s["t"], s["y"])
    final_th = kp / (K + kp)
    wn = np.sqrt(K + kp); zeta = C / (2 * wn)
    os_th = 100 * np.exp(-np.pi * zeta / np.sqrt(1 - zeta**2)) if zeta < 1 else 0.0
    ax.plot(s["t"], s["y"], lw=1.8, label=f"Kp={kp}: stops at {m['final']:.3f} m")
    ax.axhline(final_th, color=ax.lines[-1].get_color(), ls=":", lw=0.8)
    lines.append(f"Kp={kp:4d} final theory={final_th:.4f} sim={m['final']:.4f} | "
                 f"zeta={zeta:.3f} OS theory={os_th:5.2f}% sim={m['overshoot']:5.2f}% | "
                 f"rise={m['rise']:.3f}s settle={m['settling']:.3f}s")
target_line(ax)
ax.set_xlabel("Time (s)"); ax.set_ylabel("Position (m)")
ax.set_title("P only: a stronger Kp gets closer to 1 m but bounces more")
ax.legend(loc="lower right")
save(fig, "fig05a_P_only.png")

# ---------------- add I (PI) ----------------
fig, ax = plt.subplots()
lines.append("PI (Kp=300)")
for ki in [0, 100, 300, 600]:
    s = simulate(plant(), PID(300, ki), T=3)
    m = step_metrics(s["t"], s["y"])
    ax.plot(s["t"], s["y"], lw=1.6, label=f"Ki={ki}: final {m['final']:.4f} m, OS {m['overshoot']:.0f} %")
    lines.append(fmt_row(f"PI Ki={ki}", m))
target_line(ax)
ax.set_xlabel("Time (s)"); ax.set_ylabel("Position (m)")
ax.set_title("Adding I (Kp=300): the 62.5 mm gap is removed, bounce stays")
ax.legend(loc="lower right")
save(fig, "fig05b_PI.png")

# ---------------- add D (PD) ----------------
fig, ax = plt.subplots()
lines.append("PD (Kp=300): damping ratio zeta = (c+Kd)/(2*sqrt(k+Kp))")
for kd in [0, 10, 20, 30]:
    s = simulate(plant(), PID(300, 0, kd), T=1.5)
    m = step_metrics(s["t"], s["y"])
    zeta = (C + kd) / (2 * np.sqrt(K + 300))
    ax.plot(s["t"], s["y"], lw=1.6, label=f"Kd={kd}: ζ={zeta:.2f}, OS {m['overshoot']:.1f} %")
    lines.append(f"Kd={kd:3d} zeta={zeta:.3f} " + fmt_row("", m))
target_line(ax)
ax.set_xlabel("Time (s)"); ax.set_ylabel("Position (m)")
ax.set_title("Adding D (Kp=300): extra damping removes the bounce")
ax.legend(loc="lower right")
save(fig, "fig05c_PD.png")

open(os.path.join(FIG_DIR, "sec5_results.txt"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
