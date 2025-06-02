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
from src.data_helper.read_variable import read_climatology
from src.data_helper.read_composite import read_comp_var



# %%
def to_plot_data(eke):
    # fake data to plot
    eke = eke.rename({"plev": "lat"})  # fake lat to plot correctly the lon
    eke["lat"] = -1 * (eke["lat"] / 1000 - 10)  # fake lat to plot correctly the lon
    # Solve the problem on 180 longitude by extending the data
    return eke


#%%%
# config
time_window = (-10, 5)
suffix = "_ano"
remove_zonmean = False

# %%
uhat_levels_div = np.arange(-12, 13, 2)
upvp_levels_div = np.arange(-20, 21, 5)
vsts_levels_div = np.arange(-3, 3.1, 0.5)
vptp_levels_div = np.arange(-1.2, 1.3, 0.2)
vptp_levels_low_div = np.arange(-4, 4.1, 1)
scale_hus = 5e4

# %%
###### read upvp
# climatology
upvp_clim_first = read_climatology("upvp", "1850", name="upvp")
upvp_clim_last = read_climatology("upvp", "2090", name="upvp")
# pos ano
upvp_pos_first = read_comp_var(
    "upvp", "pos", 1850, time_window=time_window, name="upvp", suffix=suffix, remove_zonmean=remove_zonmean
)
upvp_neg_first = read_comp_var(
    "upvp", "neg", 1850, time_window=time_window, name="upvp", suffix=suffix, remove_zonmean=remove_zonmean
)

upvp_pos_last = read_comp_var(
    "upvp", "pos", 2090, time_window=time_window, name="upvp", suffix=suffix, remove_zonmean=remove_zonmean
)
upvp_neg_last = read_comp_var(
    "upvp", "neg", 2090, time_window=time_window, name="upvp", suffix=suffix, remove_zonmean=remove_zonmean
)

# diff
upvp_diff_first = upvp_pos_first - upvp_neg_first
upvp_diff_last = upvp_pos_last - upvp_neg_last

# %%
usvs_clim_first = read_climatology("usvs", "1850", name="usvs")
usvs_clim_last = read_climatology("usvs", "2090", name="usvs")

# pos ano   
usvs_pos_first = read_comp_var(
    "usvs", "pos", 1850, time_window=time_window, name="usvs", suffix=suffix, remove_zonmean=remove_zonmean
)
usvs_neg_first = read_comp_var(
    "usvs", "neg", 1850, time_window=time_window, name="usvs", suffix=suffix, remove_zonmean=remove_zonmean
)

usvs_pos_last = read_comp_var(
    "usvs", "pos", 2090, time_window=time_window, name="usvs", suffix=suffix, remove_zonmean=remove_zonmean
)
usvs_neg_last = read_comp_var(
    "usvs", "neg", 2090, time_window=time_window, name="usvs", suffix=suffix, remove_zonmean=remove_zonmean
)

# map smoothing
usvs_pos_first = map_smooth(usvs_pos_first, 11, 5)
usvs_neg_first = map_smooth(usvs_neg_first, 11, 5)
usvs_pos_last = map_smooth(usvs_pos_last, 11, 5)
usvs_neg_last = map_smooth(usvs_neg_last, 11, 5)
# diff
usvs_diff_first = usvs_pos_first - usvs_neg_first
usvs_diff_last = usvs_pos_last - usvs_neg_last
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

upvp_pos_ax = axes[0, 0]
upvp_neg_ax = axes[0, 1]

usvs_pos_ax = axes[1, 0]
usvs_neg_ax = axes[1, 1]

# plot upvp pos
upvp_pos_first.sel(plev = 25000).plot.contourf(
    x="lon",
    y="lat",
    ax=upvp_pos_ax,
    levels=upvp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend =  "both",
)

# plot upvp neg
upvp_neg_first.sel(plev = 25000).plot.contourf(
    x="lon",
    y="lat",
    ax=upvp_neg_ax,
    levels=upvp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend =  "both",
)

# plot usvs pos
usvs_pos_first.sel(plev = 25000).plot.contourf(
    x="lon",
    y="lat",
    ax=usvs_pos_ax,
    levels=upvp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend =  "both",
)

# plot usvs neg
map = usvs_neg_first.sel(plev = 25000).plot.contourf(
    x="lon",
    y="lat",
    ax=usvs_neg_ax,
    levels=upvp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend =  "both",
)

# Use levels without zero and black contour lines
levels_no_zero = [lvl for lvl in upvp_levels_div if lvl != 0]

# plot upvp pos (last 10 years) as contour lines
upvp_pos_last.sel(plev=25000).plot.contour(
    x="lon",
    y="lat",
    ax=upvp_pos_ax,
    levels=levels_no_zero,
    colors='k',
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
    linewidths=0.5,
)

# plot upvp neg (last 10 years)
upvp_neg_last.sel(plev=25000).plot.contour(
    x="lon",
    y="lat",
    ax=upvp_neg_ax,
    levels=levels_no_zero,
    colors='k',
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# plot usvs pos (last 10 years)
usvs_pos_last.sel(plev=25000).plot.contour(
    x="lon",
    y="lat",
    ax=usvs_pos_ax,
    levels=levels_no_zero,
    colors='k',
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# plot usvs neg (last 10 years)
line = usvs_neg_last.sel(plev=25000).plot.contour(
    x="lon",
    y="lat",
    ax=usvs_neg_ax,
    levels=levels_no_zero,
    colors='k',
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
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
    label="$\overline{u'v'}$ [m$^2$s$^{-2}$]",
    extend="both",
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
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/upvp_pos_neg.pdf", 
                 dpi = 300, bbox_inches='tight')


# %%
