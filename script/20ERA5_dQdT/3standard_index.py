#%%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import logging
import glob
import os
# %%
import mpi4py.MPI as MPI
# %%
logging.basicConfig(level=logging.INFO)

# %%
pc_nonstd_dir = "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/pc_nonstd/"
# %%
daily_files = glob.glob(f"{pc_nonstd_dir}*.nc")
# %%

pc_nonstd = xr.open_mfdataset(daily_files, combine = 'by_coords')
#%%
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()

if rank == 0:
    logging.info(f"size is {size}")

# %%
pc_files = np.array_split(daily_files, size)[rank]  # years on this core
# %%
for i, pc_file in enumerate(pc_files):
    logging.info(f"Rank {rank}, file {pc_file} {i}/{len(pc_files)}")
    pc = xr.open_dataset(pc_file).pc
    pc_mean - 