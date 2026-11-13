
import numpy as np
from common import *

out = []

# ---------- (a) windup with a 30 N motor ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2))
for aw, ls in [(False, "-"), (True, "--")]:
    s = simulate(plant(), PID(KP9, KI9, KD9, u_min=-U_MAX, u_max=U_MAX, anti_windup=aw), T=3)
    m = step_metrics(s["t"], s["y"])
    lab = "anti-windup ON" if aw else "no anti-windup"
    a1.plot(s["t"], s["y"], ls, lw=1.6, label=f"{lab}: OS {m['overshoot']:.1f} %")
    a2.plot(s["t"], s["u"], ls, lw=1.4, label=lab)
    out.append(fmt_row(f"7a {lab}", m))
target_line(a1)
a1.set_title("(a) Position with 30 N motor limit"); a1.set_xlabel("Time (s)"); a1.set_ylabel("Position (m)")
a1.legend(loc="lower right")
a2.axhline(20, color="gray", ls=":", label="20 N needed to hold 1 m")
a2.set_title("(a) Motor force"); a2.set_xlabel("Time (s)"); a2.set_ylabel("Force (N)")
a2.legend(loc="lower right")
save(fig, "fig07a_windup.png")

# ---------- (b) noisy sensor makes D jumpy ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2))
for tau, lab in [(0.0, "raw D"), (D_TAU, f"filtered D (τ={D_TAU*1000:.0f} ms)")]:
    s = simulate(plant(), PID(KP, KI, KD, d_filter_tau=tau, d_on_measurement=tau > 0), T=2.0, noise=NOISE)
    tail = s["t"] > 1.0
    a1.plot(s["t"], s["u"], lw=0.7 if tau == 0 else 1.3, label=f"{lab}: σ(u)={np.std(s['u'][tail]):.1f} N")
    a2.plot(s["t"], (s["y"] - 1) * 1000, lw=0.8, label=lab)
    out.append(f"7b {lab:24s} force std (t>1s) = {np.std(s['u'][tail]):.2f} N, "
               f"peak-to-peak = {np.ptp(s['u'][tail]):.1f} N, position std = {np.std(s['y'][tail])*1000:.3f} mm")
a1.set_ylim(-60, 100); a1.set_xlim(0, 2)
a1.set_title("(b) Motor force with ±1 mm noise"); a1.set_xlabel("Time (s)"); a1.set_ylabel("Force (N)")
a1.legend(loc="upper right")
a2.set_xlim(1.0, 2.0); a2.set_ylim(-1.5, 1.5)
a2.set_title("(b) Position error after settling"); a2.set_xlabel("Time (s)"); a2.set_ylabel("y − 1 (mm)")
a2.legend(loc="lower right")
save(fig, "fig07b_noise.png")

# ---------- (c) derivative kick ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2))
for dm, lab in [(False, "D on error"), (True, "D on measurement")]:
    s = simulate(plant(), PID(KP, KI, KD, d_on_measurement=dm), T=2.5, step_time=0.5)
    a1.plot(s["t"], s["u"], lw=1.4, label=f"{lab}: peak {s['u'].max():.0f} N")
    a2.plot(s["t"], s["y"], lw=1.4, label=lab)
    out.append(f"7c {lab:18s} peak force = {s['u'].max():.1f} N  " +
               fmt_row("", step_metrics(s["t"], s["y"], t0=0.5)))
a1.set_yscale("symlog", linthresh=100)
a1.set_xlim(0.3, 1.5); a2.set_xlim(0.3, 1.5)
a1.set_title("(c) Force when target jumps at t=0.5 s"); a1.set_xlabel("Time (s)"); a1.set_ylabel("Force (N, log scale)")
a1.legend(loc="upper left")
a2.plot(s["t"], s["r"], "k--", lw=0.9, label="Target")
a2.set_title("(c) Position"); a2.set_xlabel("Time (s)"); a2.set_ylabel("Position (m)")
a2.legend(loc="lower right")
save(fig, "fig07c_kick.png")

# ---------- (d) slow controller update ----------
fig, ax = plt.subplots()
for dc in [0.001, 0.05, 0.07, 0.08]:
    s = simulate(plant(), PID(KP, KI, KD), T=2.0, dt_ctrl=dc)
    m = step_metrics(s["t"], s["y"])
    swing = np.ptp(s["y"][s["t"] > 1.5])
    tag = ("UNSTABLE (grows)" if np.abs(s["y"]).max() > 2 else
           f"keeps swinging ±{swing/2:.2f} m" if swing > 0.05 else f"OS {m['overshoot']:.1f} %")
    ax.plot(s["t"], s["y"], lw=1.4, label=f"update every {dc*1000:.0f} ms: {tag}")
    out.append(f"7d dt={dc*1000:4.0f} ms max|y|={np.abs(s['y']).max():8.3f} " + fmt_row("", m))
target_line(ax)
ax.set_ylim(-0.3, 2.5)
ax.set_xlabel("Time (s)"); ax.set_ylabel("Position (m)")
ax.set_title("(d) Updating the controller too slowly causes bounce, then instability")
ax.legend(loc="upper right")
save(fig, "fig07d_sampling.png")

open(os.path.join(FIG_DIR, "sec7_results.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
