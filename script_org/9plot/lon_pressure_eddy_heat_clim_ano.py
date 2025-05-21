# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line, map_smooth
from src.plotting.util import lon2x
from matplotlib.ticker import ScalarFormatter
from src.data_helper.read_variable import vert_integrate


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
from src.data_helper.read_variable import read_composite_MPI  # noqa: E402
from src.data_helper.read_variable import read_MPI_GE_uhat
#%%
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

    return erase_white_line(data)

#%%
def read_composite_ano(var, decade, phase, **kwargs):

    name = kwargs.get("name", var)  # default name is the same as var
    before = kwargs.get("before", "5_0")  # default is 5-0 days before
    smooth_value = kwargs.get("smooth_value", 5)  # default is no smoothing
    # u hat is in different path
    if var == 'uhat':
        composite_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/"
        if decade == 1850:
            if phase == 'pos':
                composite_path += "jetstream_MJJAS_first10_pos.nc"
            elif phase == 'neg':
                composite_path += "jetstream_MJJAS_first10_neg.nc"
        elif decade == 2090:
            if phase == 'pos':
                composite_path += "jetstream_MJJAS_last10_pos.nc"
            elif phase == 'neg':
                composite_path += "jetstream_MJJAS_last10_neg.nc"

        composite_ano = xr.open_dataarray(composite_path)

    # 5-0 days 
    else:
        composite_ano = read_composite_MPI(var, name, decade = decade, before = before, return_as = phase, ano = True, smooth_value=smooth_value)

    return composite_ano


#%%
def to_plot_data(eke):
    # fake data to plot
    eke = eke.rename({"plev": "lat"})  # fake lat to plot correctly the lon
    eke["lat"] = -1*(eke["lat"]/1000 -10)  # fake lat to plot correctly the lon
    # Solve the problem on 180 longitude by extending the data
    return eke
#%%

##### climatology

steady_first = read_climatology("vsets", 1850, name = 'vsets')
steady_last = read_climatology("vsets", 2090, name = 'vsets')


transient_first = read_climatology("vpetp", 1850, name = 'vpetp')
transient_last = read_climatology("vpetp", 2090, name = 'vpetp')


#%%
steady_first_pos = read_climatology("vsets", 1850, "pos", name = 'vsets')
steady_last_pos = read_climatology("vsets", 2090, "pos", name = 'vsets')

transient_first_pos = read_climatology("vpetp", 1850, "pos", name = 'vpetp')
transient_last_pos = read_climatology("vpetp", 2090, "pos", name = 'vpetp')

steady_first_neg = read_climatology("vsets", 1850, "neg", name = 'vsets')
steady_last_neg = read_climatology("vsets", 2090, "neg", name = 'vsets')

transient_first_neg = read_climatology("vpetp", 1850, "neg", name = 'vpetp')
transient_last_neg = read_climatology("vpetp", 2090, "neg", name = 'vpetp')
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
vpetp_first_profile = vpetp_first.sel(lat=slice(30, 50)).mean(dim="lat")
vpetp_last_profile = vpetp_last.sel(lat=slice(30, 50)).mean(dim="lat")

vsets_first_profile = vsets_first.sel(lat=slice(30, 50)).mean(dim="lat")
vsets_last_profile = vsets_last.sel(lat=slice(30, 50)).mean(dim="lat")

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

# %%
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
# second col for transient eddies
vpetp_first_plot.plot.contourf(
    ax=profile_ax_transient_first,
    levels=vptp_levels_div,
    cmap="RdBu_r",
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
# second col for transient eddies
vpetp_last_plot.plot.contourf(
    ax=profile_ax_transient_last,
    levels=vptp_levels_div,
    cmap="RdBu_r",
    transform=ccrs.PlateCarree(),
    add_colorbar = False
)


###### maps
### steady eddies


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
    qflux_first["lat"].values[::4],
    qflux_first["u"].values[::4, ::4],
    qflux_first["v"].values[::4, ::4],
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
    -2,
    0.05,
    r"$0.05 g kg^{-1} m s^{-1}$",
    transform=ccrs.PlateCarree(),
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 12},
)


transient_last_flux_arrow.set_color("yellow")





# FuncFormatter can be used as a decorator
@mticker.FuncFormatter
def major_formatter(x, pos):
    return f"{int((x-10)*-10)}"


for ax in [profile_ax_steady_first, profile_ax_steady_last]:
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


for ax in [profile_ax_steady_first, profile_ax_transient_first,
            profile_ax_steady_last, profile_ax_transient_last]:
    ax.set_aspect(1.4)
    ax.set_xticklabels([])


for ax in [map_ax_steady_first, map_ax_transient_first,
            map_ax_steady_last, map_ax_transient_last]:
    ax.coastlines(color="black", linewidth=0.5)  # Light gray with 70% lightness
    # continents light gray
    # add gidlines at lat every 20 degree, and lon every 60 degree
    ax.set_xlim(-180, 180)  # 
    ax.set_ylim(20, 60)  # 
    ax.set_title("")

for ax in [map_ax_steady_last, map_ax_transient_last]:
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        linewidth=0.5,
        linestyle="dotted",
        color="gray",
        alpha=0.5,
        draw_labels=True,)
    

    gl.xlabels_top = False
    gl.xlines = False


    gl.ylabels_right = False
    gl.ylines = False
    gl.ylocator = mticker.FixedLocator([30, 50])
    gl.yformatter = LATITUDE_FORMATTER




# %%
