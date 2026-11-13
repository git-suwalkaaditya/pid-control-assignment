
import numpy as np


def step_metrics(t, y, target=1.0, t0=0.0, band=0.02):
    m = t >= t0
    t, y = t[m] - t0, y[m]
    tail = max(1, len(y) // 20)
    yf = float(np.mean(y[-tail:]))
    out = dict(final=yf, ss_error=target - yf)
    if abs(yf) < 1e-9:
        return dict(out, rise=np.nan, overshoot=np.nan, settling=np.nan, peak=np.nan, t_peak=np.nan)

    def first_cross(level):
        idx = np.argmax(y >= level)
        if y[idx] < level:
            return np.nan
        if idx == 0:
            return t[0]
        # linear interpolation between samples
        return t[idx - 1] + (level - y[idx - 1]) * (t[idx] - t[idx - 1]) / (y[idx] - y[idx - 1])

    t10, t90 = first_cross(0.1 * yf), first_cross(0.9 * yf)
    ipk = int(np.argmax(y))
    overshoot = max(0.0, (y[ipk] - yf) / yf * 100)
    outside = np.where(np.abs(y - yf) > band * abs(yf))[0]
    settling = 0.0 if len(outside) == 0 else t[min(outside[-1] + 1, len(t) - 1)]
    return dict(out, rise=t90 - t10, t10=t10, t90=t90, overshoot=overshoot,
                peak=float(y[ipk]), t_peak=float(t[ipk]), settling=float(settling))


def fmt_row(name, mt):
    return (f"{name:<28s} rise={mt['rise']:6.3f}s  OS={mt['overshoot']:6.2f}%  "
            f"settle={mt['settling']:6.3f}s  final={mt['final']:7.4f}m  ess={mt['ss_error']*1000:8.2f}mm")
