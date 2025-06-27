# %%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_helper.read_variable import read_climatology_decmean

#%%

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
    L = 2.5e6  # Latent heat of vaporization (J/kg)
    es0 = 611.0  # Reference saturation vapor pressure at T0 (Pa)
    T0 = 273.15  # Reference temperature (K)
    P0 = 101325  # Standard atmospheric pressure (Pa)

    # Calculate saturation vapor pressure using Clausius-Clapeyron equation
    es = es0 * np.exp((L / Rv) * (1 / T0 - 1 / T))

    # Calculate saturation specific humidity
    qs = (Rd / Rv) * es / (P0 - (1 - Rd / Rv) * es)

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
    es = es0 * np.exp((L / Rv) * (1 / T0 - 1 / T))
    des_dT = es * L / (Rv * T**2)

    # Calculate derivative of qs
    dqs_dT = (Rd / Rv) * des_dT * P0 / (P0 - (1 - Rd / Rv) * es) ** 2

    return dqs_dT


# %%
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
delta_T = 13  # Length of tangent line (±10K)
T_range_tangent = np.array([np.linspace(T, T + delta_T, 100) for T in T_tangent])
q_tangent = [
    q + dq * (T_line - T)
    for T, q, dq, T_line in zip(T_tangent, q_s_tangent, dqs_dT_tangent, T_range_tangent)
]
#%%
# qpqp

qp = read_climatology_decmean('hus_prime', name = 'hus')
#%%
# convert to g/kg
qp = qp * 1000  # Convert from kg/kg to g/kg

#%%
# to pandas dataframe
qp['year'] = qp.year- 9
#%%
qp_df = qp.to_dataframe().reset_index()


# %%
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
# plot CC
# Plot main curve
axes[0].plot(T_kelvin, q_s, "k-", linewidth=2, label="q*(T)")

# Plot tangent lines
colors = ["C0", "C1"]
for i, (T, T_line, q_line) in enumerate(zip(T_tangent, T_range_tangent, q_tangent)):
    axes[0].plot(T_line, q_line, f"{colors[i]}--", label=f"Tangent at T={T}K")
    axes[0].plot(T, calculate_saturation_specific_humidity(T), f"{colors[i]}o")

delta_x = np.arange(T_tangent[0], T_tangent[0] + 9, 0.1)

# hline
axes[0].plot(
    delta_x,
    [calculate_saturation_specific_humidity(T_tangent[0])] * len(delta_x),
    "C0",
    linestyle="dotted",
)

# vline at T_tangent[0] + 9
axes[0].plot(
    [T_tangent[0] + 9] * len(delta_x),
    np.linspace(
        calculate_saturation_specific_humidity(T_tangent[0]),
        calculate_saturation_specific_humidity(T_tangent[0] + 7),
        len(delta_x),
    ),
    "C0",
    linestyle="dotted",
)

# Add text annotations
axes[0].text(
    T_tangent[0] + 4.5,
    calculate_saturation_specific_humidity(T_tangent[0]) - 0.003,
    r"$T'$",
    fontsize=12,
    ha="center",
)
axes[0].text(
    T_tangent[0] + 10,
    calculate_saturation_specific_humidity(T_tangent[0] + 7) / 2 + 0.006,
    r"$q^*'$",
    fontsize=12,
    va="center",
    rotation=90,
)

# axes[0].grid(True)
axes[0].set_xlabel("Temperature (K)")
axes[0].set_ylabel("Saturation Specific Humidity (kg/kg)")
axes[0].legend()
axes[0].ticklabel_format(style="sci", axis="y", scilimits=(0, 0))

# text 'first10' and 'last10' at the T_tangent[0] and T_tangent[1] points
axes[0].text(
    T_tangent[0] - 2,
    calculate_saturation_specific_humidity(T_tangent[0]),
    "first10",
    fontsize=12,
    ha="right",
    color="C0",
)
axes[0].text(
    T_tangent[1] - 2,
    calculate_saturation_specific_humidity(T_tangent[1]),
    "last10",
    fontsize=12,
    ha="right",
    color="C1",
)

# Change y-tick labels from kg/kg to g/kg
yticks = axes[0].get_yticks()
axes[0].set_yticklabels([f"{y * 1000:.0f}" for y in yticks])
axes[0].set_ylabel("Saturation varpor pressure (hPa)")



sns.lineplot(
    data=qp_df,
    x="year",
    y="hus",
    ax=axes[1],
    color='k',
    linewidth=2,
)
axes[1].ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
axes[1].set_ylabel(r"$q'$ (g/kg)")


# Add 'a' at the left corner of the first subplot
axes[0].text(
    -0.05,
    1.05,
    "a",
    transform=axes[0].transAxes,
    fontsize=16,
    fontweight="bold",
    va="top",
    ha="right",
)
axes[1].text(
    -0.05,
    1.05,
    "b",
    transform=axes[1].transAxes,
    fontsize=16,
    fontweight="bold",
    va="top",
    ha="right",
)


plt.tight_layout()

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0main_text/CC_moisture_tangent_slope.pdf",
    dpi=300,
)
# %%
