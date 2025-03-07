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

from src.extremes.before_extreme import read_NAO_extremes
logging.basicConfig(level=logging.INFO)


#%%
def read_hf( decade, suffix = '_ano', var='eke', name = None, **kwargs):
    """
    read high frequency data
    """
    if name is None:
        name = kwargs.get('name', var) # default name is the same as var
    plev = kwargs.get('plev', 50000)

    time_tag = f"{decade}0501-{decade+9}0930"
    data_path = (
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily{suffix}/"
    )
    files = glob.glob(data_path + "r*i1p1f1/" + f"{var}*{time_tag}*.nc")
    # sort files
    files.sort(key=lambda x: int(x.split('/')[-2][1:].split('i')[0]))

    data = xr.open_mfdataset(
        files, combine="nested", concat_dim="ens",
        chunks = {"ens": 1, "time": -1, "lat": -1, "lon": -1, "plev": 1}
    )
    data = data[name]
    data = data.sel(plev = plev)

    data['ens'] = range(1, 51)

    return data

    
#%%
def read_all_data(decade, var, **kwargs):
    logging.info("reading NAO extremes")
    # wave breaking
    NAO_pos = read_NAO_extremes(decade, 'positive')
    NAO_neg = read_NAO_extremes(decade, 'negative')

    logging.info("reading upvp")
    hf_data = read_hf( decade, var = var, suffix='_ano', **kwargs)  # change the suffix to read different data
    

    return NAO_pos, NAO_neg, hf_data


#%%
def process_data(decade, var):
    # read data
    NAO_pos, NAO_neg, data = read_all_data(decade, var = var, kwargs={'name': 'upvp', 'plev': 25000})

    # select data before NAO events, here 'var' is only for column name
    logging.info (f"selecting data for {decade} \n")
    eke_NAO_pos = before_NAO_mean(NAO_pos, data)
    eke_NAO_neg = before_NAO_mean(NAO_neg, data)

    logging.info(f"saving data for decade {decade} \n")
    save_dir_pos=f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_NAO_pos_15_5_mean_{decade}.nc'
    save_dir_neg=f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_NAO_neg_15_5_mean_{decade}.nc'


    eke_NAO_pos.to_netcdf(save_dir_pos)
    eke_NAO_neg.to_netcdf(save_dir_neg)


#%%

# nodes for different decades
decade = int(sys.argv[1]) if len(sys.argv) > 1 else 1850

logging.info(f"processing decade {decade} \n")
process_data(decade, 'eke')



# %%
