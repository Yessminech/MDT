import matplotlib.pyplot as plt
from fmpy import simulate_fmu
import numpy as np

# Constants
FMU_NON_IDEAL = 'ADU_Non_Ideal.fmu'
FMU_IDEAL = 'ADU_Ideal.fmu'
SIM_START = 0.0
SIM_STOP = 1.0

XLABEL = "Input voltage $U_{in}$ (LSB)"
YLABEL = "Digital output code"

# Non-ideal ADU output variables
OUTPUT_NON_IDEAL = ['ramp.y', 'ramp.offset', 'adu.Umin', 'adu.Umax', 'adu.steps', 'adu.int_o']
U_MIN_NI = 'adu.Umin'
U_MAX_NI = 'adu.Umax'
STEPS_NI = 'adu.steps'
INT_O_NI = 'adu.int_o'
RAMP_Y_NI = 'ramp.y'

# Ideal ADU output variables
OUTPUT_IDEAL = ['rampVoltage.v', 'rampVoltage.offset', 'aDUideal.uMin', 'aDUideal.uMax', 'aDUideal.steps', 'aDUideal.yInteger']
U_MIN_I = 'aDUideal.uMin'
U_MAX_I = 'aDUideal.uMax'
STEPS_I = 'aDUideal.steps'
Y_INT_I = 'aDUideal.yInteger'
RAMP_V_I = 'rampVoltage.v'


def adu8bit_non_ideal():  # TODO why is this showing ideal behavior?
    """Simulate non-ideal 8-bit ADU."""
    result = simulate_fmu(
        filename=FMU_NON_IDEAL,
        start_time=SIM_START,
        stop_time=SIM_STOP,
        output=OUTPUT_NON_IDEAL,
        fmi_type='ModelExchange',
    )
    return result


def adu8bit_ideal():
    """Simulate ideal 8-bit ADU."""
    result = simulate_fmu(
        filename=FMU_IDEAL,
        start_time=SIM_START,
        stop_time=SIM_STOP,
        output=OUTPUT_IDEAL,
        fmi_type='ModelExchange',
    )
    return result


def plot_transfer_curve_non_ideal(result, title):
    """Plot transfer curve for non-ideal ADU."""
    umin = float(result[U_MIN_NI][0])
    umax = float(result[U_MAX_NI][0])
    steps = int(result[STEPS_NI][0])
    lsb = (umax - umin) / (steps - 1)

    x = (result[RAMP_Y_NI] - umin) / lsb
    y = result[INT_O_NI].astype(int)

    idx = np.argsort(x)
    x = x[idx]
    y = y[idx]

    y_unique, first_idx = np.unique(y, return_index=True)
    x_clean = x[first_idx]
    y_clean = y_unique

    plt.figure(figsize=(12, 7))
    plt.step(x_clean, y_clean, where='post', linewidth=2, color='blue')
    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_transfer_curve_ideal(result, title):
    """Plot transfer curve for ideal ADU."""
    umin = float(result[U_MIN_I][0])
    umax = float(result[U_MAX_I][0])
    steps = int(result[STEPS_I][0])
    lsb = (umax - umin) / (steps - 1)

    x = (result[RAMP_V_I] - umin) / lsb
    y = result[Y_INT_I].astype(int)

    # TODO understand this sorting and cleaning
    idx = np.argsort(x)
    x = x[idx]
    y = y[idx]

    y_unique, first_idx = np.unique(y, return_index=True)
    x_clean = x[first_idx]
    y_clean = y_unique

    plt.figure(figsize=(12, 7))
    plt.step(x_clean, y_clean, where='post', linewidth=2, color='green')
    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_overlaying_transfer_curves(result_non_ideal, result_ideal, title):
    """Plot overlaying transfer curves for non-ideal vs ideal ADU."""
    # Non-ideal clean
    umin_n = float(result_non_ideal[U_MIN_NI][0])
    umax_n = float(result_non_ideal[U_MAX_NI][0])
    steps_n = int(result_non_ideal[STEPS_NI][0])
    lsb_n = (umax_n - umin_n) / (steps_n - 1)

    x_n = (result_non_ideal[RAMP_Y_NI] - umin_n) / lsb_n
    y_n = result_non_ideal[INT_O_NI].astype(int)

    # TODO understand this sorting and cleaning
    idx_n = np.argsort(x_n)
    x_n = x_n[idx_n]
    y_n = y_n[idx_n]
    y_nu, i_n = np.unique(y_n, return_index=True)
    x_n = x_n[i_n]
    y_n = y_nu

    # Ideal clean
    umin_i = float(result_ideal[U_MIN_I][0])
    umax_i = float(result_ideal[U_MAX_I][0])
    steps_i = int(result_ideal[STEPS_I][0])
    lsb_i = (umax_i - umin_i) / (steps_i - 1)

    # TODO understand this sorting and cleaning
    x_i = (result_ideal[RAMP_V_I] - umin_i) / lsb_i
    y_i = result_ideal[Y_INT_I].astype(int)
    idx_i = np.argsort(x_i)
    x_i = x_i[idx_i]
    y_i = y_i[idx_i]
    y_iu, i_i = np.unique(y_i, return_index=True)
    x_i = x_i[i_i]
    y_i = y_iu

    plt.figure(figsize=(12, 7))
    plt.step(x_n, y_n, where='post', linewidth=2, label='Non-Ideal', color='blue')
    plt.step(x_i, y_i, where='post', linewidth=2, linestyle='--', label='Ideal', color='green')
    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    
# TODO test and complete DNL and INL calculations and plots
def compute_dnl_error(result_non_ideal, result_ideal):
    """Compute Differential Non-Linearity (DNL) error."""
    y_non_ideal = result_non_ideal[INT_O_NI].astype(int)
    y_ideal = result_ideal[Y_INT_I].astype(int)

    dnl_error = np.zeros_like(y_non_ideal, dtype=float)
    for i in range(1, len(y_non_ideal)):
        dnl_error[i] = (y_non_ideal[i] - y_non_ideal[i - 1]) - (y_ideal[i] - y_ideal[i - 1])

    return dnl_error

def compute_inl_error(dnl_error):
    """Compute Integral Non-Linearity (INL) error from DNL error."""
    inl_error = np.cumsum(dnl_error)
    return inl_error

def plot_dnl_error(dnl_error, title):
    """Plot Differential Non-Linearity (DNL) error."""
    plt.figure(figsize=(12, 7))
    plt.plot(dnl_error, marker='o', linestyle='-', color='red')
    plt.xlabel("Digital Output Code")
    plt.ylabel("DNL Error")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
def plot_inl_error(inl_error, title):
    """Plot Integral Non-Linearity (INL) error."""
    plt.figure(figsize=(12, 7))
    plt.plot(inl_error, marker='o', linestyle='-', color='purple')
    plt.xlabel("Digital Output Code")
    plt.ylabel("INL Error")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
def main():
    """Main function to run ADU8bit simulations and plot results."""
    result_adu_non_ideal = adu8bit_non_ideal()
    result_adu_ideal = adu8bit_ideal()

    plot_transfer_curve_non_ideal(result_adu_non_ideal, "Transfer Curve ADU8bit Non-Ideal")
    plot_transfer_curve_ideal(result_adu_ideal, "Transfer Curve ADU8bit Ideal")
    plot_overlaying_transfer_curves(result_adu_non_ideal, result_adu_ideal, "Overlaying Transfer Curves ADU8bit Non-Ideal vs Ideal")
    plot_dnl_error(compute_dnl_error(result_adu_non_ideal, result_adu_ideal), "DNL Error ADU8bit Non-Ideal vs Ideal")
    plot_inl_error(compute_inl_error(compute_dnl_error(result_adu_non_ideal, result_adu_ideal)), "INL Error ADU8bit Non-Ideal vs Ideal")

if __name__ == "__main__":
    main()