#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from src.compute.slurm_cluster import init_dask_slurm_cluster


#%%
client, cluster = init_dask_slurm_cluster(scale =2, processes=20, memory='200GB', walltime='08:00:00')
# %%
period = 'first10'
#%%
first_va = xr.open_mfdataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_MJJAS_{period}/*.nc",
                             combine='nested', concat_dim='ens').va
# rechunk data
#%%
first_va = first_va.chunk({'ens':1, 'lat':96, 'lon':192, 'plev':1, 'time':-1})

#%%
first_va = first_va.sel(plev=25000)
first_va_var = first_va.sel(lat = slice(30,60)).var()
first_va_var.to_netcdf(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/band_variance/{period}_var_midlat.nc")

# %%
last_va = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_MJJAS_last10/*.nc",
                                combine='nested', concat_dim='ens').va
# rechunk data
last_va = last_va.chunk({'ens':1, 'lat':96, 'lon':192, 'plev':1, 'time':-1})
last_va = last_va.sel(plev=25000)
last_va_var = last_va.sel(lat = slice(30,60)).var()
last_va_var.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/band_variance/last_var_midlat.nc")


# %%
