# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line, map_smooth, NA_box
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
suffix = "_ano"
remove_zonmean = False

################### read div_p #####################
# %%
# transient part
upvp_pos_first = read_comp_var(
    "Fdiv_phi_transient",
    "pos",
    1850,
    time_window=time_window,
    name="div",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)
upvp_neg_first = read_comp_var(
    "Fdiv_phi_transient",
    "neg",
    1850,
    time_window=time_window,
    name="div",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)

upvp_pos_last = read_comp_var(
    "Fdiv_phi_transient",
    "pos",
    2090,
    time_window=time_window,
    name="div",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)
upvp_neg_last = read_comp_var(
    "Fdiv_phi_transient",
    "neg",
    2090,
    time_window=time_window,
    name="div",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)
# quasi-stationary part
usvs_pos_first = read_comp_var(
    "Fdiv_phi_steady",
    "pos",
    1850,
    time_window=time_window,
    name="div",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)
usvs_neg_first = read_comp_var(
    "Fdiv_phi_steady",
    "neg",
    1850,
    time_window=time_window,
    name="div",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)

usvs_pos_last = read_comp_var(
    "Fdiv_phi_steady",
    "pos",
    2090,
    time_window=time_window,
    name="div",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)
usvs_neg_last = read_comp_var(
    "Fdiv_phi_steady",
    "neg",
    2090,
    time_window=time_window,
    name="div",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)

# map smoothing
upvp_pos_first = map_smooth(upvp_pos_first, 5, 5)
upvp_neg_first = map_smooth(upvp_neg_first, 5, 5)
upvp_pos_last = map_smooth(upvp_pos_last, 5, 5)
upvp_neg_last = map_smooth(upvp_neg_last, 5, 5)

usvs_pos_first = map_smooth(usvs_pos_first, 5, 5)
usvs_neg_first = map_smooth(usvs_neg_first, 5, 5)
usvs_pos_last = map_smooth(usvs_pos_last, 5, 5)
usvs_neg_last = map_smooth(usvs_neg_last, 5, 5)

# erase white line before plotting
upvp_pos_first = erase_white_line(upvp_pos_first)
upvp_neg_first = erase_white_line(upvp_neg_first)
upvp_pos_last = erase_white_line(upvp_pos_last)
upvp_neg_last = erase_white_line(upvp_neg_last)
usvs_pos_first = erase_white_line(usvs_pos_first)
usvs_neg_first = erase_white_line(usvs_neg_first)
usvs_pos_last = erase_white_line(usvs_pos_last)
usvs_neg_last = erase_white_line(usvs_neg_last)
# %%
###################### read vpetp, vsets ######################
# pos ano
vpetp_pos_first = read_comp_var(
    "Fdiv_p_transient",
    "pos",
    1850,
    time_window=time_window,
    name="div2",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)
vpetp_neg_first = read_comp_var(
    "Fdiv_p_transient",
    "neg",
    1850,
    time_window=time_window,
    name="div2",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)

vpetp_pos_last = read_comp_var(
    "Fdiv_p_transient",
    "pos",
    2090,
    time_window=time_window,
    name="div2",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)
vpetp_neg_last = read_comp_var(
    "Fdiv_p_transient",
    "neg",
    2090,
    time_window=time_window,
    name="div2",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)
# pos ano
vsets_pos_first = read_comp_var(
    "Fdiv_p_steady",
    "pos",
    1850,
    time_window=time_window,
    name="div2",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)
vsets_neg_first = read_comp_var(
    "Fdiv_p_steady",
    "neg",
    1850,
    time_window=time_window,
    name="div2",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)

vsets_pos_last = read_comp_var(
    "Fdiv_p_steady",
    "pos",
    2090,
    time_window=time_window,
    name="div2",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)
vsets_neg_last = read_comp_var(
    "Fdiv_p_steady",
    "neg",
    2090,
    time_window=time_window,
    name="div2",
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir="MPI_GE_CMIP6_allplev",
)

# map smoothing
vpetp_pos_first = map_smooth(vpetp_pos_first, 5, 5)
vpetp_neg_first = map_smooth(vpetp_neg_first, 5, 5)
vpetp_pos_last = map_smooth(vpetp_pos_last, 5, 5)
vpetp_neg_last = map_smooth(vpetp_neg_last, 5, 5)

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


# %%
######################### read ua, va ##########################
ua_pos_first = read_comp_var(
    "ua",
    phase="pos",
    decade=1850,
    time_window=(-10, 5),
    ano=False,
    model_dir="MPI_GE_CMIP6",
).sel(plev=25000)
ua_neg_first = read_comp_var(
    "ua",
    phase="neg",
    decade=1850,
    time_window=(-10, 5),
    ano=False,
    model_dir="MPI_GE_CMIP6",
).sel(plev=25000)
ua_pos_last = read_comp_var(
    "ua",
    phase="pos",
    decade=2090,
    time_window=(-10, 5),
    ano=False,
    model_dir="MPI_GE_CMIP6",
).sel(plev=25000)
ua_neg_last = read_comp_var(
    "ua",
    phase="neg",
    decade=2090,
    time_window=(-10, 5),
    ano=False,
    model_dir="MPI_GE_CMIP6",
).sel(plev=25000)

va_pos_first = read_comp_var(
    "va",
    phase="pos",
    decade=1850,
    time_window=(-10, 5),
    ano=False,
    model_dir="MPI_GE_CMIP6",
).sel(plev=25000)
va_neg_first = read_comp_var(
    "va",
    phase="neg",
    decade=1850,
    time_window=(-10, 5),
    ano=False,
    model_dir="MPI_GE_CMIP6",
).sel(plev=25000)
va_pos_last = read_comp_var(
    "va",
    phase="pos",
    decade=2090,
    time_window=(-10, 5),
    ano=False,
    model_dir="MPI_GE_CMIP6",
).sel(plev=25000)
va_neg_last = read_comp_var(
    "va",
    phase="neg",
    decade=2090,
    time_window=(-10, 5),
    ano=False,
    model_dir="MPI_GE_CMIP6",
).sel(plev=25000)

# to flux
wndflux_pos_first = xr.Dataset(
    {
        "u": ua_pos_first,
        "v": va_pos_first,
    }
)
wndflux_neg_first = xr.Dataset(
    {
        "u": ua_neg_first,
        "v": va_neg_first,
    }
)
wndflux_pos_last = xr.Dataset(
    {
        "u": ua_pos_last,
        "v": va_pos_last,
    }
)
wndflux_neg_last = xr.Dataset(
    {
        "u": ua_neg_last,
        "v": va_neg_last,
    }
)


# climatology
ua_clima_first = read_climatology("ua", 1850, model_dir="MPI_GE_CMIP6_allplev").sel(
    plev=25000
)
ua_clima_last = read_climatology("ua", 2090, model_dir="MPI_GE_CMIP6_allplev").sel(
    plev=25000
)
va_clima_first = read_climatology("va", 1850, model_dir="MPI_GE_CMIP6_allplev").sel(
    plev=25000
)
va_clima_last = read_climatology("va", 2090, model_dir="MPI_GE_CMIP6_allplev").sel(
    plev=25000
)


# to anomaly
ua_pos_first_ano = ua_pos_first - ua_clima_first
ua_neg_first_ano = ua_neg_first - ua_clima_first
ua_pos_last_ano = ua_pos_last - ua_clima_last
ua_neg_last_ano = ua_neg_last - ua_clima_last

va_pos_first_ano = va_pos_first - va_clima_first
va_neg_first_ano = va_neg_first - va_clima_first
va_pos_last_ano = va_pos_last - va_clima_last
va_neg_last_ano = va_neg_last - va_clima_last

# to flux
wndflux_pos_first_ano = xr.Dataset(
    {
        "u": ua_pos_first_ano,
        "v": va_pos_first_ano,
    }
)

wndflux_neg_first_ano = xr.Dataset(
    {
        "u": ua_neg_first_ano,
        "v": va_neg_first_ano,
    }
)
wndflux_pos_last_ano = xr.Dataset(
    {
        "u": ua_pos_last_ano,
        "v": va_pos_last_ano,
    }
)
wndflux_neg_last_ano = xr.Dataset(
    {
        "u": ua_neg_last_ano,
        "v": va_neg_last_ano,
    }
)


# %%
upvp_levels = np.arange(-3, 3.1, 0.5)
vptp_levels = np.arange(-12, 12.1, 3)
wnd_scale = 150

# %%
fig, axes = plt.subplots(
    2,
    2,
    figsize=(12, 8),
    subplot_kw={"projection": ccrs.NorthPolarStereo(-40, 80)},
    sharex=True,
    sharey=False,
)


# first row, upvp, sum
# positive
sum_color = (upvp_pos_first + usvs_pos_first).plot.contourf(
    ax=axes[0, 0],
    levels=upvp_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)

sum_lines = (upvp_pos_last + usvs_pos_last).plot.contour(
    ax=axes[0, 0],
    levels=[l for l in upvp_levels if l != 0],
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
)


# quiver for wind anomaly
sum_arrows = axes[0, 0].quiver(
    wndflux_pos_first.lon.values[::7],
    wndflux_pos_first.lat.values[::6],
    wndflux_pos_first.u.values[::6, ::7],
    wndflux_pos_first.v.values[::6, ::7],
    scale=wnd_scale,
    transform=ccrs.PlateCarree(),
    color="purple",
    width=0.005,
)

# negative
sum_color_neg = (upvp_neg_first + usvs_neg_first).plot.contourf(
    ax=axes[0, 1],
    levels=upvp_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)
sum_lines_neg = (upvp_neg_last + usvs_neg_last).plot.contour(
    ax=axes[0, 1],
    levels=[l for l in upvp_levels if l != 0],
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
)
# quiver for wind anomaly
sum_arrows_neg = axes[0, 1].quiver(
    wndflux_neg_first.lon.values[::7],
    wndflux_neg_first.lat.values[::6],
    wndflux_neg_first.u.values[::6, ::7],
    wndflux_neg_first.v.values[::6, ::7],
    scale=wnd_scale,
    transform=ccrs.PlateCarree(),
    color="purple",
    width=0.005,
)

# second row, vpetp, sum
# positive
vpetp_color = (vpetp_pos_first + vsets_pos_first).plot.contourf(
    ax=axes[1, 0],
    levels=vptp_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)
vpetp_lines = (vpetp_pos_last + vsets_pos_last).plot.contour(
    ax=axes[1, 0],
    levels=[l for l in vptp_levels if l != 0],
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
)

# negative
vpetp_color_neg = (vpetp_neg_first + vsets_neg_first).plot.contourf(
    ax=axes[1, 1],
    levels=vptp_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)
vpetp_lines_neg = (vpetp_neg_last + vsets_neg_last).plot.contour(
    ax=axes[1, 1],
    levels=[l for l in vptp_levels if l != 0],
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
)


# Add colorbar axes using fig.add_axes for better alignment with tight_layout. vertical
fig.tight_layout()
plt.subplots_adjust(wspace=-0.24, hspace=-0.4)

# Colorbar for first row (upvp sum)
cbar_ax1 = fig.add_axes([0.92, 0.4, 0.015, 0.3])
cbar1 = fig.colorbar(
    sum_color,
    cax=cbar_ax1,
    orientation="vertical",
    extend="both",
    shrink=0.6,
)
cbar1.set_label(
    r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m s$^{-1}$ day$^{-1}$]",
    fontsize=12,
)
cbar1.ax.tick_params(labelsize=10)

# Colorbar for second row (vpetp sum)
cbar_ax2 = fig.add_axes([0.92, 0.03, 0.015, 0.3])
cbar2 = fig.colorbar(
    vpetp_color,
    cax=cbar_ax2,
    orientation="vertical",
    extend="both",
    shrink=0.6,
)
cbar2.set_label(
    r"$\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta'}}{\overline{\theta}_p} \right)$ [m s$^{-1}$ day$^{-1}$]",
    fontsize=12,
)
cbar2.ax.tick_params(labelsize=10)

for ax in axes.flat:
    ax.coastlines(color="grey", linewidth=1)
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="dotted",
    )
    gl.xlocator = mticker.FixedLocator(
        [-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180]
    )
    gl.ylocator = mticker.FixedLocator([10, 30, 50, 70, 90])
    ax.set_title("")
    ax.set_extent([-180, 180, 20, 90], crs=ccrs.PlateCarree())
    clip_map(ax)

# add a, b, c, d to each subplot
for i, ax in enumerate(axes.flat):
    ax.text(
        0.02,
        0.55,
        chr(97 + i),  # chr(97) is 'a', chr(98) is 'b', etc.
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        va="top",
        ha="left",
    )



# add quiver key for the second row
qk = axes[0, 1].quiverkey(
    sum_arrows_neg,
    0.8,
    0.05,
    10,
    r"10 $m s^{-1}$",
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 10},
    labelsep=0.05,
)


# add box region
NA_box(axes[1, 0], lon_min=280, lon_max=360, lat_min=40, lat_max=80)

# save figure
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/upvp_vpetp_sum_ano.pdf",
    bbox_inches="tight",
    dpi=300,
    transparent=True,
)


# %%
