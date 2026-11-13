
import numpy as np
from common import *

T_RUN = 40.0

def peaks(t, y):
    i = np.where((y[1:-1] > y[:-2]) & (y[1:-1] >= y[2:]))[0] + 1
    return t[i], y[i]

def growth(kp):
    """ratio of the last two oscillation peaks (1 = steady swing)"""
    s = simulate(ThirdOrderLag(), PID(kp), T=T_RUN)
    tp, yp = peaks(s["t"], s["y"] - s["y"][-int(5/DT):].mean())
    return (yp[-1] / yp[-2]) if len(yp) > 2 else 0.0, s

# 1) raise Kp until the output swings steadily (bisection on peak ratio = 1)
lo, hi = 4.0, 12.0
for _ in range(30):
    mid = 0.5 * (lo + hi)
    g, _ = growth(mid)
    lo, hi = (mid, hi) if g < 1 else (lo, mid)
Ku = 0.5 * (lo + hi)
_, s_u = growth(Ku)
tp, _ = peaks(s_u["t"], s_u["y"])
Pu = float(np.mean(np.diff(tp[-6:])))
res = [f"Ku (sim) = {Ku:.3f}  (theory 8)", f"Pu (sim) = {Pu:.3f} s (theory 2*pi/sqrt(3) = {2*np.pi/np.sqrt(3):.3f} s)"]

fig, ax = plt.subplots()
for kp in [4.0, Ku, 9.0]:
    s = simulate(ThirdOrderLag(), PID(kp), T=25)
    ax.plot(s["t"], s["y"], lw=1.4, label=f"Kp={kp:.2f}" + (" = Ku (steady swing)" if kp == Ku else ""))
ax.set_ylim(-0.5, 2.2)
ax.set_xlabel("Time (s)"); ax.set_ylabel("Output y")
ax.set_title(f"Ziegler–Nichols step 1: P only, find Ku = {Ku:.2f}, Pu = {Pu:.2f} s")
ax.legend(loc="upper left")
save(fig, "fig08a_zn_ultimate.png")

# 2) apply recipes, then improve
def gains(kp, ti, td):
    return kp, kp / ti, kp * td

tunings = {
    "Z-N classic (0.6Ku, Pu/2, Pu/8)":    (gains(0.6 * Ku, Pu / 2, Pu / 8), False),
    "Step A: Z-N with Ki cut to 0.8":     ((0.6 * Ku, 0.8, 0.6 * Ku * Pu / 8), False),
    "Improved: Kp=4, Ki=0.8, Kd=3":       ((4.0, 0.8, 3.0), True),
}
fig, ax = plt.subplots()
for name, ((kp, ki, kd), dm) in tunings.items():
    s = simulate(ThirdOrderLag(), PID(kp, ki, kd, d_on_measurement=dm), T=25)
    m = step_metrics(s["t"], s["y"])
    ax.plot(s["t"], s["y"], lw=1.6, label=f"{name}: OS {m['overshoot']:.0f} %, settle {m['settling']:.1f} s")
    res.append(f"{name:40s} Kp={kp:.3f} Ki={ki:.3f} Kd={kd:.3f} D_on_meas={dm} | " + fmt_row("", m))
target_line(ax, 1.0, "Target (1)")
ax.set_xlabel("Time (s)"); ax.set_ylabel("Output y")
ax.set_title("Ziegler–Nichols step 2: apply the recipe, then improve it")
ax.legend(loc="lower right")
save(fig, "fig08b_zn_step.png")

open(os.path.join(FIG_DIR, "sec8_results.txt"), "w").write("\n".join(res) + "\n")
print("\n".join(res))
