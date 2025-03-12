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

    arr = lc.rolling_lon_periodic(arr, lon_window, lat_window, stat="mean")
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


def read_composite(var, name, decade):
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

    return NAO_pos.compute(), NAO_neg.compute()


# %%
uhat_composiste = (
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/"
)
uhat_pos_first10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_first10_pos.nc")
uhat_neg_first10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_first10_neg.nc")

uhat_pos_last10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_last10_pos.nc")
uhat_neg_last10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_last10_neg.nc")
# %%
uhat_NAO_first = uhat_pos_first10 - uhat_neg_first10
uhat_NAO_last = uhat_pos_last10 - uhat_neg_last10
# %%
uhat_NAO_first = postprocess(uhat_NAO_first)
uhat_NAO_last = postprocess(uhat_NAO_last)

# %%
eke_NAO_pos_first, eke_NAO_neg_first = read_composite("eke", "eke", 1850)
eke_NAO_pos_last, eke_NAO_neg_last = read_composite("eke", "eke", 2090)
# %%
upvp_NAO_pos_first, upvp_NAO_neg_first = read_composite("upvp", "ua", 1850)
upvp_NAO_pos_last, upvp_NAO_neg_last = read_composite("upvp", "ua", 2090)
# %%
ivke_NAO_pos_first, ivke_NAO_neg_first = read_composite("ivke", "ivke", 1850)
ivke_NAO_pos_last, ivke_NAO_neg_last = read_composite("ivke", "ivke", 2090)

# %%
eke_NAO_first = eke_NAO_pos_first - eke_NAO_neg_first
eke_NAO_last = eke_NAO_pos_last - eke_NAO_neg_last

upvp_NAO_first = upvp_NAO_pos_first - upvp_NAO_neg_first
upvp_NAO_last = upvp_NAO_pos_last - upvp_NAO_neg_last

ivke_NAO_first = ivke_NAO_pos_first - ivke_NAO_neg_first
ivke_NAO_last = ivke_NAO_pos_last - ivke_NAO_neg_last
# %%
# change unit from kg/kg to g/kg
ivke_NAO_first = ivke_NAO_first * 1e6  # q^2
ivke_NAO_last = ivke_NAO_last * 1e6  # q^2

##!!!!!!!!!!!!!!!!!##
# divide by g if not yet
# ivke_NAO_first = ivke_NAO_first / 9.81
# ivke_NAO_last = ivke_NAO_last / 9.81

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
eke_levels_div = np.arange(-12, 13, 2)
upvp_levels_div = np.arange(-25, 26, 5)
uhat_levels_div = np.arange(-12, 13, 2)


# %%
fig, axes = plt.subplots(
    3, 3, figsize=(8, 10), subplot_kw={"projection": ccrs.Orthographic(-30, 90)}
)
uhat_NAO_first.plot.contourf(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=uhat_levels_div,
    extend="both",
    add_colorbar=False,
)
uhat_NAO_last.plot.contourf(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=uhat_levels_div,
    extend="both",
    add_colorbar=False,
)
uhat_diff = (uhat_NAO_last - uhat_NAO_first).plot.contourf(
    ax=axes[2, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=uhat_levels_div,
    extend="both",
    add_colorbar=False,
)


# second column for upvp
upvp_NAO_first.plot.contourf(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=upvp_levels_div,
    extend="both",
    add_colorbar=False,
)
upvp_NAO_last.plot.contourf(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=upvp_levels_div,
    extend="both",
    add_colorbar=False,
)
upvp_diff = (upvp_NAO_last - upvp_NAO_first).plot.contourf(
    ax=axes[2, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=upvp_levels_div,
    extend="both",
    add_colorbar=False,
)

# third column for eke
ivke_NAO_first.plot(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap="RdBu_r",
    levels=eke_levels_div,
    extend="both",
    add_colorbar=False,
)
ivke_NAO_last.plot(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap="RdBu_r",
    levels=eke_levels_div,
    extend="both",
    add_colorbar=False,
)
eke_diff = (ivke_NAO_last - ivke_NAO_first).plot(
    ax=axes[2, 2],
    transform=ccrs.PlateCarree(),
    cmap="RdBu_r",
    levels=eke_levels_div,
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

# Define three axes at the bottom to hold the three colorbars
cbar_ax_uhat = fig.add_axes([0.05, 0.06, 0.27, 0.01])
cbar_ax_upvp = fig.add_axes([0.37, 0.06, 0.27, 0.01])
cbar_ax_eke = fig.add_axes([0.69, 0.06, 0.27, 0.01])

cbar_uhat = fig.colorbar(uhat_diff, cax=cbar_ax_uhat, orientation="horizontal")
cbar_upvp = fig.colorbar(upvp_diff, cax=cbar_ax_upvp, orientation="horizontal")
cbar_eke = fig.colorbar(eke_diff, cax=cbar_ax_eke, orientation="horizontal")
cbar_upvp.set_label(r"$m^2/s^2$")
cbar_uhat.set_label(r"$m/s$")
cbar_eke.set_label(r"$m^2/s^2$")

# cbar_eke.formatter = ScalarFormatter()
# cbar_eke.formatter.set_scientific(True)
# cbar_eke.formatter.set_powerlimits((0, 0))

cbar_uhat.set_label(r"$m s^{-1}$")
cbar_upvp.set_label(r"$m^2 s^{-2}$")
cbar_eke.set_label(r"$g^2 kg ^{-2} m^2 s^{-2}$")


# axes[0, 0].set_title(r"$\bar{u}$ during")
# axes[0, 1].set_title(r"$u'v'$ [-5,0] days before")
# axes[0, 2].set_title(r"$[(q'u')^2 + (q'v')^2]/2$ [-15,-5] days before")

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

plt.tight_layout(w_pad=0.5, h_pad=-6)
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/transients_meachnism.pdf", dpi=300)

# %%
