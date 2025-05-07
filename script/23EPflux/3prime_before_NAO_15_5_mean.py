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
from src.prime.prime_data import vert_integrate
logging.basicConfig(level=logging.INFO)


    
#%%
def read_all_data(decade, var, **kwargs):
    logging.info("reading NAO extremes")
    # wave breaking
    NAO_pos = read_NAO_extremes(decade, 'positive')
    NAO_neg = read_NAO_extremes(decade, 'negative')

    logging.info(f"reading {var} data")
    hf_data = read_prime( decade, var = var, **kwargs)  # change the suffix to read different data
    

    return NAO_pos, NAO_neg, hf_data


#%%
def process_data(decade, var, integrate=False, **kwargs):
    # read data
    NAO_pos, NAO_neg, data = read_all_data(decade, var = var, **kwargs)

    # select data before NAO events, here 'var' is only for column name
    logging.info (f"selecting data for {decade} \n")

    # determin the time window
    if kwargs.get('window', '15_5') == '15_5':
        time_window = (-15, -5)
    elif kwargs.get('window', '5_0') == '5_0':
        time_window = (-5, 0)
    else:
        raise ValueError("window must be either '15_5' or '5_0'")
    ivke_NAO_pos = before_NAO_mean(NAO_pos, data, time_window)
    ivke_NAO_neg = before_NAO_mean(NAO_neg, data, time_window)

    if integrate:
        ivke_NAO_pos = vert_integrate(ivke_NAO_pos)
        ivke_NAO_neg = vert_integrate(ivke_NAO_neg)

    logging.info(f"saving data for decade {decade} \n")
    suffix = kwargs.get('suffix', '_ano')
    if suffix == '_ano':
        save_dir_pos=f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_pos_15_5_mean_{decade}.nc'
        save_dir_neg=f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_neg_15_5_mean_{decade}.nc'
    elif suffix == '':
        save_dir_pos=f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results_without_ano/{var}_NAO_pos_15_5_mean_{decade}.nc'
        save_dir_neg=f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results_without_ano/{var}_NAO_neg_15_5_mean_{decade}.nc'

    ivke_NAO_pos.to_netcdf(save_dir_pos)
    ivke_NAO_neg.to_netcdf(save_dir_neg)


#%%

if __name__ == "__main__":
    # nodes for different decades
    decade = int(sys.argv[1]) if len(sys.argv) > 1 else 1850
    var = str(sys.argv[2]) if len(sys.argv) > 2 else 'vptp'
    name = str(sys.argv[3]) if len(sys.argv) > 3 else 'vptp'
    window= str(sys.argv[4]) if len(sys.argv) > 4 else '15_5' # '15_5' or '5_0'
    suffix = str(sys.argv[5]) if len(sys.argv) > 4 else '' # '_ano' or ''
    integrate = False

    logging.info(f"processing decade {decade} of {var} \n")
    process_data(decade, var, integrate, name = name, plev = None, suffix = suffix)

