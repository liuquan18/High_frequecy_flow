
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
first_tas = read_data("tas", 1850, (-90, 90), False)
first_hus = read_data("hus", 1850, (-90, 90), False)
first_vt = read_data("vt", 1850, (-90, 90), False, suffix='')
#%%
wind_cmap = np.loadtxt("/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/wind_div.txt")
wind_cmap = mcolors.ListedColormap(wind_cmap)
# %%
fig, ax = plt.subplots(1, 1, figsize=(10, 5), subplot_kw={'projection': ccrs.PlateCarree()})
first_vt.isel(time = 0, ens = 0).plot(ax=ax, transform=ccrs.PlateCarree(), cmap=wind_cmap,levels = np.arange(-30, 31, 5) )
ax.coastlines()
# %%
fig, ax = plt.subplots(1, 1, figsize=(10, 5), subplot_kw={'projection': ccrs.PlateCarree()})
first_vt.isel(time = 0, ens = 3).plot(ax=ax, transform=ccrs.PlateCarree(), cmap=wind_cmap,levels = np.arange(-30, 31, 5) )
ax.coastlines()
# %%

# %%
first_hus.load()
first_tas.load()
first_vt.load()
# %%
#%%
std_first_tas = first_tas.sel(lat = slice(0, 60)).mean(dim = ('lon','lat')).quantile(0.99, dim = ('time', 'ens'))
std_first_hus = first_hus.sel(lat = slice(0, 60)).mean(dim = ('lon','lat')).quantile(0.99, dim = ('time', 'ens'))
# %%
std_first_vt_pos = first_vt.where(first_vt >0).sel(lat = slice(0, 60)).mean(dim = ('lon','lat')).quantile(0.99, dim = ('time', 'ens'))
std_first_vt_neg = first_vt.where(first_vt <0).sel(lat = slice(0, 60)).mean(dim = ('lon','lat')).quantile(0.01, dim = ('time', 'ens'))
# %%