#%%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import os
import glob
import logging
import src. compute.slurm_cluster as scluster

logging.basicConfig(level=logging.INFO)

#%%
client, cluster = scluster.init_dask_slurm_cluster(scale=10, processes= 5, memory='200GB', walltime='08:00:00', dash_address=8989)

#%%
hus = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/ERA5/hus_daily_std_mergeyear/*.nc", combine = 'by_coords')
hus = hus.var133.squeeze()
#%%
tas = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/ERA5/tas_daily_std_mergeyear/*.nc", combine = 'by_coords')
tas = tas.var130.squeeze()
#%%
# rechunk
hus = hus.chunk({"time": -1})
tas = tas.chunk({"time": -1})
#%%
data = xr.Dataset({"tas": tas, "hus": hus*1000})

# %%
# select the data where the tas is above the 10th percentile
tas_lim = data.tas.quantile(0.1, dim = ('time'))
data = data.where(data.tas >= tas_lim, drop = True)
# %%
ratio_hus = data.hus / data.tas

#%%
ratio_hus_mean = ratio_hus.mean(dim = ('time'))
#%%
ratio_hus_mean.name = 'hus_tas_ratio'

# %%
file_name = "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/moisture_variability_stat/hus_tas_daily_std_sel_timmean.nc"

ratio_hus_mean.to_netcdf(file_name)

# %%
