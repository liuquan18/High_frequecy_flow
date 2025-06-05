# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line, map_smooth
from src.plotting.util import lon2x
from matplotlib.ticker import ScalarFormatter
import src.data_helper.read_variable as read_variable


import matplotlib.colors as mcolors
import cartopy
import glob
import matplotlib.ticker as mticker

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# %%
import src.plotting.util as util

import importlib

importlib.reload(read_variable)
importlib.reload(util)
# %%
from src.data_helper.read_variable import read_climatology_uhat
from src.data_helper.read_composite import read_comp_var
from matplotlib.patches import Rectangle


# %%%
# config
time_window = (-10, 5)
suffix = "_ano"
remove_zonmean = False

# %%
vpetp_levels_div = np.arange(-4.5, 4.6, 1.5)

scale_hus = 5e4

# %%
###### read vpetp
# climatology
vpetp_clim_first = read_climatology_uhat("vpetp", "1850", name="vpetp")
vpetp_clim_last = read_climatology_uhat("vpetp", "2090", name="vpetp")
# pos ano
vpetp_pos_first = read_comp_var(
    "vpetp",
    "pos",
    1850,
    time_window=time_window,
    name="vpetp",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
)
vpetp_neg_first = read_comp_var(
    "vpetp",
    "neg",
    1850,
    time_window=time_window,
    name="vpetp",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
)

vpetp_pos_last = read_comp_var(
    "vpetp",
    "pos",
    2090,
    time_window=time_window,
    name="vpetp",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
)
vpetp_neg_last = read_comp_var(
    "vpetp",
    "neg",
    2090,
    time_window=time_window,
    name="vpetp",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
)

# diff
vpetp_diff_first = vpetp_pos_first - vpetp_neg_first
vpetp_diff_last = vpetp_pos_last - vpetp_neg_last

# %%
vsets_clim_first = read_climatology_uhat("vsets", "1850", name="vsets")
vsets_clim_last = read_climatology_uhat("vsets", "2090", name="vsets")

# pos ano
vsets_pos_first = read_comp_var(
    "vsets",
    "pos",
    1850,
    time_window=time_window,
    name="vsets",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
)
vsets_neg_first = read_comp_var(
    "vsets",
    "neg",
    1850,
    time_window=time_window,
    name="vsets",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
)

vsets_pos_last = read_comp_var(
    "vsets",
    "pos",
    2090,
    time_window=time_window,
    name="vsets",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
)
vsets_neg_last = read_comp_var(
    "vsets",
    "neg",
    2090,
    time_window=time_window,
    name="vsets",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
)

# map smoothing
vpetp_pos_first = map_smooth(vpetp_pos_first, 3, 3)
vpetp_neg_first = map_smooth(vpetp_neg_first, 3, 3)
vpetp_pos_last = map_smooth(vpetp_pos_last, 3, 3)
vpetp_neg_last = map_smooth(vpetp_neg_last, 3, 3)


vsets_pos_first = map_smooth(vsets_pos_first, 5, 5)
vsets_neg_first = map_smooth(vsets_neg_first, 5, 5)
vsets_pos_last = map_smooth(vsets_pos_last, 5, 5)
vsets_neg_last = map_smooth(vsets_neg_last, 5, 5)
# diff
vsets_diff_first = vsets_pos_first - vsets_neg_first
vsets_diff_last = vsets_pos_last - vsets_neg_last
# %%
# for the first 10 years
fig, axes = plt.subplots(
    2,
    2,
    figsize=(10, 9),
    subplot_kw={"projection": ccrs.Orthographic(-30, 70)},
    sharex=True,
    sharey=False,
)

vpetp_pos_ax = axes[0, 0]
vpetp_neg_ax = axes[0, 1]

vsets_pos_ax = axes[1, 0]
vsets_neg_ax = axes[1, 1]

# plot vpetp pos
vpetp_pos_first.sel(plev=85000).plot.contourf(
    x="lon",
    y="lat",
    ax=vpetp_pos_ax,
    levels=vpetp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# plot vpetp neg
vpetp_neg_first.sel(plev=85000).plot.contourf(
    x="lon",
    y="lat",
    ax=vpetp_neg_ax,
    levels=vpetp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# plot vsets pos
vsets_pos_first.sel(plev=85000).plot.contourf(
    x="lon",
    y="lat",
    ax=vsets_pos_ax,
    levels=vpetp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# plot vsets neg
map = vsets_neg_first.sel(plev=85000).plot.contourf(
    x="lon",
    y="lat",
    ax=vsets_neg_ax,
    levels=vpetp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# Use levels without zero and black contour lines
levels_no_zero = [lvl for lvl in vpetp_levels_div if lvl != 0]

# plot vpetp pos (last 10 years) as contour lines
vpetp_pos_last.sel(plev=85000).plot.contour(
    x="lon",
    y="lat",
    ax=vpetp_pos_ax,
    levels=levels_no_zero,
    colors="k",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
    linewidths=1,
)

# plot vpetp neg (last 10 years)
vpetp_neg_last.sel(plev=85000).plot.contour(
    x="lon",
    y="lat",
    ax=vpetp_neg_ax,
    levels=levels_no_zero,
    colors="k",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
    linewidths=1,
)

# plot vsets pos (last 10 years)
vsets_pos_last.sel(plev=85000).plot.contour(
    x="lon",
    y="lat",
    ax=vsets_pos_ax,
    levels=levels_no_zero,
    colors="k",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
    linewidths=1,
)

# plot vsets neg (last 10 years)
line = vsets_neg_last.sel(plev=85000).plot.contour(
    x="lon",
    y="lat",
    ax=vsets_neg_ax,
    levels=levels_no_zero,
    colors="k",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
    linewidths=1,
)

# add coastlines and gridlines
for ax in axes[0, :].flatten():
    ax.coastlines(color="grey", linewidth=1)
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="dotted",
    )
    ax.xlocator = None
    ax.ylocator = None

for ax in axes[-1, :]:
    ax.coastlines(color="grey", linewidth=1)
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="dotted",
    )
    ax.xlocator = None
    ax.ylocator = None

for ax in axes.flatten():
    ax.set_global()
    ax.set_title("")

# add colorbar
cax = fig.add_axes([0.98, 0.25, 0.02, 0.5])
fig.colorbar(
    map,
    cax=cax,
    orientation="vertical",
    label=r"$\overline{v'\theta'}$ [K m s$^{-1}$]",
    extend="both",
)


# Define the region in degrees east (lon: 300 to 360, lat: 40 to 80)
lon_min, lon_max = 300, 360
lat_min, lat_max = 40, 80

# Create a smooth rectangle region using lines with many points
num_points = 60
# Bottom edge
lons_bottom = np.linspace(lon_min, lon_max, num_points)
lats_bottom = np.full_like(lons_bottom, lat_min)
# Right edge
lats_right = np.linspace(lat_min, lat_max, num_points)
lons_right = np.full_like(lats_right, lon_max)
# Top edge
lons_top = np.linspace(lon_max, lon_min, num_points)
lats_top = np.full_like(lons_top, lat_max)
# Left edge
lats_left = np.linspace(lat_max, lat_min, num_points)
lons_left = np.full_like(lats_left, lon_min)

# Concatenate to form the closed loop
lons = np.concatenate([lons_bottom, lons_right, lons_top, lons_left, [lon_min]])
lats = np.concatenate([lats_bottom, lats_right, lats_top, lats_left, [lat_min]])

axes[1, 1].plot(
    lons,
    lats,
    color="yellow",
    linestyle="dashed",
    linewidth=2,
    transform=ccrs.PlateCarree(),
    zorder=10,
)


# add a, b, c,d
for i, ax in enumerate(axes.flatten()):
    ax.text(
        0.05,
        0.95,
        f"{chr(97 + i)}",
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        va="top",
        ha="left",
    )

plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eddy_heat_pos_neg.pdf",
    dpi=300,
    bbox_inches="tight",
)


# %%
