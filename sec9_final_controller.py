
import numpy as np
from common import *

ctrl = PID(KP9, KI9, KD9, dt=DT, u_min=-U_MAX, u_max=U_MAX,
           anti_windup=True, d_on_measurement=True, d_filter_tau=D_TAU)
s = simulate(plant(), ctrl, T=3.0, noise=NOISE, seed=1)
m = step_metrics(s["t"], s["y"])

naive = PID(KP9, KI9, KD9, dt=DT, u_min=-U_MAX, u_max=U_MAX)   # same gains, no fixes
sn = simulate(plant(), naive, T=3.0, noise=NOISE, seed=1)
mn = step_metrics(sn["t"], sn["y"])

fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 4.8), sharex=True)
a1.plot(sn["t"], sn["y"], color="C3", lw=1.2, alpha=0.8, label=f"same gains, no fixes: OS {mn['overshoot']:.1f} %")
a1.plot(s["t"], s["y"], color="C0", lw=1.8, label=f"final PID with fixes: OS {m['overshoot']:.2f} %")
target_line(a1)
a1.set_ylabel("Position (m)")
a1.set_title("Final PID on the block: 30 N limit, ±1 mm noise, 1 ms update")
a1.legend(loc="lower right")
a2.plot(sn["t"], sn["u"], color="C3", lw=0.6, alpha=0.7, label="no fixes")
a2.plot(s["t"], s["u"], color="C0", lw=1.2, label="with fixes")
a2.axhline(20, color="gray", ls=":", label="20 N holding force")
a2.set_xlabel("Time (s)"); a2.set_ylabel("Force (N)")
a2.legend(loc="lower right")
save(fig, "fig09_final.png")

# why Ki=600 here and not 200 (Section 6 value): compare under the real limits
c200 = PID(KP, KI, KD, dt=DT, u_min=-U_MAX, u_max=U_MAX, anti_windup=True,
           d_on_measurement=True, d_filter_tau=D_TAU)
s200 = simulate(plant(), c200, T=3.0, noise=NOISE, seed=1)
m200 = step_metrics(s200["t"], s200["y"])

tail = s["t"] > 2.0
lines = [
    f"Gains: Kp={KP9} Ki={KI9} Kd={KD9}, limit ±{U_MAX} N, D filter tau={D_TAU} s, noise ±{NOISE*1000:.0f} mm",
    fmt_row("Final PID (all fixes)", m),
    fmt_row("Same gains, no fixes", mn),
    fmt_row("All fixes but Ki=200", m200) + f"  (error at t=1 s: {(1-s200['y'][1000])*1000:.1f} mm vs {(1-s['y'][1000])*1000:.1f} mm)",
    f"Final PID: force std after settling = {np.std(s['u'][tail]):.2f} N "
    f"(no fixes: {np.std(sn['u'][tail]):.2f} N)",
    f"Final PID: final force = {np.mean(s['u'][tail]):.2f} N (theory k*x = 20 N)",
]
open(os.path.join(FIG_DIR, "sec9_results.txt"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
