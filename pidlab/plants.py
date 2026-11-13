
import numpy as np


class MassSpringDamper:
    """m x'' + c x' + k x = u    ->   G(s) = 1 / (m s^2 + c s + k)"""
    def __init__(self, m=1.0, c=10.0, k=20.0):
        self.m, self.c, self.k = m, c, k
        self.x0 = np.zeros(2)            # [position (m), velocity (m/s)]

    def deriv(self, x, u):
        pos, vel = x
        return np.array([vel, (u - self.c * vel - self.k * pos) / self.m])

    def output(self, x):
        return x[0]


class ThirdOrderLag:
    """G(s) = 1 / (s + 1)^3  realised as three first-order lags in series."""
    def __init__(self):
        self.x0 = np.zeros(3)

    def deriv(self, x, u):
        return np.array([-x[0] + u, -x[1] + x[0], -x[2] + x[1]])

    def output(self, x):
        return x[2]


def _rk4(plant, x, u, h):
    k1 = plant.deriv(x, u)
    k2 = plant.deriv(x + 0.5 * h * k1, u)
    k3 = plant.deriv(x + 0.5 * h * k2, u)
    k4 = plant.deriv(x + h * k3, u)
    return x + h / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


def simulate(plant, controller, setpoint=1.0, T=3.0, dt_sim=0.001,
             dt_ctrl=None, noise=0.0, seed=0, step_time=0.0):
    """Run a closed loop.

    setpoint : final target; it jumps from 0 to this value at step_time.
    noise    : sensor noise amplitude, uniform in [-noise, +noise].
    Returns dict with t, y (true output), y_meas, u, r arrays.
    """
    dt_ctrl = dt_ctrl or dt_sim
    ratio = max(1, int(round(dt_ctrl / dt_sim)))
    controller.dt = ratio * dt_sim
    controller.reset()
    rng = np.random.default_rng(seed)

    n = int(round(T / dt_sim)) + 1
    t = np.arange(n) * dt_sim
    y = np.zeros(n); ym = np.zeros(n); u_log = np.zeros(n); r_log = np.zeros(n)
    x = plant.x0.copy()
    u = 0.0
    for i in range(n):
        r = setpoint if t[i] >= step_time - 1e-12 else 0.0
        y[i] = plant.output(x)
        ym[i] = y[i] + (rng.uniform(-noise, noise) if noise > 0 else 0.0)
        if i % ratio == 0:                     # controller sample instant
            u = controller.update(r, ym[i])
        u_log[i], r_log[i] = u, r
        x = _rk4(plant, x, u, dt_sim)
    return dict(t=t, y=y, y_meas=ym, u=u_log, r=r_log)
