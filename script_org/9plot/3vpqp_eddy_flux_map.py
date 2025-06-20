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

from src.data_helper import read_composite

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div

# %%%
# config
time_window = (-10, 5)
suffix = "_ano"
remove_zonmean = False

################### read div_p #####################

# %%
# read transient EP flux for positive and negative phase
# read data for first decade with region = western
_, _, Tdivphi_pos_first, Tdiv_p_pos_first = read_EP_flux(
    phase="pos",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
    time_window = (-10, 5)
)
_, _, Tdivphi_neg_first, Tdiv_p_neg_first = read_EP_flux(
    phase="neg",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
    time_window = (-10, 5)
)


# last decade region
_, _, Tdivphi_pos_last, Tdiv_p_pos_last = read_EP_flux(
    phase="pos",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
    time_window = (-10, 5)
)
_, _, Tdivphi_neg_last, Tdiv_p_neg_last = read_EP_flux(
    phase="neg",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
    time_window = (-10, 5)
)

# read climatological EP flux
_, _, Tdivphi_clima_first, Tdiv_p_clima_first = (
    read_EP_flux(
        phase="clima",
        decade=1850,
        eddy="transient",
        ano=False,
        lon_mean=False,
        region=None,
    )
)
_, _, Tdivphi_clima_last, Tdiv_p_clima_last = read_EP_flux(
    phase="clima",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)

# divphi select plev = 25000, div_p select plev = 85000
Tdivphi_pos_first = Tdivphi_pos_first.sel(plev=25000)
Tdiv_p_pos_first = Tdiv_p_pos_first.sel(plev=85000)
Tdivphi_neg_first = Tdivphi_neg_first.sel(plev=25000)
Tdiv_p_neg_first = Tdiv_p_neg_first.sel(plev=85000)

Tdivphi_pos_last = Tdivphi_pos_last.sel(plev=25000)
Tdiv_p_pos_last = Tdiv_p_pos_last.sel(plev=85000)
Tdivphi_neg_last = Tdivphi_neg_last.sel(plev=25000)
Tdiv_p_neg_last = Tdiv_p_neg_last.sel(plev=85000)

# climatology
Tdivphi_clima_first = Tdivphi_clima_first.sel(plev=25000)
Tdiv_p_clima_first = Tdiv_p_clima_first.sel(plev=85000)
Tdivphi_clima_last = Tdivphi_clima_last.sel(plev=25000)
Tdiv_p_clima_last = Tdiv_p_clima_last.sel(plev=85000)


# mean over events
Tdivphi_pos_first = Tdivphi_pos_first.mean(dim="event", keep_attrs=True)
Tdiv_p_pos_first = Tdiv_p_pos_first.mean(dim="event", keep_attrs=True)
Tdivphi_neg_first = Tdivphi_neg_first.mean(dim="event", keep_attrs=True)
Tdiv_p_neg_first = Tdiv_p_neg_first.mean(dim="event", keep_attrs=True)
Tdivphi_pos_last = Tdivphi_pos_last.mean(dim="event", keep_attrs=True)
Tdiv_p_pos_last = Tdiv_p_pos_last.mean(dim="event", keep_attrs=True)
Tdivphi_neg_last = Tdivphi_neg_last.mean(dim="event", keep_attrs=True)
Tdiv_p_neg_last = Tdiv_p_neg_last.mean(dim="event", keep_attrs=True)
# anomaly

Tdivphi_pos_first_ano = Tdivphi_pos_first - Tdivphi_clima_first
Tdiv_p_pos_first_ano = Tdiv_p_pos_first - Tdiv_p_clima_first

Tdivphi_neg_first_ano = Tdivphi_neg_first - Tdivphi_clima_first
Tdiv_p_neg_first_ano = Tdiv_p_neg_first - Tdiv_p_clima_first

Tdivphi_pos_last_ano = Tdivphi_pos_last - Tdivphi_clima_last
Tdiv_p_pos_last_ano = Tdiv_p_pos_last - Tdiv_p_clima_last

Tdivphi_neg_last_ano = Tdivphi_neg_last - Tdivphi_clima_last
Tdiv_p_neg_last_ano = Tdiv_p_neg_last - Tdiv_p_clima_last

# erase white line
Tdivphi_pos_first_ano = erase_white_line(Tdivphi_pos_first_ano)
Tdiv_p_pos_first_ano = erase_white_line(Tdiv_p_pos_first_ano)
Tdivphi_neg_first_ano = erase_white_line(Tdivphi_neg_first_ano)
Tdiv_p_neg_first_ano = erase_white_line(Tdiv_p_neg_first_ano)
Tdivphi_pos_last_ano = erase_white_line(Tdivphi_pos_last_ano)
Tdiv_p_pos_last_ano = erase_white_line(Tdiv_p_pos_last_ano)
Tdivphi_neg_last_ano = erase_white_line(Tdivphi_neg_last_ano)
Tdiv_p_neg_last_ano = erase_white_line(Tdiv_p_neg_last_ano)

# erase white line for climatology
Tdivphi_clima_first = erase_white_line(Tdivphi_clima_first)
Tdiv_p_clima_first = erase_white_line(Tdiv_p_clima_first)
Tdivphi_clima_last = erase_white_line(Tdivphi_clima_last)
Tdiv_p_clima_last = erase_white_line(Tdiv_p_clima_last)

# smooth the data
Tdivphi_pos_first_ano = map_smooth(Tdivphi_pos_first_ano, 5, 5)
Tdiv_p_pos_first_ano = map_smooth(Tdiv_p_pos_first_ano, 5, 5)
Tdivphi_neg_first_ano = map_smooth(Tdivphi_neg_first_ano, 5, 5)
Tdiv_p_neg_first_ano = map_smooth(Tdiv_p_neg_first_ano, 5, 5)
Tdivphi_pos_last_ano = map_smooth(Tdivphi_pos_last_ano, 5, 5)
Tdiv_p_pos_last_ano = map_smooth(Tdiv_p_pos_last_ano, 5, 5)
Tdivphi_neg_last_ano = map_smooth(Tdivphi_neg_last_ano, 5, 5)
Tdiv_p_neg_last_ano = map_smooth(Tdiv_p_neg_last_ano, 5, 5)



#%%
    # read steady EP flux for positive and negative phase
_, _, Sdivphi_pos_first, Sdiv_p_pos_first = read_EP_flux(
    phase="pos",
    decade=1850,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
    time_window=(-10, 5)
)
_, _, Sdivphi_neg_first, Sdiv_p_neg_first = read_EP_flux(
    phase="neg",
    decade=1850,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
    time_window=(-10, 5)
)

# last decade
_, _, Sdivphi_pos_last, Sdiv_p_pos_last = read_EP_flux(
    phase="pos",
    decade=2090,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
    time_window=(-10, 5)
)
_, _, Sdivphi_neg_last, Sdiv_p_neg_last = read_EP_flux(
    phase="neg",
    decade=2090,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
    time_window=(-10, 5)
)

# read climatological EP flux
_, _, Sdivphi_clima_first, Sdiv_p_clima_first = (
    read_EP_flux(
        phase="clima",
        decade=1850,
        eddy="steady",
        ano=False,
        lon_mean=False,
        region=None,
    )
)
_, _, Sdivphi_clima_last, Sdiv_p_clima_last = read_EP_flux(
    phase="clima",
    decade=2090,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)

# divphi select plev = 25000, div_p select plev = 850
Sdivphi_pos_first = Sdivphi_pos_first.sel(plev=25000)
Sdiv_p_pos_first = Sdiv_p_pos_first.sel(plev=85000)
Sdivphi_neg_first = Sdivphi_neg_first.sel(plev=25000)
Sdiv_p_neg_first = Sdiv_p_neg_first.sel(plev=85000)

Sdivphi_pos_last = Sdivphi_pos_last.sel(plev=25000)
Sdiv_p_pos_last = Sdiv_p_pos_last.sel(plev=85000)
Sdivphi_neg_last = Sdivphi_neg_last.sel(plev=25000)
Sdiv_p_neg_last = Sdiv_p_neg_last.sel(plev=85000)

# climatology
Sdivphi_clima_first = Sdivphi_clima_first.sel(plev=25000)
Sdiv_p_clima_first = Sdiv_p_clima_first.sel(plev=85000)
Sdivphi_clima_last = Sdivphi_clima_last.sel(plev=25000)
Sdiv_p_clima_last = Sdiv_p_clima_last.sel(plev=85000)

# mean over events
Sdivphi_pos_first = Sdivphi_pos_first.mean(dim="event", keep_attrs=True)
Sdiv_p_pos_first = Sdiv_p_pos_first.mean(dim="event", keep_attrs=True)
Sdivphi_neg_first = Sdivphi_neg_first.mean(dim="event", keep_attrs=True)
Sdiv_p_neg_first = Sdiv_p_neg_first.mean(dim="event", keep_attrs=True)
Sdivphi_pos_last = Sdivphi_pos_last.mean(dim="event", keep_attrs=True)
Sdiv_p_pos_last = Sdiv_p_pos_last.mean(dim="event", keep_attrs=True)
Sdivphi_neg_last = Sdivphi_neg_last.mean(dim="event", keep_attrs=True)
Sdiv_p_neg_last = Sdiv_p_neg_last.mean(dim="event", keep_attrs=True)

# anomaly
Sdivphi_pos_first_ano = Sdivphi_pos_first - Sdivphi_clima_first
Sdiv_p_pos_first_ano = Sdiv_p_pos_first - Sdiv_p_clima_first

Sdivphi_neg_first_ano = Sdivphi_neg_first - Sdivphi_clima_first
Sdiv_p_neg_first_ano = Sdiv_p_neg_first - Sdiv_p_clima_first

Sdivphi_pos_last_ano = Sdivphi_pos_last - Sdivphi_clima_last
Sdiv_p_pos_last_ano = Sdiv_p_pos_last - Sdiv_p_clima_last

Sdivphi_neg_last_ano = Sdivphi_neg_last - Sdivphi_clima_last
Sdiv_p_neg_last_ano = Sdiv_p_neg_last - Sdiv_p_clima_last

# erase white line
Sdivphi_pos_first_ano = erase_white_line(Sdivphi_pos_first_ano)
Sdiv_p_pos_first_ano = erase_white_line(Sdiv_p_pos_first_ano)
Sdivphi_neg_first_ano = erase_white_line(Sdivphi_neg_first_ano)
Sdiv_p_neg_first_ano = erase_white_line(Sdiv_p_neg_first_ano)
Sdivphi_pos_last_ano = erase_white_line(Sdivphi_pos_last_ano)
Sdiv_p_pos_last_ano = erase_white_line(Sdiv_p_pos_last_ano)
Sdivphi_neg_last_ano = erase_white_line(Sdivphi_neg_last_ano)
Sdiv_p_neg_last_ano = erase_white_line(Sdiv_p_neg_last_ano)
#
# erase white line of climatology
Sdivphi_clima_first = erase_white_line(Sdivphi_clima_first)
Sdiv_p_clima_first = erase_white_line(Sdiv_p_clima_first)
Sdivphi_clima_last = erase_white_line(Sdivphi_clima_last)
Sdiv_p_clima_last = erase_white_line(Sdiv_p_clima_last)
#
# smooth the data
Sdivphi_pos_first_ano = map_smooth(Sdivphi_pos_first_ano, 5, 5)
Sdiv_p_pos_first_ano = map_smooth(Sdiv_p_pos_first_ano, 5, 5)
Sdivphi_neg_first_ano = map_smooth(Sdivphi_neg_first_ano, 5, 5)
Sdiv_p_neg_first_ano = map_smooth(Sdiv_p_neg_first_ano, 5, 5)
Sdivphi_pos_last_ano = map_smooth(Sdivphi_pos_last_ano, 5, 5)
Sdiv_p_pos_last_ano = map_smooth(Sdiv_p_pos_last_ano, 5, 5)
Sdivphi_neg_last_ano = map_smooth(Sdivphi_neg_last_ano, 5, 5)
Sdiv_p_neg_last_ano = map_smooth(Sdiv_p_neg_last_ano, 5, 5)





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
upvp_levels = np.arange(-2, 2.1, 0.5)

# %%
fig, axes = plt.subplots(
    2,
    2,
    figsize=(12, 8),
    subplot_kw={"projection": ccrs.NorthPolarStereo(-40, 80)},
    sharex=True,
    sharey=False,
)

# first row, upvp, transient only
# positive
sum_color = Tdivphi_pos_first_ano.plot.contourf(
    ax=axes[0, 0],
    levels=upvp_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)

sum_lines = Tdivphi_pos_last_ano.plot.contour(
    ax=axes[0, 0],
    levels=[l for l in upvp_levels if l != 0],
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
)


# negative
sum_color_neg = Tdivphi_neg_first_ano.plot.contourf(
    ax=axes[0, 1],
    levels=upvp_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)
sum_lines_neg = Tdivphi_neg_last_ano.plot.contour(
    ax=axes[0, 1],
    levels=[l for l in upvp_levels if l != 0],
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
)


# second row, stationary eddy momentum flux (Sdivphi)
# positive
stat_color = Sdivphi_pos_first_ano.plot.contourf(
    ax=axes[1, 0],
    levels=upvp_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)
stat_lines = Sdivphi_pos_last_ano.plot.contour(
    ax=axes[1, 0],
    levels=[l for l in upvp_levels if l != 0],
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
)

# negative
stat_color_neg = Sdivphi_neg_first_ano.plot.contourf(
    ax=axes[1, 1],
    levels=upvp_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)
stat_lines_neg = Sdivphi_neg_last_ano.plot.contour(
    ax=axes[1, 1],
    levels=[l for l in upvp_levels if l != 0],
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
)

# Add colorbar axes using fig.add_axes for better alignment with tight_layout. vertical
fig.tight_layout()
plt.subplots_adjust(wspace=-0.24, hspace=-0.4)

# Colorbar for first row (upvp transient)
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

# Colorbar for second row (upvp stationary)
cbar_ax2 = fig.add_axes([0.92, 0.03, 0.015, 0.3])
cbar2 = fig.colorbar(
    stat_color,
    cax=cbar_ax2,
    orientation="vertical",
    extend="both",
    shrink=0.6,
)
cbar2.set_label(
    r"$-\frac{\partial}{\partial y} (\overline{u^*v^*})$ [m s$^{-1}$ day$^{-1}$]",
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
    ax.set_extent([-180, 180, 30, 90], crs=ccrs.PlateCarree())
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


# add box region
# NA_box(axes[1, 0], lon_min=280, lon_max=360, lat_min=40, lat_max=80)

# # save figure
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0main_text/upvp_map_ano.pdf",
    bbox_inches="tight",
    dpi=300,
    transparent=True,
)


# %%
vptp_levels = np.arange(-2, 2.1, 0.5)
vptp_steady_levels = np.arange(-10, 10.1, 2)

fig, axes = plt.subplots(
    2,
    2,
    figsize=(12, 8),
    subplot_kw={"projection": ccrs.NorthPolarStereo(-40, 80)},
    sharex=True,
    sharey=False,
)

# first row, div_p, transient only
# positive
sum_color = Tdiv_p_pos_first_ano.plot.contourf(
    ax=axes[0, 0],
    levels=vptp_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)

sum_lines = Tdiv_p_pos_last_ano.plot.contour(
    ax=axes[0, 0],
    levels=[l for l in vptp_levels if l != 0],
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
)

# negative
sum_color_neg = Tdiv_p_neg_first_ano.plot.contourf(
    ax=axes[0, 1],
    levels=vptp_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)
sum_lines_neg = Tdiv_p_neg_last_ano.plot.contour(
    ax=axes[0, 1],
    levels=[l for l in vptp_levels if l != 0],
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
)

# second row, stationary eddy div_p
# positive
stat_color = Sdiv_p_pos_first_ano.plot.contourf(
    ax=axes[1, 0],
    levels=vptp_steady_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)
stat_lines = Sdiv_p_pos_last_ano.plot.contour(
    ax=axes[1, 0],
    levels=[l for l in vptp_steady_levels if l != 0],
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
)

# negative
stat_color_neg = Sdiv_p_neg_first_ano.plot.contourf(
    ax=axes[1, 1],
    levels=vptp_steady_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)
stat_lines_neg = Sdiv_p_neg_last_ano.plot.contour(
    ax=axes[1, 1],
    levels=[l for l in vptp_steady_levels if l != 0],
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
)

# Add colorbar axes using fig.add_axes for better alignment with tight_layout. vertical
fig.tight_layout()
plt.subplots_adjust(wspace=-0.24, hspace=-0.4)

# Colorbar for first row (div_p transient)
cbar_ax1 = fig.add_axes([0.92, 0.4, 0.015, 0.3])
cbar1 = fig.colorbar(
    sum_color,
    cax=cbar_ax1,
    orientation="vertical",
    extend="both",
    shrink=0.6,
)
cbar1.set_label(
    r"$-\frac{\partial}{\partial p} (\overline{v'\theta'})$ [K s$^{-1}$ day$^{-1}$]",
    fontsize=12,
)
cbar1.ax.tick_params(labelsize=10)

# Colorbar for second row (div_p stationary)
cbar_ax2 = fig.add_axes([0.92, 0.03, 0.015, 0.3])
cbar2 = fig.colorbar(
    stat_color,
    cax=cbar_ax2,
    orientation="vertical",
    extend="both",
    shrink=0.6,
)
cbar2.set_label(
    r"$-\frac{\partial}{\partial p} (\overline{v'\theta'})$ [K s$^{-1}$ day$^{-1}$]",
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
    ax.set_extent([-180, 180, 30, 90], crs=ccrs.PlateCarree())
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

# add box region
# NA_box(axes[1, 0], lon_min=280, lon_max=360, lat_min=40, lat_max=80)

# # save figure
# plt.savefig(
#     "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0main_text/vptp_map_ano.pdf",
#     bbox_inches="tight",
#     dpi=300,
#     transparent=True,
# )

# %%
