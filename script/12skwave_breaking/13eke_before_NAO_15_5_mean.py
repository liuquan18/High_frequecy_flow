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
import os

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
def read_eke( decade, suffix = '_ano', var='eke', **kwargs):
    time_tag = f"{decade}0501-{decade+9}0930"
    data_path = (
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily{suffix}/"
    )
    files = glob.glob(data_path + "r*i1p1f1/" + f"eke*{time_tag}*.nc")
    # sort files
    files.sort(key=lambda x: int(x.split('/')[-2][1:].split('i')[0]))

    data = xr.open_mfdataset(
        files, combine="nested", concat_dim="ens",
        chunks = {"ens": 1, "time": -1, "lat": -1, "lon": -1, "plev": 1}
    )
    data = data['eke']
    data = data.sel(plev = 50000)


    data['ens'] = range(1, 51)

    return data

    
#%%
def read_all_data(decade, var):
    logging.info("reading NAO extremes")
    # wave breaking
    NAO_pos = read_NAO_extremes(decade, 'positive')
    NAO_neg = read_NAO_extremes(decade, 'negative')

    logging.info("reading eke")
    eke = read_eke( decade, var = var, suffix='_ano')  # change the suffix to read different data
    

    return NAO_pos, NAO_neg, eke
#%%
def before_NAO_mean(NAO, data, lag = (-15, -5)):

    data_before_NAO = []
    for i, event in NAO.iterrows():
        event_ens = int(event.ens)
        event_date = pd.to_datetime(event.extreme_start_time)
        event_date_before_start = event_date + pd.Timedelta(days=lag[0])
        event_date_before_end = event_date + pd.Timedelta(days=lag[1])

        # -15 to -5 days before the event average
        data_NAO_event = data.sel(time=slice(event_date_before_start, event_date_before_end), ens = event_ens).mean(dim = 'time')

        data_before_NAO.append(data_NAO_event)

    data_before_NAO = xr.concat(data_before_NAO, dim='event')

    return data_before_NAO


#%%
def process_data(decade, var):
    # read data
    NAO_pos, NAO_neg, data = read_all_data(decade, var = var)

    # select data before NAO events, here 'var' is only for column name
    logging.info (f"rank {rank} is selecting data for {decade} \n")
    eke_NAO_pos = before_NAO_mean(NAO_pos, data)
    eke_NAO_neg = before_NAO_mean(NAO_neg, data)

    logging.info(f"rank {rank} is saving data for decade {decade} \n")
    save_dir_pos=f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_NAO_pos_15_5_mean_{decade}.nc'
    save_dir_neg=f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_NAO_neg_15_5_mean_{decade}.nc'


    eke_NAO_pos.to_netcdf(save_dir_pos)
    eke_NAO_neg.to_netcdf(save_dir_neg)


#%%

decades = [1850, 2090]
decade = decades[rank]
logging.info(f"rank {rank} is processing decade {decade} \n")
process_data(decade, 'eke')



# %%
