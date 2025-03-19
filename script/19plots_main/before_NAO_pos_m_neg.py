# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line
from src.plotting.util import lon2x
from matplotlib.ticker import ScalarFormatter

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
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_pos_*_mean_{decade}.nc"
    )
    neg_file = glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_neg_*_mean_{decade}.nc"
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
        f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results/ERA5_ano_{var}_NAO_pos_*_mean.nc"
    )
    neg_file=glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results/ERA5_ano_{var}_NAO_neg_*_mean.nc"
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
uhat_ERA5 = read_composite_ERA5("ua_hat", "var131")
uhat_first, uhat_last = read_MPI_GE_uhat()
#%%
upvp_ERA5 = read_composite_ERA5("upvp", "upvp")
upvp_first = read_composite_MPI("upvp", "ua", 1850)
upvp_last = read_composite_MPI("upvp", "ua", 2090)
#%%
upvp_ERA5 = smooth(upvp_ERA5, lat_window=40, lon_window=80) # smooth the data
# %%
ieke_ERA5 = read_composite_ERA5("ieke",'ieke') 
ieke_first = read_composite_MPI("ieke", "ieke", 1850)
ieke_last = read_composite_MPI("ieke", "ieke", 2090)
# %%
ivke_ERA5 = read_composite_ERA5("ivke", "ivke")
ivke_first = read_composite_MPI("ivke", "ivke", 1850)
ivke_last = read_composite_MPI("ivke", "ivke", 2090)

ivke_ERA5 = ivke_ERA5 * 1e6  # kg/kg to g/kg
ivke_first = ivke_first * 1e6  # kg/kg to g/kg
ivke_last = ivke_last * 1e6  # kg/kg to g/kg


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
vke_levels_div = np.arange(-12, 13, 2)
eke_levels_div = np.arange(-12, 13, 2)
upvp_levels_div = np.arange(-25, 26, 5)
uhat_levels_div = np.arange(-12, 13, 2)



#%%
fig, axes = plt.subplots(
    5, 3, figsize=(11, 15), subplot_kw={"projection": ccrs.Orthographic(-30, 90)}
)

eof_ERA5.plot.contourf(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    levels = zg_levels,
    add_colorbar=False,
    extend="both",
)

eof_first.plot.contourf(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    levels = zg_levels,
    add_colorbar=False,
    extend="both",
)

eof_pattern = eof_last.plot.contourf(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    levels = zg_levels,
    add_colorbar=False,
    extend="both",
)


uhat_ERA5.plot.contourf(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=uhat_levels_div,
    extend="both",
    add_colorbar=False,
)
uhat_first.plot.contourf(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=uhat_levels_div,
    extend="both",
    add_colorbar=False,
)
uhat_map = uhat_last.plot.contourf(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=uhat_levels_div,
    extend="both",
    add_colorbar=False,
)



upvp_ERA5.plot.contourf(
    ax=axes[2, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=upvp_levels_div,
    extend="both",
    add_colorbar=False,
)
upvp_first.plot.contourf(
    ax=axes[2, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=upvp_levels_div,
    extend="both",
    add_colorbar=False,
)
upvp_map = upvp_last.plot.contourf(
    ax=axes[2, 2],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=upvp_levels_div,
    extend="both",
    add_colorbar=False,
)


ieke_ERA5.plot.contourf(
    ax=axes[3, 0],
    transform=ccrs.PlateCarree(),
    cmap="RdBu_r",
    levels=eke_levels_div,
    extend="both",
    add_colorbar=False,
)
ieke_first.plot.contourf(
    ax=axes[3, 1],
    transform=ccrs.PlateCarree(),
    cmap="RdBu_r",
    levels=eke_levels_div,
    extend="both",
    add_colorbar=False,
)
ieke_map = ieke_last.plot.contourf(
    ax=axes[3, 2],
    transform=ccrs.PlateCarree(),
    cmap="RdBu_r",
    levels=eke_levels_div,
    extend="both",
    add_colorbar=False,
)



ivke_ERA5.plot(
    ax=axes[4, 0],
    transform=ccrs.PlateCarree(),
    cmap="RdBu_r",
    levels=vke_levels_div / 2,
    extend="both",
    add_colorbar=False,
)
ivke_first.plot(
    ax=axes[4, 1],
    transform=ccrs.PlateCarree(),
    cmap="RdBu_r",
    levels=vke_levels_div,
    extend="both",
    add_colorbar=False,
)
ivke_map = ivke_last.plot(
    ax=axes[4, 2],
    transform=ccrs.PlateCarree(),
    cmap="RdBu_r",
    levels=vke_levels_div,
    extend="both",
    add_colorbar=False,
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
cbar_ax_eof = fig.add_axes([0.92, 0.80, 0.01, 0.18])
cbar_ax_uhat = fig.add_axes([0.92, 0.60, 0.01, 0.18])
cbar_ax_upvp = fig.add_axes([0.92, 0.40, 0.01, 0.18])
cbar_ax_eke = fig.add_axes([0.92, 0.20, 0.01, 0.18])
cbar_ax_vke = fig.add_axes([0.92, 0.00, 0.01, 0.18])

cbar_eof = fig.colorbar(eof_pattern, cax=cbar_ax_eof, orientation="vertical")
cbar_uhat = fig.colorbar(uhat_map, cax=cbar_ax_uhat, orientation="vertical")
cbar_upvp = fig.colorbar(upvp_map, cax=cbar_ax_upvp, orientation="vertical")
cbar_eke = fig.colorbar(ieke_map, cax=cbar_ax_eke, orientation="vertical")
cbar_vke = fig.colorbar(ivke_map, cax=cbar_ax_vke, orientation="vertical")

cbar_eof.set_label(r"$Z500 \, / \, m$")
cbar_uhat.set_label(r"$\bar{u} \, / \, m \, s^{-1}$")
cbar_upvp.set_label(r"$u'v' \, / \, m^2 \, s^{-2}$")
cbar_eke.set_label(r"$eke \, / \, m^2 \, s^{-2}$")
cbar_vke.set_label(r"$q'^2 \, eke \, / \, g^2 \, kg^{-2} \, m^2 \, s^{-2}$")

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

plt.tight_layout(w_pad=-7, h_pad=1)

# plt.savefig(f"/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/transients_meachnism_{phase}.pdf", dpi=300)

# %%
