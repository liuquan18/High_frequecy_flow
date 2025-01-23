# %%
import xarray as xr
import numpy as np
import sys
import os
import glob
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import logging
import matplotlib.colors as mcolors
from src.moisture.plot_utils import draw_box


from src.moisture.longitudinal_contrast import read_data

# %%
tas_mean = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/moisture_variability_stat/tas_daily_std_mergeyear_timmean.nc"
)
tas_mean = tas_mean.var130.squeeze()
#%%
hus_mean = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/moisture_variability_stat/hus_daily_std_mergeyear_timmean.nc"
)

hus_mean = hus_mean.var133.squeeze()
hus_mean = hus_mean * 1000 # unit

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
temp_levels = np.arange(0, 16, 1)
hus_levels = np.arange(0, 5, 0.5)

temp_levels_div = np.arange(-5, 5.5, 0.5)
hus_levels_div = np.arange(-1.5, 1.6, 0.1)

# %%
fig, axes = plt.subplots(
    1, 2, figsize=(12, 5), subplot_kw={"projection": ccrs.PlateCarree(-90)}
)

tas_mean.plot(
    ax=axes[0], transform=ccrs.PlateCarree(), cmap=temp_cmap_seq, levels=temp_levels,
    cbar_kwargs={"label": r"$\Delta T$ (K)", "shrink": 0.6, 'ticks': np.arange(0, 16, 5)},

)


axes[0].set_title(r"$\Delta T$")
axes[0].coastlines()

hus_mean.plot(
    ax=axes[1], transform=ccrs.PlateCarree(), cmap=prec_cmap_seq, levels=hus_levels,
    cbar_kwargs={"label": r"$\Delta q$ (g/kg)", "shrink": 0.6, 'ticks': np.arange(0, 5, 1)},
)

axes[1].set_title(r"$\Delta q$")
axes[1].coastlines()

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/ERA5_dT_dq_map.png", dpi=300)
# %%
