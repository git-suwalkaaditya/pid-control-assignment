
from common import *

# a response with clearly visible overshoot so every measure is easy to see
s = simulate(plant(), PID(300, 300, 10), T=1.5)
t, y = s["t"], s["y"]
m = step_metrics(t, y)
yf = m["final"]

fig, ax = plt.subplots(figsize=(7.2, 3.9))
ax.plot(t, y, lw=2, label="Position y(t), PID Kp=300 Ki=300 Kd=10")
target_line(ax)
ax.fill_between(t, 0.98 * yf, 1.02 * yf, color="green", alpha=0.12, label="±2 % settling band")
# rise time
ax.plot([m["t10"], m["t90"]], [0.1 * yf, 0.9 * yf], "o", color="C1")
ax.annotate("", xy=(m["t90"], 0.35), xytext=(m["t10"], 0.35),
            arrowprops=dict(arrowstyle="<->", color="C1"))
ax.text(m["t90"] + 0.02, 0.33, f"① Rise time (10→90 %)\n    = {m['rise']*1000:.0f} ms", color="C1", fontsize=8.5)
# overshoot
ax.annotate("", xy=(m["t_peak"], m["peak"]), xytext=(m["t_peak"], yf),
            arrowprops=dict(arrowstyle="<->", color="C3"))
ax.text(m["t_peak"] + 0.03, m["peak"] - 0.03, f"② Overshoot = {m['overshoot']:.1f} %", color="C3", fontsize=8.5)
# settling
ax.axvline(m["settling"], color="green", ls=":", lw=1.4)
ax.text(m["settling"] + 0.02, 0.62, f"③ Settling time (±2 %)\n    = {m['settling']:.2f} s", color="green", fontsize=8.5)
# steady-state error
ax.text(1.0, 0.62, f"④ Steady-state error\n    = target − final\n    = {m['ss_error']*1000:.2f} mm", fontsize=8.5)
ax.set_xlabel("Time (s)"); ax.set_ylabel("Position (m)")
ax.set_title("The four measures of a step response")
ax.legend(loc="lower right")
save(fig, "fig04_metrics.png")
print(fmt_row("Sec4 example", m))
