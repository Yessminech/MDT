from fmpy import simulate_fmu
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")      # Or remove this if you fixed GUI backend

res = simulate_fmu(
    'RC_Filter.fmu',
    start_time=0,
    stop_time=0.01,
    output=['Vin.signalSource.y', 'Vs.v'],
    start_values={'Vin.f': 1000, 'Vin.V': 1.0}
)

t = res['time']
vin = res['Vin.signalSource.y']        # INPUT
vout = res['Vs.v']        # OUTPUT

plt.plot(t, vin, label='Vin (input)')
plt.plot(t, vout, label='Vout (Vs.v)')
plt.legend()
plt.grid(True)
plt.savefig("rc_filter.png", dpi=200)
