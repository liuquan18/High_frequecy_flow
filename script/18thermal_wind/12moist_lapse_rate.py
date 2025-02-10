#%%
import xarray as xr
import numpy as np
import sys
import os

import logging
import src.moisture.moist_thermal_wind as mwt

import glob
logging.basicConfig(level=logging.INFO)
# %%
node = sys.argv[1]
member= node

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

# %%
temp_path=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ta_daily/r{member}i1p1f1/"
to_path=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/malr_daily/r{member}i1p1f1/"

if rank == 0:
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    logging.info(f"This node is processing ensemble member {member}")


#%%
all_files = glob.glob(temp_path + "*.nc")
files_core = np.array_split(all_files, size)[rank]

# %%
for i, file in enumerate(files_core):
    logging.info(f"rank {rank} Processing {i+1}/{len(files_core)}")
    ds = xr.open_dataset(file, chunks = {'time': -1})

    ds = ds.ta

    ds.load()

    moist_lp = mwt.malr(ds)

    moist_lp = moist_lp.sel(plev = [100000, 85000]).mean('plev')

    moist_lp.name = 'malr'

    fname = file.split('/')[-1]
    fname = fname.replace('ta', 'malr')
    moist_lp.to_netcdf(to_path + fname)

    ds.close()
    moist_lp.close()

# %%
