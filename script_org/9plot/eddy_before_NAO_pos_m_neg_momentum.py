# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line
from src.plotting.util import lon2x
from matplotlib.ticker import ScalarFormatter
from src.prime.prime_data import vert_integrate

import matplotlib.colors as mcolors
import cartopy
import glob

# %%
import src.plotting.util as util
import src.moisture.longitudinal_contrast as lc

import importlib

importlib.reload(util)
# %%
from src.prime.prime_data import read_composite_MPI  # noqa: E402
from src.prime.prime_data import read_MPI_GE_uhat
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

# u'v' 5-0 days before steady eddies
usvs_first = read_composite_MPI("usvs", "usvs", 1850, '5_0') # 5 days before
usvs_last = read_composite_MPI("usvs", "usvs", 2090, '5_0') # 5 days before
if usvs_first.plev.size > 1:
    usvs_first = usvs_first.sel(plev=25000)
    usvs_last = usvs_last.sel(plev=25000)
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

# second column usvs 5-0 days before
usvs_first.plot.contourf(
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

# third column 5-0 days before u'v'
upvp_first.plot.contourf(
    ax=axes[0, 2],
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

# second column usvs 5-0 days before
usvs_last.plot.contourf(
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

# third column 5-0 days before u'v'
upvp_last.plot.contourf(
    ax=axes[1, 2],
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

for ax in axes.flatten():
    ax.coastlines()
    # add gidlines at lat every 20 degree, and lon every 60 degree
    ax.gridlines(draw_labels=False, linewidth=0.5, linestyle="dotted")
    ax.set_global()

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")

    axes[0, 0].set_title("eddy driven jet")
    axes[0, 1].set_title('steady eddies')
    axes[0, 2].set_title('transient eddies')


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
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/NAO_momentum_transient_steady.pdf", dpi=300, bbox_inches="tight")

# %%
