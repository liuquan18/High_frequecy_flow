#%%
import xarray as xr
import numpy as np
import pandas as pd
import logging
import glob
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
#%%
logging.basicConfig(level=logging.INFO)

# %%
import src.composite.composite as composite
import src.extremes.extreme_read as ext_read
import src.composite.composite_plot as composite_plot
#%%
import importlib
importlib.reload(composite)
importlib.reload(ext_read)
importlib.reload(composite_plot)
# %%
def composite_single_ens(variable, period, ens, plev, freq_label = None):
    pos_extreme, neg_extreme = ext_read.read_extremes(period, 8, ens, plev = plev)
    variable_ds = composite.read_variable(variable, period, ens, plev, freq_label)
    pos_comp, neg_comp = composite.event_composite(variable_ds, pos_extreme, neg_extreme)
    return pos_comp, neg_comp

# %%
def composite_variable(variable, plev, freq_label, period, stat = "mean"):
    pos_comps = []
    neg_comps = []

    for i in range(1, 51):
        pos_comp, neg_comp = composite_single_ens(variable, period, i, plev, freq_label)

        pos_comps.append(pos_comp)
        neg_comps.append(neg_comp)

    # exclude None from the list
    pos_comps = [x for x in pos_comps if x is not None]
    neg_comps = [x for x in neg_comps if x is not None]

    pos_comps = xr.concat(pos_comps, dim = "event")
    neg_comps = xr.concat(neg_comps, dim = "event")

    if stat == "mean":
        pos_comps = pos_comps.mean(dim = "event")
        neg_comps = neg_comps.mean(dim = "event")
    elif stat == "count":
        pos_comps = pos_comps.count(dim = "event")
        neg_comps = neg_comps.count(dim = "event")

    return pos_comps, neg_comps
# %%
def remove_zonalmean(zg):
    """
    remove zonal mean from the data
    """
    zg = zg - zg.mean(dim="lon")
    return zg
# %%
plev = 50000

#%%
zg_first10_pos, zg_first10_neg = composite_variable("zg", plev, None, "first10")
zg_last10_pos, zg_last10_neg = composite_variable("zg", plev, None, "last10")    
#%%
uhat_first10_pos, uhat_first10_neg = composite_variable("ua", plev, 'hat', "first10")
uhat_last10_pos, uhat_last10_neg = composite_variable("ua", plev, 'hat', "last10")
#%%
mf_first10_pos, mf_first10_neg = composite_variable("momentum_fluxes", plev, 'prime', "first10")
mf_last10_pos, mf_last10_neg = composite_variable("momentum_fluxes", plev, 'prime', "last10")

# %%
# %%
######### plot with filled contourf for mf and contour for zg ##########
fig, axes = plt.subplots(
    6, 2, figsize=(17, 15), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -13
interval_lag = 2

# filled contourf for mf
axes, p = composite_plot.plot_composite(
    mf_first10_pos,
    mf_last10_pos,
    axes,
    extreme_type="pos",
    start_lag=start_lag,
    interval_lag=interval_lag,
    levels=np.arange(-40, 41, 5),
    fill=True
)

composite_plot.plot_composite(
    zg_first10_pos,
    zg_last10_pos,
    axes,
    extreme_type="pos",
    start_lag=start_lag,
    interval_lag=interval_lag,
    levels=np.arange(-75, 76, 15),
    fill=False
)

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of positive extremes (contour interval: 15m)")
plt.tight_layout(rect=[0, 0.1, 1, 1])

# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_mf_zg_pos.png", dpi=300)
# %%
########## plot only with zg ##########
fig, axes = plt.subplots(
    6, 2, figsize=(17, 15), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -6
interval_lag = 1

composite_plot.plot_composite(
    zg_first10_pos,
    zg_last10_pos,
    axes,
    extreme_type="pos",
    start_lag=start_lag,
    interval_lag=interval_lag,
    levels=np.arange(-75, 76, 15),
    fill=False
)

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of positive extremes (contour interval: 15m)")
plt.tight_layout(rect=[0, 0.1, 1, 1])

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_zg_pos.png", dpi=300)
# %%

########## plot only with mf ##########
fig, axes = plt.subplots(
    6, 2, figsize=(17, 15), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -13
interval_lag = 2

# filled contourf for mf
axes, p = composite_plot.plot_composite(
    mf_first10_pos,
    mf_last10_pos,
    axes,
    extreme_type="pos",
    start_lag=start_lag,
    interval_lag=interval_lag,
    levels=np.arange(-40, 41, 5),
    fill=True
)

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of positive extremes (contour interval: 5m/s)")
plt.tight_layout(rect=[0, 0.1, 1, 1])

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_mf_pos.png", dpi=300)
# %%
############# plot with zg zonal mean removed ############
fig, axes = plt.subplots(
    6, 2, figsize=(17, 15), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -6
interval_lag = 1

zg_inter = 15

composite_plot.plot_composite(
    remove_zonalmean(zg_first10_pos),
    remove_zonalmean(zg_last10_pos),
    axes,
    extreme_type="pos",
    start_lag=start_lag,
    interval_lag=interval_lag,
    levels=np.arange(-75, 76, zg_inter),
    fill=False
)

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle(f"Composite of positive extremes (contour interval: {zg_inter}m)")
plt.tight_layout(rect=[0, 0.1, 1, 1])

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_zg_pos_zonalmean_removed.png", dpi=300)
# %%
