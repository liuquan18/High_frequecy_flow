# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.path as mpath
import matplotlib.ticker as mticker


from src.dynamics.EP_flux import PlotEPfluxArrows
from src.data_helper import read_composite
from src.plotting.util import erase_white_line, map_smooth, NA_box
import importlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
from src.data_helper.read_variable import read_climatology, read_climatology_decmean
from metpy.units import units
import numpy as np
import os
import cartopy
from matplotlib.patches import Rectangle
from shapely.geometry import Polygon
import metpy.calc as mpcalc
import src.plotting.util as util

importlib.reload(read_composite)
importlib.reload(util)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var
clip_map = util.clip_map
# %%
eke_first = read_climatology("eke", 1850, name="eke", model_dir="MPI_GE_CMIP6")
# %%
eke_last = read_climatology("eke", 2090, name="eke", model_dir="MPI_GE_CMIP6")
# %%
vpetp_first = read_climatology(
    "vpetp", 1850, name="vpetp", model_dir="MPI_GE_CMIP6_allplev"
)
vpetp_last = read_climatology(
    "vpetp", 2090, name="vpetp", model_dir="MPI_GE_CMIP6_allplev"
)
# %%%
# read zg'
zg_first = read_climatology(
    "zg_steady", 1850, name="zg", model_dir="MPI_GE_CMIP6_allplev"
)
zg_last = read_climatology(
    "zg_steady", 2090, name="zg", model_dir="MPI_GE_CMIP6_allplev"
)

# %%
vsets_first = read_climatology(
    "vsets", 1850, name="vsets", model_dir="MPI_GE_CMIP6_allplev"
)
vsets_last = read_climatology(
    "vsets", 2090, name="vsets", model_dir="MPI_GE_CMIP6_allplev"
)


# %%
# Compute weights as cos(lat) in radians
def coslat_weights(ds):
    lat = ds["lat"]
    weights = np.cos(np.deg2rad(lat))
    # Normalize weights so they sum to 1 over the selected latitudes
    return weights / weights.sum()


# For vpetp (lat: 40 to 80)
vpetp_lat_slice = vpetp_first.sel(lat=slice(20, 60)).lat
vpetp_weights = coslat_weights(vpetp_first.sel(lat=slice(20, 60)))
vpetp_first_profile = (
    vpetp_first.sel(lat=slice(20, 60)).weighted(vpetp_weights).mean(dim="lat")
)
vpetp_last_profile = (
    vpetp_last.sel(lat=slice(20, 60)).weighted(vpetp_weights).mean(dim="lat")
)

# For vsets (lat: 40 to 90)
vsets_lat_slice = vsets_first.sel(lat=slice(20, 60)).lat
vsets_weights = coslat_weights(vsets_first.sel(lat=slice(40, 90)))
vsets_first_profile = (
    vsets_first.sel(lat=slice(20, 60)).weighted(vsets_weights).mean(dim="lat")
)
vsets_last_profile = (
    vsets_last.sel(lat=slice(20, 60)).weighted(vsets_weights).mean(dim="lat")
)
# %%
vptp_profile_levels = np.arange(-10, 11, 2)
vsets_profile_levels = np.arange(-10, 11, 2)
#%%
vpetp_levels = np.arange(-20, 21, 5)
vsets_levels = np.arange(-40, 41, 5)

#%%
def shift_longitude(ds):
    """Shift longitude from 0-360 to -180,180."""
    if "lon" in ds.coords:
        ds = ds.assign_coords(lon=(((ds.lon + 180) % 360) - 180))
        ds = ds.sortby("lon")
    return ds


# Shift longitude for profiles
vpetp_first_profile_shifted = shift_longitude(vpetp_first_profile)
vpetp_last_profile_shifted = shift_longitude(vpetp_last_profile)
vsets_first_profile_shifted = shift_longitude(vsets_first_profile)
vsets_last_profile_shifted = shift_longitude(vsets_last_profile)


#%%%
fig = plt.figure(figsize=(12, 12))
map_ax_t = fig.add_subplot(2, 2, 1, projection=ccrs.Orthographic(-40, 80))
map_ax_s = fig.add_subplot(2, 2, 2, projection=ccrs.Orthographic(-40, 80))
erase_white_line(vpetp_first).sel(plev=85000).plot.contourf(
    ax=map_ax_t,
    levels=vpetp_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"$v'\theta'$ ( K m s$^{-1}$)", "shrink": 0.6, "orientation": "horizontal"},
)

erase_white_line(vpetp_last).sel(plev=85000).plot.contour(
    ax=map_ax_t,
    levels=[l for l in vpetp_levels if l != 0],
    colors="k",
    linewidths=1,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

map_ax_t.set_extent([-180, 180, 20, 90], crs=ccrs.PlateCarree())
clip_map(map_ax_t)


# vsets map at 850hPa
cf = erase_white_line(vsets_first).sel(plev=85000).plot.contourf(
    ax=map_ax_s,
    levels=vsets_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={
        "label": r"$v'\theta'$ (m s$^{-1}$)",
        "shrink": 0.6,
        "orientation": "horizontal",
    },
)
erase_white_line(vsets_last).sel(plev=85000).plot.contour(
    ax=map_ax_s,
    levels=[l for l in vsets_levels if l != 0],
    colors="k",
    linewidths=1,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
map_ax_s.set_extent([-180, 180, 20, 90], crs=ccrs.PlateCarree())
clip_map(map_ax_s   )

erase_white_line(vsets_first).sel(plev=85000).plot.contour(
    ax=map_ax_s,
    levels=[-20, 0],
    colors='purple',
    linewidths=2,
    linestyles='dashed',
    transform=ccrs.PlateCarree(),
    zorder=5,
)


erase_white_line(vsets_last).sel(plev=85000).plot.contour(
    ax=map_ax_s,
    levels=[-20, 0],
    colors='red',
    linewidths=2,
    linestyles='dashed',
    zorder=10,
    transform=ccrs.PlateCarree(),
)

profile_ax_t = fig.add_subplot(2, 2, 3)
profile_ax_s = fig.add_subplot(2, 2, 4)


# vpetp
cf1 = vpetp_first_profile_shifted.plot.contourf(
    ax=profile_ax_t,
    levels=vptp_profile_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$v'\theta'$ (K m s$^{-1}$)",
        "shrink": 0.6,
        "orientation": "horizontal",
    },
    extend="both",
)
vpetp_last_profile_shifted.plot.contour(
    ax=profile_ax_t,
    levels=[l for l in vptp_profile_levels if l != 0],
    colors="k",
    linewidths=1,
    add_colorbar=False,
)

# vsets
cf2 = vsets_first_profile_shifted.plot.contourf(
    ax=profile_ax_s,
    levels=vsets_profile_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$v'\theta'$ (m s$^{-1}$)",
        "shrink": 0.6,
        "orientation": "horizontal",
    },    extend="both",
)
vsets_last_profile_shifted.plot.contour(
    ax=profile_ax_s,
    levels=[l for l in vsets_profile_levels if l != 0],
    colors="k",
    linewidths=1,
    add_colorbar=False

)



NA_box(map_ax_s, lon_min=280, lon_max=360)
for ax in [map_ax_t, map_ax_s]:
    ax.set_title("")
    ax.coastlines(color="grey", linewidth=1)
    gl = ax.gridlines(draw_labels=False, linewidth=0.8, color='gray', alpha=0.5, )
    gl.xlocator = mticker.FixedLocator(np.arange(-180, 181, 30))
    gl.ylocator = mticker.FixedLocator(np.arange(20, 91, 20))

for ax in [profile_ax_t, profile_ax_s]:
    ax.set_ylim(100000, 10000)
    ax.set_xlim(-180, 180)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Pressure (Pa)")
    ax.set_xticks(np.arange(-180, 181, 60))

plt.tight_layout()

# add a, b, c
map_ax_t.text(0.1, 0.5, "a", transform=map_ax_t.transAxes, fontsize=16, fontweight="bold")
map_ax_s.text(0.1, 0.5, "b", transform=map_ax_s.transAxes, fontsize=16, fontweight="bold")

profile_ax_t.text(-0.2, 1.0, "c", transform=profile_ax_t.transAxes, fontsize=16, fontweight="bold")
profile_ax_s.text(-0.2, 1.0, "d", transform=profile_ax_s.transAxes, fontsize=16, fontweight="bold")


plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eddy_heat_flux_profile.pdf",
    bbox_inches="tight",
    dpi=300,
    metadata={"Creator": os.path.abspath(__file__)},
)


# %%
eke_levels = np.arange(80, 120, 5)
zg_levels = np.arange(-75, 80, 15)
# %%
fig, axes = plt.subplots(
    1,
    2,
    figsize=(12, 6),
    subplot_kw={"projection": ccrs.Orthographic(-40, 80)},
)

for ax in axes:
    ax.coastlines(color="grey", linewidth=1)
    ax.gridlines()
    ax.set_global()

# Plot vpetp
eke_first.sel(plev=25000).plot.contourf(
    ax=axes[0],
    levels=eke_levels,
    cmap="viridis",
    add_colorbar=True,
    extend="max",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"$eke$ (m$^2$ s$^{-2}$)", "shrink": 0.6},
)

erase_white_line(eke_last).sel(plev=25000).plot.contour(
    ax=axes[0],
    levels=[l for l in eke_levels if l != 0],
    colors="k",
    linewidths=1,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

# plot zg
erase_white_line(zg_first).sel(plev=25000).plot.contourf(
    ax=axes[1],
    levels=zg_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"zg (m)", "shrink": 0.6},
)
erase_white_line(zg_last).sel(plev=25000).plot.contour(
    ax=axes[1],
    levels=[l for l in zg_levels if l != 0],
    colors="k",
    linewidths=1,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
axes[0].set_title("")
axes[1].set_title("")


# add box on lon 280-340, lat 40-80
# Draw a smooth box (polygon) on lon 280-340, lat 40-80

NA_box(axes[1], lon_min=280, lon_max=360, lat_min=40, lat_max=80)


# add a, b
axes[0].text(0.1, 1.0, "a", transform=axes[0].transAxes, fontsize=16, fontweight="bold")
axes[1].text(0.1, 1.0, "b", transform=axes[1].transAxes, fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eke_zg_250hPa.pdf",
            bbox_inches='tight', dpi=300, metadata={
                'Creator': os.path.abspath(__file__)
            }
            )

# %%
div_Tp_first = read_climatology(
    "Fdiv_p_transient", "1850", name="div2", model_dir="MPI_GE_CMIP6_allplev"
)
div_Tp_last = read_climatology(
    "Fdiv_p_transient", "2090", name="div2", model_dir="MPI_GE_CMIP6_allplev"
)


div_Sp_first = read_climatology(
    "Fdiv_p_steady", "1850", name="div2", model_dir="MPI_GE_CMIP6_allplev"
)
div_Sp_last = read_climatology(
    "Fdiv_p_steady", "2090", name="div2", model_dir="MPI_GE_CMIP6_allplev"
)

# %%
# difference of vpetp and vsets on 850hPa
vpetp_diff = vpetp_last.sel(plev=85000) - vpetp_first.sel(plev=85000)
vsets_diff = vsets_last.sel(plev=85000) - vsets_first.sel(plev=85000)
# difference of div_Tp and div_Sp (last - first)
div_Tp_diff = div_Tp_last.sel(plev=85000) - div_Tp_first.sel(plev=85000)
div_Sp_diff = div_Sp_last.sel(plev=85000) - div_Sp_first.sel(plev=85000)


# %%
transient_p = read_climatology_decmean(var="Fdiv_p_transient", NAL=False, plev=85000)

steady_p = read_climatology_decmean(var="Fdiv_p_steady", NAL=False, plev=85000)

# %%

div_Tp_diff = transient_p.isel(time=-1)


# %%
vpetp_diff_levels = np.arange(-5, 6, 1)
vsets_diff_levels = np.arange(-5, 5, 1)

div_Tp_diff_levels = np.arange(-10, 10.1, 2)
div_Sp_diff_levels = np.arange(-20, 20.1, 2)


# %%
fig, axes = plt.subplots(
    3,
    2,
    figsize=(12, 12),
    subplot_kw={"projection": ccrs.Orthographic(-40, 80)},
)

for ax in axes.flat:
    ax.coastlines(color="grey", linewidth=1)
    ax.gridlines()
    ax.set_global()

# eke
# Plot eke difference
eke_diff = erase_white_line(eke_last).sel(plev=25000) - erase_white_line(eke_first).sel(
    plev=25000
)
eke_diff_levels = np.arange(-20, 21, 2)
eke_diff.plot.contourf(
    ax=axes[0, 0],
    levels=eke_diff_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"$\Delta$eke (m$^2$ s$^{-2}$)", "shrink": 0.6},
)

# Plot zg difference
zg_diff = erase_white_line(zg_last).sel(plev=25000) - erase_white_line(zg_first).sel(
    plev=25000
)
zg_diff_levels = np.arange(-40, 41, 5)
zg_diff.plot.contourf(
    ax=axes[0, 1],
    levels=zg_diff_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"$\Delta$zg (m)", "shrink": 0.6},
)


vpetp_diff.plot.contourf(
    ax=axes[1, 0],
    levels=vpetp_diff_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"$\Delta v' \theta'$ (K m s$^{-1}$)", "shrink": 0.6},
)
vsets_diff.plot.contourf(
    ax=axes[1, 1],
    levels=vsets_diff_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"$\Delta v'\theta'$ (m s$^{-1}$)", "shrink": 0.6},
)


div_Tp_diff.plot.contourf(
    ax=axes[2, 0],
    levels=div_Tp_diff_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"$\Delta$div $F_p^{\prime}$ (units)", "shrink": 0.6},
)
div_Sp_diff.plot.contourf(
    ax=axes[2, 1],
    levels=div_Sp_diff_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"$\Delta$div $F_p^{steady}$ (units)", "shrink": 0.6},
)


# %%
fig, axes = plt.subplots(
    3,
    2,
    figsize=(12, 12),
    subplot_kw={"projection": ccrs.Orthographic(-40, 80)},
)

for ax in axes.flat:
    ax.coastlines(color="grey", linewidth=1)
    ax.gridlines()
    ax.set_global()

# first year
transient_p.isel(year=0).div2.plot.contourf(
    ax=axes[0, 0],
    levels=div_Tp_diff_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"$\Delta$div $F_p^{\prime}$ (units)", "shrink": 0.6},
)
steady_p.isel(year=0).div2.plot.contourf(
    ax=axes[0, 1],
    levels=div_Sp_diff_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"$\Delta$div $F_p^{steady}$ (units)", "shrink": 0.6},
)

# last year
transient_p.isel(year=-1).div2.plot.contourf(
    ax=axes[1, 0],
    levels=div_Tp_diff_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"$\Delta$div $F_p^{\prime}$ (units)", "shrink": 0.6},
)

steady_p.isel(year=-1).div2.plot.contourf(
    ax=axes[1, 1],
    levels=div_Sp_diff_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"$\Delta$div $F_p^{steady}$ (units)", "shrink": 0.6},
)

# difference (last - first)
(transient_p.isel(year=-1).div2 - transient_p.isel(year=0).div2).plot.contourf(
    ax=axes[2, 0],
    levels=div_Tp_diff_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"Diff div $F_p^{\prime}$ (units)", "shrink": 0.6},
)
(steady_p.isel(year=-1).div2 - steady_p.isel(year=0).div2).plot.contourf(
    ax=axes[2, 1],
    levels=div_Sp_diff_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"Diff div $F_p^{steady}$ (units)", "shrink": 0.6},
)

# Add a yellow dashed box for sector lat 40-80, lon 300-360 (which is -60 to 0 in -180,180 convention)


def add_sector_box(ax, lat_min=40, lat_max=80, lon_min=300, lon_max=360, **kwargs):
    # Convert lon to -180,180 if needed
    lon_min = ((lon_min + 180) % 360) - 180
    lon_max = ((lon_max + 180) % 360) - 180
    # Rectangle expects lower left corner and width/height
    width = lon_max - lon_min
    height = lat_max - lat_min
    rect = Rectangle(
        (lon_min, lat_min),
        width,
        height,
        linewidth=2,
        edgecolor="yellow",
        facecolor="none",
        linestyle="--",
        zorder=10,
        transform=ccrs.PlateCarree(),
        **kwargs
    )
    ax.add_patch(rect)


for ax in axes.flat:
    clip_map(ax)

# %%
