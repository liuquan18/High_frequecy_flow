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

from src.plotting.util import clip_map
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
from matplotlib.patches import Rectangle


# %%%
# config
time_window = (-10, 5)
suffix = ""
remove_zonmean = False

# %%
vpetp_levels_div = np.arange(-4.5, 4.6, 1.5)

scale_hus = 5e4

# %%
###### read vpetp
# climatology
vpetp_clim_first = read_climatology("vpetp", "1850", name="vpetp",model_dir = 'MPI_GE_CMIP6_allplev')
vpetp_clim_last = read_climatology("vpetp", "2090", name="vpetp",model_dir = 'MPI_GE_CMIP6_allplev')
# pos ano
vpetp_pos_first = read_comp_var(
    "vpetp",
    "pos",
    1850,
    time_window=time_window,
    name="vpetp",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vpetp_neg_first = read_comp_var(
    "vpetp",
    "neg",
    1850,
    time_window=time_window,
    name="vpetp",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
    
)

vpetp_pos_last = read_comp_var(
    "vpetp",
    "pos",
    2090,
    time_window=time_window,
    name="vpetp",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vpetp_neg_last = read_comp_var(
    "vpetp",
    "neg",
    2090,
    time_window=time_window,
    name="vpetp",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)

# anomaly
vpetp_pos_first_ano = vpetp_pos_first - vpetp_clim_first
vpetp_neg_first_ano = vpetp_neg_first - vpetp_clim_first
vpetp_pos_last_ano = vpetp_pos_last - vpetp_clim_last
vpetp_neg_last_ano = vpetp_neg_last - vpetp_clim_last
# %%
vsets_clim_first = read_climatology("vsets", "1850", name="vsets", model_dir = 'MPI_GE_CMIP6_allplev')
vsets_clim_last = read_climatology("vsets", "2090", name="vsets", model_dir = 'MPI_GE_CMIP6_allplev')

# pos ano
vsets_pos_first = read_comp_var(
    "vsets",
    "pos",
    1850,
    time_window=time_window,
    name="vsets",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vsets_neg_first = read_comp_var(
    "vsets",
    "neg",
    1850,
    time_window=time_window,
    name="vsets",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)

vsets_pos_last = read_comp_var(
    "vsets",
    "pos",
    2090,
    time_window=time_window,
    name="vsets",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vsets_neg_last = read_comp_var(
    "vsets",
    "neg",
    2090,
    time_window=time_window,
    name="vsets",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
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

# erase white line before plotting
vpetp_pos_first = erase_white_line(vpetp_pos_first)
vpetp_neg_first = erase_white_line(vpetp_neg_first)
vpetp_pos_last = erase_white_line(vpetp_pos_last)
vpetp_neg_last = erase_white_line(vpetp_neg_last)
vsets_pos_first = erase_white_line(vsets_pos_first)
vsets_neg_first = erase_white_line(vsets_neg_first)
vsets_pos_last = erase_white_line(vsets_pos_last)
vsets_neg_last = erase_white_line(vsets_neg_last)

# anomaly
vsets_pos_first_ano = vsets_pos_first - vsets_clim_first
vsets_neg_first_ano = vsets_neg_first - vsets_clim_first
vsets_pos_last_ano = vsets_pos_last - vsets_clim_last
vsets_neg_last_ano = vsets_neg_last - vsets_clim_last


#%%
vpetp_levels_div = np.arange(-20, 21, 5)
vpetp_levels_steady = np.arange(-40, 41, 5)
# %%
fig, axes = plt.subplots(
    2,
    3,
    figsize=(12, 9),
    subplot_kw={"projection": ccrs.NorthPolarStereo(-40, 80)},
    sharex=True,
    sharey=False,
)

plt.subplots_adjust(wspace=-0.2, hspace=-0.2)

# First row: positive phase (first and last period)
sum_color = (vpetp_pos_first + vsets_pos_first).sel(plev=85000).plot.contourf(
    ax=axes[0, 0],
    levels=vpetp_levels_steady,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
(vpetp_pos_last + vsets_pos_last).sel(plev=85000).plot.contour(
    ax=axes[0, 0],
    levels=[l for l in vpetp_levels_steady if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# Transient
trans_color = vpetp_pos_first.sel(plev=85000).plot.contourf(
    ax=axes[0, 1],
    levels=vpetp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
vpetp_pos_last.sel(plev=85000).plot.contour(
    ax=axes[0, 1],
    levels=[l for l in vpetp_levels_div if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# Steady
steady_color = vsets_pos_first.sel(plev=85000).plot.contourf(
    ax=axes[0, 2],
    levels=vpetp_levels_steady,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
vsets_pos_last.sel(plev=85000).plot.contour(
    ax=axes[0, 2],
    levels=[l for l in vpetp_levels_steady if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# Second row: negative phase (first and last period)
sum_color_neg = (vpetp_neg_first + vsets_neg_first).sel(plev=85000).plot.contourf(
    ax=axes[1, 0],
    levels=vpetp_levels_steady,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
(vpetp_neg_last + vsets_neg_last).sel(plev=85000).plot.contour(
    ax=axes[1, 0],
    levels=[l for l in vpetp_levels_steady if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# Transient
trans_color_neg = vpetp_neg_first.sel(plev=85000).plot.contourf(
    ax=axes[1, 1],
    levels=vpetp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
vpetp_neg_last.sel(plev=85000).plot.contour(
    ax=axes[1, 1],
    levels=[l for l in vpetp_levels_div if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# Steady
steady_color_neg = vsets_neg_first.sel(plev=85000).plot.contourf(
    ax=axes[1, 2],
    levels=vpetp_levels_steady,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
vsets_neg_last.sel(plev=85000).plot.contour(
    ax=axes[1, 2],
    levels=[l for l in vpetp_levels_steady if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# Add colorbar axes using fig.add_axes for better alignment with tight_layout
fig.tight_layout()
fig.subplots_adjust(wspace=-0.03, hspace=-0.5, top=1., bottom=0.15)

width_shrink = axes[1, 0].get_position().width * 0.8
offset = (axes[1, 0].get_position().width - width_shrink) / 2

cax_sum = fig.add_axes([
    axes[1, 0].get_position().x0 + offset,
    0.08,
    width_shrink,
    0.02
])
cax_prime = fig.add_axes([
    axes[1, 1].get_position().x0 + offset,
    0.08,
    width_shrink,
    0.02
])
cax_steady = fig.add_axes([
    axes[1, 2].get_position().x0 + offset,
    0.08,
    width_shrink,
    0.02
])

fig.colorbar(
    sum_color,
    cax=cax_sum,
    orientation="horizontal",
    label=r"$\overline{v'\theta'} + \overline{v^*\theta^*}$ [K m s$^{-1}$] (sum)",
)
fig.colorbar(
    trans_color,
    cax=cax_prime,
    orientation="horizontal",
    label=r"$\overline{v'\theta'}$ [K m s$^{-1}$] (transient)",
)
fig.colorbar(
    steady_color,
    cax=cax_steady,
    orientation="horizontal",
    label=r"$\overline{v^*\theta^*}$ [K m s$^{-1}$] (steady)",
)

for ax in axes.flat:
    ax.coastlines(color="grey", linewidth=1)
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="dotted",
    )
    gl.xlocator = mticker.FixedLocator([-180,-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180])
    gl.ylocator = mticker.FixedLocator([10, 30, 50, 70, 90])
    ax.set_title("")
    ax.set_extent([-180, 180, 20, 90], crs=ccrs.PlateCarree())
    clip_map(ax)

# Add panel labels a, b, c, ...
for i, ax in enumerate(axes.flat):
    ax.text(
        0.1,
        0.5,
        f"{chr(97 + i)}",
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top",
        ha="right",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=0.2),
        zorder=10,
    )

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eddy_heat_flux_withoutano.pdf",
    bbox_inches="tight",
    dpi=300,
    transparent=True,
)



#%%
vpetp_levels_div = np.arange(-20, 21, 5)
vpetp_levels_steady = np.arange(-40, 41, 5)
scale_hus = 5e4

# %%
fig, axes = plt.subplots(
    2,
    3,
    figsize=(15, 10),
    subplot_kw={"projection": ccrs.NorthPolarStereo(-40, 80)},
    sharex=True,
    sharey=False,
)

# first 10 years
# sum (transient + steady)
sum_color_first = (vpetp_clim_first.sel(plev=85000) + vsets_clim_first.sel(plev=85000)).plot.contourf(
    ax=axes[0, 0],
    levels=vpetp_levels_steady,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# transient
prime_color_first = vpetp_clim_first.sel(plev=85000).plot.contourf(
    ax=axes[0, 1],
    levels=vpetp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# steady
steady_color_first = vsets_clim_first.sel(plev=85000).plot.contourf(
    ax=axes[0, 2],
    levels=vpetp_levels_steady,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# last 10 years
# sum (transient + steady)
sum_color_last = (vpetp_clim_last.sel(plev=85000) + vsets_clim_last.sel(plev=85000)).plot.contourf(
    ax=axes[1, 0],
    levels=vpetp_levels_steady,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# transient
prime_color_last = vpetp_clim_last.sel(plev=85000).plot.contourf(
    ax=axes[1, 1],
    levels=vpetp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# steady
steady_color_last = vsets_clim_last.sel(plev=85000).plot.contourf(
    ax=axes[1, 2],
    levels=vpetp_levels_steady,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)

fig.tight_layout()
fig.subplots_adjust(wspace=-0.03, hspace=-0.5, top=1., bottom=0.15)

width_shrink = axes[1, 0].get_position().width * 0.8
offset = (axes[1, 0].get_position().width - width_shrink) / 2

cax_sum = fig.add_axes([
    axes[1, 0].get_position().x0 + offset,
    0.08,
    width_shrink,
    0.02
])
cax_prime = fig.add_axes([
    axes[1, 1].get_position().x0 + offset,
    0.08,
    width_shrink,
    0.02
])
cax_steady = fig.add_axes([
    axes[1, 2].get_position().x0 + offset,
    0.08,
    width_shrink,
    0.02
])

fig.colorbar(
    sum_color_first,
    cax=cax_sum,
    orientation="horizontal",
    label=r"$\overline{v'\theta'} + \overline{v^*\theta^*}$ [K m s$^{-1}$] (sum)",
)
fig.colorbar(
    prime_color_first,
    cax=cax_prime,
    orientation="horizontal",
    label=r"$\overline{v'\theta'}$ [K m s$^{-1}$] (transient)",
)
fig.colorbar(
    steady_color_first,
    cax=cax_steady,
    orientation="horizontal",
    label=r"$\overline{v^*\theta^*}$ [K m s$^{-1}$] (steady)",
)

for ax in axes.flat:
    ax.coastlines(color="grey", linewidth=1)
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="dotted",
    )
    ax.set_title("")
    ax.set_extent([-180, 180, 20, 90], crs=ccrs.PlateCarree())
    gl.xlocator = mticker.FixedLocator([-180,-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180])
    gl.ylocator = mticker.FixedLocator([10, 30, 50, 70, 90])
    clip_map(ax)

for i, ax in enumerate(axes.flat):
    ax.text(
        0.1,
        0.5,
        f"{chr(97 + i)}",
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top",
        ha="right",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=0.2),
        zorder=10,
    )

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eddy_heat_flux_clim.pdf",
    bbox_inches="tight",
    dpi=300,
    transparent=True,
)

# %%
