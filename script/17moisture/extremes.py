#%%
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec
import glob
import logging
import sys
import os
logging.basicConfig(level=logging.ERROR)
# %%
import src.ConTrack.contrack as ct
#%%
import importlib
importlib.reload(ct)

# %%
def extract_extreme_1year(data, threshold, gorl = '>=', var = 'tas'):
    EE = ct.contrack()
    EE.ds = data

    EE.set_up(force=True)
    EE.run_contrack(
        variable=var,
        threshold=threshold, # quantile 0.99 of [0, 60] lat mean, 3.62 K for tas,  2 g/kg for hus, 12/-12 m/s for vt
        gorl = gorl,
        overlap=0.5,
        persistence=5,
        twosided=True,
    )

    return EE.dataset

def run_cycle_1year(data, threshold, gorl = '>=', var = 'tas'):
    EE = ct.contrack()
    EE.ds = data

    EE.set_up(force=True)
    EE.run_contrack(
        variable=var,
        threshold=threshold, # quantile 0.99 of [0, 60] lat mean, 3.62 K for tas,  2 g/kg for hus, 12/-12 m/s for vt
        gorl = gorl,
        overlap=0.5,
        persistence=5,
        twosided=True,
    )

    EE_df = EE.run_lifecycle(flag = 'flag', variable=var)
    EE_df = EE_df.to_xarray()

    # drop na if row is all na
    EE_df = EE_df.dropna(axis = 0, how = 'all')
    
    return EE_df
# %%
def extract_extremes(data, threshold, gorl = '>=', var = 'tas'):

    extremes = data.groupby('time.year').apply(extract_extreme_1year, threshold = threshold, gorl = gorl, var = var)
    cycles = data.groupby('time.year').apply(run_cycle_1year, threshold = threshold, gorl = gorl, var = var)
    
    cycles = cycles.to_dataframe().reset_index().dropna(axis = 0, how = 'any' )
    # drop column 'index'
    cycles = cycles.drop(columns = 'index')
    cycles['Flag'] = cycles['year']*1000 + cycles['Flag']



    return extremes, cycles


# %%
# nodes for different ensemble members
node = sys.argv[1]
var = sys.argv[2] # tas, hus, vt
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
member = node
data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily_std/r{member}i1p1f1/"
extreme_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily_extremes/r{member}i1p1f1/"
cycle_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily_cycles/r{member}i1p1f1/"
if rank == 0:
    if not os.path.exists(extreme_path):
        os.makedirs(extreme_path)
    if not os.path.exists(cycle_path):
        os.makedirs(cycle_path)

    logging.error(f"Processing ensemble member {node}")

# %%
all_files =  glob.glob(data_path + "*.nc")
single_files = np.array_split(all_files, size)[rank]
# %%
for i, daily_file in enumerate(single_files):
    logging.error(f"rank {rank} Processing {i+1}/{len(single_files)}")

    data = xr.open_dataset(daily_file)

    if var == 'tas':
        threshold = 3.62
    elif var == 'hus':
        data = data * 1000 # change unit to g/kg
        threshold = 2
    
    extremes, cycles = extract_extremes(data, threshold = threshold, var = var)


    outname = daily_file.split('/')[-1]

    # replace 'day' with 'extreme'
    extreme_name = outname.replace('day', 'extreme')
    cycle_name = outname.replace('day', 'cycle').replace('.nc', '.csv')

    extremes.flag.to_netcdf(extreme_path + extreme_name)
    cycles.to_csv(cycle_path + cycle_name, index = False)

    data.close()