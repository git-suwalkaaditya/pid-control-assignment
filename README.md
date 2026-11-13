# PID Control:
Code for the Modern Monk Labs *Physical AI* intern assignment. 

## Setup

```bash
pip install numpy matplotlib        # tested with numpy 2.x, matplotlib 3.x, Python 3.10+
```

## Recreate every graph

```bash
python run_all.py
```
 All figures are written to `figures/`, and every number quoted in the report is written to `figures/secN_results.txt`. The noise uses a fixed random seed, so everyone gets identical graphs.

You can also run one section at a time:

| Script | Report section | Output |
|---|---|---|
| `sec1_loop_diagram.py` | 1. Basic idea | `fig01_loop.png` |
| `sec4_metrics.py` | 4. How to judge a result | `fig04_metrics.png` |
| `sec5_each_part.py` | 5. Each part alone (P, PI, PD + theory check) | `fig05a/b/c_*.png`, `sec5_results.txt` |
| `sec6_compare.py` | 6. P vs PI vs PD vs PID | `fig06_compare.png`, `sec6_results.txt` |
| `sec7_real_world.py` | 7. Windup, noise, kick, slow update | `fig07a/b/c/d_*.png`, `sec7_results.txt` |
| `sec8_ziegler_nichols.py` | 8. Ziegler–Nichols on 1/(s+1)³ | `fig08a/b_*.png`, `sec8_results.txt` |
| `sec9_final_controller.py` | 9. Final PID with all fixes | `fig09_final.png`, `sec9_results.txt` |
| `report_figures.py` | combined figures used in the report | `rep_*.png` |

## Try your own change

`experiment.py` runs the final controller and lets you change one thing at a time from the command line:

```bash
python experiment.py --m 2                    # heavier block (2 kg)
python experiment.py --kp 100 --ki 0 --kd 0   # P only, Kp = 100
python experiment.py --noise 0.005            # ±5 mm sensor noise
python experiment.py --umax 25 --no-aw        # 25 N motor, anti-windup off
python experiment.py --dt 0.05                # controller updates every 50 ms
```

It prints the four measures and saves `figures/experiment.png`.

## Code layout

```
pidlab/
  pid.py       PID class: limits, anti-windup, D on measurement, D filter
  plants.py    MassSpringDamper, ThirdOrderLag (1/(s+1)^3), simulate() with RK4 + zero-order hold
  metrics.py   rise time, overshoot, settling time, steady-state error
common.py      plant values, chosen gains, plot style
```

### Using the PID in your own loop

```python
from pidlab import PID
pid = PID(kp=300, ki=600, kd=20, dt=0.001, u_min=-30, u_max=30,
          anti_windup=True, d_on_measurement=True, d_filter_tau=0.01)
while True:
    u = pid.update(setpoint, sensor_reading)   # call once every dt seconds
    motor.apply(u)
```

## Simulation details

- The plant is integrated with 4th-order Runge–Kutta at 1 ms.
- The controller runs every `dt_ctrl` seconds (1 ms by default) and holds its output in between, like a real microcontroller.
- Sensor noise is uniform in ±1 mm with seed 0 (seed 1 in Section 9).
- Metrics are measured against the response's own final value, the same way MATLAB's `stepinfo` does. Rise time is 10→90 %, and the settling band is ±2 %.
