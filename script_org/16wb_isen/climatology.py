#%%
import xarray as xr
import numpy as np
from src.data_helper.read_variable import read_prime

# %%
def compute_climatology(variable, name):
    awb_1850 = read_prime(1850, var=variable, name=name, model_dir='MPI_GE_CMIP6', suffix = '')
    
    awb_2090 = read_prime(2090, var=variable, name=name, model_dir='MPI_GE_CMIP6', suffix = '')
    
    awb_1850_mean = awb_1850.mean(dim=['ens', 'time'])
    awb_2090_mean = awb_2090.mean(dim=['ens', 'time'])
    
    awb_1850_mean.to_netcdf(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0climatology/{variable}_1850.nc')
    awb_2090_mean.to_netcdf(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0climatology/{variable}_2090.nc')
        
# %%
#%%
compute_climatology('pv', 'pv')