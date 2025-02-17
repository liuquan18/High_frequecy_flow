#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line

# %%
ensmean_first = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_ensmean_50000_1850.nc")
ensmean_last = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_ensmean_50000_2090.nc")
# %%
ensmean_first = ensmean_first.eke
ensmean_last = ensmean_last.eke
#%%
ensmean_first = ensmean_first.mean(dim = 'time').squeeze()
ensmean_last = ensmean_last.mean(dim = 'time').squeeze()
#%%
ensmean_first.compute()
ensmean_last.compute()
#%%
ensmean_first = erase_white_line(ensmean_first)
ensmean_last = erase_white_line(ensmean_last)
# %%
fig, axes = plt.subplots(3, 1, figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree(-90)})
ensmean_first.plot.contourf(ax = axes[0], transform = ccrs.PlateCarree(), cmap = 'RdBu_r', levels = np.arange(0, 35, 5), cbar_kwargs = {'label': r'$m^2/s^2$'})

ensmean_last.plot.contourf(ax = axes[1], transform = ccrs.PlateCarree(), cmap = 'RdBu_r', levels = np.arange(0, 35, 5), cbar_kwargs = {'label': r'$m^2/s^2$'})

(ensmean_last - ensmean_first).plot.contourf(ax = axes[2], transform = ccrs.PlateCarree(), cmap = 'RdBu_r', levels = np.arange(-15, 20, 5), cbar_kwargs = {'label': r'$m^2/s^2$'})

for ax in axes:
    ax.coastlines()

    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
# %%
