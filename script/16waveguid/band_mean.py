# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from xarray.groupers import UniqueGrouper
import logging
import sys
import glob
import logging
from src.compute.slurm_cluster import init_dask_slurm_cluster
from src.waveguide.band_statistics import band_mean   
import os

logging.basicConfig(level=logging.INFO)

# %%
# nodes and cores
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
stat = 'mean'
# get period from command line
period = sys.argv[1]

from_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_MJJAS_{period}/'
to_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_band{stat}_{period}/'

# mkdir to_dir if it does not exist
if not os.path.exists(to_dir):
    os.makedirs(to_dir)

files = glob.glob(from_dir + "*.nc")
files_single = np.array_split(files, size)[rank] # each node process 5 of the files, totally 10 nodes are used

# allocate 10 dask clusters
client, cluster = init_dask_slurm_cluster(scale =1, processes=20, memory='200GB', walltime='08:00:00')

for file in files_single:
    logging.info(f"processing {os.path.basename(file)}")

    v_data = xr.open_dataset(file, chunks={
        'lat':96,
        'lon':192,
        'plev':1,
        'time':-1
    }).va
    v_data = v_data.sel(plev=25000).sel(lat=slice(0, 90))

    # weight data with cos(lat)
    v_data = v_data * np.cos(np.deg2rad(v_data.lat))

    mean = band_mean(v_data)
    mean.to_netcdf(to_dir + f'{os.path.basename(file)}')

# %%
