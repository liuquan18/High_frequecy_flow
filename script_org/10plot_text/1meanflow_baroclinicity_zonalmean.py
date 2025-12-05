# %%
import glob
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.path as mpath
import matplotlib.ticker as mticker
import matplotlib.ticker as ticker


from src.dynamics.EP_flux import PlotEPfluxArrows
from src.data_helper import read_composite
from src.plotting.util import erase_white_line, map_smooth, NA_box
import importlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
from src.data_helper.read_variable import read_climatology, read_climatology_decmean
from metpy.units import units
import numpy as np
import os
import cartopy
from matplotlib.patches import Rectangle
from shapely.geometry import Polygon
from matplotlib.ticker import FuncFormatter
import metpy.calc as mpcalc
import src.plotting.util as util

importlib.reload(read_composite)
importlib.reload(util)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var
clip_map = util.clip_map

####################################
# read transient simulation data
# %%
ua_pos_first = read_comp_var(
    "ua",
    "pos",
    1850,
    time_window=(-10, 5),
    method="mean",
    name="ua",
    model_dir="MPI_GE_CMIP6_allplev",
)
ua_neg_first = read_comp_var(
    "ua",
    "neg",
    1850,
    time_window=(-10, 5),
    method="mean",
    name="ua",
    model_dir="MPI_GE_CMIP6_allplev",
)
# %%
ua_pos_last = read_comp_var(
    "ua",
    "pos",
    2090,
    time_window=(-10, 5),
    method="mean",
    name="ua",
    model_dir="MPI_GE_CMIP6_allplev",
)
ua_neg_last = read_comp_var(
    "ua",
    "neg",
    2090,
    time_window=(-10, 5),
    method="mean",
    name="ua",
    model_dir="MPI_GE_CMIP6_allplev",
)
# %%
baroc_pos_first = read_comp_var(
    "eady_growth_rate",
    "pos",
    1850,
    time_window=(-10, 5),
    method="mean",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
baroc_neg_first = read_comp_var(
    "eady_growth_rate",
    "neg",
    1850,
    time_window=(-10, 5),
    method="mean",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
baroc_pos_last = read_comp_var(
    "eady_growth_rate",
    "pos",
    2090,
    time_window=(-10, 5),
    method="mean",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
baroc_neg_last = read_comp_var(
    "eady_growth_rate",
    "neg",
    2090,
    time_window=(-10, 5),
    method="mean",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
# %%
# baroclinicity from s-1 to day-1
baroc_pos_first = baroc_pos_first * 86400
baroc_neg_first = baroc_neg_first * 86400
baroc_pos_last = baroc_pos_last * 86400
baroc_neg_last = baroc_neg_last * 86400


# %%
# ua select 25000
ua_pos_first = ua_pos_first.sel(plev=25000)
ua_neg_first = ua_neg_first.sel(plev=25000)
ua_pos_last = ua_pos_last.sel(plev=25000)
ua_neg_last = ua_neg_last.sel(plev=25000)
# %%
# baroc select 85000
baroc_pos_first = baroc_pos_first.sel(plev=85000)
baroc_neg_first = baroc_neg_first.sel(plev=85000)
baroc_pos_last = baroc_pos_last.sel(plev=85000)
baroc_neg_last = baroc_neg_last.sel(plev=85000)

# %%
ua_diff_first = ua_pos_first - ua_neg_first
ua_diff_last = ua_pos_last - ua_neg_last
baroc_diff_first = baroc_pos_first - baroc_neg_first
baroc_diff_last = baroc_pos_last - baroc_neg_last
# %%
uhat_levels = np.arange(-30, 31, 5)
uhat_levels_div = np.arange(-15, 16, 3)  # for difference
baroc_levels = np.arange(-8, 8.1, 1)
baroc_levels_div = np.arange(-3, 3, 0.5)  # for difference

# %%
# change from lon 0-360 to -180 to 180
ua_pos_first = util.lon360to180(ua_pos_first)
ua_neg_first = util.lon360to180(ua_neg_first)
ua_pos_last = util.lon360to180(ua_pos_last)
ua_neg_last = util.lon360to180(ua_neg_last)
ua_diff_first = util.lon360to180(ua_diff_first)
ua_diff_last = util.lon360to180(ua_diff_last)

baroc_pos_first = util.lon360to180(baroc_pos_first)
baroc_neg_first = util.lon360to180(baroc_neg_first)
baroc_pos_last = util.lon360to180(baroc_pos_last)
baroc_neg_last = util.lon360to180(baroc_neg_last)
baroc_diff_first = util.lon360to180(baroc_diff_first)
baroc_diff_last = util.lon360to180(baroc_diff_last)
# %%
# zonal mean
ua_pos_first_zm = ua_pos_first.sel(lon=slice(-120, 60)).mean(dim="lon")
ua_neg_first_zm = ua_neg_first.sel(lon=slice(-120, 60)).mean(dim="lon")
ua_pos_last_zm = ua_pos_last.sel(lon=slice(-120, 60)).mean(dim="lon")
ua_neg_last_zm = ua_neg_last.sel(lon=slice(-120, 60)).mean(dim="lon")
ua_diff_first_zm = ua_diff_first.sel(lon=slice(-120, 60)).mean(dim="lon")
ua_diff_last_zm = ua_diff_last.sel(lon=slice(-120, 60)).mean(dim="lon")
# %%
baroc_pos_first_zm = baroc_pos_first.sel(lon=slice(-120, 0)).mean(dim="lon")
baroc_neg_first_zm = baroc_neg_first.sel(lon=slice(-120, 0)).mean(dim="lon")
baroc_pos_last_zm = baroc_pos_last.sel(lon=slice(-120, 0)).mean(dim="lon")
baroc_neg_last_zm = baroc_neg_last.sel(lon=slice(-120, 0)).mean(dim="lon")
baroc_diff_first_zm = baroc_diff_first.sel(lon=slice(-120, 0)).mean(dim="lon")
baroc_diff_last_zm = baroc_diff_last.sel(lon=slice(-120, 0)).mean(dim="lon")

# %%
# calculate the data and load the data for plotting
ua_pos_first_zm = ua_pos_first_zm.compute()
ua_neg_first_zm = ua_neg_first_zm.compute()
ua_pos_last_zm = ua_pos_last_zm.compute()
ua_neg_last_zm = ua_neg_last_zm.compute()
ua_diff_first_zm = ua_diff_first_zm.compute()
ua_diff_last_zm = ua_diff_last_zm.compute()
# %%
baroc_pos_first_zm = baroc_pos_first_zm.compute()
baroc_neg_first_zm = baroc_neg_first_zm.compute()
baroc_pos_last_zm = baroc_pos_last_zm.compute()
baroc_neg_last_zm = baroc_neg_last_zm.compute()
baroc_diff_first_zm = baroc_diff_first_zm.compute()
baroc_diff_last_zm = baroc_diff_last_zm.compute()
# %%
# only northern hemisphere
ua_pos_first_zm = ua_pos_first_zm.sel(lat=slice(0, 90))
ua_neg_first_zm = ua_neg_first_zm.sel(lat=slice(0, 90))
ua_pos_last_zm = ua_pos_last_zm.sel(lat=slice(0, 90))
ua_neg_last_zm = ua_neg_last_zm.sel(lat=slice(0, 90))
ua_diff_first_zm = ua_diff_first_zm.sel(lat=slice(0, 90))
ua_diff_last_zm = ua_diff_last_zm.sel(lat=slice(0, 90))

baroc_pos_first_zm = baroc_pos_first_zm.sel(lat=slice(0, 90))
baroc_neg_first_zm = baroc_neg_first_zm.sel(lat=slice(0, 90))
baroc_pos_last_zm = baroc_pos_last_zm.sel(lat=slice(0, 90))
baroc_neg_last_zm = baroc_neg_last_zm.sel(lat=slice(0, 90))
baroc_diff_first_zm = baroc_diff_first_zm.sel(lat=slice(0, 90))
baroc_diff_last_zm = baroc_diff_last_zm.sel(lat=slice(0, 90))

# %%
# read mean state
ua_first = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_monthly_ensmean/ua_monmean_ensmean_185005_185909.nc"
)
ua_last = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_monthly_ensmean/ua_monmean_ensmean_209005_209909.nc"
)
# %%
# change from lon 0-360 to -180 to 180
ua_first = util.lon360to180(ua_first.ua)
ua_last = util.lon360to180(ua_last.ua)
# %%
ua_first = ua_first.sel(plev=25000).sel(lon=slice(-120, 60)).mean(dim=("lon", "time"))
ua_last = ua_last.sel(plev=25000).sel(lon=slice(-120, 60)).mean(dim=("lon", "time"))
ua_first = ua_first.sel(lat=slice(0, 90)).compute()
ua_last = ua_last.sel(lat=slice(0, 90)).compute()

# %%
baroc_first = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/eady_growth_rate_monthly_ensmean/eady_growth_rate_monmean_ensmean_185005_185909.nc"
)
baroc_last = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/eady_growth_rate_monthly_ensmean/eady_growth_rate_monmean_ensmean_209005_209909.nc"
)

# lon
baroc_first = util.lon360to180(baroc_first.eady_growth_rate)
baroc_last = util.lon360to180(baroc_last.eady_growth_rate)


baroc_first = (
    baroc_first.sel(plev=85000).sel(lon=slice(-120, 0)).mean(dim=("lon", "time"))
)
baroc_last = (
    baroc_last.sel(plev=85000).sel(lon=slice(-120, 0)).mean(dim=("lon", "time"))
)
baroc_first = baroc_first.sel(lat=slice(0, 90)).compute()
baroc_last = baroc_last.sel(lat=slice(0, 90)).compute()


# %%
###########################
# read 4xco2 simulation data
def read_composite_vco2(simulaitons="vco2_4xco2_land", var="jet"):
    from_path = f"/work/mh0033/m300883/Tel_MMLE/data/{simulaitons}/composite_{var}/"

    pos_file = glob.glob(from_path + "*pos.nc")[0]
    neg_file = glob.glob(from_path + "*neg.nc")[0]

    pos_data = xr.open_dataset(pos_file)
    neg_data = xr.open_dataset(neg_file)

    if var in pos_data:
        pos_data = pos_data[var]
    elif "u" in pos_data:
        pos_data = pos_data["u"]
    else:
        pos_data = pos_data[list(pos_data.data_vars)[0]]

    if var in neg_data:
        neg_data = neg_data[var]
    elif "u" in neg_data:
        neg_data = neg_data["u"]
    else:
        neg_data = neg_data[list(neg_data.data_vars)[0]]

    return pos_data, neg_data


# %%


def read_mean_vco2(
    simulations, var="u", decade="1850", plev=25000, lons=slice(None, None)
):
    data_path = f"/scratch/m/m300883/{simulations}/{var}_monmean/"
    files = glob.glob(data_path + "*/*.nc")
    # sort files to ensure consistent order
    files.sort()
    jet_data = xr.open_mfdataset(files, combine="nested", concat_dim="ens")
    jet_data["time"] = pd.to_datetime(jet_data["time"].values, format="ISO8601")
    # change lon from 0-360 to -180-180
    if "lon" in jet_data.coords:
        jet_data = jet_data.assign_coords(
            lon=(((jet_data.lon + 180) % 360) - 180)
        ).sortby("lon")
    jet_data = jet_data.sel(plev=plev)
    jet_data = jet_data.sel(lon=lons).mean(dim="lon").sel(lat=slice(90, 0))
    jet_data = jet_data.mean(dim=("time", "ens"))

    # return dataarray than dataset
    jet_data = jet_data[var] if var in jet_data else jet_data[list(jet_data.data_vars)[0]]
    return jet_data


# %%
ua_pos_land, ua_neg_land = read_composite_vco2(simulaitons="vco2_4xco2_land", var="jet")
ua_pos_ocean, ua_neg_ocean = read_composite_vco2(
    simulaitons="vco2_4xco2_ocean", var="jet"
)
ua_pos_slab, ua_neg_slab = read_composite_vco2(
    simulaitons="vco2_4xco2_land_mlo", var="jet"
)
ua_pos_all, ua_neg_all = read_composite_vco2(simulaitons="vco2_4xco2_all", var="jet")

baroc_pos_land, baroc_neg_land = read_composite_vco2(
    simulaitons="vco2_4xco2_land", var="eady_growth_rate"
)
baroc_pos_ocean, baroc_neg_ocean = read_composite_vco2(
    simulaitons="vco2_4xco2_ocean", var="eady_growth_rate"
)
baroc_pos_slab, baroc_neg_slab = read_composite_vco2(
    simulaitons="vco2_4xco2_land_mlo", var="eady_growth_rate"
)
baroc_pos_all, baroc_neg_all = read_composite_vco2(
    simulaitons="vco2_4xco2_all", var="eady_growth_rate"
)
# %%
ua_land = read_mean_vco2(simulations="vco2_4xco2_land", var="u", decade="1850")
ua_ocean = read_mean_vco2(simulations="vco2_4xco2_ocean", var="u", decade="1850")
ua_all = read_mean_vco2(simulations="vco2_4xco2_all", var="u", decade="1850")
ua_slab = read_mean_vco2(simulations="vco2_4xco2_land_mlo", var="u", decade="1900")

#%%
baroc_land = read_mean_vco2(
    simulations="vco2_4xco2_land",
    var="eady_growth_rate",
    decade="1850",
    plev=85000,
)
baroc_ocean = read_mean_vco2(
    simulations="vco2_4xco2_ocean",
    var="eady_growth_rate",
    decade="1850",
    plev=85000,
)
baroc_all = read_mean_vco2(
    simulations="vco2_4xco2_all",
    var="eady_growth_rate",
    decade="1850",
    plev=85000,
)

baroc_slab = read_mean_vco2(
    simulations="vco2_4xco2_land_mlo",
    var="eady_growth_rate",
    decade="1900",
    plev=85000,
)
#%%
# load the mean data
ua_land = ua_land.compute()
ua_ocean = ua_ocean.compute()
ua_all = ua_all.compute()
ua_slab = ua_slab.compute()

baroc_land = baroc_land.compute()
baroc_ocean = baroc_ocean.compute()
baroc_all = baroc_all.compute()
baroc_slab = baroc_slab.compute()

# %%
# New plot: 2x2 layout for jet stream (UA) analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12), sharey=True)

# Define bar width for all subplots
bar_width = 2  # degrees latitude

# axes[0, 0]: Composite difference (Pos - Neg) for first and last periods
lat = ua_diff_first_zm.lat.values

# Plot difference lines
ua_diff_first = ua_diff_first_zm.values
ua_diff_last = ua_diff_last_zm.values
axes[0, 0].plot(ua_diff_first, lat, "k-", label="1850", linewidth=2)
axes[0, 0].plot(ua_diff_last, lat, "k--", label="2090", linewidth=2)
axes[0, 0].axvline(0, color="black", linestyle=":", alpha=0.5)
axes[0, 0].set_xlabel("UA (Pos - Neg) [m/s]", fontsize=12)
axes[0, 0].set_ylabel("Latitude [°]", fontsize=12)
axes[0, 0].set_title("Composite: First vs Last Period", fontsize=14, fontweight="bold")
axes[0, 0].legend(loc="upper left")

# Secondary x-axis: plot change as bars
ax_bar = axes[0, 0].twiny()
ua_change = ua_diff_last_zm - ua_diff_first_zm

# Scale the data by 2 so that when displayed, it appears at half value
ax_bar.barh(
    lat, ua_change * 2, height=bar_width, alpha=0.3, color="red", label="2090 - 1850"
)

# Now align the axes - they should have the same limits
xlim1 = axes[0, 0].get_xlim()
ax_bar.set_xlim(xlim1)


# Format tick labels to show half the actual value
def half_formatter(x, pos):
    return f"{x/2:.1f}"


ax_bar.xaxis.set_major_formatter(FuncFormatter(half_formatter))

ax_bar.axvline(0, color="red", linestyle=":", alpha=0.5)
ax_bar.set_xlabel("Change (2090 - 1850) [m/s]", fontsize=12, color="red")
ax_bar.tick_params(axis="x", labelcolor="red")
ax_bar.legend(loc="upper right")


# axes[0, 1]: Mean state difference (Last - First)
lat = ua_last.lat.values

# Plot mean state line
axes[0, 1].plot(ua_first, lat, "k-", label="1850 Mean", linewidth=2)
axes[0, 1].plot(ua_last, lat, "k--", label="2090 Mean", linewidth=2)
axes[0, 1].axvline(0, color="black", linestyle=":", alpha=0.5)
axes[0, 1].set_xlabel("UA [m/s]", fontsize=12)
axes[0, 1].set_title("Mean State Change", fontsize=14, fontweight="bold")
axes[0, 1].legend(loc="upper left")

# Secondary x-axis: plot difference as bars
ax_bar = axes[0, 1].twiny()
ua_mean_diff = (ua_last - ua_first).values
ax_bar.barh(
    lat, ua_mean_diff, height=bar_width, alpha=0.3, color="gray", label="2090 - 1850"
)
ax_bar.axvline(0, color="gray", linestyle=":", alpha=0.5)
ax_bar.set_xlabel("UA Change [m/s]", fontsize=12, color="gray")
ax_bar.tick_params(axis="x", labelcolor="gray")
ax_bar.legend(loc="upper right")

# axes[1, 0]: Composite difference for simulations
lat = ua_pos_all.lat.values

# Plot "all" experiment
ua_all_diff = (ua_pos_all - ua_neg_all).squeeze()
axes[1, 0].plot(
    ua_all_diff, lat, color="black", linestyle="--", linewidth=2, label="All"
)
axes[1, 0].axvline(0, color="black", linestyle=":", alpha=0.5)
axes[1, 0].set_xlabel("UA (Pos - Neg) [m/s] (All)", fontsize=12)
axes[1, 0].set_ylabel("Latitude [°]", fontsize=12)
axes[1, 0].set_title("Composite: Different Experiments", fontsize=14, fontweight="bold")
axes[1, 0].legend(loc="upper left")
# Secondary x-axis: plot differences as bars
ax_bar = axes[1, 0].twiny()

# Calculate differences
ua_ocean_diff = (ua_pos_ocean - ua_neg_ocean).squeeze() - ua_all_diff
ua_slab_diff = (ua_pos_slab - ua_neg_slab).squeeze() - ua_all_diff

# Plot horizontal bars - scale by 2 so displayed values are half
ax_bar.barh(
    lat, ua_ocean_diff * 2, height=bar_width, color="C0", alpha=0.3, label="Ocean - All"
)
ax_bar.barh(
    lat, ua_slab_diff * 2, height=bar_width, color="red", alpha=0.3, label="Slab - All"
)

# Align the axes - they should have the same limits
xlim1 = axes[1, 0].get_xlim()
ax_bar.set_xlim(xlim1)


# Format tick labels to show half the actual value
def half_formatter(x, pos):
    return f"{x/2:.1f}"


ax_bar.xaxis.set_major_formatter(FuncFormatter(half_formatter))

ax_bar.axvline(0, color="C0", linestyle=":", alpha=0.5)
ax_bar.set_xlabel("Difference from All [m/s]", fontsize=12, color="C0")
ax_bar.tick_params(axis="x", labelcolor="C0")
ax_bar.legend(loc="upper right")

# axes[1, 1]: Mean state difference (Land - All)
lat = ua_land.lat.values


# Calculate differences
diff_ocean_all = ua_ocean - ua_all
diff_slab_all = ua_slab - ua_all

# Calculate bar height based on latitude spacing
bar_height = np.abs(np.diff(lat).mean())

# Plot differences as horizontal bar plots
# ax.barh(
#     lat, diff_land_all, color="gray", alpha=0.7, label="Land - All", height=bar_height
# )
axes[1, 1].barh(
    lat,
    diff_ocean_all,
    color="C0",
    alpha=0.3,
    label="Ocean - All",
    height=bar_height,
    edgecolor="C0",
    linewidth=0.5,
)
axes[1, 1].barh(
    lat,
    diff_slab_all,
    color="red",
    alpha=0.3,
    label="Slab - All",
    height=bar_height,
    edgecolor="red",
    linewidth=0.5,
)

# Add zero line for reference
axes[1, 1].axvline(0, color="black", linestyle="--")

# Add labels and formatting
axes[1, 1].set_xlabel("UA Difference [m/s]", fontsize=12)
axes[1, 1].set_title("Mean State: Experiment Differences", fontsize=14, fontweight="bold")
axes[1, 1].legend(loc="upper right")

# Set common y-axis properties
for ax in axes.flat:
    ax.set_ylim([0, 90])
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# %%
# New plot: 2x2 layout for baroclinicity analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12), sharey=True)

# Define bar width for all subplots
bar_width = 2  # degrees latitude

# axes[0, 0]: Composite difference (Pos - Neg) for first and last periods
lat = baroc_diff_first_zm.lat.values

# Plot difference lines
baroc_diff_first = baroc_diff_first_zm.values
baroc_diff_last = baroc_diff_last_zm.values
axes[0, 0].plot(baroc_diff_first, lat, "k-", label="1850", linewidth=2)
axes[0, 0].plot(baroc_diff_last, lat, "k--", label="2090", linewidth=2)
axes[0, 0].axvline(0, color="black", linestyle=":", alpha=0.5)
axes[0, 0].set_xlabel("Baroclinicity (Pos - Neg) [day⁻¹]", fontsize=12)
axes[0, 0].set_ylabel("Latitude [°]", fontsize=12)
axes[0, 0].set_title("Composite: First vs Last Period", fontsize=14, fontweight="bold")
axes[0, 0].legend(loc="upper left")

# Secondary x-axis: plot change as bars
ax_bar = axes[0, 0].twiny()
baroc_change = baroc_diff_last_zm - baroc_diff_first_zm

# Scale the data by 2 so that when displayed, it appears at half value
ax_bar.barh(
    lat, baroc_change * 2, height=bar_width, alpha=0.3, color="red", label="2090 - 1850"
)

# Now align the axes - they should have the same limits
xlim1 = axes[0, 0].get_xlim()
ax_bar.set_xlim(xlim1)


# Format tick labels to show half the actual value
def half_formatter(x, pos):
    return f"{x/2:.2f}"


ax_bar.xaxis.set_major_formatter(FuncFormatter(half_formatter))

ax_bar.axvline(0, color="red", linestyle=":", alpha=0.5)
ax_bar.set_xlabel("Change (2090 - 1850) [day⁻¹]", fontsize=12, color="red")
ax_bar.tick_params(axis="x", labelcolor="red")
ax_bar.legend(loc="upper right")


# axes[0, 1]: Mean state difference (Last - First)
lat = baroc_last.lat.values

# Plot mean state line
axes[0, 1].plot(baroc_first, lat, "k-", label="1850 Mean", linewidth=2)
axes[0, 1].plot(baroc_last, lat, "k--", label="2090 Mean", linewidth=2)
axes[0, 1].axvline(0, color="black", linestyle=":", alpha=0.5)
axes[0, 1].set_xlabel("Baroclinicity [day⁻¹]", fontsize=12)
axes[0, 1].set_title("Mean State Change", fontsize=14, fontweight="bold")
axes[0, 1].legend(loc="upper left")

# Secondary x-axis: plot difference as bars
ax_bar = axes[0, 1].twiny()
baroc_mean_diff = (baroc_last - baroc_first).values
ax_bar.barh(
    lat, baroc_mean_diff, height=bar_width, alpha=0.3, color="gray", label="2090 - 1850"
)

ax_bar.axvline(0, color="gray", linestyle=":", alpha=0.5)
ax_bar.set_xlabel("Baroclinicity Change [day⁻¹]", fontsize=12, color="gray")
ax_bar.tick_params(axis="x", labelcolor="gray")
ax_bar.legend(loc="upper right")

# axes[1, 0]: Composite difference for simulations
lat = baroc_pos_all.lat.values

# Plot "all" experiment
baroc_all_diff = (baroc_pos_all - baroc_neg_all).squeeze()
axes[1, 0].plot(
    baroc_all_diff, lat, color="black", linestyle="--", linewidth=2, label="All"
)
axes[1, 0].axvline(0, color="black", linestyle=":", alpha=0.5)
axes[1, 0].set_xlabel("Baroclinicity (Pos - Neg) [day⁻¹] (All)", fontsize=12)
axes[1, 0].set_ylabel("Latitude [°]", fontsize=12)
axes[1, 0].set_title("Composite: Different Experiments", fontsize=14, fontweight="bold")
axes[1, 0].legend(loc="upper left")

# Secondary x-axis: plot differences as bars
ax_bar = axes[1, 0].twiny()

# Calculate differences
baroc_ocean_diff = (baroc_pos_ocean - baroc_neg_ocean).squeeze() - baroc_all_diff
baroc_slab_diff = (baroc_pos_slab - baroc_neg_slab).squeeze() - baroc_all_diff

# Plot horizontal bars - scale by 2 so displayed values are half
ax_bar.barh(
    lat, baroc_ocean_diff * 2, height=bar_width, color="C0", alpha=0.3, label="Ocean - All"
)
ax_bar.barh(
    lat, baroc_slab_diff * 2, height=bar_width, color="red", alpha=0.3, label="Slab - All"
)

# Align the axes - they should have the same limits
xlim1 = axes[1, 0].get_xlim()
ax_bar.set_xlim(xlim1)


# Format tick labels to show half the actual value
def half_formatter(x, pos):
    return f"{x/2:.2f}"


ax_bar.xaxis.set_major_formatter(FuncFormatter(half_formatter))

ax_bar.axvline(0, color="C0", linestyle=":", alpha=0.5)
ax_bar.set_xlabel("Difference from All [day⁻¹]", fontsize=12, color="C0")
ax_bar.tick_params(axis="x", labelcolor="C0")
ax_bar.legend(loc="upper right")

# axes[1, 1]: Mean state difference (Ocean/Slab - All)
lat = baroc_land.lat.values

# Calculate differences
diff_ocean_all = baroc_ocean - baroc_all
diff_slab_all = baroc_slab - baroc_all

# Calculate bar height based on latitude spacing
bar_height = np.abs(np.diff(lat).mean())

# Plot differences as horizontal bar plots
axes[1, 1].barh(
    lat,
    diff_ocean_all,
    color="C0",
    alpha=0.3,
    label="Ocean - All",
    height=bar_height,
    edgecolor="C0",
    linewidth=0.5,
)
axes[1, 1].barh(
    lat,
    diff_slab_all,
    color="red",
    alpha=0.3,
    label="Slab - All",
    height=bar_height,
    edgecolor="red",
    linewidth=0.5,
)

# Add zero line for reference
axes[1, 1].axvline(0, color="black", linestyle="--")

# Add labels and formatting
axes[1, 1].set_xlabel("Baroclinicity Difference [day⁻¹]", fontsize=12)
axes[1, 1].set_title("Mean State: Experiment Differences", fontsize=14, fontweight="bold")
axes[1, 1].legend(loc="upper right")

# Set common y-axis properties
for ax in axes.flat:
    ax.set_ylim([0, 90])
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# %%
