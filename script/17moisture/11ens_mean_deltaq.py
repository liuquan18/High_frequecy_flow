# %%
import xarray as xr
import numpy as np
import sys
import os
import glob
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
# %%
import src.moisture.longitudinal_contrast as lc

import logging
logging.basicConfig(level=logging.INFO)
# %%
def read_var(var = 'hus'):
    first_ens = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_monthly_ensmean/{var}_monmean_ensmean_185005_185909.nc")
    last_ens = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_monthly_ensmean/{var}_monmean_ensmean_209005_209909.nc")
    # 
    first_ens = first_ens[var].mean(dim = 'time')
    last_ens = last_ens[var].mean(dim = 'time')
    if var == 'hus':
        first_ens = first_ens * 1000
        last_ens = last_ens * 1000
    # 
    first_ens_q_std = lc.rolling_lon_periodic(first_ens, 33, 5, stat = 'std')
    last_ens_q_std = lc.rolling_lon_periodic(last_ens, 33, 5, stat = 'std')
    #
    diff = last_ens_q_std - first_ens_q_std

    return first_ens_q_std, last_ens_q_std, diff
#%%
first_ens_q_std, last_ens_q_std, diff = read_var('hus')
#%%
first_ens_t_std, last_ens_t_std, diff_t = read_var('tas')
#%%
temp_levels = np.arange(0,16,1)
hus_levels = np.arange(0,5,0.5)

temp_levels_div = np.arange(-5,5.5,0.5)
hus_levels_div = np.arange(-1.5,1.6,0.1)

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
fig, axes = plt.subplots(
    3, 2, figsize=(11, 9), subplot_kw={'projection': ccrs.PlateCarree(-90)}
)

# plot t
first_ens_t_std.plot(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_seq,
    cbar_kwargs={"label": r"$\Delta T$ (K)", "shrink": 0.6, 'ticks': np.arange(0, 16, 5)},
    levels=temp_levels,
    extend='max',
)
axes[0, 0].set_title("1850-1859")
axes[0, 0].coastlines()
axes[0, 0].set_global()

last_ens_t_std.plot(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_seq,
    cbar_kwargs={"label": r"$\Delta T$ (K)", "shrink": 0.6, 'ticks': np.arange(0, 16, 5)},
    levels=temp_levels,
    extend='max',
)
axes[1, 0].set_title("2090-2099")
axes[1, 0].coastlines()
axes[1, 0].set_global()

diff_t.plot(
    ax=axes[2, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    cbar_kwargs={"label": r"$\Delta T$ (K)", "shrink": 0.6, 'ticks': np.arange(-4, 5, 2)},
    levels=temp_levels_div,
    extend='both',
)
axes[2, 0].set_title("2090-2099 - 1850-1859")
axes[2, 0].coastlines()
axes[2, 0].set_global()

first_ens_q_std.plot(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_seq,
    cbar_kwargs={"label": r"$\Delta q$ (g/kg)", "shrink": 0.6, 'ticks': np.arange(0, 5, 1)},
    levels=hus_levels,
    extend='max',
)
axes[0, 1].set_title("1850-1859")
axes[0, 1].coastlines()
axes[0, 1].set_global()

last_ens_q_std.plot(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_seq,
    cbar_kwargs={"label": r"$\Delta q$ (g/kg)", "shrink": 0.6, 'ticks': np.arange(0, 5, 1)},
    levels=hus_levels,
    extend='max',
)
axes[1, 1].set_title("2090-2099")
axes[1, 1].coastlines()
axes[1, 1].set_global()

diff.plot(
    ax=axes[2, 1],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_div,
    cbar_kwargs={"label": r"$\Delta q$ (g/kg)", "shrink": 0.6, 'ticks': np.arange(-1.5, 1.6, 0.5)},
    levels=hus_levels_div,
    extend='both',
)
axes[2, 1].set_title("2090-2099 - 1850-1859")
axes[2, 1].coastlines()
axes[2, 1].set_global()

# latitude ticks
for i, ax in enumerate(axes.flatten()):
    if i % 2 == 0:
        ax.set_yticks(np.arange(-60, 76, 30), crs=ccrs.PlateCarree())
        ax.set_ylabel("Latitude")
        ax.yaxis.set_major_formatter(LatitudeFormatter())
    else:
        ax.set_yticks([])

    if i // 2 == 2:
        ax.set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())
        ax.set_xticklabels(['180°', '120°W', '60°W', '0°', '60°E', '120°E'])
    else:
        ax.set_xticks([])

axes[1, 1].set_xlabel("Longitude")

# a, b, c labels for each subplots
for i, ax in enumerate(axes.flatten()):
    ax.text(
        -0.1,
        1.0,
        chr(97 + i),
        transform=ax.transAxes,
        size=12,
        weight="bold",
    )
    ax.set_ylabel('')
    ax.set_xlabel('')

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/hus_tas_monthly_std.png", dpi=300)
# %%
