# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line, map_smooth
from src.plotting.util import lon2x
from matplotlib.ticker import ScalarFormatter
from src.prime.prime_data import vert_integrate


import matplotlib.colors as mcolors
import cartopy
import glob
import matplotlib.ticker as mticker

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# %%
import src.plotting.util as util
import src.moisture.longitudinal_contrast as lc

import importlib

importlib.reload(util)
# %%
from src.prime.prime_data import read_composite_MPI  # noqa: E402
from src.prime.prime_data import read_MPI_GE_uhat
#%%
def to_plot_data(eke):
    # fake data to plot
    eke = eke.rename({"plev": "lat"})  # fake lat to plot correctly the lon
    eke["lat"] = -1*(eke["lat"]/1000 -10)  # fake lat to plot correctly the lon
    # Solve the problem on 180 longitude by extending the data
    return eke

def read_climatology(var, decade, **kwargs):

    name = kwargs.get("name", var)  # default name is the same as var
    if var == "uhat":
        data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/*{decade}*.nc"
    else:
        data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_monthly_ensmean/{var}_monmean_ensmean_{decade}*.nc"

    file = glob.glob(data_path)
    if len(file) == 0:
        raise ValueError(f"no file found for {var} in {decade}")
    data = xr.open_dataset(file[0])
    data = data[name]

    if "time" in data.dims:
        data = data.mean(dim="time")

    return data

#### read ua and va hat

#%%
uhat_first_pos = read_composite_MPI("ua_hat", "ua", 1850, before = "15_5", return_as="pos")
uhat_last_pos = read_composite_MPI("ua_hat", "ua", 2090, before = "15_5", return_as="pos")

uhat_first_neg = read_composite_MPI("ua_hat", "ua", 1850, before = "15_5", return_as="neg")
uhat_last_neg = read_composite_MPI("ua_hat", "ua", 2090, before = "15_5", return_as="neg")
#%%
vhat_first_pos = read_composite_MPI("va_hat", "va", 1850, before = "15_5", return_as="pos")
vhat_last_pos = read_composite_MPI("va_hat", "va", 2090, before = "15_5", return_as="pos")

vhat_first_neg = read_composite_MPI("va_hat", "va", 1850, before = "15_5", return_as="neg")
vhat_last_neg = read_composite_MPI("va_hat", "va", 2090, before = "15_5", return_as="neg")

####### read zg
# wip
#%%

#%%
###### read up vp
# climatology
upvp_first = read_climatology("upvp", "1850", name = "ua")
upvp_last = read_climatology("upvp", "2090", name = "ua")
#%%
# composite
upvp_first_pos = read_composite_MPI("upvp", "upvp", 1850, before = "15_5", return_as="pos")
upvp_last_pos = read_composite_MPI("upvp", "upvp", 2090, before = "15_5", return_as="pos")

upvp_first_neg = read_composite_MPI("upvp", "upvp", 1850, before = "15_5", return_as="neg")
upvp_last_neg = read_composite_MPI("upvp", "upvp", 2090, before = "15_5", return_as="neg")
# diff
upvp_first_diff = read_composite_MPI("upvp", "upvp", 1850, before = "15_5", return_as="diff")
upvp_last_diff = read_composite_MPI("upvp", "upvp", 2090, before = "15_5", return_as="diff")
#%%


# %%
vpetp_first = read_composite_MPI("vpetp", "vpetp", 1850)
vpetp_last = read_composite_MPI("vpetp", "vpetp", 2090)
#%%
vsets_first = read_composite_MPI("vsets", "vsets", 1850)
vsets_last = read_composite_MPI("vsets", "vsets", 2090)
# %%
# smooth the data
vpetp_first = map_smooth(vpetp_first, lon_win=10, lat_win=3)
vpetp_last = map_smooth(vpetp_last, lon_win=10, lat_win=3)
vsets_first = map_smooth(vsets_first, lon_win=10, lat_win=3)
vsets_last = map_smooth(vsets_last, lon_win=10, lat_win=3)

#%%
vpetp_first_low = vpetp_first.sel(plev=85000)
vpetp_last_low = vpetp_last.sel(plev=85000)

vsets_first_low = vsets_first.sel(plev=85000)
vsets_last_low = vsets_last.sel(plev=85000)
#%%
# meridional mean between 30-50N
vpetp_first_profile = vpetp_first.sel(lat=slice(20, 50)).mean(dim="lat")
vpetp_last_profile = vpetp_last.sel(lat=slice(20, 50)).mean(dim="lat")

vsets_first_profile = vsets_first.sel(lat=slice(20, 50)).mean(dim="lat")
vsets_last_profile = vsets_last.sel(lat=slice(20, 50)).mean(dim="lat")

#%%
# fake data to plot
vpetp_first_plot = to_plot_data(vpetp_first_profile)
vpetp_last_plot = to_plot_data(vpetp_last_profile)
vsets_first_plot = to_plot_data(vsets_first_profile)
vsets_last_plot = to_plot_data(vsets_last_profile)

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
#%%%
# steady eddies
vsqs_first = read_composite_MPI("vsqs", "vsqs", 1850)
vsqs_last = read_composite_MPI("vsqs", "vsqs", 2090)

usqs_first = read_composite_MPI("usqs", "usqs", 1850)
usqs_last = read_composite_MPI("usqs", "usqs", 2090)

# integrate qs
usqs_first = vert_integrate(usqs_first)
usqs_last = vert_integrate(usqs_last)
vsqs_first = vert_integrate(vsqs_first)
vsqs_last = vert_integrate(vsqs_last)
# to flux
sflux_first = xr.Dataset({'u': usqs_first*1e3, 'v': vsqs_first*1e3}) #g/kg m/s
sflux_last = xr.Dataset({'u': usqs_last*1e3, 'v': vsqs_last*1e3})
#%%
## climatology
vsets_first_clim = read_climatology("vsets", "1850")
vsets_last_clim = read_climatology("vsets", "2090")
vpetp_first_clim = read_climatology("vpetp", "1850")
vpetp_last_clim = read_climatology("vpetp", "2090")


# smooth the data
vsets_first_clim = map_smooth(vsets_first_clim, lon_win=10, lat_win=3)
vsets_last_clim = map_smooth(vsets_last_clim, lon_win=10, lat_win=3)
vpetp_first_clim = map_smooth(vpetp_first_clim, lon_win=10, lat_win=3)
vpetp_last_clim = map_smooth(vpetp_last_clim, lon_win=10, lat_win=3)

# meridional mean between 20-50N
vsets_first_clim = vsets_first_clim.sel(lat=slice(20, 50)).mean(dim="lat")
vsets_last_clim = vsets_last_clim.sel(lat=slice(20, 50)).mean(dim="lat")
vpetp_first_clim = vpetp_first_clim.sel(lat=slice(20, 50)).mean(dim="lat")
vpetp_last_clim = vpetp_last_clim.sel(lat=slice(20, 50)).mean(dim="lat")

# fake data to plot
vsets_first_clim_plot = to_plot_data(vsets_first_clim)
vsets_last_clim_plot = to_plot_data(vsets_last_clim)
vpetp_first_clim_plot = to_plot_data(vpetp_first_clim)
vpetp_last_clim_plot = to_plot_data(vpetp_last_clim)

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
vsts_levels_div = np.arange(-3, 3.1, 0.5)
vptp_levels_div = np.arange(-1.2, 1.3, 0.2)

scale_div = 1
scale_steady_div = 5
#%%
fig = plt.figure(figsize=(10, 10))
grid = plt.GridSpec(
    nrows = 4,
    ncols = 2,
    height_ratios=[1, 0.5, 1, 0.5],
    width_ratios=[1, 1],
    hspace = -0.5,
)

profile_ax_steady_first = fig.add_subplot(grid[0, 0], projection=ccrs.Mercator(central_longitude=-90))
profile_ax_transient_first = fig.add_subplot(grid[0, 1], projection=ccrs.Mercator(central_longitude=-90))
profile_ax_steady_last = fig.add_subplot(grid[2, 0], projection=ccrs.Mercator(central_longitude=-90))
profile_ax_transient_last = fig.add_subplot(grid[2, 1], projection=ccrs.Mercator(central_longitude=-90))

map_ax_steady_first = fig.add_subplot(grid[1, 0], projection=ccrs.PlateCarree(central_longitude=-90))
map_ax_transient_first = fig.add_subplot(grid[1, 1], projection=ccrs.PlateCarree(central_longitude=-90))
map_ax_steady_last = fig.add_subplot(grid[3, 0], projection=ccrs.PlateCarree(central_longitude=-90))
map_ax_transient_last = fig.add_subplot(grid[3, 1], projection=ccrs.PlateCarree(central_longitude=-90))



# first row first ten years
# first col for steady eddies
vsets_first_plot.plot.contourf(
    ax=profile_ax_steady_first,
    levels=vsts_levels_div,
    cmap="RdBu_r",
    transform=ccrs.PlateCarree(),
    add_colorbar = False
)

vsets_first_clim_plot.plot.contour(
    ax=profile_ax_steady_first,
    levels=np.delete(vsts_levels_div*10, np.where(vsts_levels_div*10 == 0)),
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    add_colorbar = False
)



# second col for transient eddies
vpetp_first_plot.plot.contourf(
    ax=profile_ax_transient_first,
    levels=vptp_levels_div,
    cmap="RdBu_r",
    transform=ccrs.PlateCarree(),
    add_colorbar = False
)

vpetp_first_clim_plot.plot.contour(
    ax=profile_ax_transient_first,
    levels=np.delete(vptp_levels_div*10, np.where(vptp_levels_div*10 == 0)),
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    add_colorbar = False
)


# second row for last ten years
# first col for steady eddies
vsets_last_plot.plot.contourf(
    ax=profile_ax_steady_last,
    levels=vsts_levels_div,
    cmap="RdBu_r",
    transform=ccrs.PlateCarree(),
    add_colorbar = False

)

vsets_last_clim_plot.plot.contour(
    ax=profile_ax_steady_last,
    levels=np.delete(vsts_levels_div*10, np.where(vsts_levels_div*10 == 0)),
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    add_colorbar = False
)


# second col for transient eddies
vpetp_last_plot.plot.contourf(
    ax=profile_ax_transient_last,
    levels=vptp_levels_div,
    cmap="RdBu_r",
    transform=ccrs.PlateCarree(),
    add_colorbar = False
)

vpetp_last_clim_plot.plot.contour(
    ax=profile_ax_transient_last,
    levels=np.delete(vptp_levels_div*10, np.where(vptp_levels_div*10 == 0)),
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    add_colorbar = False
)


###### maps
### steady eddies
vsets_first_low.plot.contourf(
    ax=map_ax_steady_first,
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vsts_levels_div,
    add_colorbar=False,
    extend="both",
    add_label=False,
)
# quiver
steady_first_flux_arrow = map_ax_steady_first.quiver(
    sflux_first["lon"].values[::4],
    sflux_first["lat"].values[::3],
    sflux_first["u"].values[::3, ::4],
    sflux_first["v"].values[::3, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_steady_div,
    color="black",
    pivot="middle",
)
# last
vsets_last_low.plot.contourf(
    ax=map_ax_steady_last,
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vsts_levels_div,
    add_colorbar=True,      
    extend="both",
    cbar_kwargs={
        "label": r"$ v' \theta'_e/ K m s^{-1}$",
        "orientation": "horizontal",
        "pad": 0.2,
        "shrink": 0.8,
        "aspect": 20,
    },
    add_label=False,
)
# quiver
steady_last_flux_arrow = map_ax_steady_last.quiver(
    sflux_last["lon"].values[::4],
    sflux_last["lat"].values[::3],
    sflux_last["u"].values[::3, ::4],
    sflux_last["v"].values[::3, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_steady_div,
    color="black",
    pivot="middle",
)

# add quiver key
quiver_key = map_ax_steady_last.quiverkey(
    steady_last_flux_arrow,
    0.65,
    -1.5,
    0.5,
    r"$0.5 g kg^{-1} m s^{-1}$",
    transform=ccrs.PlateCarree(),
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 12},
)
steady_last_flux_arrow.set_color("yellow")
steady_first_flux_arrow.set_color("yellow")



### transient eddies
vpetp_first_low.plot.contourf(
    ax=map_ax_transient_first,
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    add_colorbar=False,
    extend="both",
    add_label=False,
)

# quiver
transient_first_flux_arrow = map_ax_transient_first.quiver(
    qflux_first["lon"].values[::4],
    qflux_first["lat"].values[::3],
    qflux_first["u"].values[::3, ::4],
    qflux_first["v"].values[::3, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_div,
    color="black",
    pivot="middle",
)

# last
vpetp_last_low.plot.contourf(
    ax=map_ax_transient_last,
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    levels=vptp_levels_div,
    add_colorbar=True,
    extend="both",  
    cbar_kwargs={
        "label": r"$ v' \theta'_e/ K m s^{-1}$",
        "orientation": "horizontal",
        "pad": 0.2,
        "shrink": 0.8,
        "aspect": 20,
    },
    add_label=False,
)
# quiver
transient_last_flux_arrow = map_ax_transient_last.quiver(
    qflux_last["lon"].values[::4],
    qflux_last["lat"].values[::3],
    qflux_last["u"].values[::3, ::4],
    qflux_last["v"].values[::3, ::4],
    transform=ccrs.PlateCarree(),
    scale=scale_div,
    color="black",
    pivot="middle",
)

# add quiver key
quiver_key = map_ax_transient_last.quiverkey(
    transient_last_flux_arrow,
    0.65,
    -1.5,
    0.05,
    r"$0.05 g kg^{-1} m s^{-1}$",
    transform=ccrs.PlateCarree(),
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 12},
)


transient_last_flux_arrow.set_color("yellow")
transient_first_flux_arrow.set_color("yellow")





# FuncFormatter can be used as a decorator
@mticker.FuncFormatter
def major_formatter(x, pos):
    return f"{int((x-10)*-10)}"




for ax in [profile_ax_steady_first, profile_ax_transient_first,
            profile_ax_steady_last, profile_ax_transient_last]:
    ax.set_aspect(1.4)
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
    gl.ylocator = mticker.FixedLocator([-90., -75., -60., -40., -15.])
    gl.yformatter = major_formatter
    gl.xlabels_top = False
    gl.xlabels_bottom = False
    gl.xlocator = mticker.FixedLocator([])


for ax in [map_ax_steady_first, map_ax_transient_first,
            map_ax_steady_last, map_ax_transient_last]:
    ax.coastlines(color="black", linewidth=0.5)  # Light gray with 70% lightness
    # continents light gray
    # add gidlines at lat every 20 degree, and lon every 60 degree
    ax.set_xlim(-180, 180)  # 
    ax.set_ylim(0, 70)  # 
    ax.set_title("")

    # hline at y = 30 and y = 50
    ax.axhline(20, color="gray", linewidth=0.5, linestyle="--")
    ax.axhline(50, color="gray", linewidth=0.5, linestyle="--")



for ax in [map_ax_steady_last, map_ax_transient_last]:

    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        linewidth=0.5,
        linestyle="dotted",
        color="gray",
        alpha=0.5,
        draw_labels=True,)
    

    gl.xlabels_top = False
    gl.xlabels_bottom = False
    gl.xlines = False


    gl.ylabels_right = False
    gl.ylines = False
    gl.ylocator = mticker.FixedLocator([20, 50])
    gl.yformatter = LATITUDE_FORMATTER

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/lon_pressure_eddy_heat.pdf",
    bbox_inches="tight",
    dpi=300,
    transparent=True,
)


# %%
