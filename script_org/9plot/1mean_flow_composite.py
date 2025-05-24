# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature

import matplotlib.colors as mcolors
from src.plotting.util import map_smooth
from src.plotting.util import erase_white_line
from matplotlib.colors import ListedColormap
import matplotlib as mpl
import cmocean

# %%
def read_comp_var(var, phase, decade, time_window=(-5, 5), **kwargs):
    name = kwargs.get("name", var)
    method = kwargs.get("method", "mean")
    basedir = (
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_range/"
    )
    file_name = basedir + f"{var}_NAO_{phase}_{decade}.nc"
    ds = xr.open_dataset(file_name)[name]
    ds = ds.sel(time=slice(*time_window))
    if method == "mean":
        ds = ds.mean(dim="time")
    elif method == "sum":
        ds = ds.sum(dim=("time", "ens"))
    return ds



#%%
wb_time_window = (-10, 5)
# %%
uhat_composiste = (
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/"
)
uhat_pos_first10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_first10_pos.nc")
uhat_neg_first10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_first10_neg.nc")

uhat_pos_last10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_last10_pos.nc")
uhat_neg_last10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_last10_neg.nc")

uhat_NAO_diff_first = uhat_pos_first10 - uhat_neg_first10
uhat_NAO_diff_last = uhat_pos_last10 - uhat_neg_last10


# %%
theta_pos_first = read_comp_var(
    "theta_2pvu", "pos", 1850, name="__xarray_dataarray_variable__"
)
theta_pos_last = read_comp_var(
    "theta_2pvu", "pos", 2090, name="__xarray_dataarray_variable__"
)
theta_neg_first = read_comp_var(
    "theta_2pvu", "neg", 1850, name="__xarray_dataarray_variable__"
)
theta_neg_last = read_comp_var(
    "theta_2pvu", "neg", 2090, name="__xarray_dataarray_variable__"
)

theta_diff_first = theta_pos_first - theta_neg_first
theta_diff_last = theta_pos_last - theta_neg_last
# %%
# ua
ua_pos_first = read_comp_var("ua", "pos", 1850, name="ua")
ua_pos_last = read_comp_var("ua", "pos", 2090, name="ua")
ua_neg_first = read_comp_var("ua", "neg", 1850, name="ua")
ua_neg_last = read_comp_var("ua", "neg", 2090, name="ua")

# va
va_pos_first = read_comp_var("va", "pos", 1850, name="va")
va_pos_last = read_comp_var("va", "pos", 2090, name="va")
va_neg_first = read_comp_var("va", "neg", 1850, name="va")
va_neg_last = read_comp_var("va", "neg", 2090, name="va")

# %%
# stratrospheric wb
stra_wb_pos_first = read_comp_var(
    "wb_stratospheric", "pos", 1850, name="flag", time_window=wb_time_window
)
stra_wb_pos_last = read_comp_var(
    "wb_stratospheric", "pos", 2090, name="flag", time_window=wb_time_window
)
stra_wb_neg_first = read_comp_var(
    "wb_stratospheric", "neg", 1850, name="flag", time_window=wb_time_window
)
stra_wb_neg_last = read_comp_var(
    "wb_stratospheric", "neg", 2090, name="flag", time_window=wb_time_window
)

# tropospheric wb
tro_wb_pos_first = read_comp_var(
    "wb_tropospheric", "pos", 1850, name="flag", time_window=wb_time_window
)
tro_wb_pos_last = read_comp_var(
    "wb_tropospheric", "pos", 2090, name="flag", time_window=wb_time_window
)
tro_wb_neg_first = read_comp_var(
    "wb_tropospheric", "neg", 1850, name="flag", time_window=wb_time_window
)
tro_wb_neg_last = read_comp_var(
    "wb_tropospheric", "neg", 2090, name="flag", time_window=wb_time_window
)

# wb diff
stra_wb_diff_first = stra_wb_pos_first - stra_wb_neg_first
stra_wb_diff_last = stra_wb_pos_last - stra_wb_neg_last
tro_wb_diff_first = tro_wb_pos_first - tro_wb_neg_first
tro_wb_diff_last = tro_wb_pos_last - tro_wb_neg_last
# %%
# anticyclonic wb
awb_pos_first = read_comp_var(
    "wb_anticyclonic", "pos", 1850, name="flag", time_window=wb_time_window
)
awb_pos_last = read_comp_var(
    "wb_anticyclonic", "pos", 2090, name="flag", time_window=wb_time_window
)
awb_neg_first = read_comp_var(
    "wb_anticyclonic", "neg", 1850, name="flag", time_window=wb_time_window
)
awb_neg_last = read_comp_var(
    "wb_anticyclonic", "neg", 2090, name="flag", time_window=wb_time_window
)
# cyclonic wb
cwb_pos_first = read_comp_var(
    "wb_cyclonic", "pos", 1850, name="flag", time_window=wb_time_window
)
cwb_pos_last = read_comp_var(
    "wb_cyclonic", "pos", 2090, name="flag", time_window=wb_time_window
)
cwb_neg_first = read_comp_var(
    "wb_cyclonic", "neg", 1850, name="flag", time_window=wb_time_window
)
cwb_neg_last = read_comp_var(
    "wb_cyclonic", "neg", 2090, name="flag", time_window=wb_time_window
)

# diff
awb_diff_first = awb_pos_first - awb_neg_first
cwb_diff_first = cwb_pos_first - cwb_neg_first

awb_diff_last = awb_pos_last - awb_neg_last
cwb_diff_last = cwb_pos_last - cwb_neg_last

# %%
# erase white line for all the datasets
uhat_pos_first10 = erase_white_line(uhat_pos_first10)
uhat_neg_first10 = erase_white_line(uhat_neg_first10)
uhat_pos_last10 = erase_white_line(uhat_pos_last10)
uhat_neg_last10 = erase_white_line(uhat_neg_last10)

uhat_NAO_diff_first = erase_white_line(uhat_NAO_diff_first)
uhat_NAO_diff_last = erase_white_line(uhat_NAO_diff_last)

theta_pos_first = erase_white_line(theta_pos_first)
theta_pos_last = erase_white_line(theta_pos_last)
theta_neg_first = erase_white_line(theta_neg_first)
theta_neg_last = erase_white_line(theta_neg_last)

theta_diff_first = erase_white_line(theta_diff_first)
theta_diff_last = erase_white_line(theta_diff_last)


# %%
ua_pos_first = erase_white_line(ua_pos_first)
ua_pos_last = erase_white_line(ua_pos_last)
ua_neg_first = erase_white_line(ua_neg_first)
ua_neg_last = erase_white_line(ua_neg_last)
va_pos_first = erase_white_line(va_pos_first)
va_pos_last = erase_white_line(va_pos_last)
va_neg_first = erase_white_line(va_neg_first)
va_neg_last = erase_white_line(va_neg_last)
# ua and va to dataset
wnd_pos_first = xr.merge([ua_pos_first, va_pos_first])
wnd_neg_first = xr.merge([ua_neg_first, va_neg_first])
wnd_pos_last = xr.merge([ua_pos_last, va_pos_last])
wnd_neg_last = xr.merge([ua_neg_last, va_neg_last])

wnd_diff_first = wnd_pos_first - wnd_neg_first
wnd_diff_last = wnd_pos_last - wnd_neg_last

# wind select 250hPa
wnd_pos_first = wnd_pos_first.sel(plev=25000)
wnd_neg_first = wnd_neg_first.sel(plev=25000)
wnd_pos_last = wnd_pos_last.sel(plev=25000)
wnd_neg_last = wnd_neg_last.sel(plev=25000)

wnd_diff_first = wnd_diff_first.sel(plev=25000)
wnd_diff_last = wnd_diff_last.sel(plev=25000)


# %%
stra_wb_pos_first = erase_white_line(stra_wb_pos_first)
stra_wb_pos_last = erase_white_line(stra_wb_pos_last)
stra_wb_neg_first = erase_white_line(stra_wb_neg_first)
stra_wb_neg_last = erase_white_line(stra_wb_neg_last)
tro_wb_pos_first = erase_white_line(tro_wb_pos_first)
tro_wb_pos_last = erase_white_line(tro_wb_pos_last)
tro_wb_neg_first = erase_white_line(tro_wb_neg_first)
tro_wb_neg_last = erase_white_line(tro_wb_neg_last)
awb_pos_first = erase_white_line(awb_pos_first)
awb_pos_last = erase_white_line(awb_pos_last)
awb_neg_first = erase_white_line(awb_neg_first)
awb_neg_last = erase_white_line(awb_neg_last)
cwb_pos_first = erase_white_line(cwb_pos_first)
cwb_pos_last = erase_white_line(cwb_pos_last)
cwb_neg_first = erase_white_line(cwb_neg_first)
cwb_neg_last = erase_white_line(cwb_neg_last)
awb_diff_first = erase_white_line(awb_diff_first)
awb_diff_last = erase_white_line(awb_diff_last)
cwb_diff_first = erase_white_line(cwb_diff_first)
cwb_diff_last = erase_white_line(cwb_diff_last)
# %%
# smooth the wb data
stra_wb_pos_first = map_smooth(stra_wb_pos_first, 3, 3)
stra_wb_pos_last = map_smooth(stra_wb_pos_last, 3, 3)
stra_wb_neg_first = map_smooth(stra_wb_neg_first, 3, 3)
stra_wb_neg_last = map_smooth(stra_wb_neg_last, 3, 3)
tro_wb_pos_first = map_smooth(tro_wb_pos_first, 3, 3)
tro_wb_pos_last = map_smooth(tro_wb_pos_last, 3, 3)
tro_wb_neg_first = map_smooth(tro_wb_neg_first, 3, 3)
tro_wb_neg_last = map_smooth(tro_wb_neg_last, 3, 3)
tro_wb_diff_first = map_smooth(tro_wb_diff_first, 3, 3)
tro_wb_diff_last = map_smooth(tro_wb_diff_last, 3, 3)
stra_wb_diff_first = map_smooth(stra_wb_diff_first, 3, 3)
stra_wb_diff_last = map_smooth(stra_wb_diff_last, 3, 3)

# anticyclonic and cyclonic wb
awb_pos_first = map_smooth(awb_pos_first, 3, 3)
awb_pos_last = map_smooth(awb_pos_last, 3, 3)
awb_neg_first = map_smooth(awb_neg_first, 3, 3)
awb_neg_last = map_smooth(awb_neg_last, 3, 3)
cwb_pos_first = map_smooth(cwb_pos_first, 3, 3)
cwb_pos_last = map_smooth(cwb_pos_last, 3, 3)
cwb_neg_first = map_smooth(cwb_neg_first, 3, 3)
cwb_neg_last = map_smooth(cwb_neg_last, 3, 3)

awb_diff_first = map_smooth(awb_diff_first, 3, 3)
awb_diff_last = map_smooth(awb_diff_last, 3, 3)
cwb_diff_first = map_smooth(cwb_diff_first, 3, 3)
cwb_diff_last = map_smooth(cwb_diff_last, 3, 3)
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
prec_cmap_seq = mcolors.ListedColormap(prec_cmap_seq, name="prec_seq")
prec_cmap_div = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_div.txt"
)
prec_cmap_div = mcolors.ListedColormap(prec_cmap_div, name="prec_div")


# %%
uhat_levels_div = np.arange(-12, 13, 2)
temp_levels = np.arange(300, 360, 5)  # K instead of C
temp_levels_div = np.arange(-10, 11, 1)

wb_levels = np.arange(0., 0.05, 0.005)
wb_levels_div = np.arange(-0.02, 0.021, 0.005)

wnd_scale = 150
wnd_scale_div = 150
# %%
# first 10 years, but with anticyclonic and cyclonic wb
# first 10 years
fig, axes = plt.subplots(
    nrows=3,
    ncols=3,
    figsize=(12, 12),
    subplot_kw={"projection": ccrs.Orthographic(-30, 90)},
    constrained_layout=True,
)
# rows for different variables
# columns for pos, neg, diff
# uhat

v = uhat_levels_div
viridis = mpl.colormaps['jet']
my_cmap = ListedColormap(viridis(np.linspace(0,1,len(v))))

uhat_pos_first10 = map_smooth(uhat_pos_first10, 3, 3)
uhat_pos_first10.plot.contourf(
    ax=axes[0, 0],
    levels=uhat_levels_div,
    cmap=my_cmap,
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$\overline{u}$ (m/s)",
        "orientation": "horizontal",
        "shrink": 0.8,
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)

uhat_neg_first10.plot.contourf(
    ax=axes[0, 1],
    levels=uhat_levels_div,
    cmap=my_cmap,
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$\overline{u}$ (m/s)",
        "orientation": "horizontal",
        "shrink": 0.8,
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)

uhat_NAO_diff_first.plot.contourf(
    ax=axes[0, 2],
    levels=uhat_levels_div,
    cmap=my_cmap,
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$\overline{u}$ (m/s)",
        "orientation": "horizontal",
        "shrink": 0.8,
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)

# theta
theta_pos_first.plot.contourf(
    ax=axes[1, 0],
    levels=temp_levels,
    cmap=temp_cmap_div,
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$\overline{\theta}$ (K)",
        "orientation": "horizontal",
        "shrink": 0.8,
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)
theta_neg_first.plot.contourf(
    ax=axes[1, 1],
    levels=temp_levels,
    cmap=temp_cmap_div,
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$\overline{\theta}$ (K)",
        "orientation": "horizontal",
        "shrink": 0.8,
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)
theta_diff_first.plot.contourf(
    ax=axes[1, 2],
    levels=temp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$\overline{\theta}$ (K)",
        "orientation": "horizontal",
        "shrink": 0.8,
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)

# wind quiver
wnd_quiver = axes[1, 0].quiver(
    wnd_pos_first["lon"].values[::5],
    wnd_pos_first.lat[::5],
    wnd_pos_first["ua"].values[::5, ::5],
    wnd_pos_first["va"].values[::5, ::5],
    transform=ccrs.PlateCarree(),
    scale=wnd_scale,
    color="black",
)

# add key for quiver
axes[1, 0].quiverkey(
    wnd_quiver,
    0.9,
    0.03,
    20,
    r"20 m/s",
    labelpos="E",
    transform=axes[1, 0].transAxes,
    coordinates="axes",
)

# wind quiver
wnd_quiver = axes[1, 1].quiver(
    wnd_neg_first["lon"].values[::5],
    wnd_neg_first.lat[::5],
    wnd_neg_first["ua"].values[::5, ::5],
    wnd_neg_first["va"].values[::5, ::5],
    transform=ccrs.PlateCarree(),
    scale=wnd_scale,
    color="black",
)

# wind quiver
wnd_quiver = axes[1, 2].quiver(
    wnd_diff_first["lon"].values[::5],
    wnd_diff_first.lat[::5],
    wnd_diff_first["ua"].values[::5, ::5],
    wnd_diff_first["va"].values[::5, ::5],
    transform=ccrs.PlateCarree(),
    scale=wnd_scale_div,
    color="black",
)
# Mask values between 0 and 0.01 for awb_pos_first and awb_neg_first
awb_pos_first_masked = awb_pos_first.where((awb_pos_first <= 0) | (awb_pos_first >= 0.01))
awb_neg_first_masked = awb_neg_first.where((awb_neg_first <= 0) | (awb_neg_first >= 0.01))

# Create a colormap with a transparent color for the 0-0.01 interval
orig_cmap = cmocean.cm.thermal(np.linspace(0, 1, len(wb_levels)))
cmap_with_transparent = np.array(orig_cmap)
# Find the indices corresponding to 0 and 0.01
zero_idx = np.where(np.isclose(wb_levels, 0))[0][0]
one_idx = np.where(np.isclose(wb_levels, 0.01))[0][0]
cmap_with_transparent[zero_idx:one_idx, -1] = 0  # Set alpha to 0 for 0-0.01
masked_cmap = ListedColormap(cmap_with_transparent)

norm = mpl.colors.BoundaryNorm(wb_levels, masked_cmap.N)

awb_pos_first_masked.plot.contourf(
    ax=axes[2, 0],
    levels=wb_levels,
    cmap=masked_cmap,
    norm=norm,
    add_colorbar=True,
    cbar_kwargs={
        "label": "wave breaking freq",
        "orientation": "horizontal",
        "shrink": 0.8,
        "ticks": wb_levels[::2],
        "format": '%.2f',
    },
    transform=ccrs.PlateCarree(),
    extend="max",
)
cwb_pos_first.plot.contour(
    ax=axes[2, 0],
    levels=wb_levels[2:],
    colors="black",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="max",
)

awb_neg_first_masked.plot.contourf(
    ax=axes[2, 1],
    levels=wb_levels,
    cmap=masked_cmap,
    norm=norm,
    add_colorbar=True,
    cbar_kwargs={
        "label": "wave breaking freq",
        "orientation": "horizontal",
        "shrink": 0.8,
        "ticks": wb_levels[::2],
        "format": '%.2f',
    },
    transform=ccrs.PlateCarree(),
    extend="max",
)
cwb_neg_first.plot.contour(
    ax=axes[2, 1],
    levels=wb_levels[2:], # Skip the first two levels (0 and 0.005)
    colors="black",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="max",
)

#Find the index closest to zero
zero_idx = np.argmin(np.abs(wb_levels_div))

# SGet ticks every 2 steps from center
ticks = np.sort(np.unique(np.concatenate([
    wb_levels_div[zero_idx::-2],   # e.g., [0.0, -0.01, -0.03]
    wb_levels_div[zero_idx::2]     # e.g., [0.0, 0.01, 0.03]
])))


awb_diff_first.plot.contourf(
    ax=axes[2, 2],
    levels=wb_levels_div,  # Use the same levels as before
    cmap="coolwarm",
    add_colorbar=True,
    cbar_kwargs={
        "label": "wave breaking freq",
        "orientation": "horizontal",
        "shrink": 0.8,
        "ticks": ticks,  # Show every two ticks, counting from the center (0)
        "format": '%.2f',
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)


cwb_diff_first.plot.contour(
    ax=axes[2, 2],
    levels=wb_levels_div[wb_levels_div != 0],
    colors="black",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)


# add coastlines and gridlines
for ax in axes[0, :].flatten():
    ax.coastlines(color="grey", linewidth=1)
    # gridlines
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="--",
    )
    # Remove tick marks
    ax.xlocator = None
    ax.ylocator = None

for ax in axes[-1, :]:
    ax.coastlines(color="grey", linewidth=1)
    # gridlines
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="--",
    )
    # Remove tick marks
    ax.xlocator = None
    ax.ylocator = None
    
for ax in axes.flatten():
    ax.set_global()
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0mean_flow/mean_flow_first10.pdf", bbox_inches='tight', dpi = 300)
# %%

# %%
# last 10 years, but with anticyclonic and cyclonic wb
fig, axes = plt.subplots(
    nrows=3,
    ncols=3,
    figsize=(12, 12),
    subplot_kw={"projection": ccrs.Orthographic(-30, 90)},
    constrained_layout=True,
)

v = uhat_levels_div
viridis = mpl.colormaps['jet']
my_cmap = ListedColormap(viridis(np.linspace(0, 1, len(v))))

uhat_pos_last10 = map_smooth(uhat_pos_last10, 3, 3)
uhat_pos_last10.plot.contourf(
    ax=axes[0, 0],
    levels=uhat_levels_div,
    cmap=my_cmap,
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$\overline{u}$ (m/s)",
        "orientation": "horizontal",
        "shrink": 0.8,
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)

uhat_neg_last10.plot.contourf(
    ax=axes[0, 1],
    levels=uhat_levels_div,
    cmap=my_cmap,
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$\overline{u}$ (m/s)",
        "orientation": "horizontal",
        "shrink": 0.8,
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)

uhat_NAO_diff_last.plot.contourf(
    ax=axes[0, 2],
    levels=uhat_levels_div,
    cmap=my_cmap,
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$\overline{u}$ (m/s)",
        "orientation": "horizontal",
        "shrink": 0.8,
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)

# theta
theta_pos_last.plot.contourf(
    ax=axes[1, 0],
    levels=temp_levels,
    cmap=temp_cmap_div,
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$\overline{\theta}$ (K)",
        "orientation": "horizontal",
        "shrink": 0.8,
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)
theta_neg_last.plot.contourf(
    ax=axes[1, 1],
    levels=temp_levels,
    cmap=temp_cmap_div,
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$\overline{\theta}$ (K)",
        "orientation": "horizontal",
        "shrink": 0.8,
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)
theta_diff_last.plot.contourf(
    ax=axes[1, 2],
    levels=temp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=True,
    cbar_kwargs={
        "label": r"$\overline{\theta}$ (K)",
        "orientation": "horizontal",
        "shrink": 0.8,
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)

# wind quiver
wnd_quiver = axes[1, 0].quiver(
    wnd_pos_last["lon"].values[::5],
    wnd_pos_last.lat[::5],
    wnd_pos_last["ua"].values[::5, ::5],
    wnd_pos_last["va"].values[::5, ::5],
    transform=ccrs.PlateCarree(),
    scale=wnd_scale,
    color="black",
)

axes[1, 0].quiverkey(
    wnd_quiver,
    0.9,
    0.03,
    20,
    r"20 m/s",
    labelpos="E",
    transform=axes[1, 0].transAxes,
    coordinates="axes",
)

wnd_quiver = axes[1, 1].quiver(
    wnd_neg_last["lon"].values[::5],
    wnd_neg_last.lat[::5],
    wnd_neg_last["ua"].values[::5, ::5],
    wnd_neg_last["va"].values[::5, ::5],
    transform=ccrs.PlateCarree(),
    scale=wnd_scale,
    color="black",
)

wnd_quiver = axes[1, 2].quiver(
    wnd_diff_last["lon"].values[::5],
    wnd_diff_last.lat[::5],
    wnd_diff_last["ua"].values[::5, ::5],
    wnd_diff_last["va"].values[::5, ::5],
    transform=ccrs.PlateCarree(),
    scale=wnd_scale_div,
    color="black",
)

# Mask values between 0 and 0.01 for awb_pos_last and awb_neg_last
awb_pos_last_masked = awb_pos_last.where((awb_pos_last <= 0) | (awb_pos_last >= 0.01))
awb_neg_last_masked = awb_neg_last.where((awb_neg_last <= 0) | (awb_neg_last >= 0.01))

# Create a colormap with a transparent color for the 0-0.01 interval
orig_cmap = cmocean.cm.thermal(np.linspace(0, 1, len(wb_levels)))
cmap_with_transparent = np.array(orig_cmap)
zero_idx = np.where(np.isclose(wb_levels, 0))[0][0]
one_idx = np.where(np.isclose(wb_levels, 0.01))[0][0]
cmap_with_transparent[zero_idx:one_idx, -1] = 0
masked_cmap = ListedColormap(cmap_with_transparent)
norm = mpl.colors.BoundaryNorm(wb_levels, masked_cmap.N)

awb_pos_last_masked.plot.contourf(
    ax=axes[2, 0],
    levels=wb_levels,
    cmap=masked_cmap,
    norm=norm,
    add_colorbar=True,
    cbar_kwargs={
        "label": "wave breaking freq",
        "orientation": "horizontal",
        "shrink": 0.8,
        "ticks": wb_levels[::2],
        "format": '%.2f',
    },
    transform=ccrs.PlateCarree(),
    extend="max",
)
cwb_pos_last.plot.contour(
    ax=axes[2, 0],
    levels=wb_levels[2:],
    colors="black",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="max",
)

awb_neg_last_masked.plot.contourf(
    ax=axes[2, 1],
    levels=wb_levels,
    cmap=masked_cmap,
    norm=norm,
    add_colorbar=True,
    cbar_kwargs={
        "label": "wave breaking freq",
        "orientation": "horizontal",
        "shrink": 0.8,
        "ticks": wb_levels[::2],
        "format": '%.2f',
    },
    transform=ccrs.PlateCarree(),
    extend="max",
)
cwb_neg_last.plot.contour(
    ax=axes[2, 1],
    levels=wb_levels[2:],
    colors="black",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="max",
)

# Mask values between -0.01 and 0.01 for awb_diff_last and cwb_diff_last
awb_diff_masked = awb_diff_last.where((awb_diff_last <= -0.01) | (awb_diff_last >= 0.01))
cwb_diff_masked = cwb_diff_last.where((cwb_diff_last <= -0.01) | (cwb_diff_last >= 0.01))

orig_cmap = plt.cm.viridis(np.linspace(0, 1, len(wb_levels_div) - 1))
cmap_with_transparent = np.array(orig_cmap)
mask_start = np.where(np.isclose(wb_levels_div[:-1], -0.005))[0][0]
mask_end = np.where(np.isclose(wb_levels_div[1:], 0.005))[0][0] + 1
cmap_with_transparent[mask_start:mask_end, -1] = 0
masked_cmap = ListedColormap(cmap_with_transparent)
norm = mpl.colors.BoundaryNorm(wb_levels_div, ncolors=masked_cmap.N)

awb_diff_masked.plot.contourf(
    ax=axes[2, 2],
    levels=wb_levels_div,
    cmap=masked_cmap,
    norm=norm,
    add_colorbar=True,
    cbar_kwargs={
        "label": "wave breaking freq",
        "orientation": "horizontal",
        "shrink": 0.8,
        "ticks": wb_levels_div[wb_levels_div != 0][::2],
        "format": '%.2f',
        "extend": "both",
    },
    transform=ccrs.PlateCarree(),
    extend="both",
)

cwb_diff_masked.plot.contour(
    ax=axes[2, 2],
    levels=wb_levels_div[wb_levels_div != 0],
    colors="black",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend="both",
)

for ax in axes[0, :].flatten():
    ax.coastlines(color="grey", linewidth=1)
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="--",
    )
    ax.xlocator = None
    ax.ylocator = None

for ax in axes[-1, :]:
    ax.coastlines(color="grey", linewidth=1)
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="--",
    )
    ax.xlocator = None
    ax.ylocator = None

for ax in axes.flatten():
    ax.set_global()

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0mean_flow/mean_flow_last10.pdf", bbox_inches='tight', dpi=300)

# %%
