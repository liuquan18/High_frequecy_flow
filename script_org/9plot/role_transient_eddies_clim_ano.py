# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line, map_smooth
from src.plotting.util import lon2x
from matplotlib.ticker import ScalarFormatter
import src.plotting.prime_data as prime_data


import matplotlib.colors as mcolors
import cartopy
import glob
import matplotlib.ticker as mticker

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# %%
import src.plotting.util as util

import importlib

importlib.reload(prime_data)
importlib.reload(util)
# %%
from src.plotting.prime_data import read_composite_MPI  # noqa: E402
from src.plotting.prime_data import read_climatology


# %%
def to_plot_data(eke):
    # fake data to plot
    eke = eke.rename({"plev": "lat"})  # fake lat to plot correctly the lon
    eke["lat"] = -1 * (eke["lat"] / 1000 - 10)  # fake lat to plot correctly the lon
    # Solve the problem on 180 longitude by extending the data
    return eke


#%%%
# config
time_window = "6_0"
ano = True
# %%
uhat_levels_div = np.arange(-12, 13, 2)
upvp_levels_div = np.arange(-8, 9, 2)
vsts_levels_div = np.arange(-3, 3.1, 0.5)
vptp_levels_div = np.arange(-1.2, 1.3, 0.2)

scale_hus = 5e4

# %%
###### read upvp
# climatology
upvp_first_clim = read_climatology("upvp", "1850", name="upvp")
upvp_last_clim = read_climatology("upvp", "2090", name="upvp")
# pos ano
upvp_first_pos = read_composite_MPI(
    "upvp", "upvp", 1850, before=time_window, return_as="pos",ano = ano
)
upvp_last_pos = read_composite_MPI(
    "upvp", "upvp", 2090, before=time_window, return_as="pos",ano = ano
)
# neg ano
upvp_first_neg = read_composite_MPI(
    "upvp", "upvp", 1850, before=time_window, return_as="neg",ano = ano
)
upvp_last_neg = read_composite_MPI(
    "upvp", "upvp", 2090, before=time_window, return_as="neg",ano = ano
)
# diff
upvp_first_diff = read_composite_MPI(
    "upvp", "upvp", 1850, before=time_window,ano = ano, return_as="diff"
)
upvp_last_diff = read_composite_MPI(
    "upvp", "upvp", 2090, before=time_window,ano = ano, return_as="diff"
)
# %%
###### read heat flux
# climatology
vpetp_first_clim = read_climatology("vpetp", "1850", name="vpetp")
vpetp_last_clim = read_climatology("vpetp", "2090", name="vpetp")
# pos ano
vpetp_first_pos = read_composite_MPI(
    "vpetp", "vpetp", 1850, before=time_window, return_as="pos",ano = ano, smooth_value=3,
)
vpetp_last_pos = read_composite_MPI(
    "vpetp", "vpetp", 2090, before=time_window, return_as="pos",ano = ano, smooth_value=3,
)
# neg ano
vpetp_first_neg = read_composite_MPI(
    "vpetp", "vpetp", 1850, before=time_window, return_as="neg",ano = ano, smooth_value=3,
)
vpetp_last_neg = read_composite_MPI(
    "vpetp", "vpetp", 2090, before=time_window, return_as="neg",ano = ano, smooth_value=3,
)

vpetp_first_diff = read_composite_MPI(
    "vpetp", "vpetp", 1850, before=time_window,ano = ano, return_as="diff", smooth_value=3,
)
vpetp_last_diff = read_composite_MPI(
    "vpetp", "vpetp", 2090, before=time_window,ano = ano, return_as="diff", smooth_value=3,
)


# # smooth the data
# vpetp_first_clim = map_smooth(vpetp_first_clim, lon_win=10, lat_win=3)
# vpetp_last_clim = map_smooth(vpetp_last_clim, lon_win=10, lat_win=3)

# vpetp_first_pos = map_smooth(vpetp_first_pos, lon_win=10, lat_win=3)
# vpetp_last_pos = map_smooth(vpetp_last_pos, lon_win=10, lat_win=3)

# vpetp_first_neg = map_smooth(vpetp_first_neg, lon_win=10, lat_win=3)
# vpetp_last_neg = map_smooth(vpetp_last_neg, lon_win=10, lat_win=3)

# vpetp_first_diff = map_smooth(vpetp_first_diff, lon_win=10, lat_win=3)
# vpetp_last_diff = map_smooth(vpetp_last_diff, lon_win=10, lat_win=3)

# profile
vpetp_profile_first_clim = vpetp_first_clim.sel(lat=slice(20, 50)).mean(dim="lat")
vpetp_profile_last_clim = vpetp_last_clim.sel(lat=slice(20, 50)).mean(dim="lat")

# pos ano
vpetp_profile_first_pos = vpetp_first_pos.sel(lat=slice(20, 50)).mean(dim="lat")
vpetp_profile_last_pos = vpetp_last_pos.sel(lat=slice(20, 50)).mean(dim="lat")

# neg ano
vpetp_profile_first_neg = vpetp_first_neg.sel(lat=slice(20, 50)).mean(dim="lat")
vpetp_profile_last_neg = vpetp_last_neg.sel(lat=slice(20, 50)).mean(dim="lat")

# diff
vpetp_profile_first_diff = vpetp_first_diff.sel(lat=slice(20, 50)).mean(dim="lat")
vpetp_profile_last_diff = vpetp_last_diff.sel(lat=slice(20, 50)).mean(dim="lat")
# fake data to plot
vpetp_first_clim_plot = to_plot_data(vpetp_profile_first_clim)
vpetp_last_clim_plot = to_plot_data(vpetp_profile_last_clim)
vpetp_first_pos_plot = to_plot_data(vpetp_profile_first_pos)
vpetp_last_pos_plot = to_plot_data(vpetp_profile_last_pos)
vpetp_first_neg_plot = to_plot_data(vpetp_profile_first_neg)
vpetp_last_neg_plot = to_plot_data(vpetp_profile_last_neg)
vpetp_first_diff_plot = to_plot_data(vpetp_profile_first_diff)
vpetp_last_diff_plot = to_plot_data(vpetp_profile_last_diff)

# %%
####### read moisture flux
# climatology
upqp_first_clim = read_climatology("upqp", "1850", name="upqp")
upqp_last_clim = read_climatology("upqp", "2090", name="upqp")

vpqp_first_clim = read_climatology("vpqp", "1850", name="vpqp")
vpqp_last_clim = read_climatology("vpqp", "2090", name="vpqp")

# integrate qp
upqp_first_clim = prime_data.vert_integrate(upqp_first_clim)
upqp_last_clim = prime_data.vert_integrate(upqp_last_clim)
vpqp_first_clim = prime_data.vert_integrate(vpqp_first_clim)
vpqp_last_clim = prime_data.vert_integrate(vpqp_last_clim)

# into flux
qp_first_clim = xr.Dataset(
    {"u": upqp_first_clim * 1e3, "v": vpqp_first_clim * 1e3}
)  # g/kg m/s
qp_last_clim = xr.Dataset(
    {"u": upqp_last_clim * 1e3, "v": vpqp_last_clim * 1e3}
)  # g/kg m/s
# pos ano
upqp_first_pos = read_composite_MPI(
    "upqp", "upqp", 1850, before=time_window, return_as="pos",ano = ano
)
upqp_last_pos = read_composite_MPI(
    "upqp", "upqp", 2090, before=time_window, return_as="pos",ano = ano
)
# neg ano
upqp_first_neg = read_composite_MPI(
    "upqp", "upqp", 1850, before=time_window, return_as="neg",ano = ano
)
upqp_last_neg = read_composite_MPI(
    "upqp", "upqp", 2090, before=time_window, return_as="neg",ano = ano
)

vpqp_first_pos = read_composite_MPI(
    "vpqp", "vpqp", 1850, before=time_window, return_as="pos",ano = ano
)
vpqp_last_pos = read_composite_MPI(
    "vpqp", "vpqp", 2090, before=time_window, return_as="pos",ano = ano
)
# neg ano
vpqp_first_neg = read_composite_MPI(
    "vpqp", "vpqp", 1850, before=time_window, return_as="neg",ano = ano
)
vpqp_last_neg = read_composite_MPI(
    "vpqp", "vpqp", 2090, before=time_window, return_as="neg",ano = ano
)
# integrate qp
upqp_first_pos = prime_data.vert_integrate(upqp_first_pos)
upqp_last_pos = prime_data.vert_integrate(upqp_last_pos)
vpqp_first_pos = prime_data.vert_integrate(vpqp_first_pos)
vpqp_last_pos = prime_data.vert_integrate(vpqp_last_pos)
upqp_first_neg = prime_data.vert_integrate(upqp_first_neg)
upqp_last_neg = prime_data.vert_integrate(upqp_last_neg)
vpqp_first_neg = prime_data.vert_integrate(vpqp_first_neg)
vpqp_last_neg = prime_data.vert_integrate(vpqp_last_neg)


# into flux
qflux_first_pos = xr.Dataset(
    {"u": upqp_first_pos * 1e3, "v": vpqp_first_pos * 1e3}
)  # g/kg m/s
qflux_last_pos = xr.Dataset(
    {"u": upqp_last_pos * 1e3, "v": vpqp_last_pos * 1e3}
)  # g/kg m/s

qflux_first_neg = xr.Dataset(
    {"u": upqp_first_neg * 1e3, "v": vpqp_first_neg * 1e3}
)  # g/kg m/s
qflux_last_neg = xr.Dataset(
    {"u": upqp_last_neg * 1e3, "v": vpqp_last_neg * 1e3}
)  # g/kg m/

qflux_first_diff = qflux_first_pos - qflux_first_neg
qflux_last_diff = qflux_last_pos - qflux_last_neg


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
# first decade
fig, axes = plt.subplots(
    3,
    3,
    figsize=(10, 6),
    subplot_kw={"projection": ccrs.PlateCarree(-90)},
    # gridspec_kw={"height_ratios": [ 0.5, 1, 0.5], "width_ratios": [1, 1]},
    sharex=True,
    sharey=False,
)
#
pos_upvp_ax = axes[0, 0]
neg_upvp_ax = axes[0, 1]
diff_upvp_ax = axes[0, 2]

pos_vptp_profile_ax = axes[1, 0]
neg_vptp_profile_ax = axes[1, 1]
diff_vptp_profile_ax = axes[1, 2]

pos_vptp_map_ax = axes[2, 0]
neg_vptp_map_ax = axes[2, 1]
diff_vptp_map_ax = axes[2, 2]

# map of upvp
# pos
map_upvp = upvp_first_pos.sel(plev=25000).plot.contourf(
    ax=pos_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{u'v'}$ (m$^2$ s$^{-2}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": upvp_levels_div,
    },
)

# climatology as contour
upvp_first_clim.sel(plev=25000).plot.contour(
    ax=pos_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(upvp_levels_div*10, np.where(upvp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
    alpha=0.5,
    zorder=10,
)

# neg
map_upvp = upvp_first_neg.sel(plev=25000).plot.contourf(
    ax=neg_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{u'v'}$ (m$^2$ s$^{-2}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": upvp_levels_div,
    },
)
# climatology as contour
upvp_first_clim.sel(plev=25000).plot.contour(
    ax=neg_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(upvp_levels_div*10, np.where(upvp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
    alpha=0.5,
    zorder=10,
)
# diff
map_upvp = upvp_first_diff.sel(plev=25000).plot.contourf(
    ax=diff_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{u'v'}$ (m$^2$ s$^{-2}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": upvp_levels_div,
    },
)
# climatology as contour
upvp_first_clim.sel(plev=25000).plot.contour(
    ax=diff_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(upvp_levels_div*10, np.where(upvp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
    alpha=0.5,
    zorder=10,
)


# profile of upvp
# pos
profile_upvp = vpetp_first_pos_plot.plot.contourf(
    ax=pos_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": vptp_levels_div[::2][::2],
    },
)
# climatology as contour
vpetp_first_clim_plot.plot.contour(
    ax=pos_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(vptp_levels_div*10, np.where(vptp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
)
# neg
profile_upvp = vpetp_first_neg_plot.plot.contourf(
    ax=neg_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": vptp_levels_div[::2],
    },
)
# climatology as contour
vpetp_first_clim_plot.plot.contour(
    ax=neg_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(vptp_levels_div*10, np.where(vptp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
    zorder=10,
)

# diff
profile_upvp = vpetp_first_diff_plot.plot.contourf(
    ax=diff_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": vptp_levels_div[::2],
    },
)
# climatology as contour
vpetp_first_clim_plot.plot.contour(
    ax=diff_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(vptp_levels_div*10, np.where(vptp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
    zorder=10,
)

# map of vpetp
# pos
map_vpetp = vpetp_last_pos.sel(plev=85000).plot.contourf(
    ax=pos_vptp_map_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.06,
        "aspect": 30,
        "ticks": vptp_levels_div[::2],
    },
)
# quiver of qflux
qflux_arrow = pos_vptp_map_ax.quiver(
    qflux_first_pos.lon.values[::4],
    qflux_first_pos.lat.values[::4],
    qflux_first_pos.u.values[::4, ::4],
    qflux_first_pos.v.values[::4, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_hus,
)

# neg
map_vpetp = vpetp_last_neg.sel(plev=85000).plot.contourf(
    ax=neg_vptp_map_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.06,
        "aspect": 30,
        "ticks": vptp_levels_div[::2],
    },
)
# quiver of qflux
qflux_arrow = neg_vptp_map_ax.quiver(
    qflux_first_neg.lon.values[::4],
    qflux_first_neg.lat.values[::4],
    qflux_first_neg.u.values[::4, ::4],
    qflux_first_neg.v.values[::4, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_hus,
)

# diff
map_vpetp = vpetp_last_diff.sel(plev=85000).plot.contourf(
    ax=diff_vptp_map_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.06,
        "aspect": 30,
        "ticks": vptp_levels_div[::2],
    },
)
# quiver of qflux
qflux_arrow = diff_vptp_map_ax.quiver(
    qflux_first_diff.lon.values[::4],
    qflux_first_diff.lat.values[::4],
    qflux_first_diff.u.values[::4, ::4],
    qflux_first_diff.v.values[::4, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_hus,
)

# FuncFormatter can be used as a decorator
@mticker.FuncFormatter
def major_formatter(x, pos):
    return f"{int((x-10)*-10)}"


for ax in [pos_vptp_profile_ax, neg_vptp_profile_ax, diff_vptp_profile_ax]:
    ax.set_aspect(2)
    ax.set_xticklabels([])
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        linewidth=0.5,
        linestyle="dotted",
        color="gray",
        alpha=0.5,
        draw_labels=True,
    )
    gl.xlines = False
    gl.ylines = False
    gl.ylocator = mticker.FixedLocator([-90.0, -75.0, -60.0, -40.0, -15.0])
    gl.yformatter = major_formatter
    gl.xlabels_top = False
    gl.xlabels_bottom = False
    gl.xlocator = mticker.FixedLocator([])


for ax in [
    pos_upvp_ax,
    neg_upvp_ax,
    diff_upvp_ax,
    pos_vptp_map_ax,
    neg_vptp_map_ax,
    diff_vptp_map_ax,
]:
    # ax.set_aspect(0.8)
    ax.coastlines(color="black", linewidth=0.5)  # Light gray with 70% lightness
    # continents light gray
    # add gidlines at lat every 20 degree, and lon every 60 degree
    ax.set_xlim(-180, 180)  #
    ax.set_ylim(0, 85)  #
    ax.set_title("")

    # hline at y = 30 and y = 50
for ax in [
    pos_vptp_map_ax,
    neg_vptp_map_ax,
    diff_vptp_map_ax,
]:
    ax.axhline(20, color="gray", linewidth=0.5, linestyle="--")
    ax.axhline(50, color="gray", linewidth=0.5, linestyle="--")
    # add x ticks for longitude
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=2,
        color="gray",
        alpha=0.5,
        linestyle="--",
    )
    gl.xlabels_top = False
    gl.xlabels_bottom = True
    gl.ylabels_left = False
    gl.xlines = False
    gl.ylines = False
    gl.xlocator = mticker.FixedLocator(np.arange(-180, 181, 60))
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.ylocator = mticker.FixedLocator([20, 50])


plt.tight_layout()
plt.savefig(f"/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/transient_eddies_{time_window}_clim_ano_first.pdf", dpi=300)
# %%
# last decade
fig, axes = plt.subplots(
    3,
    3,
    figsize=(10, 6),
    subplot_kw={"projection": ccrs.PlateCarree(-90)},
    sharex=True,
    sharey=False,
)
#
pos_upvp_ax = axes[0, 0]
neg_upvp_ax = axes[0, 1]
diff_upvp_ax = axes[0, 2]

pos_vptp_profile_ax = axes[1, 0]
neg_vptp_profile_ax = axes[1, 1]
diff_vptp_profile_ax = axes[1, 2]

pos_vptp_map_ax = axes[2, 0]
neg_vptp_map_ax = axes[2, 1]
diff_vptp_map_ax = axes[2, 2]

# map of upvp
# pos
map_upvp = upvp_last_pos.sel(plev=25000).plot.contourf(
    ax=pos_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{u'v'}$ (m$^2$ s$^{-2}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": upvp_levels_div,
    },
)

# climatology as contour
upvp_last_clim.sel(plev=25000).plot.contour(
    ax=pos_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(upvp_levels_div*10, np.where(upvp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
    alpha=0.5,
    zorder=10,
)

# neg
map_upvp = upvp_last_neg.sel(plev=25000).plot.contourf(
    ax=neg_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{u'v'}$ (m$^2$ s$^{-2}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": upvp_levels_div,
    },
)
# climatology as contour
upvp_last_clim.sel(plev=25000).plot.contour(
    ax=neg_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(upvp_levels_div*10, np.where(upvp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
    alpha=0.5,
    zorder=10,
)
# diff
map_upvp = upvp_last_diff.sel(plev=25000).plot.contourf(
    ax=diff_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{u'v'}$ (m$^2$ s$^{-2}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": upvp_levels_div,
    },
)
# climatology as contour
upvp_last_clim.sel(plev=25000).plot.contour(
    ax=diff_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(upvp_levels_div*10, np.where(upvp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
    alpha=0.5,
    zorder=10,
)


# profile of upvp
# pos
profile_upvp = vpetp_last_pos_plot.plot.contourf(
    ax=pos_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": vptp_levels_div[::2][::2],
    },
)
# climatology as contour
vpetp_last_clim_plot.plot.contour(
    ax=pos_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(vptp_levels_div*10, np.where(vptp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
)
# neg
profile_upvp = vpetp_last_neg_plot.plot.contourf(
    ax=neg_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": vptp_levels_div[::2],
    },
)
# climatology as contour
vpetp_last_clim_plot.plot.contour(
    ax=neg_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(vptp_levels_div*10, np.where(vptp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
    zorder=10,
)

# diff
profile_upvp = vpetp_last_diff_plot.plot.contourf(
    ax=diff_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": vptp_levels_div[::2],
    },
)
# climatology as contour
vpetp_last_clim_plot.plot.contour(
    ax=diff_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(vptp_levels_div*10, np.where(vptp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
    zorder=10,
)

# map of vpetp
# pos
map_vpetp = vpetp_last_pos.sel(plev=85000).plot.contourf(
    ax=pos_vptp_map_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.06,
        "aspect": 30,
        "ticks": vptp_levels_div[::2],
    },
)
# quiver of qflux
qflux_arrow = pos_vptp_map_ax.quiver(
    qflux_last_pos.lon.values[::4],
    qflux_last_pos.lat.values[::4],
    qflux_last_pos.u.values[::4, ::4],
    qflux_last_pos.v.values[::4, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_hus,
)

# neg
map_vpetp = vpetp_last_neg.sel(plev=85000).plot.contourf(
    ax=neg_vptp_map_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.06,
        "aspect": 30,
        "ticks": vptp_levels_div[::2],
    },
)
# quiver of qflux
qflux_arrow = neg_vptp_map_ax.quiver(
    qflux_last_neg.lon.values[::4],
    qflux_last_neg.lat.values[::4],
    qflux_last_neg.u.values[::4, ::4],
    qflux_last_neg.v.values[::4, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_hus,
)

# diff
map_vpetp = vpetp_last_diff.sel(plev=85000).plot.contourf(
    ax=diff_vptp_map_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.06,
        "aspect": 30,
        "ticks": vptp_levels_div[::2],
    },
)
# quiver of qflux
qflux_arrow = diff_vptp_map_ax.quiver(
    qflux_last_diff.lon.values[::4],
    qflux_last_diff.lat.values[::4],
    qflux_last_diff.u.values[::4, ::4],
    qflux_last_diff.v.values[::4, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_hus,
)

# FuncFormatter can be used as a decorator
@mticker.FuncFormatter
def major_formatter(x, pos):
    return f"{int((x-10)*-10)}"


for ax in [pos_vptp_profile_ax, neg_vptp_profile_ax, diff_vptp_profile_ax]:
    ax.set_aspect(2)
    ax.set_xticklabels([])
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        linewidth=0.5,
        linestyle="dotted",
        color="gray",
        alpha=0.5,
        draw_labels=True,
    )
    gl.xlines = False
    gl.ylines = False
    gl.ylocator = mticker.FixedLocator([-90.0, -75.0, -60.0, -40.0, -15.0])
    gl.yformatter = major_formatter
    gl.xlabels_top = False
    gl.xlabels_bottom = False
    gl.xlocator = mticker.FixedLocator([])


for ax in [
    pos_upvp_ax,
    neg_upvp_ax,
    diff_upvp_ax,
    pos_vptp_map_ax,
    neg_vptp_map_ax,
    diff_vptp_map_ax,
]:
    ax.coastlines(color="black", linewidth=0.5)
    ax.set_xlim(-180, 180)
    ax.set_ylim(0, 85)
    ax.set_title("")

for ax in [
    pos_vptp_map_ax,
    neg_vptp_map_ax,
    diff_vptp_map_ax,
]:
    ax.axhline(20, color="gray", linewidth=0.5, linestyle="--")
    ax.axhline(50, color="gray", linewidth=0.5, linestyle="--")
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=2,
        color="gray",
        alpha=0.5,
        linestyle="--",
    )
    gl.xlabels_top = False
    gl.xlabels_bottom = True
    gl.ylabels_left = False
    gl.xlines = False
    gl.ylines = False
    gl.xlocator = mticker.FixedLocator(np.arange(-180, 181, 60))
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.ylocator = mticker.FixedLocator([20, 50])

plt.tight_layout()
plt.savefig(f"/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/transient_eddies_{time_window}_clim_ano_last.pdf", dpi=300)
# %%
# a new plot, the first column shows the difference between pos and neg in the first decade,
# the second column shows the difference between pos and neg in the last decade
fig, axes = plt.subplots(
    3,
    2,
    figsize=(10, 10),
    subplot_kw={"projection": ccrs.PlateCarree(-90)},
    sharex=True,
    sharey=False,
)

first_upvp_ax = axes[0, 0]
last_upvp_ax = axes[0, 1]

first_vptp_profile_ax = axes[1, 0]
last_vptp_profile_ax = axes[1, 1]

first_vptp_map_ax = axes[2, 0]
last_vptp_map_ax = axes[2, 1]

# map of upvp
# first diff
map_upvp = upvp_first_diff.sel(plev=25000).plot.contourf(
    ax=first_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{u'v'}$ (m$^2$ s$^{-2}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": upvp_levels_div,
    },
)

# climatology as contour
upvp_first_clim.sel(plev=25000).plot.contour(
    ax=first_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(upvp_levels_div*10, np.where(upvp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
    alpha=0.5,
    zorder=10,
)

# last diff
map_upvp = upvp_last_diff.sel(plev=25000).plot.contourf(
    ax=last_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{u'v'}$ (m$^2$ s$^{-2}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": upvp_levels_div,
    },
)
# climatology as contour
upvp_last_clim.sel(plev=25000).plot.contour(
    ax=last_upvp_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(upvp_levels_div*10, np.where(upvp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
    alpha=0.5,
    zorder=10,
)

# profile of vpetp
# first diff
profile_upvp = vpetp_first_diff_plot.plot.contourf(
    ax=first_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": vptp_levels_div[::2][::2],
    },
)

# climatology as contour
vpetp_first_clim_plot.plot.contour(
    ax=first_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(vptp_levels_div*10, np.where(vptp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
)

# last diff
profile_upvp = vpetp_last_diff_plot.plot.contourf(
    ax=last_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.05,
        "aspect": 30,
        "ticks": vptp_levels_div[::2],
    },
)
# climatology as contour
vpetp_last_clim_plot.plot.contour(
    ax=last_vptp_profile_ax,
    transform=ccrs.PlateCarree(),
    levels=np.delete(vptp_levels_div*10, np.where(vptp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
    linewidths=0.5,
    linestyles="solid",
    zorder=10,
)

# map of vpetp
# first diff
map_vpetp = vpetp_first_diff.sel(plev=85000).plot.contourf(
    ax=first_vptp_map_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.06,
        "aspect": 30,
        "ticks": vptp_levels_div[::2],
    },
)
# quiver of qflux
qflux_arrow = first_vptp_map_ax.quiver(
    qflux_first_diff.lon.values[::4],
    qflux_first_diff.lat.values[::4],
    qflux_first_diff.u.values[::4, ::4],
    qflux_first_diff.v.values[::4, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_hus,
)

# last diff
map_vpetp = vpetp_last_diff.sel(plev=85000).plot.contourf(
    ax=last_vptp_map_ax,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    extend="both",
    cbar_kwargs={
        "label": r"$\overline{v'\theta'}$ (K m s$^{-1}$)",
        "orientation": "horizontal",
        "pad": 0.06,
        "aspect": 30,
        "ticks": vptp_levels_div[::2],
    },
)
# quiver of qflux
qflux_arrow = last_vptp_map_ax.quiver(
    qflux_last_diff.lon.values[::4],
    qflux_last_diff.lat.values[::4],
    qflux_last_diff.u.values[::4, ::4],
    qflux_last_diff.v.values[::4, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_hus,
)

# FuncFormatter can be used as a decorator
@mticker.FuncFormatter
def major_formatter(x, pos):
    return f"{int((x-10)*-10)}"
for ax in [first_vptp_profile_ax, last_vptp_profile_ax]:
    ax.set_aspect(2)
    ax.set_xticklabels([])
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        linewidth=0.5,
        linestyle="dotted",
        color="gray",
        alpha=0.5,
        draw_labels=True,
    )
    gl.xlines = False
    gl.ylines = False
    gl.ylocator = mticker.FixedLocator([-90.0, -75.0, -60.0, -40.0, -15.0])
    gl.yformatter = major_formatter
    gl.xlabels_top = False
    gl.xlabels_bottom = False
    gl.xlocator = mticker.FixedLocator([])

for ax in [
    first_upvp_ax,
    last_upvp_ax,
    first_vptp_map_ax,
    last_vptp_map_ax,
]:
    ax.coastlines(color="black", linewidth=0.5)
    ax.set_xlim(-180, 180)
    ax.set_ylim(0, 85)
    ax.set_title("")
for ax in [
    first_vptp_map_ax,
    last_vptp_map_ax,
]:
    ax.axhline(20, color="gray", linewidth=0.5, linestyle="--")
    ax.axhline(50, color="gray", linewidth=0.5, linestyle="--")
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=2,
        color="gray",
        alpha=0.5,
        linestyle="--",
    )
    gl.xlabels_top = False
    gl.xlabels_bottom = True
    gl.ylabels_left = False
    gl.xlines = False
    gl.ylines = False
    gl.xlocator = mticker.FixedLocator(np.arange(-180, 181, 60))
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.ylocator = mticker.FixedLocator([20, 50])
plt.tight_layout()
plt.savefig(f"/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/transient_eddies_{time_window}_clim_ano_diff.pdf", dpi=300, bbox_inches='tight')
# %%
