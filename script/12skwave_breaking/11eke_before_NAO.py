# %%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import logging
import re

from src.extremes.before_extreme import read_NAO_extremes, sel_before_NAO
logging.basicConfig(level=logging.INFO)
#%%
# nodes for different decades
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # [0,1,2,3,4,5,6,7,8,9]
    size = comm.Get_size()  # 10

except:
    logging.warning("::: Warning: Proceeding without mpi4py! :::")
    rank = 0
    size = 1

if rank == 0:
    logging.info(f"::: Running on {size} cores :::")



#%%
def read_eke( decade, suffix = '_ano_2060N', var='eke', **kwargs):
    time_tag = f"{decade}0501-{decade+9}0930"
    data_path = (
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily{suffix}/"
    )
    files = glob.glob(data_path + "r*i1p1f1/" + f"eke*{time_tag}*.nc")
    # sort files
    files.sort(key=lambda x: int(x.split('/')[-2][1:].split('i')[0]))

    data = xr.open_mfdataset(
        files, combine="nested", concat_dim="ens",
        chunks = {"ens": -1, "time": -1, "lat": -1, "lon": -1}
    )
    data = data['eke']
    data.load()

    try:
        data = data.drop_vars(('plev','lat'))
    except ValueError:
        try:
            data = data.drop_vars(('lat'))
        except ValueError:
            pass

    data['ens'] = range(1, 51)
    # change longitude from 0-360 to -180-180
    data = data.assign_coords(lon=(data.lon + 180) % 360 - 180).sortby("lon")

    return data

    
#%%
def read_all_data(decade, var):
    logging.info("reading NAO extremes")
    # wave breaking
    NAO_pos = read_NAO_extremes(decade, 'positive')
    NAO_neg = read_NAO_extremes(decade, 'negative')

    logging.info("reading eke")
    eke = read_eke( decade, var = var, suffix='_ano_3060N')  # change the suffix to read different data
    

    return NAO_pos, NAO_neg, eke



#%%
def process_data(decade, var):
    # read data
    NAO_pos, NAO_neg, data = read_all_data(decade, var = var)

    # select data before NAO events, here 'var' is only for column name
    logging.info (f"rank {rank} is selecting data for {decade} \n")
    eke_NAO_pos = sel_before_NAO(NAO_pos, data, var = 'eke')
    eke_NAO_neg = sel_before_NAO(NAO_neg, data, var = 'eke')

    logging.info(f"rank {rank} is saving data for decade {decade} \n")

    eke_NAO_pos.to_csv(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_NAO_pos/{var}_NAO_pos_{decade}.csv')
    eke_NAO_neg.to_csv(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_NAO_neg/{var}_NAO_neg_{decade}.csv')
    
#%%
decades_all = np.arange(1850, 2100, 10)
decade_single = np.array_split(decades_all, size)[rank]
var = sys.argv[1] # 'eke' or 'eke_high'

#%%
for decade in decade_single:
    logging.info(f"rank {rank} is processing decade {decade} \n")
    process_data(decade, var = var)

# %%
