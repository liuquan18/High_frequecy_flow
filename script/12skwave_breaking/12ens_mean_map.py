#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# %%
ensmean_first = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_ensmean_50000_1850.nc")
ensmean_last = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_ensmean_50000_2090.nc")
# %%
ensmean_first = ensmean_first.eke
ensmean_last = ensmean_last.eke
#%%
ensmean_first = ensmean_first.mean(dim = 'time').squeeze()
ensmean_last = ensmean_last.mean(dim = 'time').squeeze()

# %%
fig, axes = plt.subplots(3, 1, figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree(-90)})
ensmean_first.plot.contourf(ax = axes[0], transform = ccrs.PlateCarree(), cmap = 'RdBu_r', levels = np.arange(-0.5, 0.6, 0.1)*1e-5, cbar_kwargs = {'label': 'm^2/s^2'})

ensmean_last.plot.contourf(ax = axes[1], transform = ccrs.PlateCarree(), cmap = 'RdBu_r', levels = np.arange(-0.5, 0.6, 0.1)*1e-5, cbar_kwargs = {'label': 'm^2/s^2'})

(ensmean_last - ensmean_first).plot.contourf(ax = axes[2], transform = ccrs.PlateCarree(), cmap = 'RdBu_r', levels = np.arange(-0.5, 0.6, 0.1)*1e-5, cbar_kwargs = {'label': 'm^2/s^2'})

for ax in axes:
    ax.coastlines()

    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
# %%
