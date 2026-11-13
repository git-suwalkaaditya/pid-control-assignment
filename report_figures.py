
import numpy as np
from common import *


def panel_P_PI_PD():
    fig, ax = plt.subplots(1, 3, figsize=(10.5, 3.1), sharey=True)
    for kp in [20, 50, 100, 300]:
        s = simulate(plant(), PID(kp), T=1.2)
        ax[0].plot(s["t"], s["y"], label=f"Kp={kp}")
    for ki in [0, 100, 300, 600]:
        s = simulate(plant(), PID(300, ki), T=3)
        ax[1].plot(s["t"], s["y"], label=f"Ki={ki}")
    for kd in [0, 10, 20, 30]:
        s = simulate(plant(), PID(300, 0, kd), T=1.2)
        ax[2].plot(s["t"], s["y"], label=f"Kd={kd}")
    titles = ["(a) P only", "(b) P + I  (Kp=300)", "(c) P + D  (Kp=300)"]
    for a, ti in zip(ax, titles):
        target_line(a, label="target"); a.set_title(ti); a.set_xlabel("Time (s)"); a.legend(loc="lower right", fontsize=7.5)
    ax[0].set_ylabel("Position (m)")
    save(fig, "rep_P_PI_PD.png")


def panel_real_world():
    fig, ax = plt.subplots(2, 2, figsize=(9.5, 6.2))
    # (a) windup
    for aw, ls in [(False, "-"), (True, "--")]:
        s = simulate(plant(), PID(KP9, KI9, KD9, u_min=-U_MAX, u_max=U_MAX, anti_windup=aw), T=3)
        m = step_metrics(s["t"], s["y"])
        ax[0, 0].plot(s["t"], s["y"], ls, label=("with" if aw else "without") + f" anti-windup ({m['overshoot']:.0f}% OS)")
    target_line(ax[0, 0], label="target")
    ax[0, 0].set_title("(a) 30 N motor limit: windup"); ax[0, 0].set_ylabel("Position (m)")
    # (b) noise
    for tau, lab, lw in [(0.0, "raw D", 0.6), (D_TAU, "filtered D (10 ms)", 1.3)]:
        s = simulate(plant(), PID(KP, KI, KD, d_filter_tau=tau, d_on_measurement=tau > 0), T=1.5, noise=NOISE)
        ax[0, 1].plot(s["t"], s["u"], lw=lw, label=lab)
    ax[0, 1].set_ylim(-40, 80); ax[0, 1].set_title("(b) ±1 mm sensor noise: motor force")
    ax[0, 1].set_ylabel("Force (N)")
    # (c) kick
    for dm, lab in [(False, "D on error"), (True, "D on measurement")]:
        s = simulate(plant(), PID(KP, KI, KD, d_on_measurement=dm), T=1.2, step_time=0.5)
        ax[1, 0].plot(s["t"], s["u"], label=f"{lab} (peak {s['u'].max():,.0f} N)")
    ax[1, 0].set_yscale("symlog", linthresh=100); ax[1, 0].set_xlim(0.4, 1.0)
    ax[1, 0].set_title("(c) target jumps at 0.5 s: derivative kick"); ax[1, 0].set_ylabel("Force (N, log)")
    # (d) sampling
    for dc in [0.001, 0.05, 0.08]:
        s = simulate(plant(), PID(KP, KI, KD), T=1.5, dt_ctrl=dc)
        ax[1, 1].plot(s["t"], s["y"], label=f"update every {dc*1000:.0f} ms")
    target_line(ax[1, 1], label="target"); ax[1, 1].set_ylim(-0.3, 2.3)
    ax[1, 1].set_title("(d) slow controller update"); ax[1, 1].set_ylabel("Position (m)")
    for a in ax.flat:
        a.set_xlabel("Time (s)"); a.legend(loc="best", fontsize=7.5)
    save(fig, "rep_real_world.png")


def panel_zn():
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.2))
    for kp in [4.0, 7.99, 9.0]:
        s = simulate(ThirdOrderLag(), PID(kp), T=20)
        ax[0].plot(s["t"], s["y"], label=f"Kp={kp:g}" + (" (= Ku)" if kp == 7.99 else ""))
    ax[0].set_ylim(-0.6, 2.9); ax[0].set_title("(a) P only: finding Ku and Pu")
    Ku, Pu = 7.99, 3.63
    for (kp, ki, kd), lab in [((0.6 * Ku, 1.2 * Ku / Pu, 0.075 * Ku * Pu), "Z-N table"),
                              ((4.8, 0.8, 0.6 * Ku * Pu / 8), "Ki reduced to 0.8"),
                              ((4.0, 0.8, 3.0), "final: Kp=4, Ki=0.8, Kd=3")]:
        s = simulate(ThirdOrderLag(), PID(kp, ki, kd, d_on_measurement=True), T=25)
        m = step_metrics(s["t"], s["y"])
        ax[1].plot(s["t"], s["y"], label=f"{lab} ({m['overshoot']:.0f}% OS)")
    target_line(ax[1], label="target"); ax[1].set_title("(b) step response after tuning")
    for a in ax:
        a.set_xlabel("Time (s)"); a.set_ylabel("Output"); a.legend(fontsize=7.5, loc="upper right", ncol=3 if a is ax[0] else 1)
    save(fig, "rep_zn.png")


if __name__ == "__main__":
    panel_P_PI_PD(); panel_real_world(); panel_zn()
