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
from src.index_generate.project_index import project_field_to_pattern
# %%
logging.basicConfig(level=logging.INFO)

# %%
daily_dir = "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_daily_rm_trend/"

daily_files = glob.glob(f"{daily_dir}*.nc")
# %%
eof_file = "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/EOF_result/eof_result_Z500_1979_2024.nc"
# %%
pc_dir = "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/pc_nonstd/"
# %%

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()

if rank == 0:
    if not os.path.exists(pc_dir):
        os.makedirs(pc_dir)
    logging.info(f"size is {size}")
#%%
daily_files_single = np.array_split(daily_files, size)[rank]  # years on this core
# %%
for i, daily_file in enumerate(daily_files_single):
    logging.info(f"Rank {rank}, file {daily_file} {i}/{len(daily_files_single)}")
    daily_field = xr.open_dataset(daily_file).var129.squeeze()
    eof = xr.open_dataset(eof_file).eof.sel(mode = 'NAO').squeeze()
    eof['plev'] = 50000

    try:
        daily_field['time'] = pd.to_datetime(daily_field.time.values)

    except:
        logging.info("Time already in datetime format")
        pass

    projected_pcs = project_field_to_pattern(daily_field, eof, standard=False, plev = None)
    projected_pcs.name = "pc"
    projected_pcs.to_netcdf(f"{pc_dir}{os.path.basename(daily_file).replace('rm_trend','NAO')}")