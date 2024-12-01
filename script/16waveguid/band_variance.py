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
from src.waveguide.band_statistics import band_variance
import os

logging.basicConfig(level=logging.INFO)

# %%
# nodes and cores
period = sys.argv[1]
node = int(sys.argv[2]) # node =  0-14

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
stat = 'var'


#%%
from_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_MJJAS_{period}/'
to_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_band{stat}_{period}/'

# mkdir to_dir if it does not exist
if not os.path.exists(to_dir):
    os.makedirs(to_dir)

files = glob.glob(from_dir + "*.nc")
files_node = np.array_split(files, 15)[node] # each node process 5 of the files, totally 10 nodes are used


# read mean 
band_means = xr.open_mfdataset(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_bandmean_allens/va_bandmean_{period}_all.nc').__xarray_dataarray_variable__

for i, file in enumerate(files_node):
    logging.info("*************************")
    logging.info(f'node: {node} {i+1}/{len(files_node)}')

    v_data = xr.open_dataset(file, chunks={
        'lat':96,
        'lon':192,
        'plev':1,
        'time':-1
    }).va
    v_data = v_data.sel(plev=25000).sel(lat=slice(0, 90))

    # weight data with cos(lat)
    v_data = v_data * np.cos(np.deg2rad(v_data.lat))


    all_times = v_data.time.values
    single_times = np.array_split(all_times, size)[rank]
    variance_all = []
    for i, time in enumerate(single_times):
        logging.info(f'node: {node} rank: {rank} {i+1}/{len(single_times)}')
        logging.info(time)
        va = v_data.sel(time = time)
        variance = band_variance(va, mean = band_means)

        variance_all.append(variance)


    # collect all ranks
    variance_all = comm.gather(variance_all, root=0)

    if rank == 0:
        variance_all = [item for sublist in variance_all for item in sublist]
        variance = xr.concat(variance_all, dim='time')

        variance.to_netcdf(to_dir + f'{os.path.basename(file)}')
        logging.info(f'{os.path.basename(file)} saved')
# %%
