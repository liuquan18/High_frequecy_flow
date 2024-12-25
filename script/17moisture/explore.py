#%%
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import sys
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
logging.basicConfig(level=logging.INFO)

#%%
import src.waveguide.band_statistics as bs
#%%
import importlib
importlib.reload(bs)


# %%
hur = xr.open_dataset("/pool/data/CMIP6/data/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r10i1p1f1/day/hur/gn/v20190710/hur_day_MPI-ESM1-2-LR_historical_r10i1p1f1_gn_18500101-18691231.nc").hur
# %%
tas = xr.open_dataset("/pool/data/CMIP6/data/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r10i1p1f1/day/tas/gn/v20190710/tas_day_MPI-ESM1-2-LR_historical_r10i1p1f1_gn_18500101-18691231.nc").tas
# %%
hur = hur.sel(plev = slice(100000, 85000))

#%%
weights = hur.plev
weights.name = "weights"
weights
# %%
hur_weighted = hur.weighted(weights)
# %%
hur_weighted_mean = hur_weighted.mean(dim = 'plev')
# %%
hur = hur_weighted_mean.sel(time = slice('1850-06-01', '1850-06-03'))
tas = tas.sel(time = slice('1850-06-01', '1850-06-03'))

# %%
def rolling_lon_periodic(arr, lon_window, lat_window, stat = 'std'):
    extended_arr = xr.concat([arr, arr], dim='lon')
    if stat == 'mean':
        rolled_result = extended_arr.rolling(lon=lon_window, lat=lat_window, center=True).mean()
    elif stat == 'std':
        rolled_result = extended_arr.rolling(lon=lon_window, lat=lat_window, center=True).std()
    elif stat == 'var':
        rolled_result = extended_arr.rolling(lon=lon_window, lat=lat_window, center=True).var()
    else:
        raise ValueError(f"Unsupported stat: {stat}")
    original_size = arr.sizes['lon']
    final_result = rolled_result.isel({'lon': slice(original_size-lon_window//2, 2*original_size-lon_window//2)})
    return final_result.sortby('lon')
# %%
hur_rolled = rolling_lon_periodic(hur, 33, 5, 'std')
# %%
tas_rolled = rolling_lon_periodic(tas, 33, 5, 'std')
# %%
hur_tas_ratio_rolled = hur_rolled / tas_rolled
# %%
# plot hur_tas_ratio with cartopy
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree(100))
hur_tas_ratio_rolled.isel(time = 0).plot(ax=ax, transform=ccrs.PlateCarree(), cmap = 'coolwarm', levels = np.arange(0,10,1))
ax.coastlines()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/rolling_hur_tas_ratio_ex.png")

# %%
# hur rolled std
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree(100))
hur_rolled.isel(time = 0).plot(ax=ax, transform=ccrs.PlateCarree(), cmap = 'coolwarm', levels=np.arange(0, 30,1))
ax.coastlines()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/rolling_hur_std_ex.png")
# %%
# tas rolled std
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree(100))
tas_rolled.isel(time = 0).plot(ax=ax, transform=ccrs.PlateCarree(), cmap = 'coolwarm', levels=np.arange(0, 10,1))
ax.coastlines()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/rolling_tas_std_ex.png")
# %%
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree(100))
tas.isel(time = 0).plot(ax=ax, transform=ccrs.PlateCarree(), cmap = 'coolwarm')
ax.coastlines()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/tas_ex.png")
# %%
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree(100))
hur.isel(time = 0).plot(ax=ax, transform=ccrs.PlateCarree(), cmap = 'coolwarm')
ax.coastlines()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/hur_ex.png")
# %%
