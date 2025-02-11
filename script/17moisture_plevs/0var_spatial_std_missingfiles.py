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
missing_files = [
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r2i1p1f1/hus_day_MPI-ESM1-2-LR_r2i1p1f1_gn_18600501-18690930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r2i1p1f1/hus_day_MPI-ESM1-2-LR_r2i1p1f1_gn_18900501-18990930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r2i1p1f1/hus_day_MPI-ESM1-2-LR_r2i1p1f1_gn_20100501-20190930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r2i1p1f1/hus_day_MPI-ESM1-2-LR_r2i1p1f1_gn_20500501-20590930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r13i1p1f1/hus_day_MPI-ESM1-2-LR_r13i1p1f1_gn_19000501-19090930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r13i1p1f1/hus_day_MPI-ESM1-2-LR_r13i1p1f1_gn_19700501-19790930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r13i1p1f1/hus_day_MPI-ESM1-2-LR_r13i1p1f1_gn_19800501-19890930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r13i1p1f1/hus_day_MPI-ESM1-2-LR_r13i1p1f1_gn_20200501-20290930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r17i1p1f1/hus_day_MPI-ESM1-2-LR_r17i1p1f1_gn_18600501-18690930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r17i1p1f1/hus_day_MPI-ESM1-2-LR_r17i1p1f1_gn_19200501-19290930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r17i1p1f1/hus_day_MPI-ESM1-2-LR_r17i1p1f1_gn_19300501-19390930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r17i1p1f1/hus_day_MPI-ESM1-2-LR_r17i1p1f1_gn_19600501-19690930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r17i1p1f1/hus_day_MPI-ESM1-2-LR_r17i1p1f1_gn_19700501-19790930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r17i1p1f1/hus_day_MPI-ESM1-2-LR_r17i1p1f1_gn_19900501-19990930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r17i1p1f1/hus_day_MPI-ESM1-2-LR_r17i1p1f1_gn_20600501-20690930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r17i1p1f1/hus_day_MPI-ESM1-2-LR_r17i1p1f1_gn_20800501-20890930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r23i1p1f1/hus_day_MPI-ESM1-2-LR_r23i1p1f1_gn_18500501-18590930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r23i1p1f1/hus_day_MPI-ESM1-2-LR_r23i1p1f1_gn_19800501-19890930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r23i1p1f1/hus_day_MPI-ESM1-2-LR_r23i1p1f1_gn_20200501-20290930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r23i1p1f1/hus_day_MPI-ESM1-2-LR_r23i1p1f1_gn_20600501-20690930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r26i1p1f1/hus_day_MPI-ESM1-2-LR_r26i1p1f1_gn_19100501-19190930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r26i1p1f1/hus_day_MPI-ESM1-2-LR_r26i1p1f1_gn_19300501-19390930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r26i1p1f1/hus_day_MPI-ESM1-2-LR_r26i1p1f1_gn_19400501-19490930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r26i1p1f1/hus_day_MPI-ESM1-2-LR_r26i1p1f1_gn_19500501-19590930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r26i1p1f1/hus_day_MPI-ESM1-2-LR_r26i1p1f1_gn_19900501-19990930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r26i1p1f1/hus_day_MPI-ESM1-2-LR_r26i1p1f1_gn_20100501-20190930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r26i1p1f1/hus_day_MPI-ESM1-2-LR_r26i1p1f1_gn_20800501-20890930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r26i1p1f1/hus_day_MPI-ESM1-2-LR_r26i1p1f1_gn_20900501-20990930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r28i1p1f1/hus_day_MPI-ESM1-2-LR_r28i1p1f1_gn_19200501-19290930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r28i1p1f1/hus_day_MPI-ESM1-2-LR_r28i1p1f1_gn_19700501-19790930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r28i1p1f1/hus_day_MPI-ESM1-2-LR_r28i1p1f1_gn_20200501-20290930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r28i1p1f1/hus_day_MPI-ESM1-2-LR_r28i1p1f1_gn_20700501-20790930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r33i1p1f1/hus_day_MPI-ESM1-2-LR_r33i1p1f1_gn_18500501-18590930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r33i1p1f1/hus_day_MPI-ESM1-2-LR_r33i1p1f1_gn_19000501-19090930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r33i1p1f1/hus_day_MPI-ESM1-2-LR_r33i1p1f1_gn_19600501-19690930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r33i1p1f1/hus_day_MPI-ESM1-2-LR_r33i1p1f1_gn_19900501-19990930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r44i1p1f1/hus_day_MPI-ESM1-2-LR_r44i1p1f1_gn_18900501-18990930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r44i1p1f1/hus_day_MPI-ESM1-2-LR_r44i1p1f1_gn_19900501-19990930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r44i1p1f1/hus_day_MPI-ESM1-2-LR_r44i1p1f1_gn_20200501-20290930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r44i1p1f1/hus_day_MPI-ESM1-2-LR_r44i1p1f1_gn_20800501-20890930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r46i1p1f1/hus_day_MPI-ESM1-2-LR_r46i1p1f1_gn_18500501-18590930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r46i1p1f1/hus_day_MPI-ESM1-2-LR_r46i1p1f1_gn_19200501-19290930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r46i1p1f1/hus_day_MPI-ESM1-2-LR_r46i1p1f1_gn_19600501-19690930.nc",
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily/r46i1p1f1/hus_day_MPI-ESM1-2-LR_r46i1p1f1_gn_20100501-20190930.nc"
]
# %%
missing_files_single = np.array_split(missing_files, size)[rank]

for i, file in enumerate(missing_files):
    logging.info(f"rank {rank} Processing {i+1}/{len(missing_files)}")

    to_file = file.replace('hus_daily', 'hus_daily_std')
    
    ds = xr.open_dataset(file, chunks = {'time': 5, 'plev': 1})
    ds = ds['hus']

    lon_window = 33
    lat_window = 5

    ds_std = lc.rolling_lon_periodic(ds, lon_window, lat_window, stat = 'std')
    ds_std.to_netcdf(to_file)
    ds.close()
    ds_std.close()

# %%
