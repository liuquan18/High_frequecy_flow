# %%
import xarray as xr
import numpy as np
import sys
import os
import glob
import pandas as pd
# %%
import src.moisture.longitudinal_contrast as lc
import src. compute.slurm_cluster as scluster

import logging
logging.basicConfig(level=logging.INFO)

#%%
client, cluster = scluster.init_dask_slurm_cluster(scale=10, processes= 10, memory='200GB', walltime='08:00:00', dash_address=8989)

#%%
var = sys.argv[1] # tas or hus
base_dir=f'/work/mh0033/m300883/High_frequecy_flow/data/ERA5/{var}_daily/'

files = glob.glob(base_dir+'*.nc')


#%%
for file in files:
    logging.info(f'Reading {os.path.basename(file)}')
    ds = xr.open_dataset(file, chunks={'time': 1, 'lat':120, 'lon':800})

    if 'tas' in file:
        var_code = 'var130'
    elif 'hus' in file:
        var_code = 'var133'

    ds = ds[var_code]
    # lon interval 0.28125 deg, lat interval 0.27
    # 
    lon_window = 200 # 60/0.28125
    lat_window = 30 # 10/0.27
    ds_std = lc.rolling_lon_periodic(ds, lon_window, lat_window, stat = 'std')

    outfile=file.replace('_daily', '_daily_std')
    logging.info(f'Saving to {outfile}')
    ds_std.to_netcdf(outfile)

    ds.close()
    ds_std.close()


# %%
