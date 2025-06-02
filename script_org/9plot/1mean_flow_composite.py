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
from src.data_helper.read_composite import read_comp_var


#%%
wb_time_window = (-10, 5)
theta_time_window = (-5, 5)
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
    "theta_2pvu", "pos", 1850, name="__xarray_dataarray_variable__",
    time_window=theta_time_window, method='mean'
)
theta_pos_last = read_comp_var(
    "theta_2pvu", "pos", 2090, name="__xarray_dataarray_variable__",
    time_window=theta_time_window, method='mean'
)
theta_neg_first = read_comp_var(
    "theta_2pvu", "neg", 1850, name="__xarray_dataarray_variable__",
    time_window=theta_time_window, method='mean'
)
theta_neg_last = read_comp_var(
    "theta_2pvu", "neg", 2090, name="__xarray_dataarray_variable__",
    time_window=theta_time_window, method='mean'
)

theta_diff_first = theta_pos_first - theta_neg_first
theta_diff_last = theta_pos_last - theta_neg_last
# %%
# ua
ua_pos_first = read_comp_var("ua", "pos", 1850, name="ua", time_window=theta_time_window)
ua_pos_last = read_comp_var("ua", "pos", 2090, name="ua", time_window=theta_time_window)
ua_neg_first = read_comp_var("ua", "neg", 1850, name="ua", time_window=theta_time_window)
ua_neg_last = read_comp_var("ua", "neg", 2090, name="ua" , time_window=theta_time_window)

# va
va_pos_first = read_comp_var("va", "pos", 1850, name="va", time_window=theta_time_window)
va_pos_last = read_comp_var("va", "pos", 2090, name="va", time_window=theta_time_window)
va_neg_first = read_comp_var("va", "neg", 1850, name="va", time_window=theta_time_window)
va_neg_last = read_comp_var("va", "neg", 2090, name="va", time_window=theta_time_window)

# %%
# stratrospheric wb
stra_wb_pos_first = read_comp_var(
    "wb_stratospheric", "pos", 1850, name="flag", time_window=wb_time_window, method = 'sum'
)
stra_wb_pos_last = read_comp_var(
    "wb_stratospheric", "pos", 2090, name="flag", time_window=wb_time_window, method = 'sum'
)
stra_wb_neg_first = read_comp_var(
    "wb_stratospheric", "neg", 1850, name="flag", time_window=wb_time_window, method = 'sum'
)
stra_wb_neg_last = read_comp_var(
    "wb_stratospheric", "neg", 2090, name="flag", time_window=wb_time_window, method = 'sum'
)

# tropospheric wb
tro_wb_pos_first = read_comp_var(
    "wb_tropospheric", "pos", 1850, name="flag", time_window=wb_time_window, method = 'sum'
)
tro_wb_pos_last = read_comp_var(
    "wb_tropospheric", "pos", 2090, name="flag", time_window=wb_time_window, method = 'sum'
)
tro_wb_neg_first = read_comp_var(
    "wb_tropospheric", "neg", 1850, name="flag", time_window=wb_time_window, method = 'sum'
)
tro_wb_neg_last = read_comp_var(
    "wb_tropospheric", "neg", 2090, name="flag", time_window=wb_time_window, method = 'sum'
)

# wb diff
stra_wb_diff_first = stra_wb_pos_first - stra_wb_neg_first
stra_wb_diff_last = stra_wb_pos_last - stra_wb_neg_last
tro_wb_diff_first = tro_wb_pos_first - tro_wb_neg_first
tro_wb_diff_last = tro_wb_pos_last - tro_wb_neg_last
# %%
# anticyclonic wb
awb_pos_first = read_comp_var(
    "wb_anticyclonic", "pos", 1850, name="flag", time_window=wb_time_window, method = 'sum'
)
awb_pos_last = read_comp_var(
    "wb_anticyclonic", "pos", 2090, name="flag", time_window=wb_time_window, method = 'sum'
)
awb_neg_first = read_comp_var(
    "wb_anticyclonic", "neg", 1850, name="flag", time_window=wb_time_window, method = 'sum'
)
awb_neg_last = read_comp_var(
    "wb_anticyclonic", "neg", 2090, name="flag", time_window=wb_time_window, method = 'sum'
)
# cyclonic wb
cwb_pos_first = read_comp_var(
    "wb_cyclonic", "pos", 1850, name="flag", time_window=wb_time_window, method = 'sum'
)
cwb_pos_last = read_comp_var(
    "wb_cyclonic", "pos", 2090, name="flag", time_window=wb_time_window, method = 'sum'
)
cwb_neg_first = read_comp_var(
    "wb_cyclonic", "neg", 1850, name="flag", time_window=wb_time_window, method = 'sum'
)
cwb_neg_last = read_comp_var(
    "wb_cyclonic", "neg", 2090, name="flag", time_window=wb_time_window, method = 'sum'
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
uhat_levels_div = np.arange(-15, 16, 3)
temp_levels = np.arange(300, 360, 5)  # K instead of C
temp_levels_div = np.arange(-10, 11, 1)

awb_levels = np.arange(10, 50, 5)
awb_levels_div = np.arange(-20, 22, 5)

cwb_levels = np.arange(7, 22, 3)
cwb_levels_div = np.arange(-10, 11, 2.5)

wnd_scale = 150
wnd_scale_div = 150
#%%
# Custom thermal colormap: select one more chunk than awb_levels, drop the first chunk (too dark)
thermal_colors = cmocean.cm.thermal(np.linspace(0, 1, len(awb_levels) + 1))[1:]
cust_cmap = ListedColormap(thermal_colors, name="thermal_custom")

# %%
# Plot 1: uhat (jet stream), overlay last10 as contour on first10, 1 row x 3 columns
fig, axes = plt.subplots(
    nrows=1, ncols=3, figsize=(12, 4),
    subplot_kw={"projection": ccrs.Orthographic(-30, 90)},
    constrained_layout=True,
)


# Exclude 0 from contour levels
contour_levels = uhat_levels_div[uhat_levels_div != 0]

# Positive phase
cf = uhat_pos_first10.plot.contourf(
    ax=axes[0], levels=uhat_levels_div, cmap='RdBu_r', add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="both",
)
uhat_pos_last10.plot.contour(
    ax=axes[0], levels=contour_levels, colors="black", linewidths=1,
    transform=ccrs.PlateCarree(),
)
axes[0].set_title("Positive phase")

# Negative phase
cf = uhat_neg_first10.plot.contourf(
    ax=axes[1], levels=uhat_levels_div, cmap='RdBu_r', add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="both",
)
uhat_neg_last10.plot.contour(
    ax=axes[1], levels=contour_levels, colors="black", linewidths=1,
    transform=ccrs.PlateCarree(),
)
axes[1].set_title("Negative phase")

# Difference
cf = uhat_NAO_diff_first.plot.contourf(
    ax=axes[2], levels=uhat_levels_div, cmap='RdBu_r', add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="both",
)
uhat_NAO_diff_last.plot.contour(
    ax=axes[2], levels=contour_levels, colors="black", linewidths=1,
    transform=ccrs.PlateCarree(),
)
axes[2].set_title("Difference")

for ax in axes:
    ax.coastlines(color="grey", linewidth=1)
    ax.gridlines(draw_labels=False, linewidth=1, color="grey", alpha=0.5, linestyle="--")
    ax.set_global()

# Add colorbar to the bottom of each column
for coli, ax in enumerate(axes):
    fig.colorbar(
        cf,
        ax=ax,
        shrink=0.8,
        orientation="horizontal",
        label=r"$\overline{u}$ (m/s)",
    )

# add a, b, c labels
for i, ax in enumerate(axes):
    ax.text(
        0.05, 1.05, chr(97 + i), transform=ax.transAxes,
        fontsize=14, fontweight='bold', va='top', ha='right'
    )

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0mean_flow/uhat_composite.pdf", bbox_inches='tight', dpi=300)

# %%

# #%%
# # Plot 2: Potential temperature
# fig, axes = plt.subplots(
#     nrows=2, ncols=3, figsize=(12, 8),
#     subplot_kw={"projection": ccrs.Orthographic(-30, 90)},
#     constrained_layout=True,
# )
# # First 10 years
# theta_pos_first.plot.contourf(
#     ax=axes[0, 0], levels=temp_levels, cmap=temp_cmap_div, add_colorbar=False,
#     transform=ccrs.PlateCarree(), extend="both",
# )
# theta_neg_first.plot.contourf(
#     ax=axes[0, 1], levels=temp_levels, cmap=temp_cmap_div, add_colorbar=False,
#     transform=ccrs.PlateCarree(), extend="both",
# )
# theta_diff_first.plot.contourf(
#     ax=axes[0, 2], levels=temp_levels_div, cmap=temp_cmap_div, add_colorbar=False,
#     transform=ccrs.PlateCarree(), extend="both",
# )
# # Last 10 years
# pos_map = theta_pos_last.plot.contourf(
#     ax=axes[1, 0], levels=temp_levels, cmap=temp_cmap_div, add_colorbar=False,
#     transform=ccrs.PlateCarree(), extend="both",
# )
# neg_map = theta_neg_last.plot.contourf(
#     ax=axes[1, 1], levels=temp_levels, cmap=temp_cmap_div, add_colorbar=False,
#     transform=ccrs.PlateCarree(), extend="both",
# )
# diff_map = theta_diff_last.plot.contourf(
#     ax=axes[1, 2], levels=temp_levels_div, cmap=temp_cmap_div, add_colorbar=False,
#     transform=ccrs.PlateCarree(), extend="both",
# )
# for ax in axes.flatten():
#     ax.coastlines(color="grey", linewidth=1)
#     ax.gridlines(draw_labels=False, linewidth=1, color="grey", alpha=0.5, linestyle="--")
#     ax.set_global()
# axes[0, 0].set_title("Positive phase")
# axes[0, 1].set_title("Negative phase")
# axes[0, 2].set_title("Difference")

# # Add wind quiver to each subplot in the theta plot
# # First 10 years
# wnd_quiver = axes[0, 0].quiver(
#     wnd_pos_first["lon"].values[::5],
#     wnd_pos_first.lat[::5],
#     wnd_pos_first["ua"].values[::5, ::5],
#     wnd_pos_first["va"].values[::5, ::5],
#     transform=ccrs.PlateCarree(),
#     scale=wnd_scale,
#     color="black",
# )
# axes[0, 0].quiverkey(
#     wnd_quiver,
#     0.9,
#     0.03,
#     20,
#     r"20 m/s",
#     labelpos="E",
#     transform=axes[0, 0].transAxes,
#     coordinates="axes",
# )

# wnd_quiver = axes[0, 1].quiver(
#     wnd_neg_first["lon"].values[::5],
#     wnd_neg_first.lat[::5],
#     wnd_neg_first["ua"].values[::5, ::5],
#     wnd_neg_first["va"].values[::5, ::5],
#     transform=ccrs.PlateCarree(),
#     scale=wnd_scale,
#     color="black",
# )

# wnd_quiver = axes[0, 2].quiver(
#     wnd_diff_first["lon"].values[::5],
#     wnd_diff_first.lat[::5],
#     wnd_diff_first["ua"].values[::5, ::5],
#     wnd_diff_first["va"].values[::5, ::5],
#     transform=ccrs.PlateCarree(),
#     scale=wnd_scale_div,
#     color="black",
# )

# # Last 10 years
# wnd_quiver = axes[1, 0].quiver(
#     wnd_pos_last["lon"].values[::5],
#     wnd_pos_last.lat[::5],
#     wnd_pos_last["ua"].values[::5, ::5],
#     wnd_pos_last["va"].values[::5, ::5],
#     transform=ccrs.PlateCarree(),
#     scale=wnd_scale,
#     color="black",
# )
# axes[1, 0].quiverkey(
#     wnd_quiver,
#     0.9,
#     0.03,
#     20,
#     r"20 m/s",
#     labelpos="E",
#     transform=axes[1, 0].transAxes,
#     coordinates="axes",
# )

# wnd_quiver = axes[1, 1].quiver(
#     wnd_neg_last["lon"].values[::5],
#     wnd_neg_last.lat[::5],
#     wnd_neg_last["ua"].values[::5, ::5],
#     wnd_neg_last["va"].values[::5, ::5],
#     transform=ccrs.PlateCarree(),
#     scale=wnd_scale,
#     color="black",
# )

# wnd_quiver = axes[1, 2].quiver(
#     wnd_diff_last["lon"].values[::5],
#     wnd_diff_last.lat[::5],
#     wnd_diff_last["ua"].values[::5, ::5],
#     wnd_diff_last["va"].values[::5, ::5],
#     transform=ccrs.PlateCarree(),
#     scale=wnd_scale_div,
#     color="black",
# )

# # Add colorbar to the bottom of each column
# for coli, map in enumerate([pos_map, neg_map, diff_map]):
#     fig.colorbar(
#         map,
#         ax=axes[:, coli],
#         shrink=0.8,
#         orientation="horizontal",
#         label=r"$\overline{v' \theta}$ (K m s$^{-1}$)",
#     )

# # add a, b, c labels
# for i, ax in enumerate(axes.flatten()):
#     ax.text(
#         0.05, 1.05, chr(97 + i), transform=ax.transAxes,
#         fontsize=14, fontweight='bold', va='top', ha='right'
#     )

# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0mean_flow/theta_2x3.pdf", bbox_inches='tight', dpi=300)

#%%
# Plot 3: Wave breaking (AWB/CWB)
fig, axes = plt.subplots(
    nrows=2, ncols=3, figsize=(12, 8),
    subplot_kw={"projection": ccrs.Orthographic(-30, 90)},
    constrained_layout=True,
)
# First 10 years
awb_map_pos_first = awb_pos_first.plot.contourf(
    ax=axes[0, 0], levels=awb_levels, cmap=cust_cmap, add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="max",
)
cwb_contour = cwb_pos_first.plot.contour(
    ax=axes[0, 0], levels=cwb_levels, colors="black", add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="max",
)
if 10 in cwb_levels:
    axes[0, 0].clabel(cwb_contour, [10], fmt='%d', fontsize=8)

awb_map_neg_first = awb_neg_first.plot.contourf(
    ax=axes[0, 1], levels=awb_levels, cmap=cust_cmap, add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="max",
)
cwb_contour = cwb_neg_first.plot.contour(
    ax=axes[0, 1], levels=cwb_levels, colors="black", add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="max",
)
if 10 in cwb_levels:
    axes[0, 1].clabel(cwb_contour, [10], fmt='%d', fontsize=8)

zero_idx = np.argmin(np.abs(awb_levels_div))
ticks = np.sort(np.unique(np.concatenate([awb_levels_div[zero_idx::-2], awb_levels_div[zero_idx::2]])))
awb_map_diff_first = awb_diff_first.plot.contourf(
    ax=axes[0, 2], levels=awb_levels_div, cmap="coolwarm", add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="both",
)
cwb_contour = cwb_diff_first.plot.contour(
    ax=axes[0, 2], levels=cwb_levels_div[cwb_levels_div != 0], colors="black", add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="both",
)
axes[0, 2].clabel(cwb_contour, [-5, 5], fmt='%g', fontsize=8)

# Last 10 years
awb_map_pos_last = awb_pos_last.plot.contourf(
    ax=axes[1, 0], levels=awb_levels, cmap=cust_cmap, add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="max",
)
cwb_contour = cwb_pos_last.plot.contour(
    ax=axes[1, 0], levels=cwb_levels, colors="black", add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="max",
)
if 10 in cwb_levels:
    axes[1, 0].clabel(cwb_contour, [10], fmt='%d', fontsize=8)

awb_map_neg_last = awb_neg_last.plot.contourf(
    ax=axes[1, 1], levels=awb_levels, cmap=cust_cmap, add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="max",
)
cwb_contour = cwb_neg_last.plot.contour(
    ax=axes[1, 1], levels=cwb_levels, colors="black", add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="max",
)
if 10 in cwb_levels:
    axes[1, 1].clabel(cwb_contour, [10], fmt='%d', fontsize=8)

zero_idx = np.argmin(np.abs(awb_levels_div))
ticks = np.sort(np.unique(np.concatenate([awb_levels_div[zero_idx::-2], awb_levels_div[zero_idx::2]])))
awb_map_diff_last = awb_diff_last.plot.contourf(
    ax=axes[1, 2], levels=awb_levels_div, cmap="coolwarm", add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="both",
)
cwb_contour = cwb_diff_last.plot.contour(
    ax=axes[1, 2], levels=cwb_levels_div[cwb_levels_div != 0], colors="black", add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="both",
)
axes[1, 2].clabel(cwb_contour, [-5, 5], fmt='%g', fontsize=8)

for ax in axes.flatten():
    ax.coastlines(color="grey", linewidth=1)
    ax.gridlines(draw_labels=False, linewidth=1, color="grey", alpha=0.5, linestyle="--")
    ax.set_global()
axes[0, 0].set_title("Positive phase")
axes[0, 1].set_title("Negative phase")
axes[0, 2].set_title("Difference")

# Add colorbar to the bottom of each column
for coli, (map, label, ticks_, fmt) in enumerate([
    (awb_map_pos_last, "AWB freq", awb_levels[::2], '%.0f'),
    (awb_map_neg_last, "AWB freq", awb_levels[::2], '%.0f'),
    (awb_map_diff_last, "AWB freq diff", ticks, '%.0f')
]):
    fig.colorbar(
        map,
        ax=axes[:, coli],
        shrink=0.8,
        orientation="horizontal",
        label=label,
        ticks=ticks_,
        format=fmt,
    )

# add a, b, c labels
for i, ax in enumerate(axes.flatten()):
    ax.text(
        0.05, 1.05, chr(97 + i), transform=ax.transAxes,
        fontsize=14, fontweight='bold', va='top', ha='right'
    )

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0mean_flow/wb_2x3.pdf", bbox_inches='tight', dpi=300)

# %%
fig, axes = plt.subplots(
    nrows=3, ncols=3, figsize=(12, 12),
    subplot_kw={"projection": ccrs.Orthographic(-30, 90)},
    constrained_layout=True,
)

# --- First row: uhat (jet stream) ---
contour_levels = uhat_levels_div[uhat_levels_div != 0]

# Positive phase
cf_uhat_pos = uhat_pos_first10.plot.contourf(
    ax=axes[0, 0], levels=uhat_levels_div, cmap='RdBu_r', add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="both",
)
uhat_pos_last10.plot.contour(
    ax=axes[0, 0], levels=contour_levels, colors="black", linewidths=1,
    transform=ccrs.PlateCarree(),
)
axes[0, 0].set_title("Positive phase")

# Negative phase
cf_uhat_neg = uhat_neg_first10.plot.contourf(
    ax=axes[0, 1], levels=uhat_levels_div, cmap='RdBu_r', add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="both",
)
uhat_neg_last10.plot.contour(
    ax=axes[0, 1], levels=contour_levels, colors="black", linewidths=1,
    transform=ccrs.PlateCarree(),
)
axes[0, 1].set_title("Negative phase")

# Difference
cf_uhat_diff = uhat_NAO_diff_first.plot.contourf(
    ax=axes[0, 2], levels=uhat_levels_div, cmap='RdBu_r', add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="both",
)
uhat_NAO_diff_last.plot.contour(
    ax=axes[0, 2], levels=contour_levels, colors="black", linewidths=1,
    transform=ccrs.PlateCarree(),
)
axes[0, 2].set_title("Difference")

# --- Second row: Anticyclonic wave breaking (AWB) ---
awb_map_pos_first = awb_pos_first.plot.contourf(
    ax=axes[1, 0], levels=awb_levels, cmap=cust_cmap, add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="max",
)
awb_map_neg_first = awb_neg_first.plot.contourf(
    ax=axes[1, 1], levels=awb_levels, cmap=cust_cmap, add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="max",
)
awb_map_diff_first = awb_diff_first.plot.contourf(
    ax=axes[1, 2], levels=awb_levels_div, cmap="coolwarm", add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="both",
)

awb_contour_pos_last = awb_pos_last.plot.contour(
    ax=axes[1, 0], levels=awb_levels, colors="black", linewidths=1,
    transform=ccrs.PlateCarree(), add_colorbar=False
)
awb_contour_neg_last = awb_neg_last.plot.contour(
    ax=axes[1, 1], levels=awb_levels, colors="black", linewidths=1,
    transform=ccrs.PlateCarree(), add_colorbar=False
)
awb_contour_diff_last = awb_diff_last.plot.contour(
    ax=axes[1, 2], levels=awb_levels_div[awb_levels_div != 0], colors="black", linewidths=1,
    transform=ccrs.PlateCarree(), add_colorbar=False
)
if 10 in awb_levels:
    axes[1, 0].clabel(awb_contour_pos_last, [10], fmt='%d', fontsize=8)
    axes[1, 1].clabel(awb_contour_neg_last, [10], fmt='%d', fontsize=8)
if np.any(np.isin([-5, 5], awb_levels_div)):
    axes[1, 2].clabel(awb_contour_diff_last, [-5, 5], fmt='%g', fontsize=8)

# --- Third row: Cyclonic wave breaking (CWB) ---
cwb_map_pos_first = cwb_pos_first.plot.contourf(
    ax=axes[2, 0], levels=cwb_levels, cmap=cust_cmap, add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="max",
)
cwb_map_neg_first = cwb_neg_first.plot.contourf(
    ax=axes[2, 1], levels=cwb_levels, cmap=cust_cmap, add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="max",
)
cwb_map_diff_first = cwb_diff_first.plot.contourf(
    ax=axes[2, 2], levels=cwb_levels_div, cmap="coolwarm", add_colorbar=False,
    transform=ccrs.PlateCarree(), extend="both",
)

cwb_contour_pos_last = cwb_pos_last.plot.contour(
    ax=axes[2, 0], levels=cwb_levels, colors="black", linewidths=1,
    transform=ccrs.PlateCarree(), add_colorbar=False
)
cwb_contour_neg_last = cwb_neg_last.plot.contour(
    ax=axes[2, 1], levels=cwb_levels, colors="black", linewidths=1,
    transform=ccrs.PlateCarree(), add_colorbar=False
)
cwb_contour_diff_last = cwb_diff_last.plot.contour(
    ax=axes[2, 2], levels=cwb_levels_div[cwb_levels_div != 0], colors="black", linewidths=1,
    transform=ccrs.PlateCarree(), add_colorbar=False
)
if 10 in cwb_levels:
    axes[2, 0].clabel(cwb_contour_pos_last, [10], fmt='%d', fontsize=8)
    axes[2, 1].clabel(cwb_contour_neg_last, [10], fmt='%d', fontsize=8)
if np.any(np.isin([-5, 5], cwb_levels_div)):
    axes[2, 2].clabel(cwb_contour_diff_last, [-5, 5], fmt='%g', fontsize=8)

# --- Formatting ---
for ax in axes.flatten():
    ax.coastlines(color="grey", linewidth=1)
    ax.gridlines(draw_labels=False, linewidth=1, color="grey", alpha=0.5, linestyle="--")
    ax.set_global()

axes[0, 0].set_title("Positive phase")
axes[0, 1].set_title("Negative phase")
axes[0, 2].set_title("Difference")
axes[1, 0].set_title("AWB Positive phase")
axes[1, 1].set_title("AWB Negative phase")
axes[1, 2].set_title("AWB Difference")
axes[2, 0].set_title("CWB Positive phase")
axes[2, 1].set_title("CWB Negative phase")
axes[2, 2].set_title("CWB Difference")

# Colorbars
# uhat row
for coli, (cf, label) in enumerate([
    (cf_uhat_pos, r"$\overline{u}$ (m/s)"),
    (cf_uhat_neg, r"$\overline{u}$ (m/s)"),
    (cf_uhat_diff, r"$\overline{u}$ (m/s)")
]):
    fig.colorbar(
        cf,
        ax=axes[0, coli],
        shrink=0.6,
        orientation="horizontal",
        label=label,
    )
# AWB row
zero_idx_awb = np.argmin(np.abs(awb_levels_div))
ticks_awb = np.sort(np.unique(np.concatenate([awb_levels_div[zero_idx_awb::-2], awb_levels_div[zero_idx_awb::2]])))
for coli, (map, label, ticks_, fmt) in enumerate([
    (awb_map_pos_first, "AWB freq", awb_levels[::2], '%.0f'),
    (awb_map_neg_first, "AWB freq", awb_levels[::2], '%.0f'),
    (awb_map_diff_first, "AWB freq diff", ticks_awb, '%.0f')
]):
    fig.colorbar(
        map,
        ax=axes[1, coli],
        shrink=0.6,
        orientation="horizontal",
        label=label,
        ticks=ticks_,
        format=fmt,
    )
# CWB row
zero_idx_cwb = np.argmin(np.abs(cwb_levels_div))
# For difference, show all ticks in cwb_levels_div (not just a subset)
for coli, (map, label, ticks_, fmt) in enumerate([
    (cwb_map_pos_first, "CWB freq", cwb_levels, '%.0f'),
    (cwb_map_neg_first, "CWB freq", cwb_levels, '%.0f'),
    (cwb_map_diff_first, "CWB freq diff", cwb_levels_div, '%.0f')
]):
    fig.colorbar(
        map,
        ax=axes[2, coli],
        shrink=0.6,
        orientation="horizontal",
        label=label,
        ticks=ticks_,
        format=fmt,
    )

# add a, b, c, d, e, f, g, h, i labels
for i, ax in enumerate(axes.flatten()):
    ax.text(
        0.05, 1.05, chr(97 + i), transform=ax.transAxes,
        fontsize=14, fontweight='bold', va='top', ha='right'
    )
    ax.set_title("")

# plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0mean_flow/uhat_wb_composite.pdf", bbox_inches='tight', dpi=300)

# %%
