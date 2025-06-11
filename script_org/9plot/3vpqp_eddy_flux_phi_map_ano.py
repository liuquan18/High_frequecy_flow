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
vpetp_clim_first = read_climatology("Fdiv_phi_steady", "1850", name="div2",model_dir = 'MPI_GE_CMIP6_allplev')
vpetp_clim_last = read_climatology("Fdiv_phi_steady", "2090", name="div2",model_dir = 'MPI_GE_CMIP6_allplev')
# pos ano
vpetp_pos_first = read_comp_var(
    "Fdiv_phi_transient",
    "pos",
    1850,
    time_window=time_window,
    name='div2',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vpetp_neg_first = read_comp_var(
    "Fdiv_phi_transient",
    "neg",
    1850,
    time_window=time_window,
    name='div2',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
    
)

vpetp_pos_last = read_comp_var(
    "Fdiv_phi_transient",
    "pos",
    2090,
    time_window=time_window,
    name='div2',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vpetp_neg_last = read_comp_var(
    "Fdiv_phi_transient",
    "neg",
    2090,
    time_window=time_window,
    name='div2',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)

# %%
vsets_clim_first = read_climatology("Fdiv_phi_steady", "1850", name='div2', model_dir = 'MPI_GE_CMIP6_allplev')
vsets_clim_last = read_climatology("Fdiv_phi_steady", "2090", name='div2', model_dir = 'MPI_GE_CMIP6_allplev')

# pos ano
vsets_pos_first = read_comp_var(
    "Fdiv_phi_steady",
    "pos",
    1850,
    time_window=time_window,
    name='div2',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vsets_neg_first = read_comp_var(
    "Fdiv_phi_steady",
    "neg",
    1850,
    time_window=time_window,
    name='div2',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)

vsets_pos_last = read_comp_var(
    "Fdiv_phi_steady",
    "pos",
    2090,
    time_window=time_window,
    name='div2',
    suffix=suffix,
    remove_zonmean=remove_zonmean,
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vsets_neg_last = read_comp_var(
    "Fdiv_phi_steady",
    "neg",
    2090,
    time_window=time_window,
    name='div2',
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
# read vapor flux
upqp_pos_first = read_comp_var("upqp", phase="pos", decade=1850, time_window=(-10, 5), ano = False).sel(plev = 85000)
upqp_neg_first = read_comp_var("upqp", phase="neg", decade=1850, time_window=(-10, 5), ano = False).sel(plev = 85000)
upqp_pos_last = read_comp_var("upqp", phase="pos", decade=2090, time_window=(-10, 5), ano = False).sel(plev = 85000)
upqp_neg_last = read_comp_var("upqp", phase="neg", decade=2090, time_window=(-10, 5), ano = False).sel(plev = 85000)

#
vpqp_pos_first = read_comp_var("vpqp", phase="pos", decade=1850, time_window=(-10, 5), ano = False).sel(plev = 85000)
vpqp_neg_first = read_comp_var("vpqp", phase="neg", decade=1850, time_window=(-10, 5), ano = False).sel(plev = 85000)
vpqp_pos_last = read_comp_var("vpqp", phase="pos", decade=2090, time_window=(-10, 5), ano = False).sel(plev = 85000)
vpqp_neg_last = read_comp_var("vpqp", phase="neg", decade=2090, time_window=(-10, 5), ano = False).sel(plev = 85000)

# # to flux
qpflux_pos_first = xr.Dataset(
    {"u": upqp_pos_first*1e3, "v": vpqp_pos_first*1e3}
)
qpflux_neg_first = xr.Dataset(
    {"u": upqp_neg_first*1e3, "v": vpqp_neg_first*1e3}
)
qpflux_pos_last = xr.Dataset(
    {"u": upqp_pos_last*1e3, "v": vpqp_pos_last*1e3}
)
qpflux_neg_last = xr.Dataset(
    {"u": upqp_neg_last*1e3, "v": vpqp_neg_last*1e3}
)
#%%
# read climatological vapor flux
upqp_clima_first = read_climatology("upqp", 1850, model_dir = 'MPI_GE_CMIP6').sel(plev = 85000)
upqp_clima_last = read_climatology("upqp", 2090, model_dir = 'MPI_GE_CMIP6').sel(plev = 85000)

vpqp_clima_first = read_climatology("vpqp", 1850, model_dir = 'MPI_GE_CMIP6').sel(plev = 85000)
vpqp_clima_last = read_climatology("vpqp", 2090, model_dir = 'MPI_GE_CMIP6').sel(plev = 85000)

# to flux
qpflux_clima_first = xr.Dataset(
    {"u": upqp_clima_first*1e3, "v": vpqp_clima_first*1e3}
)
qpflux_clima_last = xr.Dataset(
    {"u": upqp_clima_last*1e3, "v": vpqp_clima_last*1e3}
)
#%%
# anomaly
qpflux_pos_first_ano = qpflux_pos_first - qpflux_clima_first
qpflux_neg_first_ano = qpflux_neg_first - qpflux_clima_first
qpflux_pos_last_ano = qpflux_pos_last - qpflux_clima_last
qpflux_neg_last_ano = qpflux_neg_last - qpflux_clima_last


#%%
usqs_pos_first = read_comp_var("usqs", phase="pos", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
usqs_neg_first = read_comp_var("usqs", phase="neg", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)

usqs_pos_last = read_comp_var("usqs", phase="pos", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
usqs_neg_last = read_comp_var("usqs", phase="neg", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)

vsqs_pos_first = read_comp_var("vsqs", phase="pos", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
vsqs_neg_first = read_comp_var("vsqs", phase="neg", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)

vsqs_pos_last = read_comp_var("vsqs", phase="pos", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
vsqs_neg_last = read_comp_var("vsqs", phase="neg", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)

# to flux
qsflux_pos_first = xr.Dataset(
    {"u": usqs_pos_first*1e3, "v": vsqs_pos_first*1e3}
)
qsflux_neg_first = xr.Dataset(
    {"u": usqs_neg_first*1e3, "v": vsqs_neg_first*1e3}
)

qsflux_pos_last = xr.Dataset(
    {"u": usqs_pos_last*1e3, "v": vsqs_pos_last*1e3}
)

qsflux_neg_last = xr.Dataset(
    {"u": usqs_neg_last*1e3, "v": vsqs_neg_last*1e3}
)
#%%
# read climatological vapor flux
usqs_clima_first = read_climatology("usqs", 1850, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
usqs_clima_last = read_climatology("usqs", 2090, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
vsqs_clima_first = read_climatology("vsqs", 1850, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
vsqs_clima_last = read_climatology("vsqs", 2090, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)

# to flux
qsflux_clima_first = xr.Dataset(
    {"u": usqs_clima_first*1e3, "v": vsqs_clima_first*1e3}
)
qsflux_clima_last = xr.Dataset(
    {"u": usqs_clima_last*1e3, "v": vsqs_clima_last*1e3}
)

# anomaly
qsflux_pos_first_ano = qsflux_pos_first - qsflux_clima_first
qsflux_neg_first_ano = qsflux_neg_first - qsflux_clima_first
qsflux_pos_last_ano = qsflux_pos_last - qsflux_clima_last
qsflux_neg_last_ano = qsflux_neg_last - qsflux_clima_last

#%%
qsumflux_pos_first = (qpflux_pos_first + qsflux_pos_first)
qsumflux_neg_first = (qpflux_neg_first + qsflux_neg_first)
qsumflux_pos_last = (qpflux_pos_last + qsflux_pos_last)
qsumflux_neg_last = (qpflux_neg_last + qsflux_neg_last  )
#%%
# anomaly
qsumflux_pos_first_ano = (qpflux_pos_first_ano + qsflux_pos_first_ano)
qsumflux_neg_first_ano = (qpflux_neg_first_ano + qsflux_neg_first_ano)
qsumflux_pos_last_ano = (qpflux_pos_last_ano + qsflux_pos_last_ano)
qsumflux_neg_last_ano = (qpflux_neg_last_ano + qsflux_neg_last_ano)
#%%
qscale_sum = 20
qscale = 10
qscale_steady =20

#%%
vpetp_levels_div = np.arange(-4, 4.1, 0.5)
vpetp_levels_steady = np.arange(-8, 8.1, 2)
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

# quiver for vapor flux anomaly
sum_arrows = axes[0, 0].quiver(
    qsumflux_pos_first_ano.lon.values[::5],
    qsumflux_pos_first_ano.lat.values[::5],
    qsumflux_pos_first_ano.u.values[::5, ::5],
    qsumflux_pos_first_ano.v.values[::5, ::5],
    scale=qscale_sum,
    transform=ccrs.PlateCarree(),
    color="green",
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


# quiver for vapor flux anomaly
trans_arrows = axes[0, 1].quiver(
    qpflux_pos_first_ano.lon.values[::5],
    qpflux_pos_first_ano.lat.values[::5],
    qpflux_pos_first_ano.u.values[::5, ::5],
    qpflux_pos_first_ano.v.values[::5, ::5],
    scale=qscale,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
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
# quiver for vapor flux anomaly
steady_arrows = axes[0, 2].quiver(
    qsflux_pos_first_ano.lon.values[::5],
    qsflux_pos_first_ano.lat.values[::5],
    qsflux_pos_first_ano.u.values[::5, ::5],
    qsflux_pos_first_ano.v.values[::5, ::5],
    scale=qscale_steady,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
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


# quiver for vapor flux anomaly
sum_arrows_neg = axes[1, 0].quiver(
    qsumflux_neg_first_ano.lon.values[::5],
    qsumflux_neg_first_ano.lat.values[::5],
    qsumflux_neg_first_ano.u.values[::5, ::5],
    qsumflux_neg_first_ano.v.values[::5, ::5],
    scale=qscale_sum,
    transform=ccrs.PlateCarree(),
    color="green",
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

# quiver for vapor flux anomaly
trans_arrows_neg = axes[1, 1].quiver(
    qpflux_neg_first_ano.lon.values[::5],
    qpflux_neg_first_ano.lat.values[::5],
    qpflux_neg_first_ano.u.values[::5, ::5],
    qpflux_neg_first_ano.v.values[::5, ::5],
    scale=qscale,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
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
steady_arrows_neg = axes[1, 2].quiver(
    qsflux_neg_first_ano.lon.values[::5],
    qsflux_neg_first_ano.lat.values[::5],
    qsflux_neg_first_ano.u.values[::5, ::5],
    qsflux_neg_first_ano.v.values[::5, ::5],
    scale=qscale_steady,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
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
    label=r"$\overline{v'\theta'}$ [K m s$^{-1}$] (sum)",
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
    label=r"$\overline{v'\theta'}$ [K m s$^{-1}$] (steady)",
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
    2,
    r"2 $m s^{-1} g kg ^{-1}$",
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 10},
    labelsep=0.05,

)

qk = axes[1, 1].quiverkey(
    trans_arrows_neg,
    0.6,
    -0.05,
    2,
    r"2 $m s^{-1} g kg ^{-1}$",
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 10},
    labelsep=0.05,
)

qk = axes[1, 2].quiverkey(
    steady_arrows_neg,
    0.6,
    -0.05,
    2,
    r"2 $m s^{-1} g kg ^{-1}$",
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 10},
    labelsep=0.05,
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
