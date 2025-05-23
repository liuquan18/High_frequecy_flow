#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature

import matplotlib.colors as mcolors
from src.plotting.util import map_smooth

# %%
def read_comp_var(var, phase, decade, time_window = (-5, 5), **kwargs):
    name = kwargs.get("name", var)
    basedir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_range/"
    file_name = basedir + f"{var}_NAO_{phase}_{decade}.nc"
    ds = xr.open_dataset(file_name)[name]
    ds = ds.sel(time=slice(*time_window))
    ds = ds.mean(dim=("time", "ens"))
    return ds
#%%
def read_comp_wb(decade, wb_type, phase, time_window = (-15, 0)):
    basedir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_range/{wb_type}_{phase}_{decade}.nc"
    ds = xr.open_dataset(basedir).flag
    ds = ds.sel(time=slice(*time_window))
    ds = ds.sum(dim=("time", "ens"))
    return ds
# %%
uhat_composiste = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/"
uhat_pos_first10 = xr.open_dataarray(
    f"{uhat_composiste}jetstream_MJJAS_first10_pos.nc"
)
uhat_neg_first10 = xr.open_dataarray(
    f"{uhat_composiste}jetstream_MJJAS_first10_neg.nc"
)

uhat_pos_last10 = xr.open_dataarray(
    f"{uhat_composiste}jetstream_MJJAS_last10_pos.nc"
)
uhat_neg_last10 = xr.open_dataarray(
    f"{uhat_composiste}jetstream_MJJAS_last10_neg.nc"
)

uhat_NAO_diff_first = uhat_pos_first10 - uhat_neg_first10
uhat_NAO_diff_last = uhat_pos_last10 - uhat_neg_last10



# %%
theta_pos_first = read_comp_var('theta_2pvu', "pos", 1850, name='__xarray_dataarray_variable__')
theta_pos_last = read_comp_var('theta_2pvu', "pos", 2090, name='__xarray_dataarray_variable__')
theta_neg_first = read_comp_var('theta_2pvu', "neg", 1850, name='__xarray_dataarray_variable__')
theta_neg_last = read_comp_var('theta_2pvu', "neg", 2090, name='__xarray_dataarray_variable__')
#%%
theta_diff_first = theta_pos_first - theta_neg_first
theta_diff_last = theta_pos_last - theta_neg_last
# %%
# ua
ua_pos_first = read_comp_var('ua', "pos", 1850, name='ua')
ua_pos_last = read_comp_var('ua', "pos", 2090, name='ua')
ua_neg_first = read_comp_var('ua', "neg", 1850, name='ua')
ua_neg_last = read_comp_var('ua', "neg", 2090, name='ua')
#%%
# va
va_pos_first = read_comp_var('va', "pos", 1850, name='va')
va_pos_last = read_comp_var('va', "pos", 2090, name='va')
va_neg_first = read_comp_var('va', "neg", 1850, name='va')
va_neg_last = read_comp_var('va', "neg", 2090, name='va')
#%%
# ua and va to dataset
wnd_pos_first = xr.merge([ua_pos_first, va_pos_first])
wnd_neg_first = xr.merge([ua_neg_first, va_neg_first])
wnd_pos_last = xr.merge([ua_pos_last, va_pos_last])
wnd_neg_last = xr.merge([ua_neg_last, va_neg_last])

#%%
wnd_diff_first = wnd_pos_first - wnd_neg_first
wnd_diff_last = wnd_pos_last - wnd_neg_last
#%%
# wind select 250hPa
wnd_pos_first = wnd_pos_first.sel(plev=25000)
wnd_neg_first = wnd_neg_first.sel(plev=25000)
wnd_pos_last = wnd_pos_last.sel(plev=25000)
wnd_neg_last = wnd_neg_last.sel(plev=25000)

wnd_diff_first = wnd_diff_first.sel(plev=25000)
wnd_diff_last = wnd_diff_last.sel(plev=25000)
# %%
AWB_pos_first = read_comp_wb(1850, "AWB", "pos")
CWB_neg_first = read_comp_wb(1850, "CWB", "neg")

AWB_pos_last = read_comp_wb(2090, "AWB", "pos")
CWB_neg_last = read_comp_wb(2090, "CWB", "neg")
#%%
AWB_diff_first = AWB_pos_first - CWB_neg_first
AWB_diff_last = AWB_pos_last - CWB_neg_last


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
temp_levels = np.arange(290, 360, 5)  # K instead of C
temp_levels_div = np.arange(-10, 11, 1)
wnd_scale = 150
wnd_scale_div = 150
# %%
# first 10 years
fig, axes = plt.subplots(
    nrows = 3,
    ncols = 3,
    figsize = (12, 10),
    subplot_kw={"projection": ccrs.Orthographic(-30, 90)},
    constrained_layout = True,
)
# rows for different variables
# columns for pos, neg, diff
# uhat
uhat_pos_first10.plot.contourf(
    ax=axes[0, 0],
    levels=uhat_levels_div,
    cmap='jet',
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

uhat_neg_first10.plot.contourf(
    ax=axes[0, 1],
    levels=uhat_levels_div,
    cmap='jet',
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

uhat_NAO_diff_first.plot.contourf(
    ax=axes[0, 2],
    levels=uhat_levels_div,
    cmap='jet',
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

# theta
theta_pos_first.plot.contourf(
    ax=axes[1, 0],
    levels=temp_levels,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
theta_neg_first.plot.contourf(
    ax=axes[1, 1],
    levels=temp_levels,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
theta_diff_first.plot.contourf(
    ax=axes[1, 2],
    levels=temp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

# wind quiver
wnd_quiver = axes[1,0].quiver(
    wnd_pos_first["lon"].values[::5],
    wnd_pos_first.lat[::5],
    wnd_pos_first["ua"].values[::5, ::5],
    wnd_pos_first["va"].values[::5, ::5],
    transform=ccrs.PlateCarree(),
    scale=wnd_scale,
    color="black",
)

# wind quiver
wnd_quiver = axes[1,1].quiver(
    wnd_neg_first["lon"].values[::5],
    wnd_neg_first.lat[::5],
    wnd_neg_first["ua"].values[::5, ::5],
    wnd_neg_first["va"].values[::5, ::5],
    transform=ccrs.PlateCarree(),
    scale=wnd_scale,
    color="black",
)

# wind quiver
wnd_quiver = axes[1,2].quiver(
    wnd_diff_first["lon"].values[::5],
    wnd_diff_first.lat[::5],
    wnd_diff_first["ua"].values[::5, ::5],
    wnd_diff_first["va"].values[::5, ::5],
    transform=ccrs.PlateCarree(),
    scale=wnd_scale_div,
    color="black",
)

# wb
AWB_pos_first.plot(
    ax=axes[2, 0],
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

CWB_neg_first.plot(
    ax=axes[2, 1],
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

AWB_diff_first.plot(
    ax=axes[2, 2],
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

# add coastlines and gridlines
for ax in axes.flatten():
    ax.coastlines(color="grey", linewidth=1)

# %%