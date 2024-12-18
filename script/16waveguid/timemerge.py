#%%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import logging
logging.basicConfig(level=logging.INFO)
import sys
#%%
period = sys.argv[1]
# %%
def mergetime(period, ens):
    data_path = f'/scratch/m/m300883/waveguide/{period}/r{ens}i1p1f1/'
    to_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_bandvar_{period}/'
    #
    files = glob.glob(data_path + '*.nc')
    files.sort()
    #
    new_filename = files[0].split('/')[-1][:-14]
    time_end_label = files[-1].split('/')[-1].split('_')[-1].split('.')[0][11:]
    # replace the last part of the path (time) with the time of files[-1]
    new_filename = new_filename +'-'+ time_end_label + '.nc'
    #
    data = xr.open_mfdataset(files, combine='by_coords')
    #
    data.to_netcdf(to_path + new_filename)
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

allens = range(21,51)
sing_ens = np.array_split(allens, size)[rank]

for i, ens in enumerate(sing_ens):
    logging.info(f'period {period}, ensemble {ens} rank {rank} {i+1}/{len(sing_ens)}')
    mergetime(period, ens)
    print(f'ensemble {ens} done')
# %%
