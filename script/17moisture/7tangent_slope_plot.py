# %%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns


# %%
def read_data(decade):
    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/husDBtas_hussatDBtas_dec/moist_tas_ratio_{decade}.nc"
    data = xr.open_dataset(base_dir)
    return data


# %%
def sector(data):
    box_EAA = [
        -35,
        140,
        20,
        60,
    ]  # [lon_min, lon_max, lat_min, lat_max] Eurasia and Africa
    box_NAM = [-145, -70, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North America
    box_NAL = [-70, -35, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Atlantic
    box_NPO = [140, -145, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Pacific

    data_EAA = data.sel(lon=slice(box_EAA[0], box_EAA[1])).mean(dim=("lon", "lat"))
    data_NAM = data.sel(lon=slice(box_NAM[0], box_NAM[1])).mean(dim=("lon", "lat"))
    data_NAL = data.sel(lon=slice(box_NAL[0], box_NAL[1])).mean(dim=("lon", "lat"))
    data_NPO1 = data.sel(lon=slice(box_NPO[0], 180))
    data_NPO2 = data.sel(lon=slice(-180, box_NPO[1]))
    data_NPO = xr.concat([data_NPO1, data_NPO2], dim="lon").mean(dim=("lon", "lat"))
    return data_EAA, data_NAM, data_NAL, data_NPO


# %%
dfs = []

for i in range(1850, 2100, 10):
    data = read_data(i)
    EAA, NAM, NAL, NPO = sector(data)

    dfs.append(
        {
            "decade": i,
            "hus": EAA.hus.values.item(),
            "hussat": EAA.hussat.values.item(),
            "region": "EAA",
        }
    )
    dfs.append(
        {
            "decade": i,
            "hus": NAM.hus.values.item(),
            "hussat": NAM.hussat.values.item(),
            "region": "NAM",
        }
    )
    dfs.append(
        {
            "decade": i,
            "hus": NAL.hus.values.item(),
            "hussat": NAL.hussat.values.item(),
            "region": "NAL",
        }
    )
    dfs.append(
        {
            "decade": i,
            "hus": NPO.hus.values.item(),
            "hussat": NPO.hussat.values.item(),
            "region": "NPO",
        }
    )

df = pd.DataFrame(dfs)
# %%
# minus the value of 1850 ['hus', 'hussat'] from all values
df_ano = pd.DataFrame()
df_ano["decade"] = df["decade"]
df_ano["hus"] = df["hus"] - df[df["decade"] == 1850]["hus"].values[0]
df_ano["hussat"] = df["hussat"] - df[df["decade"] == 1850]["hussat"].values[0]
df_ano["region"] = df["region"]
# %%
# CC


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
    r"$\Delta tas$",
    fontsize=12,
    ha="center",
)
axes[0].text(
    T_tangent[0] + 9.9,
    calculate_saturation_specific_humidity(T_tangent[0] + 7) / 2 + 0.006,
    r"$\Delta hus$",
    fontsize=12,
    va="center",
    rotation=90,
)

# axes[0].grid(True)
axes[0].set_xlabel("Temperature (K)")
axes[0].set_ylabel("Saturation Specific Humidity (kg/kg)")
axes[0].set_title("Clausius-Clapeyron Relation")
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

# Add 'a' at the left corner of the first subplot
axes[0].text(-0.05, 1.05, 'a', transform=axes[0].transAxes, fontsize=16, fontweight='bold', va='top', ha='right')

## plot the ratio
# Update the region labels
df["region"] = df["region"].replace(
    {
        "EAA": "Eurasia_North_Africa",
        "NAM": "North_America",
        "NAL": "North_Atlantic",
        "NPO": "North_Pacific",
    }
)

sns.lineplot(
    data=df,
    x="decade",
    y="hus",
    hue="region",
    ax=axes[1],
    palette=[
        sns.color_palette()[3],
        sns.color_palette()[1],
        sns.color_palette()[0],
        sns.color_palette()[-1],
    ],
)
sns.lineplot(
    data=df,
    x="decade",
    y="hussat",
    hue="region",
    ax=axes[1],
    linestyle="dotted",
    legend=False,
    palette=[
        sns.color_palette()[3],
        sns.color_palette()[1],
        sns.color_palette()[0],
        sns.color_palette()[-1],
    ],
)

axes[1].set_title("Moist-get-moister in continents and oceans")
axes[1].set_ylabel(r"$\Delta$ moisture / $\Delta$ tas ($g \cdot kg^{-1}K^{-1}$)")

# create custom legend, solid line for 'hus' and dashed line for 'hussat'
handles, labels = axes[1].get_legend_handles_labels()
lines = [
    plt.Line2D([0], [0], color="grey", lw=2),
    plt.Line2D([0], [0], color="grey", lw=2, linestyle="dotted"),
]
custom_labels = ["hus", "hussat"]
axes[1].legend(handles + lines, labels + custom_labels, loc="upper left", frameon=False)


# Update legend to match line colors and remove lines before labels
new_labels = [
    "Eurasia_North_Africa",
    "North_America",
    "North_Atlantic",
    "North_Pacific",
    "hus",
    "hussat",
]
new_colors = [
    sns.color_palette()[3],
    sns.color_palette()[1],
    sns.color_palette()[0],
    sns.color_palette()[-1],
]

for text, color in zip(axes[1].get_legend().get_texts()[:4], new_colors):
    text.set_color(color)

# Remove lines before labels
for handle in axes[1].get_legend().legendHandles[:4]:
    handle.set_visible(False)
axes[1].set_ylim(0.39, 1.05)

# Add 'b' at the left corner of the second subplot
axes[1].text(-0.05, 1.05, 'b', transform=axes[1].transAxes, fontsize=16, fontweight='bold', va='top', ha='right')

plt.tight_layout()

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/CC_moisture_tangent_slope.pdf", dpi = 300)
# %%
