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
awb_pos_first = read_comp_var(
    "wb_anticyclonic",
    "pos",
    1850,
    time_window=(-10, 5),
    method="no_stat",
    name="flag",
    model_dir="MPI_GE_CMIP6_allplev",
)

awb_neg_first = read_comp_var(
    "wb_anticyclonic",
    "neg",
    1850,
    time_window=(-10, 5),
    method="no_stat",
    name="flag",
    model_dir="MPI_GE_CMIP6_allplev",
)
awb_pos_last = read_comp_var(
    "wb_anticyclonic",
    "pos",
    2090,
    time_window=(-10, 5),
    method="no_stat",
    name="flag",
    model_dir="MPI_GE_CMIP6_allplev",
)
awb_neg_last = read_comp_var(
    "wb_anticyclonic",
    "neg",
    2090,
    time_window=(-10, 5),
    method="no_stat",
    name="flag",
    model_dir="MPI_GE_CMIP6_allplev",
)

# %%
cwb_pos_first = read_comp_var(
    "wb_cyclonic",
    "pos",
    1850,
    time_window=(-10, 5),
    method="no_stat",
    name="flag",
    model_dir="MPI_GE_CMIP6_allplev",
)
cwb_neg_first = read_comp_var(
    "wb_cyclonic",
    "neg",
    1850,
    time_window=(-10, 5),
    method="no_stat",
    name="flag",
    model_dir="MPI_GE_CMIP6_allplev",
)
cwb_pos_last = read_comp_var(
    "wb_cyclonic",
    "pos",
    2090,
    time_window=(-10, 5),
    method="no_stat",
    name="flag",
    model_dir="MPI_GE_CMIP6_allplev",
)
cwb_neg_last = read_comp_var(
    "wb_cyclonic",
    "neg",
    2090,
    time_window=(-10, 5),
    method="no_stat",
    name="flag",
    model_dir="MPI_GE_CMIP6_allplev",
)


# %%
# change from lon 0-360 to -180 to 180
awb_pos_first = util.lon360to180(awb_pos_first)
awb_neg_first = util.lon360to180(awb_neg_first)
awb_pos_last = util.lon360to180(awb_pos_last)
awb_neg_last = util.lon360to180(awb_neg_last)

cwb_pos_first = util.lon360to180(cwb_pos_first)
cwb_neg_first = util.lon360to180(cwb_neg_first)
cwb_pos_last = util.lon360to180(cwb_pos_last)
cwb_neg_last = util.lon360to180(cwb_neg_last)

# %%
lon_range = (-120, 60)
# zonal mean
awb_pos_first_zm = (
    awb_pos_first.sel(time=slice(-10, 5))
    .sel(lon=slice(lon_range[0], lon_range[1]))
    .mean(dim = 'lon')
    .sum(dim=("time", "event"))
)
awb_neg_first_zm = (
    awb_neg_first.sel(time=slice(-10, 5))
    .sel(lon=slice(lon_range[0], lon_range[1]))
    .mean(dim = 'lon')
    .sum(dim=("time", "event"))
)
awb_pos_last_zm = (
    awb_pos_last.sel(time=slice(-10, 5))
    .sel(lon=slice(lon_range[0], lon_range[1]))
    .mean(dim="lon")
    .sum(dim=("time", "event")) # sum over time and event
)
awb_neg_last_zm = (
    awb_neg_last.sel(time=slice(-10, 5))
    .sel(lon=slice(lon_range[0], lon_range[1]))
    .mean(dim="lon")
    .sum(dim=("time", "event"))
)

cwb_pos_first_zm = (
    cwb_pos_first.sel(time=slice(-10, 5))
    .sel(lon=slice(lon_range[0], lon_range[1]))
    .mean(dim="lon")
    .sum(dim=("time", "event"))
)
cwb_neg_first_zm = (
    cwb_neg_first.sel(time=slice(-10, 5))
    .sel(lon=slice(lon_range[0], lon_range[1]))
    .mean(dim="lon")
    .sum(dim=("time", "event"))
)
cwb_pos_last_zm = (
    cwb_pos_last.sel(time=slice(-10, 5))
    .sel(lon=slice(lon_range[0], lon_range[1]))
    .mean(dim="lon")
    .sum(dim=("time", "event"))
)
cwb_neg_last_zm = (
    cwb_neg_last.sel(time=slice(-10, 5))
    .sel(lon=slice(lon_range[0], lon_range[1]))
    .mean(dim="lon")
    .sum(dim=("time", "event"))
)

# %%
# calculate the data and load the data for plotting
awb_pos_first_zm = awb_pos_first_zm.compute()
awb_neg_first_zm = awb_neg_first_zm.compute()
awb_pos_last_zm = awb_pos_last_zm.compute()
awb_neg_last_zm = awb_neg_last_zm.compute()

cwb_pos_first_zm = cwb_pos_first_zm.compute()
cwb_neg_first_zm = cwb_neg_first_zm.compute()
cwb_pos_last_zm = cwb_pos_last_zm.compute()
cwb_neg_last_zm = cwb_neg_last_zm.compute()

# %%
# only northern hemisphere
awb_pos_first_zm = awb_pos_first_zm.sel(lat=slice(0, 90))
awb_neg_first_zm = awb_neg_first_zm.sel(lat=slice(0, 90))
awb_pos_last_zm = awb_pos_last_zm.sel(lat=slice(0, 90))
awb_neg_last_zm = awb_neg_last_zm.sel(lat=slice(0, 90))

cwb_pos_first_zm = cwb_pos_first_zm.sel(lat=slice(0, 90))
cwb_neg_first_zm = cwb_neg_first_zm.sel(lat=slice(0, 90))
cwb_pos_last_zm = cwb_pos_last_zm.sel(lat=slice(0, 90))
cwb_neg_last_zm = cwb_neg_last_zm.sel(lat=slice(0, 90))

# %%
# calculate differences
awb_diff_first_zm = awb_pos_first_zm - awb_neg_first_zm
awb_diff_last_zm = awb_pos_last_zm - awb_neg_last_zm

cwb_diff_first_zm = cwb_pos_first_zm - cwb_neg_first_zm
cwb_diff_last_zm = cwb_pos_last_zm - cwb_neg_last_zm


# %%
# New plot: 1x2 layout for AWB and CWB analysis
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

# Define bar width for all subplots
bar_width = 2  # degrees latitude

# axes[0]: AWB Composite difference (Pos - Neg) for first and last periods
lat = awb_diff_first_zm.lat.values

# Plot difference lines
awb_diff_first = awb_diff_first_zm.values
awb_diff_last = awb_diff_last_zm.values
(line1,) = axes[0].plot(awb_diff_first, lat, "k-", label="1850s", linewidth=2)
(line2,) = axes[0].plot(awb_diff_last, lat, "k--", label="2090s", linewidth=2)
axes[0].axvline(0, color="black", linestyle=":", alpha=0.5)
axes[0].set_xlabel("AWB frequency", fontsize=12)
axes[0].set_ylabel("Latitude [°]", fontsize=12)
axes[0].set_title("Anticyclonic Wave Breaking")

# Secondary x-axis: plot change as bars
ax_bar = axes[0].twiny()
awb_change = awb_diff_last_zm - awb_diff_first_zm

# Scale the data by 2 so that when displayed, it appears at half value
bar1 = ax_bar.barh(
    lat, awb_change * 2, height=bar_width, alpha=0.3, color="red", label="2090s - 1850s"
)

# Now align the axes - they should have the same limits
axes[0].set_xlim(-25, 25)
xlim1 = axes[0].get_xlim()
ax_bar.set_xlim(xlim1)


# Format tick labels to show half the actual value
def half_formatter_awb(x, pos):
    return f"{x/2:.2f}"


ax_bar.xaxis.set_major_formatter(FuncFormatter(half_formatter_awb))

ax_bar.axvline(0, color="red", linestyle=":", alpha=0.5)
ax_bar.set_xlabel(r"$\Delta$ AWB frequency", fontsize=12, color="red")
ax_bar.tick_params(axis="x", labelcolor="red")

# Combined legend
axes[0].legend(
    [line1, line2, bar1], ["1850s", "2090s", "2090s - 1850s"], loc="lower right"
)

# axes[1]: CWB Composite difference (Pos - Neg) for first and last periods
lat = cwb_diff_first_zm.lat.values

# Plot difference lines
cwb_diff_first = cwb_diff_first_zm.values
cwb_diff_last = cwb_diff_last_zm.values
(line1,) = axes[1].plot(cwb_diff_first, lat, "k-", label="1850s", linewidth=2)
(line2,) = axes[1].plot(cwb_diff_last, lat, "k--", label="2090s", linewidth=2)
axes[1].axvline(0, color="black", linestyle=":", alpha=0.5)
axes[1].set_xlabel("CWB frequency", fontsize=12)
axes[1].set_title("Cyclonic Wave Breaking")

# Secondary x-axis: plot change as bars
ax_bar = axes[1].twiny()
cwb_change = cwb_diff_last_zm - cwb_diff_first_zm

# Scale the data by 2 so that when displayed, it appears at half value
bar1 = ax_bar.barh(
    lat,
    cwb_change * 2,
    height=bar_width,
    alpha=0.3,
    color="red",
    label="2090s - 1850s",
)

# Now align the axes - they should have the same limits
axes[1].set_xlim(-10, 10)
xlim1 = axes[1].get_xlim()
ax_bar.set_xlim(xlim1)


# Format tick labels to show half the actual value
def half_formatter_cwb(x, pos):
    return f"{x/2:.2f}"


ax_bar.xaxis.set_major_formatter(FuncFormatter(half_formatter_cwb))

ax_bar.axvline(0, color="red", linestyle=":", alpha=0.5)
ax_bar.set_xlabel(r"$\Delta$ CWB frequency", fontsize=12, color="red")
ax_bar.tick_params(axis="x", labelcolor="red")

# Combined legend
axes[1].legend(
    [line1, line2, bar1], ["1850s", "2090s", "2090s - 1850s"], loc="lower right"
)

plt.tight_layout()
# %%
