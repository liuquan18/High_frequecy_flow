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
node = sys.argv[1]
var = sys.argv[2] # 'tas' or 'hur'
member = node
logging.info(f"This node is processing {var} ensemble member {member}")
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
from_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily/r{member}i1p1f1/'
to_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily_std/r{member}i1p1f1/'

if rank == 0:
    if not os.path.exists(to_path):
        os.makedirs(to_path)

#%%
all_files = glob.glob(from_path + "*.nc")
files_core = np.array_split(all_files, size)[rank]

# %%
for i, file in enumerate(files_core):
    logging.info(f"rank {rank} Processing {i+1}/{len(files_core)}")
    ds = xr.open_dataset(file, chunks = {'time': 50})
    ds = ds[var]
    lon_window = 33
    lat_window = 5
    ds_std = lc.rolling_lon_periodic(ds, lon_window, lat_window, stat = 'std')
    ds_std.to_netcdf(to_path + file.split('/')[-1])
    ds.close()
    ds_std.close()
    
# %%
