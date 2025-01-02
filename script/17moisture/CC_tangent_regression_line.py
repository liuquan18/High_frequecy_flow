# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from src.moisture.longitudinal_contrast import read_data
from sklearn.linear_model import LinearRegression

# %%
first_ratio = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_ratio.nc").__xarray_dataarray_variable__
last_ratio = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_ratio.nc").__xarray_dataarray_variable__


# %%
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
#%%
first_ratio_2060 = first_ratio.sel(lat = slice (20,60)).mean(dim = ('lat', 'lon'))
last_ratio_2060 = last_ratio.sel(lat = slice (20,60)).mean(dim = ('lat', 'lon'))

# %%
plot_tas_std = np.arange(0, 10, 0.1)
# %%
# tangent line
# Calculate tangent lines at T=250K and T=290K
T_tangent = np.array([290.4, 295.6])
dqs_dT_tangent = calculate_dqs_dT(T_tangent) * 1000

# %%
delta_tas = plot_tas_std
# %%
dqs_first = dqs_dT_tangent[0] * delta_tas
# %%
dqs_last = dqs_dT_tangent[1] * delta_tas
# %%
hus_first = first_ratio_2060.values * delta_tas
hus_last = last_ratio_2060.values * delta_tas



# %%
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
# sns.scatterplot(data = df, x = 'tas', y = 'hus', hue = 'decade', size='vt_extreme_freq',sizes=(50,500), ax = ax)

ax.plot(plot_tas_std, hus_first, label="first10")
ax.plot(plot_tas_std, hus_last, label="last10")


ax.plot(
    plot_tas_std,
    dqs_first,
    label="CC tagent_line at 290.4K",
    linestyle="--",
    color="C0",
)
ax.plot(
    plot_tas_std, dqs_last, label="CC tagent_line at 295.6K", linestyle="--", color="C1"
)


ax.legend(ncol=2)

ax.set_xlabel("tas_diff (K)")
ax.set_ylabel("hus_diff (g/kg)")

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/compare_CC_tangent.png")

# %%
