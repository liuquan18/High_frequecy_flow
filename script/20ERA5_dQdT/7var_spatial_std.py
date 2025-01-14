# %%
import xarray as xr
import numpy as np
import sys
import os
import glob
# %%
import src.moisture.longitudinal_contrast as lc

import logging
logging.basicConfig(level=logging.INFO)
#%%
# nodes for different ensemble members
var = sys.argv[1] # 'tas' or 'hur'
#%%
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # [0,1,2,3,4,5,6,7,8,9]
    size = comm.Get_size()  # 10
except:
    logging.warning("::: Warning: Proceeding without mpi4py! :::")
    rank = 0
    size = 1
#%%
from_path = f'/work/mh0033/m300883/High_frequecy_flow/data/ERA5/{var}_daily/'
to_path = f'/work/mh0033/m300883/High_frequecy_flow/data/ERA5/{var}_daily_std/'

if rank == 0:
    if not os.path.exists(to_path):
        os.makedirs(to_path)


#%%
all_files = glob.glob(from_path + "*.nc")
files_core = np.array_split(all_files, size)[rank]

# %%
for i, file in enumerate(files_core):
    logging.info(f"rank {rank} Processing {i+1}/{len(files_core)}")
    ds = xr.open_dataset(file, chunks = {'time': 1})
    if var == 'tas':
        var_code = 'var130'
    elif var == 'hus':
        var_code = 'var133'

    ds = ds[var_code]
    # lon interval 0.28125 deg, lat interval 0.27
    # 
    lon_window = 200 # 60/0.28125
    lat_window = 30 # 10/0.27
    ds_std = lc.rolling_lon_periodic(ds, lon_window, lat_window, stat = 'std')
    ds_std.to_netcdf(to_path + file.split('/')[-1])
    ds.close()
    ds_std.close()
    
# %%
