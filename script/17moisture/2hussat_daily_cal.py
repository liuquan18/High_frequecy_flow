#%%
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
member = node
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
hus_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_daily/r{member}i1p1f1/'
hur_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hur_daily/r{member}i1p1f1/'
# %%
hussat_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hussat_daily/r{member}i1p1f1/'
if rank == 0:
    if not os.path.exists(hussat_path):
        os.makedirs(hussat_path)
    logging.info(f"This node is processing ensemble member {member}")

#%%
all_decs = np.arange(1850, 2100, 10)
single_decs = np.array_split(all_decs, size)[rank]
# %%
for i, dec in enumerate(single_decs):
    logging.info(f"rank {rank} Processing {dec}, {i+1}/{len(single_decs)}")
    end_dec = dec + 9
    hus_file = glob.glob(hus_path + f'*{dec}0501-{end_dec}0930.nc')
    hur_file = glob.glob(hur_path + f'*{dec}0501-{end_dec}0930.nc')


    hus = xr.open_dataset(hus_file[0], chunks = {'time': -1})
    hur = xr.open_dataset(hur_file[0], chunks = {'time': -1})

    hus = hus.hus
    hur = hur.hur/100

    hussat = hus/hur

    hussat.name = 'hussat'
    hussat_filename = hus_file[0].split('/')[-1].replace('hus', 'hussat')

    hussat.to_netcdf(hussat_path + hussat_filename)
