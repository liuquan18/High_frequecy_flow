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
from src.composite.composite import before_NAO_mean
from src.prime.prime_data import read_prime
logging.basicConfig(level=logging.INFO)

    
#%%
def read_all_data(decade, var, **kwargs):
    logging.info("reading NAO extremes")
    # wave breaking
    NAO_pos = read_NAO_extremes(decade, 'positive')
    NAO_neg = read_NAO_extremes(decade, 'negative')

    logging.info(f"reading {var}")
    eke = read_prime( decade, var = var, **kwargs)  # change the suffix to read different data
    

    return NAO_pos, NAO_neg, eke

#%%
def process_data(decade, var, **kwargs):
    # read data
    NAO_pos, NAO_neg, data = read_all_data(decade, var = var, **kwargs)

    # select data before NAO events, here 'var' is only for column name
    logging.info (f"selecting data for {decade} \n")
    eke_NAO_pos = before_NAO_mean(NAO_pos, data)
    eke_NAO_neg = before_NAO_mean(NAO_neg, data)

    logging.info(f"saving data for decade {decade} \n")
    save_dir_pos=f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_pos_15_5_mean_{decade}.nc'
    save_dir_neg=f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_neg_15_5_mean_{decade}.nc'


    eke_NAO_pos.to_netcdf(save_dir_pos)
    eke_NAO_neg.to_netcdf(save_dir_neg)


#%%

# nodes for different decades
decade = int(sys.argv[1]) if len(sys.argv) > 1 else 1850

logging.info(f"processing decade {decade} \n")
process_data(decade, 'eke')



# %%
process_data(1850, 'ieke', name = 'ieke', suffix = '', plev = None)
# %%
