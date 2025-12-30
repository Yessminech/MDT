import matplotlib.pyplot as plt
from fmpy import simulate_fmu

# Color constants
COLOR_BLUE = 'tab:blue'
COLOR_ORANGE = 'tab:orange'


def ADU8bit_non_ideal(): # TODO why is this showing ideal behavior?
    fmu_file = '/tmp/OpenModelica_yessmine/OMEdit/ADU_Non_Ideal.fmu'

    uin = 'ramp.y'      
    uout = 'dau.real_o'   

    tstart = 0.0
    tstop = 0.1

    result_adu = simulate_fmu(
        filename=fmu_file,
        start_time=tstart,
        stop_time=tstop,
        output=[uin, uout],
        fmi_type='ModelExchange',      
    )
    return result_adu

def ADU8bit_ideal():
    fmu_file = '/tmp/OpenModelica_yessmine/OMEdit/ADU_Ideal.fmu'

    uin = 'rampVoltage.v'      
    uout = 'aDUideal.y'   

    tstart = 0.0
    tstop = 0.1

    result_adu = simulate_fmu(
        filename=fmu_file,
        start_time=tstart,
        stop_time=tstop,
        output=[uin, uout],
        fmi_type='ModelExchange',    
    )
    return result_adu


plt.close('all')
 
# ADU8bit simulation
# non-ideal and ideal case side by side
result_adu_non_ideal = ADU8bit_non_ideal()
result_adu_ideal = ADU8bit_ideal()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Values")
ax1.plot(result_adu_non_ideal['time'], result_adu_non_ideal['ramp.y'], color=COLOR_BLUE, label='Input Voltage (V)')
ax1.plot(result_adu_non_ideal['time'], result_adu_non_ideal['dau.real_o'], color=COLOR_ORANGE, label='ADU Output (V)')
ax1.set_title("Non-Ideal ADU8bit")
ax1.legend()

ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Values")
ax2.plot(result_adu_ideal['time'], result_adu_ideal['rampVoltage.v'], color=COLOR_BLUE, label='Input Voltage (V)')
ax2.plot(result_adu_ideal['time'], result_adu_ideal['aDUideal.y'], color=COLOR_ORANGE, label='ADU Output (V)')
ax2.set_title("Ideal ADU8bit")
ax2.legend()

fig.suptitle("FMU Simulation Results for ADU8bit")
fig.tight_layout()
plt.show()
