"""

Examples
  python experiment.py                         # final PID on the given block
  python experiment.py --m 2                   # heavier block
  python experiment.py --kp 100 --ki 0 --kd 0  # P only
  python experiment.py --noise 0.005           # +/-5 mm sensor noise
  python experiment.py --umax 25 --no-aw       # weaker motor, anti-windup off
  python experiment.py --dt 0.05               # controller updates every 50 ms
"""
import argparse
import numpy as np
from common import *

ap = argparse.ArgumentParser()
ap.add_argument("--m", type=float, default=M); ap.add_argument("--c", type=float, default=C)
ap.add_argument("--k", type=float, default=K)
ap.add_argument("--kp", type=float, default=KP9); ap.add_argument("--ki", type=float, default=KI9)
ap.add_argument("--kd", type=float, default=KD9)
ap.add_argument("--umax", type=float, default=U_MAX, help="force limit in N (use 0 for no limit)")
ap.add_argument("--noise", type=float, default=NOISE, help="sensor noise amplitude in m")
ap.add_argument("--tau", type=float, default=D_TAU, help="D filter time constant in s")
ap.add_argument("--dt", type=float, default=DT, help="controller update period in s")
ap.add_argument("--target", type=float, default=TARGET)
ap.add_argument("--T", type=float, default=3.0)
ap.add_argument("--no-aw", action="store_true", help="switch anti-windup off")
a = ap.parse_args()

lim = a.umax if a.umax > 0 else np.inf
ctrl = PID(a.kp, a.ki, a.kd, u_min=-lim, u_max=lim, anti_windup=not a.no_aw,
           d_on_measurement=True, d_filter_tau=a.tau)
s = simulate(MassSpringDamper(a.m, a.c, a.k), ctrl, setpoint=a.target, T=a.T,
             dt_ctrl=a.dt, noise=a.noise)
m = step_metrics(s["t"], s["y"], target=a.target)
print(vars(a)); print(fmt_row("result", m))
print(f"P-only theory: final = Kp/(k+Kp)*target = {a.kp/(a.k+a.kp)*a.target:.4f} m; "
      f"holding force k*target = {a.k*a.target:.1f} N")

fig, (a1, a2) = plt.subplots(2, 1, figsize=(7, 4.8), sharex=True)
a1.plot(s["t"], s["y"], label="position"); target_line(a1, a.target, "target")
a1.set_ylabel("Position (m)"); a1.legend(); a1.set_title(f"Experiment: OS {m['overshoot']:.1f} %, settle {m['settling']:.2f} s")
a2.plot(s["t"], s["u"], lw=0.8, label="force"); a2.set_xlabel("Time (s)"); a2.set_ylabel("Force (N)"); a2.legend()
save(fig, "experiment.png")
