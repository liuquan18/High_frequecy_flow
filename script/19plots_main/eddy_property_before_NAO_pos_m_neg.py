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
def smooth(arr, lat_window=5, lon_window=5):

    arr = lc.rolling_lon_periodic(arr, lon_window, lat_window, stat="median")
    return arr


# %%
def remove_zonalmean(arr):
    arr = arr - arr.mean(dim="lon")
    return arr


# %%
def postprocess(ds, do_smooth=True, remove_zonal=False):
    if do_smooth:
        ds = smooth(ds)
    if remove_zonal:
        ds = remove_zonalmean(ds)
    ds = erase_white_line(ds)
    return ds


# %%


def read_composite_MPI(var, name, decade, before = '15_5'):
    pos_file = glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_pos_{before}_mean_{decade}.nc"
    )
    neg_file = glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_neg_{before}_mean_{decade}.nc"
    )
    if len(pos_file) == 0 or len(neg_file) == 0:
        raise ValueError(f"no file found for {var} in {decade}")
    NAO_pos = xr.open_dataset(pos_file[0])
    NAO_neg = xr.open_dataset(neg_file[0])
    NAO_pos = NAO_pos[name]
    NAO_neg = NAO_neg[name]

    NAO_pos = NAO_pos.mean(dim="event").squeeze()
    NAO_neg = NAO_neg.mean(dim="event").squeeze()

    NAO_pos = postprocess(NAO_pos)
    NAO_neg = postprocess(NAO_neg)

    diff = NAO_pos - NAO_neg

    return diff.compute()

#%%
def read_composite_ERA5(var, name):
    pos_file=glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results/ERA5_allplev_{var}_NAO_pos_*_mean.nc"
    )
    neg_file=glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results/ERA5_allplev_{var}_NAO_neg_*_mean.nc"
    )
    if len(pos_file) == 0 or len(neg_file) == 0:
        raise ValueError(f"no file found for {var}")
    NAO_pos = xr.open_dataset(pos_file[0])
    NAO_neg = xr.open_dataset(neg_file[0])
    NAO_pos = NAO_pos[name]
    NAO_neg = NAO_neg[name]

    try:
        NAO_pos = NAO_pos.mean(dim="event").squeeze()
        NAO_neg = NAO_neg.mean(dim="event").squeeze()
    except ValueError:
        NAO_pos = NAO_pos.squeeze()
        NAO_neg = NAO_neg.squeeze()


    NAO_pos = postprocess(NAO_pos)
    NAO_neg = postprocess(NAO_neg)

    diff = NAO_pos - NAO_neg

    return diff.compute()
#%%
def read_MPI_GE_uhat():
    uhat_composiste = (
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/"
)
    uhat_pos_first10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_first10_pos.nc")
    uhat_neg_first10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_first10_neg.nc")

    uhat_pos_last10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_last10_pos.nc")
    uhat_neg_last10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_last10_neg.nc")

    uhat_NAO_first = uhat_pos_first10 - uhat_neg_first10
    uhat_NAO_last = uhat_pos_last10 - uhat_neg_last10

    uhat_NAO_first = postprocess(uhat_NAO_first)
    uhat_NAO_last = postprocess(uhat_NAO_last)
    return uhat_NAO_first,uhat_NAO_last

#%%
# u hat
uhat_first, uhat_last = read_MPI_GE_uhat()

#%%
# u'v' 5-0 days before 
upvp_first = read_composite_MPI("upvp", "ua", 1850, '5_0') # 5 days before
upvp_last = read_composite_MPI("upvp", "ua", 2090, '5_0') # 5 days before
#%%
# v't' -15 - 5 days before
vptp_first = read_composite_MPI("vptp", "vptp", 1850)
vptp_last = read_composite_MPI("vptp", "vptp", 2090)
# select v't' at 850 hPa
vptp_first = vptp_first.sel(plev=85000)
vptp_last = vptp_last.sel(plev=85000)
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
vptp_levels_div = np.arange(-1, 1.1, 0.2)

scale_div = 0.5

#%%
fig, axes = plt.subplots(
    2, 3, figsize=(12, 10), subplot_kw={"projection": ccrs.Orthographic(-30, 90)}
)

# first row first ten years
# first column -15 - 5 days before
vptp_first.plot.contourf(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$ v' \theta'/ K m s^{-1}$",
        "orientation": "horizontal",
        "pad": 0.05,
        "shrink": 0.8,
        "aspect": 20,
    },
)

# quiver
first_flux_arrow = axes[0, 0].quiver(
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
quiver_key = axes[0, 0].quiverkey(
    first_flux_arrow,
    0.75,
    0.01,
    0.05,
    r"$0.05 g kg^{-1} m s^{-1}$",
    transform=ccrs.PlateCarree(),
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 12},
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

# third column uhat
uhat_first.plot.contourf(
    ax=axes[0, 2],
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

# second row last ten years
# first column -15 - 5 days before
vptp_last.plot.contourf(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$ v' \theta'/ K m s^{-1}$",
        "orientation": "horizontal",
        "pad": 0.05,
        "shrink": 0.8,
        "aspect": 20,
    },
)

# quiver
last_flux_arrow = axes[1, 0].quiver(
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
quiver_key = axes[1, 0].quiverkey(
    last_flux_arrow,
    0.75,
    0.01,
    0.05,
    r"$0.05 g kg^{-1} m s^{-1}$",
    transform=ccrs.PlateCarree(),
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 12},
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
# third column uhat
uhat_last.plot.contourf(
    ax=axes[1, 2],
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



for ax in axes.flatten():
    ax.coastlines()
    # add gidlines at lat every 20 degree, and lon every 60 degree
    ax.gridlines(draw_labels=False, linewidth=0.5, linestyle="dotted")
    ax.set_global()

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")
    
    axes[0, 0].set_title('(-15, -5)')
    axes[0, 1].set_title('(-5, 0)')
    axes[0, 2].set_title('(event period)')

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
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/NAO_uhat_upvp_vptpMPI_GE.png", dpi=300)

# %%
