
import numpy as np


class PID:
    def __init__(self, kp, ki=0.0, kd=0.0, dt=0.001,
                 u_min=-np.inf, u_max=np.inf,
                 anti_windup=False, d_on_measurement=False, d_filter_tau=0.0):
        self.kp, self.ki, self.kd, self.dt = kp, ki, kd, dt
        self.u_min, self.u_max = u_min, u_max
        self.anti_windup = anti_windup
        self.d_on_measurement = d_on_measurement
        self.tau = d_filter_tau
        self.reset()

    def reset(self):
        self.integral = 0.0      # stores Ki * sum(e*dt), units of output (N)
        self.prev_e = None
        self.prev_y = None
        self.d_filt = 0.0

    def update(self, setpoint, measurement):
        dt = self.dt
        e = setpoint - measurement

        # --- P: present error
        p = self.kp * e

        # --- D: rate of change of error (or of -measurement)
        if self.prev_e is None:            # first call: no history yet
            d_raw = 0.0
        elif self.d_on_measurement:
            d_raw = -(measurement - self.prev_y) / dt
        else:
            d_raw = (e - self.prev_e) / dt
        a = dt / (self.tau + dt)           # tau = 0 -> a = 1 -> no filtering
        self.d_filt += a * (d_raw - self.d_filt)
        d = self.kd * self.d_filt

        # --- I: accumulated past error (tentative)
        i_new = self.integral + self.ki * e * dt

        u_unsat = p + i_new + d
        u = float(np.clip(u_unsat, self.u_min, self.u_max))

        if self.anti_windup and u != u_unsat:
            # saturated: only accept the integration if it helps leave saturation
            pushing_further = (u_unsat > self.u_max and e > 0) or \
                              (u_unsat < self.u_min and e < 0)
            if not pushing_further:
                self.integral = i_new
        else:
            self.integral = i_new

        self.prev_e, self.prev_y = e, measurement
        self.last_terms = (p, self.integral, d)
        return u
