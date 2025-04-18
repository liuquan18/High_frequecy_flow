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
def read_composite_MPI(var, name, decade, ano = False):
    if ano:
        pos_file = glob.glob(
            f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_pos_15_5_mean_{decade}.nc"
        )
        neg_file = glob.glob(
            f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_neg_15_5_mean_{decade}.nc"
        )
    else:
        pos_file = glob.glob(
            f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results_without_ano/{var}_NAO_pos_15_5_mean_{decade}.nc"
        )
        neg_file = glob.glob(
            f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results_without_ano/{var}_NAO_neg_15_5_mean_{decade}.nc"
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
# heat flux
vptp_pos_first, vptp_neg_first = read_composite_MPI("vptp", "vptp", 1850)
vptp_pos_last, vptp_neg_last = read_composite_MPI("vptp", "vptp", 2090)
# %%
vptp_pos_first = vptp_pos_first.sel(plev=85000)
vptp_neg_first = vptp_neg_first.sel(plev=85000)
vptp_pos_last = vptp_pos_last.sel(plev=85000)
vptp_neg_last = vptp_neg_last.sel(plev=85000)
# %%
upqp_pos_first, upqp_neg_first = read_composite_MPI("upqp", "upqp", 1850)
upqp_pos_last, upqp_neg_last = read_composite_MPI("upqp", "upqp", 2090)
# %%
vpqp_pos_first, vpqp_neg_first = read_composite_MPI(
    "vpqp", "vptp", 1850
)  # the name has not changed
vpqp_pos_last, vpqp_neg_last = read_composite_MPI("vpqp", "vptp", 2090)

# %%
# integrate
upqp_pos_first = vert_integrate(upqp_pos_first)
upqp_neg_first = vert_integrate(upqp_neg_first)
upqp_pos_last = vert_integrate(upqp_pos_last)
upqp_neg_last = vert_integrate(upqp_neg_last)
# %%
vpqp_pos_first = vert_integrate(vpqp_pos_first)
vpqp_neg_first = vert_integrate(vpqp_neg_first)
vpqp_pos_last = vert_integrate(vpqp_pos_last)
vpqp_neg_last = vert_integrate(vpqp_neg_last)
# %%
qflux_pos_first = xr.Dataset(
    {
        "u": upqp_pos_first * 1e3,
        "v": vpqp_pos_first * 1e3,
    }
)

qflux_pos_last = xr.Dataset(
    {
        "u": upqp_pos_last * 1e3,
        "v": vpqp_pos_last * 1e3,
    }
)
qflux_neg_first = xr.Dataset(
    {
        "u": upqp_neg_first * 1e3,
        "v": vpqp_neg_first * 1e3,
    }
)
qflux_neg_last = xr.Dataset(
    {
        "u": upqp_neg_last * 1e3,
        "v": vpqp_neg_last * 1e3,
    }
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
# for anomaly
# upvp_levels_div = np.arange(-2, 2.1, 0.5)
vptp_levels_div = np.arange(-1, 1.1, 0.2)

vptp_levels = np.arange(-10, 11, 2)

scale = 5

scale_div = 0.5


# %%
fig, axes = plt.subplots(
    3, 3, figsize=(12, 10), subplot_kw={"projection": ccrs.Orthographic(-90, 80)}
)

vptp_pos_first.plot.contourf(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels,
    extend="both",
    add_colorbar=False,
)

vptp_pos_map = vptp_pos_last.plot.contourf(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels,
    extend="both",
    add_colorbar=False,
)

# diff
vptp_diff_map = (vptp_pos_last - vptp_pos_first).plot.contourf(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels,
    extend="both",
    add_colorbar=False,
)

# second row for neg
vptp_neg_first.plot.contourf(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels,
    extend="both",
    add_colorbar=False,
)
vptp_neg_map = vptp_neg_last.plot.contourf(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels,
    extend="both",
    add_colorbar=False,
)
# diff
vptp_neg_diff_map = (vptp_neg_last - vptp_neg_first).plot.contourf(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    extend="both",
    add_colorbar=False,
)

# pos neg diff
vptp_phase_map = (vptp_pos_first - vptp_neg_first).plot.contourf(
    ax=axes[2, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    extend="both",
    add_colorbar=False,
)
vptp_phase_map = (vptp_pos_last - vptp_neg_last).plot.contourf(
    ax=axes[2, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    extend="both",
    add_colorbar=False,
)
# diff
((vptp_pos_last - vptp_neg_last) - (vptp_pos_first - vptp_neg_first)).plot.contourf(
    ax=axes[2, 2],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    extend="both",
    add_colorbar=False,
)
## add corresponding quiver
qflux_pos_first.isel(lon=slice(None, None, 3), lat=slice(None, None, 3)).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    scale=scale,
    color="black",
)

qflux_pos_last.isel(lon=slice(None, None, 3), lat=slice(None, None, 3)).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    scale=scale,
    color="black",
)

(qflux_pos_last - qflux_pos_first).isel(
    lon=slice(None, None, 3), lat=slice(None, None, 3)
).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    scale=scale_div,
    color="black",
)
qflux_neg_first.isel(lon=slice(None, None, 3), lat=slice(None, None, 3)).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    scale=scale,
    color="black",
)
qflux_neg_last.isel(lon=slice(None, None, 3), lat=slice(None, None, 3)).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    scale=scale,
    color="black",
)

(qflux_neg_last - qflux_neg_first).isel(
    lon=slice(None, None, 3), lat=slice(None, None, 3)
).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    scale=scale_div,
    color="black",
)
qflux_phase_map = (qflux_pos_first - qflux_neg_first).isel(
    lon=slice(None, None, 3), lat=slice(None, None, 3)
).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[2, 0],
    transform=ccrs.PlateCarree(),
    scale=scale_div,
    color="black",
)
qflux_phase_map = (qflux_pos_last - qflux_neg_last).isel(
    lon=slice(None, None, 3), lat=slice(None, None, 3)
).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[2, 1],
    transform=ccrs.PlateCarree(),
    scale=scale_div,
    color="black",
)
(qflux_pos_last - qflux_pos_first - (qflux_neg_last - qflux_neg_first)).isel(
    lon=slice(None, None, 3), lat=slice(None, None, 3)
).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[2, 2],
    transform=ccrs.PlateCarree(),
    scale=scale_div,
    color="black",
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

# cbar_eof = fig.colorbar(eof_pattern, cax=cbar_ax_eof, orientation="vertical")
# cbar_uhat = fig.colorbar(uhat_map, cax=cbar_ax_uhat, orientation="vertical")
# cbar_upvp = fig.colorbar(upvp_map, cax=cbar_ax_upvp, orientation="vertical")
# cbar_eke = fig.colorbar(ieke_map, cax=cbar_ax_eke, orientation="vertical")
# cbar_vke = fig.colorbar(ivke_map, cax=cbar_ax_vke, orientation="vertical")

# cbar_eof.set_label(r"$Z500 \, / \, m$")
# cbar_uhat.set_label(r"$\bar{u} \, / \, m \, s^{-1}$")
# cbar_upvp.set_label(r"$u'v' \, / \, m^2 \, s^{-2}$")
# cbar_eke.set_label(r"$eke \, / \, m^2 \, s^{-2}$")
# cbar_vke.set_label(r"$q'^2 \, eke \, / \, g^2 \, kg^{-2} \, m^2 \, s^{-2}$")

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
upqp_first_clim = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/upqp_monthly_ensmean/upqp_monmean_ensmean_185005_185909.nc")
upqp_last_clim = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/upqp_monthly_ensmean/upqp_monmean_ensmean_209005_209909.nc")
# %%
vpqp_first_clim = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vpqp_monthly_ensmean/vpqp_monmean_ensmean_185005_185909.nc")
vpqp_last_clim = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vpqp_monthly_ensmean/vpqp_monmean_ensmean_209005_209909.nc")
# %%
upqp_first_clim = upqp_first_clim["upqp"].mean(dim = "time")
upqp_last_clim = upqp_last_clim["upqp"].mean(dim = "time")
vpqp_first_clim = vpqp_first_clim["vptp"].mean(dim = "time") # name not updated
vpqp_last_clim = vpqp_last_clim["vptp"].mean(dim = "time")
# %%
# integrate
upqp_first_clim = vert_integrate(upqp_first_clim)
upqp_last_clim = vert_integrate(upqp_last_clim)
vpqp_first_clim = vert_integrate(vpqp_first_clim)
vpqp_last_clim = vert_integrate(vpqp_last_clim)
# %%
# to flux
qflux_first_clim = xr.Dataset(
    {
        "u": upqp_first_clim * 1e3,
        "v": vpqp_first_clim * 1e3,
    }
)

qflux_last_clim = xr.Dataset(
    {
        "u": upqp_last_clim * 1e3,
        "v": vpqp_last_clim * 1e3,
    }
)
#%%
vptp_first_clim = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vptp_monthly_ensmean/vptp_monmean_ensmean_185005_185909.nc")
vptp_last_clim = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vptp_monthly_ensmean/vptp_monmean_ensmean_209005_209909.nc")
#%%
vptp_first_clim = vptp_first_clim["vptp"].sel(plev=85000).mean(dim = "time")
vptp_last_clim = vptp_last_clim["vptp"].sel(plev=85000).mean(dim = "time")
# %%
fig, axes = plt.subplots(
    2, 3, figsize=(12, 10), subplot_kw={"projection": ccrs.Orthographic(-90, 80)}
)

vptp_first_clim.plot.contourf(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels,
    extend="both",
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$v'\theta '\, / \, K \, m \, s^{-1}$",
        "shrink": 0.8,
        "orientation": "horizontal",}
)

vptp_map = vptp_last_clim.plot.contourf(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels,
    extend="both",
    add_colorbar=True,cbar_kwargs={
        "label": r"$v'\theta '\, / \, K \, m \, s^{-1}$",
        "shrink": 0.8,
        "orientation": "horizontal",}
,
)

# diff
vptp_diff_map = (vptp_last_clim - vptp_first_clim).plot.contourf(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    extend="both",
    add_colorbar=True,cbar_kwargs={
        "label": r"$v'\theta '\, / \, K \, m \, s^{-1}$",
        "shrink": 0.8,
        "orientation": "horizontal",}
,
)

# quiver
ens_quiver = qflux_first_clim.isel(lon=slice(None, None, 3), lat=slice(None, None, 3)).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    scale=scale,
    color="black",
)
qflux_last_clim.isel(lon=slice(None, None, 3), lat=slice(None, None, 3)).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    scale=scale,
    color="black",
)
(qflux_last_clim - qflux_first_clim).isel(
    lon=slice(None, None, 3), lat=slice(None, None, 3)
).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    scale=scale_div,
    color="black",
)


# pos neg diff
vptp_phase_map = (vptp_pos_first - vptp_neg_first).plot.contourf(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    extend="both",
    add_colorbar=True,cbar_kwargs={
        "label": r"$v'\theta '\, / \, K \, m \, s^{-1}$",
        "shrink": 0.8,
        "orientation": "horizontal",}
,
)
vptp_phase_map = (vptp_pos_last - vptp_neg_last).plot.contourf(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    extend="both",
    add_colorbar=True,cbar_kwargs={
        "label": r"$v'\theta '\, / \, K \, m \, s^{-1}$",
        "shrink": 0.8,
        "orientation": "horizontal",}
,
)
# diff
((vptp_pos_last - vptp_neg_last) - (vptp_pos_first - vptp_neg_first)).plot.contourf(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    extend="both",
    add_colorbar=True,cbar_kwargs={
        "label": r"$v'\theta '\, / \, K \, m \, s^{-1}$",
        "shrink": 0.8,
        "orientation": "horizontal",}
,
)
# quiver
qflux_phase_map = (qflux_pos_first - qflux_neg_first).isel(
    lon=slice(None, None, 3), lat=slice(None, None, 3)
).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    scale=scale_div,
    color="black",
)
qflux_phase_map = (qflux_pos_last - qflux_neg_last).isel(
    lon=slice(None, None, 3), lat=slice(None, None, 3)
).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    scale=scale_div,
    color="black",
)
(qflux_pos_last - qflux_pos_first - (qflux_neg_last - qflux_neg_first)).isel(
    lon=slice(None, None, 3), lat=slice(None, None, 3)
).plot.quiver(
    x="lon",
    y="lat",
    u="u",
    v="v",
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    scale=scale_div,
    color="black",
)

# add legend for the quiver
axes[0, 0].quiverkey(
    ens_quiver,
    0.9,
    0.9,
    scale,
    label="5 m/s",
    labelpos="E",
    coordinates="figure",
    color="black",
)

axes[1, 0].quiverkey(
    qflux_phase_map,
    0.9,
    0.9,
    scale_div,
    label="0.5 m/s",
    labelpos="E",
    coordinates="figure",
    color="black",
)



for ax in axes.flatten():
    ax.coastlines()
    # add gidlines at lat every 20 degree, and lon every 60 degree
    ax.gridlines(draw_labels=False, linewidth=0.5, linestyle="dotted")
    ax.set_global()

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")

# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/eddy_flux_before_NAO_pos_or_neg.png", dpi=300, bbox_inches="tight")

# %%
