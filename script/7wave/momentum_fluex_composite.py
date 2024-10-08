# %%
import xarray as xr
import numpy as np
import pandas as pd
import logging
import glob
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# %%
logging.basicConfig(level=logging.INFO)

# %%
import src.composite.composite as composite
import src.extremes.extreme_read as ext_read
import src.composite.composite_plot as composite_plot

# %%
import importlib

importlib.reload(composite)
importlib.reload(ext_read)
importlib.reload(composite_plot)


# %%
def composite_single_ens(variable, period, ens, plev, freq_label=None):
    pos_extreme, neg_extreme = ext_read.read_extremes(period, 8, ens, plev=plev)
    variable_ds = composite.read_variable(variable, period, ens, plev, freq_label)
    pos_comp, neg_comp = composite.event_composite(
        variable_ds, pos_extreme, neg_extreme
    )
    return pos_comp, neg_comp


# %%
def composite_variable(variable, plev, freq_label, period, stat="mean"):
    pos_comps = []
    neg_comps = []

    for i in range(1, 51):
        pos_comp, neg_comp = composite_single_ens(variable, period, i, plev, freq_label)

        pos_comps.append(pos_comp)
        neg_comps.append(neg_comp)

    # exclude None from the list
    pos_comps = [x for x in pos_comps if x is not None]
    neg_comps = [x for x in neg_comps if x is not None]

    pos_comps = xr.concat(pos_comps, dim="event")
    neg_comps = xr.concat(neg_comps, dim="event")

    if stat == "mean":
        pos_comps = pos_comps.mean(dim="event")
        neg_comps = neg_comps.mean(dim="event")
    elif stat == "count":
        pos_comps = pos_comps.count(dim="event")
        neg_comps = neg_comps.count(dim="event")

    return pos_comps, neg_comps


# %%
def create_symmetric_levels(interval, num_levels):
    # Ensure num_levels is odd to have a center at 0
    if num_levels % 2 == 0:
        num_levels += 1

    # Calculate the maximum absolute value
    max_abs = (num_levels - 1) / 2 * interval

    # Create the levels array
    levels = np.linspace(-max_abs, max_abs, num_levels)

    return levels


# %%
plev = 25000
# %%
# mf_levels = create_symmetric_levels(5, 15)
# zg_levels = create_symmetric_levels(15, 11)

mf_levels = np.arange(-25, 26, 5)
zg_levels = np.arange(-75, 76, 15)
# %%
zg_first10_pos, zg_first10_neg = composite_variable("zg", plev, None, "first10")
zg_last10_pos, zg_last10_neg = composite_variable("zg", plev, None, "last10")
# %%
uhat_first10_pos, uhat_first10_neg = composite_variable("ua", 70000, "hat", "first10")
uhat_last10_pos, uhat_last10_neg = composite_variable("ua", 70000, "hat", "last10")
# %%
mf_first10_pos, mf_first10_neg = composite_variable(
    "E_N", plev, "prime", "first10"
)
mf_last10_pos, mf_last10_neg = composite_variable(
    "E_N", plev, "prime", "last10"
)

# %%
# %%
######### plot with filled contourf for mf and contour for zg ##########
fig, axes = plt.subplots(
    6, 2, figsize=(17, 15), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -13
interval_lag = 2
remove_zonalmean = False

mf_levels = np.arange(-25, 26, 5)
zg_levels = np.arange(-75, 76, 15)

if remove_zonalmean:
    figname = "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_mf_zg_pos_zonalmean_removed.png"
else:
    figname = "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_mf_zg_pos.png"

# filled contourf for mf
axes, p = composite_plot.plot_composite(
    mf_first10_pos,
    mf_last10_pos,
    axes,
    extreme_type="pos",
    start_lag=start_lag,
    interval_lag=interval_lag,
    levels=mf_levels,
    fill=True,
    remove_zonalmean=remove_zonalmean,
)

composite_plot.plot_composite(
    zg_first10_pos,
    zg_last10_pos,
    axes,
    extreme_type="pos",
    start_lag=start_lag,
    interval_lag=interval_lag,
    levels=zg_levels,
    fill=False,
    remove_zonalmean=remove_zonalmean,
)

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of positive extremes (contour interval: 15m)")
plt.tight_layout(rect=[0, 0.1, 1, 1])

# plt.savefig(figname, dpi=300)
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
    levels=zg_levels,
    fill=False,
)

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of positive extremes (contour interval: 15m)")
plt.tight_layout(rect=[0, 0.1, 1, 1])

# plt.savefig(
#     "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_zg_pos.png",
#     dpi=300,
# )
# %%
#################### plot positive extremes with mf and uhat ####################
uhat_levels = np.arange(-10, 11, 1)
mf_levels = np.arange(-25, 26, 5)

fig, axes = plt.subplots(
    6, 2, figsize=(17, 15), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -13
interval_lag = 2

composite_plot.plot_composite(
    uhat_first10_pos,
    uhat_last10_pos,
    axes,
    extreme_type="pos",
    start_lag=start_lag,
    interval_lag=interval_lag,
    levels=uhat_levels,
    fill=False,
    remove_zonalmean=False,
)

axes, p = composite_plot.plot_composite(
    mf_first10_pos,
    mf_last10_pos,
    axes,
    extreme_type="pos",
    start_lag=start_lag,
    interval_lag=interval_lag,
    levels=mf_levels,
    fill=True,
    remove_zonalmean=False,
)

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of positive extremes (contour interval: 1m/s)")
plt.tight_layout(rect=[0, 0.1, 1, 1])

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_mf_uhat_pos.png",
    dpi=300,
)

# %%
########## plot only with mf ##########
fig, axes = plt.subplots(
    6, 2, figsize=(17, 15), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -13
interval_lag = 2

# filled contourf for mf
axes, p = composite_plot.plot_composite(
    remove_zonalmean(mf_first10_pos),
    remove_zonalmean(mf_last10_pos),
    axes,
    extreme_type="pos",
    start_lag=start_lag,
    interval_lag=interval_lag,
    levels=mf_levels,
    fill=True,
)

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of positive extremes (contour interval: 5m/s)")
plt.tight_layout(rect=[0, 0.1, 1, 1])

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_mf_pos_zonalmean_removed.png",
    dpi=300,
)
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
    fill=False,
)

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle(f"Composite of positive extremes (contour interval: {zg_inter}m)")
plt.tight_layout(rect=[0, 0.1, 1, 1])

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_zg_pos_zonalmean_removed.png",
    dpi=300,
)
# %%
############# plot for negative extremes with zg and mf ############
fig, axes = plt.subplots(
    6, 2, figsize=(17, 15), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -13
interval_lag = 2

mf_levels = np.arange(-20, 21, 4)
zg_levels = np.arange(-75, 76, 15)

# filled contourf for mf
axes, p = composite_plot.plot_composite(
    mf_first10_neg,
    mf_last10_neg,
    axes,
    extreme_type="neg",
    start_lag=start_lag,
    interval_lag=interval_lag,
    levels=mf_levels,
    fill=True,
    remove_zonalmean=True,
)

composite_plot.plot_composite(
    zg_first10_neg,
    zg_last10_neg,
    axes,
    extreme_type="neg",
    start_lag=start_lag,
    interval_lag=interval_lag,
    levels=np.arange(-75, 76, 15),
    fill=False,
    remove_zonalmean=True,
)

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of negative extremes (contour interval: 15m)")
plt.tight_layout(rect=[0, 0.1, 1, 1])

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_mf_zg_neg_zonalmean_removed.png",
    dpi=300,
)
# %%
############# plot for negative extremes with mf and uhat ############
uhat_levels = np.arange(-10, 11, 1)
mf_levels = np.arange(-20, 21, 4)

fig, axes = plt.subplots(
    6, 2, figsize=(17, 15), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)

composite_plot.plot_composite(
    uhat_first10_neg,
    uhat_last10_neg,
    axes,
    extreme_type="neg",
    start_lag=-13,
    interval_lag=2,
    levels=uhat_levels,
    fill=False,
    remove_zonalmean=False,
)


axes, p = composite_plot.plot_composite(
    mf_first10_neg,
    mf_last10_neg,
    axes,
    extreme_type="neg",
    start_lag=-13,
    interval_lag=2,
    levels=mf_levels,
    fill=True,
    remove_zonalmean=False,
)

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of negative extremes (contour interval: 5m/s)")
plt.tight_layout(rect=[0, 0.1, 1, 1])

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_mf_uhat_neg.png",
    dpi=300,
)
# %%
mf_mer_first10_pos = mf_first10_pos.sel(lat = slice(30,60) ).mean(dim="lat")
mf_mer_first10_neg = mf_first10_neg.sel(lat = slice(30,60) ).mean(dim="lat")

mf_mer_last10_pos = mf_last10_pos.sel(lat = slice(30,60) ).mean(dim="lat")
mf_mer_last10_neg = mf_last10_neg.sel(lat = slice(30,60) ).mean(dim="lat")

# %%
#### lag_lontitude plot of mf #########
fig, axes = plt.subplots(
    2, 1, figsize=(10, 8), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
levels=np.arange(-20, 21, 5)
levels = levels[(levels >= 10) | (levels <= -10)]

mf_mer_first10_pos.plot.contourf(
    ax=axes[0], levels = levels, add_colorbar=False, extend="both",
    transform=ccrs.PlateCarree()
)
axes[0].set_title('First 10 years')

p = mf_mer_last10_pos.plot.contourf(
    ax=axes[1], levels=levels, add_colorbar=False, extend="both",
    transform=ccrs.PlateCarree()
)
axes[1].set_title('Last 10 years')
# 
for ax in axes:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])
axes[0].set_xlabel(None)

# label the y-axis
for ax in [axes[0], axes[1]]:
    ax.set_yticks(range(-30, 30, 10))
    ax.set_yticklabels(range(-30, 30, 10))

    #reverse y-axis
    ax.invert_yaxis()
    ax.set_aspect('auto')
# add colorbar at the bottom
plt.colorbar(p, ax=[axes[0], axes[1]], orientation="horizontal", label=r"$m^2/s^2$", aspect=50)
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_mf_meridional_pos.png", dpi=300)
# %%
# negative
mf_mer_first10_neg = mf_first10_neg.sel(lat = slice(30,60) ).mean(dim="lat")
mf_mer_last10_neg = mf_last10_neg.sel(lat = slice(30,60) ).mean(dim="lat")


fig, axes = plt.subplots(
    2, 1, figsize=(10, 8), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
levels=np.arange(-20, 21, 5)
levels = levels[(levels >= 10) | (levels <= -10)]

mf_mer_first10_neg.plot.contourf(
    ax=axes[0], levels = levels, add_colorbar=False, extend="both",
    transform=ccrs.PlateCarree()
)
axes[0].set_title('First 10 years')

p = mf_mer_last10_neg.plot.contourf(
    ax=axes[1], levels=levels, add_colorbar=False, extend="both",
    transform=ccrs.PlateCarree()
)

axes[1].set_title('Last 10 years')

for ax in axes:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

axes[0].set_xlabel(None)

# label the y-axis
for ax in [axes[0], axes[1]]:
    ax.set_yticks(range(-30, 30, 10))
    ax.set_yticklabels(range(-30, 30, 10))

    #reverse y-axis
    ax.invert_yaxis()
    ax.set_aspect('auto')

# add colorbar at the bottom
plt.colorbar(p, ax=[axes[0], axes[1]], orientation="horizontal", label=r"$m^2/s^2$", aspect=50)
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/composite_mf_meridional_neg.png", dpi=300)
# %%
