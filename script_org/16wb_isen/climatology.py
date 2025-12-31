#%%
import xarray as xr
import numpy as np
from src.data_helper.read_variable import read_prime
# %%
awb_1850 = read_prime(1850, var='wb_anticyclonic_allisen', name='smooth_pv', model_dir='MPI_GE_CMIP6', suffix = '')
# %%
awb_2090 = read_prime(2090, var='wb_anticyclonic_allisen', name='smooth_pv', model_dir='MPI_GE_CMIP6', suffix = '')
# %%
awb_1850_mean = awb_1850.mean(dim=['ens', 'time'])
awb_2090_mean = awb_2090.mean(dim=['ens', 'time'])
# %%
awb_1850_mean.to_netcdf('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0climatology/wb_anticyclonic_allisen_1850.nc')
awb_2090_mean.to_netcdf('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0climatology/wb_anticyclonic_allisen_2090.nc')
# %%
cwb_1850 = read_prime(1850, var='wb_cyclonic_allisen', name='smooth_pv', model_dir='MPI_GE_CMIP6', suffix = '')
cwb_2090 = read_prime(2090, var='wb_cyclonic_allisen', name='smooth_pv', model_dir='MPI_GE_CMIP6', suffix = '')
# %%
cwb_1850_mean = cwb_1850.mean(dim=['ens', 'time'])
cwb_2090_mean = cwb_2090.mean(dim=['ens', 'time'])
# %%
cwb_1850_mean.to_netcdf('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0climatology/wb_cyclonic_allisen_1850.nc')
cwb_2090_mean.to_netcdf('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0climatology/wb_cyclonic_allisen_2090.nc')
# %%