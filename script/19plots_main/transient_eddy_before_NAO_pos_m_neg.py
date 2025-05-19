# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line
from src.plotting.util import lon2x
from matplotlib.ticker import ScalarFormatter
from src.plotting.prime_data import vert_integrate

import matplotlib.colors as mcolors
import cartopy
import glob

# %%
import src.plotting.util as util
import src.moisture.longitudinal_contrast as lc

import importlib

importlib.reload(util)
# %%
from src.plotting.prime_data import read_composite_MPI  # noqa: E402
from src.plotting.prime_data import read_MPI_GE_uhat
#%%
# u hat
uhat_first, uhat_last = read_MPI_GE_uhat()

#%%
# u'v' 5-0 days before 
upvp_first = read_composite_MPI("upvp", "upvp", 1850, '5_0') # 5 days before
upvp_last = read_composite_MPI("upvp", "upvp", 2090, '5_0') # 5 days before
if upvp_first.plev.size > 1:
    upvp_first = upvp_first.sel(plev=25000)
    upvp_last = upvp_last.sel(plev=25000)
#%%
# v't' -15 - 5 days before
vpetp_first = read_composite_MPI("vpetp", "vpetp", 1850)
vpetp_last = read_composite_MPI("vpetp", "vpetp", 2090)
# select v't' at 850 hPa
vpetp_first = vpetp_first.sel(plev=85000)
vpetp_last = vpetp_last.sel(plev=85000)
#%%
# v'q' -15 - 5 days before
vpqp_first = read_composite_MPI("vpqp", "vptp", 1850)
vpqp_last = read_composite_MPI("vpqp", "vptp", 2090)

upqp_first = read_composite_MPI("upqp", "upqp", 1850)
upqp_last = read_composite_MPI("upqp", "upqp", 2090)

# integrate qp
upqp_first = vert_integrate(upqp_first)
upqp_last = vert_integrate(upqp_last)

vpqp_first = vert_integrate(vpqp_first)
vpqp_last = vert_integrate(vpqp_last)

# to flux
qflux_first = xr.Dataset({'u': upqp_first*1e3, 'v': vpqp_first*1e3}) #g/kg m/s
qflux_last = xr.Dataset({'u': upqp_last*1e3, 'v': vpqp_last*1e3})


# %%
temp_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/temp_seq.txt"
)
temp_cmap_seq = mcolors.ListedColormap(temp_cmap_seq, name="temp_div")

temp_cmap_div = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/temp_div.txt"
)
temp_cmap_div = mcolors.ListedColormap(temp_cmap_div, name="temp_div")

prec_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_seq.txt"
)
prec_cmap_seq = mcolors.ListedColormap(prec_cmap_seq, name="prec_div")

prec_cmap_div = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_div.txt"
)
prec_cmap_div = mcolors.ListedColormap(prec_cmap_div, name="prec_div")

# %%
uhat_levels_div = np.arange(-12, 13, 2)
upvp_levels_div = np.arange(-25, 26, 5)
vptp_levels_div = np.arange(-2, 2.1, 0.5)

scale_div = 0.5

#%%
fig, axes = plt.subplots(
    2, 3, figsize=(12, 10), subplot_kw={"projection": ccrs.Orthographic(-30, 90)}
)

# first row first ten years
# first column uhat
uhat_first.plot.contourf(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=uhat_levels_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\hat{u} / m s^{-1}$",
        "orientation": "horizontal",
        "pad": 0.05,
        "shrink": 0.8,
        "aspect": 20,
    },
)

# second column 5-0 days before u'v'
upvp_first.plot.contourf(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=upvp_levels_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$ u' v'/ m^{2} s {-2}$",
        "orientation": "horizontal",
        "pad": 0.05,
        "shrink": 0.8,
        "aspect": 20,
    },
)

# third column -15 - 5 days before
vpetp_first.plot.contourf(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$ v' \theta'_e/ K m s^{-1}$",
        "orientation": "horizontal",
        "pad": 0.05,
        "shrink": 0.8,
        "aspect": 20,
    },
)

# quiver
first_flux_arrow = axes[0, 2].quiver(
    qflux_first["lon"].values[::3],
    qflux_first["lat"].values[::3],
    qflux_first["u"].values[::3, ::3],
    qflux_first["v"].values[::3, ::3],
    transform=ccrs.PlateCarree(),
    scale=scale_div,
    color="black",
    pivot="middle",
)
# add quiver key
# quiver_key = axes[0, 2].quiverkey(
#     first_flux_arrow,
#     0.65,
#     0.0,
#     0.05,
#     r"$0.05 g kg^{-1} m s^{-1}$",
#     transform=ccrs.PlateCarree(),
#     labelpos="E",
#     coordinates="axes",
#     fontproperties={"size": 12},
# )

# second row last ten years
# first column uhat
uhat_last.plot.contourf(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=uhat_levels_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\hat{u} / m s ^{-1}$",
        "orientation": "horizontal",
        "pad": 0.05,
        "shrink": 0.8,
        "aspect": 20,
    },
)

# second column 5-0 days before u'v'
upvp_last.plot.contourf(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=upvp_levels_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$ u' v'/ m^{2} s {-2}$",
        "orientation": "horizontal",
        "pad": 0.05,
        "shrink": 0.8,
        "aspect": 20,
    },
)

# third column -15 - 5 days before
vpetp_last.plot.contourf(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$ v' \theta_e'/ K m s^{-1}$",
        "orientation": "horizontal",
        "pad": 0.05,
        "shrink": 0.8,
        "aspect": 20,
    },
)

# quiver
last_flux_arrow = axes[1, 2].quiver(
    qflux_last["lon"].values[::3],
    qflux_last["lat"].values[::3],
    qflux_last["u"].values[::3, ::3],
    qflux_last["v"].values[::3, ::3],
    transform=ccrs.PlateCarree(),
    scale=scale_div,
    color="black",
    pivot="middle",
)
# add quiver key
quiver_key = axes[1, 2].quiverkey(
    last_flux_arrow,
    0.65,
    1.03,
    0.05,
    r"$0.05 g kg^{-1} m s^{-1}$",
    transform=ccrs.PlateCarree(),
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 12},
)

for ax in axes.flatten():
    ax.coastlines()
    # add gidlines at lat every 20 degree, and lon every 60 degree
    ax.gridlines(draw_labels=False, linewidth=0.5, linestyle="dotted")
    ax.set_global()

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")

    axes[0, 0].set_title('(event period)')
    axes[0, 1].set_title('(-5, 0)')
    axes[0, 2].set_title('(-15, -5)')

# draw boxes of NPC and NAL with smoother lines
# NPC [120, 240, 30, 50]
npc_lon = np.linspace(120, 240, 100)
npc_lat_bottom = np.full_like(npc_lon, 30)
npc_lat_top = np.full_like(npc_lon, 50)
npc_lon_left = np.full_like(npc_lat_bottom, 120)
npc_lon_right = np.full_like(npc_lat_bottom, 240)
npc_lat = np.concatenate([npc_lat_bottom, npc_lat_top[::-1], [30]])
npc_lon = np.concatenate([npc_lon, npc_lon[::-1], [120]])
axes[0, 2].plot(
    npc_lon,
    npc_lat,
    transform=ccrs.PlateCarree(),
    color="yellow",
    linewidth=2,
    ls = "--",
)

# NAL [270, 330, 30, 50]
nal_lon = np.linspace(270, 330, 100)
nal_lat_bottom = np.full_like(nal_lon, 30)
nal_lat_top = np.full_like(nal_lon, 50)
nal_lon_left = np.full_like(nal_lat_bottom, 270)
nal_lon_right = np.full_like(nal_lat_bottom, 330)
nal_lat = np.concatenate([nal_lat_bottom, nal_lat_top[::-1], [30]])
nal_lon = np.concatenate([nal_lon, nal_lon[::-1], [270]])
axes[0, 2].plot(
    nal_lon,
    nal_lat,
    transform=ccrs.PlateCarree(),
    color="yellow",
    linewidth=2,
    ls = "--",
)

# add a, b, c
for i, ax in enumerate(axes.flatten()):
    ax.text(
        0.02,
        0.95,
        f"{chr(97+i)}",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
    )

plt.tight_layout()
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/NAO_uhat_upvp_vpetpMPI_GE.pdf", dpi=300, bbox_inches="tight")

# %%
