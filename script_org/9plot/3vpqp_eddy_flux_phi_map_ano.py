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
suffix = "_ano"
remove_zonmean = False

# %%
vpetp_levels_div = np.arange(-12, 12, 1.3)

scale_hus = 5e4

# %%
###### read vpetp
# climatology
vpetp_clim_first = read_climatology("Fdiv_phi_steady", "1850", name='div',model_dir = 'MPI_GE_CMIP6_allplev')
vpetp_clim_last = read_climatology("Fdiv_phi_steady", "2090", name='div',model_dir = 'MPI_GE_CMIP6_allplev')
# pos ano
vpetp_pos_first = read_comp_var(
    "Fdiv_phi_transient",
    "pos",
    1850,
    time_window=time_window,
    name='div',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vpetp_neg_first = read_comp_var(
    "Fdiv_phi_transient",
    "neg",
    1850,
    time_window=time_window,
    name='div',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
    
)

vpetp_pos_last = read_comp_var(
    "Fdiv_phi_transient",
    "pos",
    2090,
    time_window=time_window,
    name='div',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vpetp_neg_last = read_comp_var(
    "Fdiv_phi_transient",
    "neg",
    2090,
    time_window=time_window,
    name='div',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)

# %%
vsets_clim_first = read_climatology("Fdiv_phi_steady", "1850", name='div', model_dir = 'MPI_GE_CMIP6_allplev')
vsets_clim_last = read_climatology("Fdiv_phi_steady", "2090", name='div', model_dir = 'MPI_GE_CMIP6_allplev')

# pos ano
vsets_pos_first = read_comp_var(
    "Fdiv_phi_steady",
    "pos",
    1850,
    time_window=time_window,
    name='div',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vsets_neg_first = read_comp_var(
    "Fdiv_phi_steady",
    "neg",
    1850,
    time_window=time_window,
    name='div',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)

vsets_pos_last = read_comp_var(
    "Fdiv_phi_steady",
    "pos",
    2090,
    time_window=time_window,
    name='div',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vsets_neg_last = read_comp_var(
    "Fdiv_phi_steady",
    "neg",
    2090,
    time_window=time_window,
    name='div',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
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
#%%
# read ua, va
ua_pos_first = read_comp_var("ua", phase="pos", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
ua_neg_first = read_comp_var("ua", phase="neg", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
ua_pos_last = read_comp_var("ua", phase="pos", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
ua_neg_last = read_comp_var("ua", phase="neg", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)

va_pos_first = read_comp_var("va", phase="pos", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
va_neg_first = read_comp_var("va", phase="neg", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
va_pos_last = read_comp_var("va", phase="pos", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
va_neg_last = read_comp_var("va", phase="neg", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
#%%
# to flux
wndflux_pos_first = xr.Dataset({
    "u": ua_pos_first,
    "v": va_pos_first,
})
wndflux_neg_first = xr.Dataset({
    "u": ua_neg_first,
    "v": va_neg_first,
})
wndflux_pos_last = xr.Dataset({
    "u": ua_pos_last,
    "v": va_pos_last,
})
wndflux_neg_last = xr.Dataset({
    "u": ua_neg_last,
    "v": va_neg_last,
})

#%%
# climatology
ua_clima_first = read_climatology("ua", 1850, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
ua_clima_last = read_climatology("ua", 2090, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
va_clima_first = read_climatology("va", 1850, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
va_clima_last = read_climatology("va", 2090, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)

#%%
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
wndflux_pos_first_ano = xr.Dataset({
    "u": ua_pos_first_ano,
    "v": va_pos_first_ano,
})

wndflux_neg_first_ano = xr.Dataset({
    "u": ua_neg_first_ano,
    "v": va_neg_first_ano,
})
wndflux_pos_last_ano = xr.Dataset({
    "u": ua_pos_last_ano,
    "v": va_pos_last_ano,
})
wndflux_neg_last_ano = xr.Dataset({ 
    "u": ua_neg_last_ano,
    "v": va_neg_last_ano,
})

#%%

wnd_scale = 150


#%%
vpetp_levels_div = np.arange(-1.5, 1.6, 0.5)
vpetp_levels_steady = np.arange(-3, 3.1, 0.5)
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
sum_color = (vpetp_pos_first + vsets_pos_first).plot.contourf(
    ax=axes[0, 0],
    levels=vpetp_levels_steady,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
(vpetp_pos_last + vsets_pos_last).plot.contour(
    ax=axes[0, 0],
    levels=[l for l in vpetp_levels_steady if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
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


# Transient
trans_color = vpetp_pos_first.plot.contourf(
    ax=axes[0, 1],
    levels=vpetp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
vpetp_pos_last.plot.contour(
    ax=axes[0, 1],
    levels=[l for l in vpetp_levels_div if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)



# Steady
steady_color = vsets_pos_first.plot.contourf(
    ax=axes[0, 2],
    levels=vpetp_levels_steady,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
vsets_pos_last.plot.contour(
    ax=axes[0, 2],
    levels=[l for l in vpetp_levels_steady if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# Second row: negative phase (first and last period)
sum_color_neg = (vpetp_neg_first + vsets_neg_first).plot.contourf(
    ax=axes[1, 0],
    levels=vpetp_levels_steady,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
(vpetp_neg_last + vsets_neg_last).plot.contour(
    ax=axes[1, 0],
    levels=[l for l in vpetp_levels_steady if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)


# quiver for wind anomaly
sum_arrows_neg = axes[1, 0].quiver(
    wndflux_neg_first.lon.values[::7],
    wndflux_neg_first.lat.values[::6],
    wndflux_neg_first.u.values[::6, ::7],
    wndflux_neg_first.v.values[::6, ::7],
    scale=wnd_scale,
    transform=ccrs.PlateCarree(),
    color="purple",
    width=0.005,
)
# Transient
trans_color_neg = vpetp_neg_first.plot.contourf(
    ax=axes[1, 1],
    levels=vpetp_levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
vpetp_neg_last.plot.contour(
    ax=axes[1, 1],
    levels=[l for l in vpetp_levels_div if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)


# Steady
steady_color_neg = vsets_neg_first.plot.contourf(
    ax=axes[1, 2],
    levels=vpetp_levels_steady,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
vsets_neg_last.plot.contour(
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
    label= r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m s$^{-1}$ day$^{-1}$]",
)
fig.colorbar(
    trans_color,
    cax=cax_prime,
    orientation="horizontal",
    label= r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m s$^{-1}$ day$^{-1}$]",
)
fig.colorbar(
    steady_color,
    cax=cax_steady,
    orientation="horizontal",
    label= r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m s$^{-1}$ day$^{-1}$]",
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



# add quiver key for the second row
qk = axes[1, 0].quiverkey(
    sum_arrows_neg,
    0.6,
    -0.05,
    10,
    r"10 $m s^{-1}$",
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 10},
    labelsep=0.05,
)

# draw box over the region lon[300, 360], lat[40, 80]
# Draw a smooth box over lon[300, 360], lat[40, 80] on axes[1,2]
lons = np.linspace(300, 360, 200)
lats = np.linspace(40, 80, 200)

# Bottom edge: lon 300->360, lat=40
lon_b = lons
lat_b = np.full_like(lons, 40)
# Right edge: lon=360, lat 40->80
lon_r = np.full_like(lats, 360)
lat_r = lats
# Top edge: lon 360->300, lat=80
lon_t = lons[::-1]
lat_t = np.full_like(lons, 80)
# Left edge: lon=300, lat 80->40
lon_l = np.full_like(lats, 300)
lat_l = lats[::-1]

lon_box = np.concatenate([lon_b, lon_r, lon_t, lon_l, [lon_b[0]]])
lat_box = np.concatenate([lat_b, lat_r, lat_t, lat_l, [lat_b[0]]])

axes[0, 1].plot(
    lon_box, lat_box,
    color="yellow",
    linestyle="dotted",
    linewidth=2,
    transform=ccrs.PlateCarree(),
    zorder=20,
)


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
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/pv_div_phi_map_anomonth.pdf",
    bbox_inches="tight",
    dpi=300,
    transparent=True,
)



# %%
