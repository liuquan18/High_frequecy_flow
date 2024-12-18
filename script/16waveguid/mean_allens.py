#%%
import numpy as np
import xarray as xr
# %%
period = 'last10'

# read mean 
band_means = xr.open_mfdataset(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_bandmean_{period}/*.nc', combine = 'nested', concat_dim = 'ens')
band_means.load()
try:
    band_means = band_means.__xarray_dataarray_variable__
except AttributeError:
    band_means = band_means.va
mean = band_means.mean(dim = 'ens')

mean.to_netcdf(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_bandmean_allens/va_bandmean_{period}_all.nc')
# %%
