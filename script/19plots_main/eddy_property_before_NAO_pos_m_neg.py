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
def postprocess(ds, do_smooth=False, remove_zonal=False):
    if do_smooth:
        ds = smooth(ds)
    if remove_zonal:
        ds = remove_zonalmean(ds)
    ds = erase_white_line(ds)
    return ds


# %%


def read_composite_MPI(var, name, decade):
    pos_file = glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_pos_15_5_mean_{decade}.nc"
    )
    neg_file = glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_neg_15_5_mean_{decade}.nc"
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
def read_NAO_pattern(model):
    if model == 'ERA5':
        eof_path = "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/EOF_result/eof_result_Z500_1979_2024.nc"
        eof = xr.open_dataset(eof_path).eof.sel(mode = 'NAO').squeeze()

    elif model == 'first':
        eof_path = "/work/mh0033/m300883/Tel_MMLE/data/MPI_GE_CMIP6/EOF_result/first_pattern_projected.nc"
        eof = xr.open_dataset(eof_path).__xarray_dataarray_variable__
    elif model == 'last':
        eof_path = "/work/mh0033/m300883/Tel_MMLE/data/MPI_GE_CMIP6/EOF_result/last_pattern_projected.nc"
        eof = xr.open_dataset(eof_path).__xarray_dataarray_variable__

    return eof
#%%
eof_ERA5 = read_NAO_pattern('ERA5')
eof_first = read_NAO_pattern('first')
eof_last = read_NAO_pattern('last')


#%%
upvp_ERA5 = None # not yet generated
upvp_first = read_composite_MPI("vptp", "vptp", 1850)
upvp_last = read_composite_MPI("vptp", "vptp", 2090)
#%%
vptp_ERA5 = None # not yet generated
vptp_first = read_composite_MPI("vptp", "vptp", 1850)
vptp_last = read_composite_MPI("vptp", "vptp", 2090)

#%%
vpqp_ERA5 = None # not yet generated
vpqp_first = read_composite_MPI("vpqp", "vptp", 1850)
vpqp_last = read_composite_MPI("vpqp", "vptp", 2090)
#%%
upqp_ERA5 = None # not yet generated
upqp_first = read_composite_MPI("upqp", "upqp", 1850)
upqp_last = read_composite_MPI("upqp", "upqp", 2090)


#%%
# integrate qp
upqp_first = vert_integrate(upqp_first)
upqp_last = vert_integrate(upqp_last)

vpqp_first = vert_integrate(vpqp_first)
vpqp_last = vert_integrate(vpqp_last)

# select vt at 850 hPa
vptp_first = vptp_first.sel(plev=85000)
vptp_last = vptp_last.sel(plev=85000)

# select upvp at 200 hPa
upvp_first = upvp_first.sel(plev=25000)
upvp_last = upvp_last.sel(plev=25000)
#%%
qflux_first = xr.Dataset({'u': upqp_first, 'v': vpqp_first})
qflux_last = xr.Dataset({'u': upqp_last, 'v': vpqp_last})
# qflux_ERA5 = xr.Dataset({'u': upqp_ERA5, 'v': vpqp_ERA5})

# %%
# ieke_ERA5 = read_composite_ERA5("ieke",'ieke') 
# ieke_first = read_composite_MPI("ieke", "ieke", 1850)
# ieke_last = read_composite_MPI("ieke", "ieke", 2090)
# #%%
# ieke_ERA5 = smooth(ieke_ERA5, lat_window=40, lon_window=80) # smooth the data
# # %%
# ivke_ERA5 = read_composite_ERA5("ivke", "ivke")
# ivke_first = read_composite_MPI("ivke", "ivke", 1850)
# ivke_last = read_composite_MPI("ivke", "ivke", 2090)

# ivke_ERA5 = ivke_ERA5 * 1e6  # kg/kg to g/kg
# ivke_first = ivke_first * 1e6  # kg/kg to g/kg
# ivke_last = ivke_last * 1e6  # kg/kg to g/kg
#%%
qflux_first.isel(lon=slice(None, None, 3), lat=slice(None, None, 3)).plot.quiver(
    x='lon', 
    y='lat', 
    u='u', 
    v='v', 
    scale=0.001,
)

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
zg_levels = np.arange(-30, 31, 5)
uhat_levels_div = np.arange(-12, 13, 2)
upvp_levels_div = np.arange(-2, 2.1, 0.5)
vptp_levels_div = np.arange(-1, 1.1, 0.2)
scale=0.001


#%%
fig, axes = plt.subplots(
    3, 3, figsize=(12, 10), subplot_kw={"projection": ccrs.Orthographic(-30, 90)}
)



# upvp_ERA5.plot.contourf(
#     ax=axes[0, 0],
#     transform=ccrs.PlateCarree(),
#     cmap=temp_cmap_div,
#     levels=upvp_levels_div,
#     extend="both",
#     add_colorbar=False,
# )

upvp_first.plot.contourf(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=upvp_levels_div,
    extend="both",
    add_colorbar=False,
)
upvp_map = upvp_last.plot.contourf(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=upvp_levels_div,
    extend="both",
    add_colorbar=False,
)

# vptp_ERA5.plot.contourf(
#     ax=axes[1, 0],

vptp_first.plot.contourf(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    extend="both",
    add_colorbar=False,
)

vptp_map = vptp_last.plot.contourf(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    extend="both",
    add_colorbar=False,
)

# eof

qflux_first.isel(lon=slice(None, None, 3), lat=slice(None, None, 3)).plot.quiver(
    x='lon', 
    y='lat', 
    u='u', 
    v='v', 
    ax =axes[2, 1],
    transform=ccrs.PlateCarree(),
    scale=scale,
    color='black',

)

qflux_map = qflux_last.isel(lon=slice(None, None, 3), lat=slice(None, None, 3)).plot.quiver(
    x='lon',
    y='lat',
    u='u',
    v='v',
    ax=axes[2, 2],
    transform=ccrs.PlateCarree(),
    scale=scale,
    color='black',
)





for ax in axes.flatten():
    ax.coastlines()
    # add gidlines at lat every 20 degree, and lon every 60 degree
    ax.gridlines(draw_labels=False, linewidth=0.5, linestyle="dotted")
    ax.set_global()

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")



# define four axes at the right of last column to hold the four colorbars
cbar_ax_eof = fig.add_axes([0.92, 0.73, 0.01, 0.2])
cbar_ax_uhat = fig.add_axes([0.92, 0.4, 0.01, 0.2])
cbar_ax_upvp = fig.add_axes([0.92, 0.06, 0.01, 0.2])
# 
# cbar_eof = fig.colorbar(eof_pattern, cax=cbar_ax_eof, orientation="vertical")
# cbar_uhat = fig.colorbar(uhat_map, cax=cbar_ax_uhat, orientation="vertical")
cbar_upvp = fig.colorbar(upvp_map, cax=cbar_ax_upvp, orientation="vertical")


# cbar_eof.set_label(r"$Z500 \, / \, m$")
# cbar_uhat.set_label(r"$\bar{u} \, / \, m \, s^{-1}$")
cbar_upvp.set_label(r"$u'v' \, / \, m^2 \, s^{-2}$")

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

plt.tight_layout(w_pad=-9, h_pad=1)


# %%
