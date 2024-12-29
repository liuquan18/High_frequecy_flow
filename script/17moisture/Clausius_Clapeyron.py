#%%
import numpy as np
import matplotlib.pyplot as plt


def calculate_saturation_specific_humidity(T):
    """
    Calculate saturation specific humidity using Clausius-Clapeyron relation
    
    Parameters:
    T (float or array): Temperature in Kelvin
    
    Returns:
    float or array: Saturation specific humidity (kg/kg)
    """
    # Constants
    Rv = 461.5  # Gas constant for water vapor (J/(kg·K))
    Rd = 287.0  # Gas constant for dry air (J/(kg·K))
    L = 2.5e6   # Latent heat of vaporization (J/kg)
    es0 = 611.0 # Reference saturation vapor pressure at T0 (Pa)
    T0 = 273.15 # Reference temperature (K)
    P0 = 101325 # Standard atmospheric pressure (Pa)
    
    # Calculate saturation vapor pressure using Clausius-Clapeyron equation
    es = es0 * np.exp((L/Rv) * (1/T0 - 1/T))
    
    # Calculate saturation specific humidity
    qs = (Rd/Rv) * es / (P0 - (1 - Rd/Rv) * es)
    
    return qs

def calculate_dqs_dT(T):
    """
    Calculate the derivative of saturation specific humidity with respect to temperature
    
    Parameters:
    T (float or array): Temperature in Kelvin
    
    Returns:
    float or array: Derivative of saturation specific humidity (kg/(kg·K))
    """
    # Constants
    Rv = 461.5
    Rd = 287.0
    L = 2.5e6
    es0 = 611.0
    T0 = 273.15
    P0 = 101325
    
    # Calculate es and its derivative
    es = es0 * np.exp((L/Rv) * (1/T0 - 1/T))
    des_dT = es * L/(Rv * T**2)
    
    # Calculate derivative of qs
    dqs_dT = (Rd/Rv) * des_dT * P0 / (P0 - (1 - Rd/Rv) * es)**2
    
    return dqs_dT
#%%
# Create temperature range
T_celsius = np.linspace(-20, 40, 200)
T_kelvin = T_celsius + 273.15

# Calculate q* and its derivative
q_s = calculate_saturation_specific_humidity(T_kelvin)
dqs_dT = calculate_dqs_dT(T_kelvin)

# Calculate tangent lines at T=250K and T=290K
T_tangent = np.array([290.4, 295.6])
q_s_tangent = calculate_saturation_specific_humidity(T_tangent)
dqs_dT_tangent = calculate_dqs_dT(T_tangent)

# Create points for tangent lines
delta_T = 10  # Length of tangent line (±10K)
T_range_tangent = np.array([np.linspace(T, T + delta_T, 100) for T in T_tangent])
q_tangent = [q + dq*(T_line - T) for T, q, dq, T_line in 
             zip(T_tangent, q_s_tangent, dqs_dT_tangent, T_range_tangent)]

# Create the plot
plt.figure(figsize=(12, 8))

# Plot main curve
plt.plot(T_kelvin, q_s, 'b-', linewidth=2, label='q*(T)')

# Plot tangent lines
colors = ['C0', 'C1']
for i, (T, T_line, q_line) in enumerate(zip(T_tangent, T_range_tangent, q_tangent)):
    plt.plot(T_line, q_line, f'{colors[i]}--', 
             label=f'Tangent at T={T}K\n(dq*/dT={dqs_dT_tangent[i]:.2e})')
    plt.plot(T, calculate_saturation_specific_humidity(T), f'{colors[i]}o')

# plt.grid(True)
plt.xlabel('Temperature (K)')
plt.ylabel('Saturation Specific Humidity (kg/kg)')
plt.title('Saturation Specific Humidity and Tangent Lines')
plt.legend()
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

# text 'first10' and 'last10' at the T_tangent[0] and T_tangent[1] points
plt.text(T_tangent[0], calculate_saturation_specific_humidity(T_tangent[0]), 'first10', fontsize=12, ha='right')
plt.text(T_tangent[1], calculate_saturation_specific_humidity(T_tangent[1]), 'last10', fontsize=12, ha='right')



plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/CC_relation.png")
# %%
