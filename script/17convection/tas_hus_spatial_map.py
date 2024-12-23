#%%
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


from src.moisture.longitudinal_contrast import read_data
# %%
first_tas = read_data("tas", 1850, False, False)
first_hus = read_data("hus", 1850, False, False)
first_data = xr.Dataset({"tas": first_tas, "hus": first_hus})

# %%

last_tas = read_data("tas", 2090, False, False)
last_hus = read_data("hus", 2090, False, False)
last_data = xr.Dataset({"tas": last_tas, "hus": last_hus})
# %%
# first_mean = first_data.mean(dim = ('time', 'ens'))
# last_mean = last_data.mean(dim = ('time', 'ens'))

# #%%
# first_mean.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_mean.nc")
# last_mean.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_mean.nc")

# #%%
# first_data.load()
# last_data.load()
# first_qu95 = first_data.quantile(0.95, dim = ('time', 'ens'))
# last_qu95 = last_data.quantile(0.95, dim = ('time', 'ens'))

# first_qu95.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_qu95.nc")
# last_qu95.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_qu95.nc")

#%%
first_mean = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_mean.nc")
last_mean = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_mean.nc")

first_qu95 = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_qu95.nc")
last_qu95 = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_qu95.nc")

#%%
temp_cmap = np.loadtxt("/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/temp_div.txt")
temp_cmap = mcolors.ListedColormap(temp_cmap, name='temp_div')

prec_cmap = np.loadtxt("/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_div.txt")
prec_cmap = mcolors.ListedColormap(prec_cmap, name='prec_div')


#%%
# %%
fig, axes = plt.subplots(4, 1, figsize = (12, 6), subplot_kw={'projection': ccrs.PlateCarree(100)})
first_mean.tas.plot(ax = axes[0], transform=ccrs.PlateCarree(), cmap = temp_cmap, cbar_kwargs = {'label': 'Temperature (K)'})
axes[0].set_title("1850-1859")
axes[0].coastlines()
axes[0].set_global()
# %%
