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

    EE_df = EE.run_lifecycle(flag = 'flag', variable=var)

    return EE.dataset, EE_df

# %%
def extract_extremes(data, threshold, gorl = '>=', var = 'vt'):

    extremes_all = []
    cycles_all = []

    for year in np.unique(data.time.dt.year.values):
        logging.error(f"Processing year {year}")
        data_year = data.sel(time = str(year))
        extremes_year, cycles_year= extract_extreme_1year(data_year, threshold = threshold, gorl = gorl, var = var)

        extremes_all.append(extremes_year)
        cycles_all.append(cycles_year)

    extremes = xr.concat(extremes_all, dim = 'time')
    cycles = pd.concat(cycles_all, axis = 0)

    return extremes, cycles


# %%
# nodes for different ensemble members
node = sys.argv[1]
var = 'vt' # tas, hus, vt
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
data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily_ano/r{member}i1p1f1/"
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


#%%
all_files =  glob.glob(data_path + "*.nc")
single_files = np.array_split(all_files, size)[rank]
# %%
for i, daily_file in enumerate(single_files):
    logging.error(f"rank {rank} Processing {i+1}/{len(single_files)}")


    data = xr.open_dataset(daily_file)
    data = data.load()

    var = 'vt'    
    extremes_pos, cycles_pos = extract_extremes(data, threshold = 15, gorl='>=', var = var)
    extremes_neg, cycles_neg = extract_extremes(data, threshold = -15, gorl='<=', var = var)


    outname = daily_file.split('/')[-1]

    # replace 'day' with 'extreme'
    extreme_name = outname.replace('day', 'extreme')
    cycle_name = outname.replace('day', 'cycle').replace('.nc', '.csv')

    extremes_pos.flag.to_netcdf(extreme_pos_path + extreme_name)
    cycles_pos.to_csv(cycle_pos_path + cycle_name, index = False)

    extremes_neg.flag.to_netcdf(extreme_neg_path + extreme_name)
    cycles_neg.to_csv(cycle_neg_path + cycle_name, index = False)

    data.close()
# %%
