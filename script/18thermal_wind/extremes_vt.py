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
def extract_extreme_1year(data, threshold, gorl, var = 'vt'):
    EE = ct.contrack()
    EE.ds = data

    EE.set_up(force=True)
    EE.run_contrack(
        variable=var,
        threshold=threshold, # quantile 0.99 of [30, 60] lat mean, 13.2/-14.7 m/s for vt
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
        threshold=threshold, 
        gorl = gorl,
        overlap=0.5,
        persistence=5,
        twosided=True,
    )

    EE_df = EE.run_lifecycle(flag = 'flag', variable=var)
    EE_df = EE_df.dropna(axis = 0, how = 'any')
    EE_df = EE_df.to_xarray()

    return EE_df
# %%
def extract_extremes(data, threshold, gorl = '>=', var = 'tas'):

    extremes = data.groupby('time.year').apply(extract_extreme_1year, threshold = threshold, gorl = gorl, var = var)
    cycles = data.groupby('time.year').apply(run_cycle_1year, threshold = threshold, gorl = gorl, var = var)
    
    cycles = cycles.to_dataframe().reset_index().dropna(axis = 0, how = 'any' )
    # drop column 'index'
    cycles = cycles.drop(columns = 'index')
    cycles['Flag_unique'] = cycles['year']*1000 + cycles['Flag']


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
data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily/r{member}i1p1f1/"
extreme_pos_path= f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily_extremes_pos/r{member}i1p1f1/"
cycle_pos_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily_cycles_pos/r{member}i1p1f1/"

extreme_neg_path= f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily_extremes_neg/r{member}i1p1f1/"
cycle_neg_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily_cycles_neg/r{member}i1p1f1/"

if rank == 0:
    if not os.path.exists(extreme_pos_path):
        os.makedirs(extreme_pos_path)
    if not os.path.exists(cycle_pos_path):
        os.makedirs(cycle_pos_path)

    if not os.path.exists(extreme_neg_path):
        os.makedirs(extreme_neg_path)

    if not os.path.exists(cycle_neg_path):
        os.makedirs(cycle_neg_path)

    logging.error(f"Processing ensemble member {node}")

# %%
all_files =  glob.glob(data_path + "*.nc")
single_files = np.array_split(all_files, size)[rank]
# %%
for i, daily_file in enumerate(single_files):
    logging.error(f"rank {rank} Processing {i+1}/{len(single_files)}")

    data = xr.open_dataset(daily_file)

    var = 'vt'    
    extremes_pos, cycles_pos = extract_extremes(data, threshold = 13.2, gorl='>=', var = var)
    extremes_neg, cycles_neg = extract_extremes(data, threshold = -14.7, gorl='<=', var = var)


    outname = daily_file.split('/')[-1]

    # replace 'day' with 'extreme'
    extreme_name = outname.replace('day', 'extreme_')
    cycle_name = outname.replace('day', 'cycle').replace('.nc', '.csv')

    extremes_pos.flag.to_netcdf(extreme_pos_path + extreme_name)
    cycles_pos.to_csv(cycle_pos_path + cycle_name, index = False)

    extremes_neg.flag.to_netcdf(extreme_neg_path + extreme_name)
    cycles_neg.to_csv(cycle_neg_path + cycle_name, index = False)

    data.close()
# %%
