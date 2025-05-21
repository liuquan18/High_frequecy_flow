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
from src.data_helper.read_variable import read_composite_MPI  # noqa: E402
from src.data_helper.read_variable import read_climatology  # noqa: E402


# %%
def to_plot_data(eke):
    # fake data to plot
    eke = eke.rename({"plev": "lat"})  # fake lat to plot correctly the lon
    eke["lat"] = -1 * (eke["lat"] / 1000 - 10)  # fake lat to plot correctly the lon
    # Solve the problem on 180 longitude by extending the data
    return eke

#%%
#### read ua and va hat

ua_first_diff = read_composite_MPI("ua", "ua", 1850, before="10_0", return_as="diff")
ua_last_diff = read_composite_MPI("ua", "ua", 2090, before="10_0", return_as="diff")

va_first_diff = read_composite_MPI("va", "va", 1850, before="10_0", return_as="diff")
va_last_diff = read_composite_MPI("va", "va", 2090, before="10_0", return_as="diff")


wind_flux_first_diff = xr.Dataset({"u": ua_first_diff, "v": va_first_diff})  # m/s
wind_flux_last_diff = xr.Dataset({"u": ua_last_diff, "v": va_last_diff})  # m/s

wind_flux_first_diff = wind_flux_first_diff.sel(plev=25000)
wind_flux_last_diff = wind_flux_last_diff.sel(plev=25000)

#%%
####### theta on 2PVU

theta_pv_first_diff = read_composite_MPI(
    "theta2PVU", "theta2PVU", 1850, before="10_0", return_as="diff", ano = False,
)
theta_pv_last_diff = read_composite_MPI(
    "theta2PVU", "theta2PVU", 2090, before="10_0", return_as="diff", ano = False,
)

# %%
ano = True
# %%
###### read up vp
# climatology
upvp_first = read_climatology("upvp", "1850", name="upvp")
upvp_last = read_climatology("upvp", "2090", name="upvp")
# %%
# diff
upvp_first_diff = read_composite_MPI(
    "upvp", "upvp", 1850, before="10_0", return_as="diff", ano=ano
)
upvp_last_diff = read_composite_MPI(
    "upvp", "upvp", 2090, before="10_0", return_as="diff", ano=ano
)
# %%
####### read heat flux vpetp
# diff
vpetp_first_diff = read_composite_MPI("vpetp", "vpetp", 1850)
vpetp_last_diff = read_composite_MPI("vpetp", "vpetp", 2090)


# smooth the data
vpetp_first_diff = map_smooth(vpetp_first_diff, lon_win=10, lat_win=3)
vpetp_last_diff = map_smooth(vpetp_last_diff, lon_win=10, lat_win=3)

vpetp_first_low = vpetp_first_diff.sel(plev=85000)
vpetp_last_low = vpetp_last_diff.sel(plev=85000)

# meridional mean between 30-50N
vpetp_first_profile = vpetp_first_diff.sel(lat=slice(20, 50)).mean(dim="lat")
vpetp_last_profile = vpetp_last_diff.sel(lat=slice(20, 50)).mean(dim="lat")

# fake data to plot
vpetp_first_plot = to_plot_data(vpetp_first_profile)
vpetp_last_plot = to_plot_data(vpetp_last_profile)

# %%
# climatology
vpetp_first_clim = read_climatology("vpetp", "1850")
vpetp_last_clim = read_climatology("vpetp", "2090")


# smooth the data
vpetp_first_clim = map_smooth(vpetp_first_clim, lon_win=10, lat_win=3)
vpetp_last_clim = map_smooth(vpetp_last_clim, lon_win=10, lat_win=3)

# meridional mean between 20-50N
vpetp_first_clim = vpetp_first_clim.sel(lat=slice(20, 50)).mean(dim="lat")
vpetp_last_clim = vpetp_last_clim.sel(lat=slice(20, 50)).mean(dim="lat")

# fake data to plot
vpetp_first_clim_plot = to_plot_data(vpetp_first_clim)
vpetp_last_clim_plot = to_plot_data(vpetp_last_clim)

# %%
# v'q' -15 - 5 days before

vpqp_first_diff = read_composite_MPI("vpqp", "vptp", 1850)
vpqp_last_diff = read_composite_MPI("vpqp", "vptp", 2090)

upqp_first_diff = read_composite_MPI("upqp", "upqp", 1850)
upqp_last_diff = read_composite_MPI("upqp", "upqp", 2090)

# integrate qp
upqp_first = read_variable.vert_integrate(upqp_first_diff)
upqp_last = read_variable.vert_integrate(upqp_last_diff)

vpqp_first = read_variable.vert_integrate(vpqp_first_diff)
vpqp_last = read_variable.vert_integrate(vpqp_last_diff)

# to flux
qflux_first_diff = xr.Dataset(
    {"u": upqp_first * 1e3, "v": vpqp_first * 1e3}
)  # g/kg m/s
qflux_last_diff = xr.Dataset({"u": upqp_last * 1e3, "v": vpqp_last * 1e3})

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
theta_levels_div = np.arange(-2, 2.1, 0.5)
upvp_levels_div = np.arange(-20, 21, 5)
vsts_levels_div = np.arange(-3, 3.1, 0.5)
vptp_levels_div = np.arange(-1.2, 1.3, 0.2)

scale_hus = 5e4

scale_wind = 60
# %%

fig, axes = plt.subplots(
    4,2, figsize=(10, 10), subplot_kw={"projection": ccrs.PlateCarree(-90)},
    gridspec_kw={"height_ratios": [0.5, 0.5, 1, 0.5], "width_ratios": [1, 1]},
    sharex=True, sharey=False
)
#
# Create a 4x2 grid of axes and assign each to a descriptive variable name
# axes[row, col] corresponds to:
# [0, 0]: map_ax_meanflow_first   - Mean flow map, first period
# [0, 1]: map_ax_meanflow_last    - Mean flow map, last period
# [1, 0]: map_ax_upvp_first       - UpVp map, first period
# [1, 1]: map_ax_upvp_last        - UpVp map, last period
# [2, 0]: profile_ax_upvp_first   - UpVp profile, first period
# [2, 1]: profile_ax_upvp_last    - UpVp profile, last period
# [3, 0]: map_ax_vpetp_first      - VpEtp map, first period
# [3, 1]: map_ax_vpetp_last       - VpEtp map, last period

map_ax_meanflow_first  = axes[0, 0]
map_ax_meanflow_last   = axes[0, 1]
map_ax_upvp_first      = axes[1, 0]
map_ax_upvp_last       = axes[1, 1]
profile_ax_upvp_first  = axes[2, 0]
profile_ax_upvp_last   = axes[2, 1]
map_ax_vpetp_first     = axes[3, 0]
map_ax_vpetp_last      = axes[3, 1]

# theta on 2PVU
theta_pv_first_diff.plot.contourf(
    ax=map_ax_meanflow_first,
    transform=ccrs.PlateCarree(),
    levels=theta_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    extend="both",
)
theta_pv_last_diff.plot.contourf(
    ax=map_ax_meanflow_last,
    transform=ccrs.PlateCarree(),
    levels=theta_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    extend="both",
)


# wind quiver for ua_hat, va_hat
first_wind_arrow = map_ax_meanflow_first.quiver(
    wind_flux_first_diff["lon"].values[::5],
    wind_flux_first_diff["lat"].values[::5],
    wind_flux_first_diff["u"].values[::5, ::5],
    wind_flux_first_diff["v"].values[::5, ::5],
    transform=ccrs.PlateCarree(),
    scale=scale_wind,
)

last_wind_arrow = map_ax_meanflow_last.quiver(
    wind_flux_last_diff["lon"].values[::5],
    wind_flux_last_diff["lat"].values[::5],
    wind_flux_last_diff["u"].values[::5, ::5],
    wind_flux_last_diff["v"].values[::5, ::5],
    transform=ccrs.PlateCarree(),
    scale=scale_wind,
)



# upvp map
upvp_first_diff.sel(plev=25000).plot.contourf(
    ax=map_ax_upvp_first,
    transform=ccrs.PlateCarree(),
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    extend="both",
)
upvp_last_diff.sel(plev=25000).plot.contourf(
    ax=map_ax_upvp_last,
    transform=ccrs.PlateCarree(),
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    extend="both",
)

# vpetp profile
vpetp_first_plot.plot.contourf(
    ax=profile_ax_upvp_first,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    extend="both",
)
vpetp_last_plot.plot.contourf(
    ax=profile_ax_upvp_last,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    extend="both",
)

# contour for climatology of vpetp
vpetp_first_clim_plot.plot.contour(
    ax=profile_ax_upvp_first,
    transform=ccrs.PlateCarree(),
    levels=np.delete(vptp_levels_div*10, np.where(vptp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
)

vpetp_last_clim_plot.plot.contour(
    ax=profile_ax_upvp_last,
    transform=ccrs.PlateCarree(),
    levels=np.delete(vptp_levels_div*10, np.where(vptp_levels_div*10 == 0)),
    add_colorbar=False,
    extend="both",
    colors="black",
)


# vpetp map
vpetp_first_low.plot.contourf(
    ax=map_ax_vpetp_first,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    extend="both",
)
vpetp_last_low.plot.contourf(
    ax=map_ax_vpetp_last,
    transform=ccrs.PlateCarree(),
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    extend="both",
)

# quiver for water vapor flux
first_qflux_arrow = map_ax_vpetp_first.quiver(
    qflux_first_diff["lon"].values[::4],
    qflux_first_diff["lat"].values[::4],
    qflux_first_diff["u"].values[::4, ::4],
    qflux_first_diff["v"].values[::4, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_hus,
)
last_qflux_arrow = map_ax_vpetp_last.quiver(
    qflux_last_diff["lon"].values[::4],
    qflux_last_diff["lat"].values[::4],
    qflux_last_diff["u"].values[::4, ::4],
    qflux_last_diff["v"].values[::4, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_hus,
)


# FuncFormatter can be used as a decorator
@mticker.FuncFormatter
def major_formatter(x, pos):
    return f"{int((x-10)*-10)}"


for ax in [profile_ax_upvp_first, profile_ax_upvp_last]:
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
    map_ax_meanflow_first,
    map_ax_meanflow_last,
    map_ax_upvp_first,
    map_ax_upvp_last,
    map_ax_vpetp_first,
    map_ax_vpetp_last,
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
    map_ax_vpetp_first,
    map_ax_vpetp_last,
]:
    ax.axhline(20, color="gray", linewidth=0.5, linestyle="--")
    ax.axhline(50, color="gray", linewidth=0.5, linestyle="--")
    # add x ticks for longitude
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=2, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.xlabels_bottom = True
    gl.ylabels_left = False
    gl.xlines = False
    gl.ylines = False
    gl.xlocator = mticker.FixedLocator(np.arange(-180, 181, 60))
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER


plt.tight_layout()
# %%
