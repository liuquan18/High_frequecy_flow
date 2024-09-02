#%%
import xarray as xr
import numpy as np
import pandas as pd
import logging
import glob
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from metpy.units import units

# Any import of metpy will activate the accessors
import metpy.calc as mpcalc
from metpy.units import units
# spatial smoothing
from scipy.ndimage import gaussian_filter

# %%
logging.basicConfig(level=logging.INFO)

# %%
import src.composite.composite as composite
import src.extremes.extreme_read as ext_read
import src.composite.composite_plot as composite_plot

# %%
from src.composite.composite import composite_variable

# %%
plev = 25000

N_first10_pos, N_first10_neg = composite_variable("E_N", plev, "prime", "first10")
N_last10_pos, N_last10_neg = composite_variable("E_N", plev, "prime", "last10")

# %%
crs_attrs_file = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_ano_first10/ua_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_18500501-18590931_ano.nc")
# %%
N_first10_pos = N_first10_pos.to_dataset()
N_first10_neg = N_first10_neg.to_dataset()
N_last10_pos = N_last10_pos.to_dataset()
N_last10_neg = N_last10_neg.to_dataset()

N_first10_pos = N_first10_pos.assign_attrs(crs_attrs_file.attrs)
N_first10_neg = N_first10_neg.assign_attrs(crs_attrs_file.attrs)
N_last10_pos = N_last10_pos.assign_attrs(crs_attrs_file.attrs)
N_last10_neg = N_last10_neg.assign_attrs(crs_attrs_file.attrs)
# %%
# metpy
N_first10_pos = N_first10_pos.metpy.parse_cf()
N_first10_neg = N_first10_neg.metpy.parse_cf()
N_last10_pos = N_last10_pos.metpy.parse_cf()
N_last10_neg = N_last10_neg.metpy.parse_cf()
# %%
# multiply units (m**2/s**2)
N_first10_pos = N_first10_pos * units("m**2/s**2")
N_first10_pos = N_first10_pos.metpy.quantify()

N_first10_neg = N_first10_neg * units("m**2/s**2")
N_first10_neg = N_first10_neg.metpy.quantify()

N_last10_pos = N_last10_pos * units("m**2/s**2")
N_last10_pos = N_last10_pos.metpy.quantify()

N_last10_neg = N_last10_neg * units("m**2/s**2")
N_last10_neg = N_last10_neg.metpy.quantify()
# %%
# spatial smoothing
N_first10_pos_sm = mpcalc.smooth_gaussian(N_first10_pos.ua, 5)
N_first10_neg_sm = mpcalc.smooth_gaussian(N_first10_neg.ua, 5)
N_last10_pos_sm = mpcalc.smooth_gaussian(N_last10_pos.ua, 5)
N_last10_neg_sm = mpcalc.smooth_gaussian(N_last10_neg.ua, 5)
#%%
# calculate the first derivative along y-axis
N_first10_pos_y = mpcalc.first_derivative(N_first10_pos_sm, axis='lat')
N_first10_neg_y = mpcalc.first_derivative(N_first10_neg_sm, axis='lat')

N_last10_pos_y = mpcalc.first_derivative(N_last10_pos_sm, axis='lat')
N_last10_neg_y = mpcalc.first_derivative(N_last10_neg_sm, axis='lat')

# %%
def plot_conourf(N_y, ax, levels = np.arange(-0.5e-4, 0.51e-4, 0.1e-4)):
 
    p = N_y.plot.contourf(ax=ax, levels=levels, extend="both",
    transform=ccrs.PlateCarree(), cmap="RdBu_r", add_colorbar=False)

    ax.set_extent([-180, 180, 0, 90], ccrs.PlateCarree())
    ax.coastlines(color="grey", linewidth=0.5)
    return ax, p

# %%
# positive
fig, axes = plt.subplots(
    6, 2, figsize=(17, 17), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -10
interval_lag = 2


start_lag = start_lag
length_lag = 6
interval_lag = interval_lag
stop_lag = start_lag + length_lag * interval_lag
extreme_type = "pos"

lag_days = np.arange(start_lag, stop=stop_lag, step=interval_lag)
periods = ["first10", "last10"]

data = [N_first10_pos_y, N_last10_pos_y]

for i, period in enumerate(periods):
    for j, lag in enumerate(lag_days):
        _, p = plot_conourf(data[i].sel(time=lag), axes[j, i])
        axes[j, i].set_title(f"{period} {extreme_type} lag {lag}")

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of positive extremes")

plt.tight_layout(rect=[0, 0.1, 1, 1])
for ax in axes[-1, :]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

# add y-axis labels for the first column
for ax in axes[:, 0]:
    ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/E_vector/N_y_composite_positive.png"
)

# %%
fig, axes = plt.subplots(
    6, 2, figsize=(17, 17), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -10
interval_lag = 2


start_lag = start_lag
length_lag = 6
interval_lag = interval_lag
stop_lag = start_lag + length_lag * interval_lag
extreme_type = "pos"

lag_days = np.arange(start_lag, stop=stop_lag, step=interval_lag)
periods = ["first10", "last10"]

data = [N_first10_pos_sm, N_last10_pos_sm]

for i, period in enumerate(periods):
    for j, lag in enumerate(lag_days):
        _, p = plot_conourf(data[i].sel(time=lag), axes[j, i],levels = np.arange(-50, 51, 10))
        axes[j, i].set_title(f"{period} {extreme_type} lag {lag}")

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of positive extremes")

plt.tight_layout(rect=[0, 0.1, 1, 1])
for ax in axes[-1, :]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

# add y-axis labels for the first column
for ax in axes[:, 0]:
    ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/E_vector/N_composite_positive.png"
)

# %%
# negative
fig, axes = plt.subplots(
    6, 2, figsize=(17, 17), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)

start_lag = -10
interval_lag = 2

start_lag = start_lag
length_lag = 6

lag_days = np.arange(start_lag, stop=start_lag + 6)
periods = ["first10", "last10"]
extreme_type = "neg"

data = [N_first10_neg_y, N_last10_neg_y]

for i, period in enumerate(periods):
    for j, lag in enumerate(lag_days):
        _, p = plot_conourf(data[i].sel(time=lag), axes[j, i])
        axes[j, i].set_title(f"{period} {extreme_type} lag {lag}")

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of negative extremes")

plt.tight_layout(rect=[0, 0.1, 1, 1])

for ax in axes[-1, :]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

# add y-axis labels for the first column
for ax in axes[:, 0]:
    ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/E_vector/N_y_composite_negative.png"
)


# %%

# negative
fig, axes = plt.subplots(
    6, 2, figsize=(17, 17), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)

start_lag = -10
interval_lag = 2

start_lag = start_lag
length_lag = 6

lag_days = np.arange(start_lag, stop=start_lag + 6)
periods = ["first10", "last10"]
extreme_type = "neg"

data = [N_first10_neg_sm, N_last10_neg_sm]

for i, period in enumerate(periods):
    for j, lag in enumerate(lag_days):
        _, p = plot_conourf(data[i].sel(time=lag), axes[j, i],levels = np.arange(-50, 51, 10))
        axes[j, i].set_title(f"{period} {extreme_type} lag {lag}")

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of negative extremes")

plt.tight_layout(rect=[0, 0.1, 1, 1])

for ax in axes[-1, :]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

# add y-axis labels for the first column

for ax in axes[:, 0]:
    ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/E_vector/N_composite_negative.png"
)

# %%
