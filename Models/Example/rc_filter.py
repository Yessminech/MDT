from fmpy import simulate_fmu
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use("Agg")  # no GUI

fmu_path = "RC_Filter.fmu"

# Simulate 10 ms, request only capacitor voltage
res = simulate_fmu(
    fmu_path,
    start_time=0.0,
    stop_time=0.01,
    output=['C1.v'],        # <--- ONLY this
    step_size=1e-5          # small step for smooth curve
)

t = res['time']
vc = res['C1.v']

plt.figure(figsize=(8, 4))
plt.plot(t, vc, label='Capacitor voltage C1.v')
plt.xlabel("Time [s]")
plt.ylabel("Voltage [V]")
plt.title("Charging of C1 from 0 V to 3.3 V")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("RC_Filter.png", dpi=200)
