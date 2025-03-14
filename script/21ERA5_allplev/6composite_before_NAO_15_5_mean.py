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

from src.extremes.before_extreme import read_NAO_extreme_ERA5
from src.composite.composite import before_NAO_mean
from src.prime.prime_data import read_prime_ERA5
logging.basicConfig(level=logging.INFO)



#%%
def read_all_data( var, **kwargs):
    logging.info("reading NAO extremes")
    NAO_pos = read_NAO_extreme_ERA5('pos', 3) # the number is too small for 5 days
    NAO_neg = read_NAO_extreme_ERA5('neg', 3)

    logging.info("reading ivke")
    hf_data = read_prime_ERA5( var = var, **kwargs)  # change the suffix to read different data


    return NAO_pos, NAO_neg, hf_data


#%%
def process_data(var, name = 'ivke', plev = None, window = (-15, -5)):
    # read data
    NAO_pos, NAO_neg, data = read_all_data(var = var, name = name, plev = plev)

    # select data before NAO events, here 'var' is only for column name
    logging.info ("selecting data for \n")
    ivke_NAO_pos = before_NAO_mean(NAO_pos, data, window)
    ivke_NAO_neg = before_NAO_mean(NAO_neg, data, window)

    logging.info("saving data for \n")
    save_dir_pos=f'/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results/{var}_NAO_pos_{abs(window[0])}_{abs(window[1])}_mean.nc'
    save_dir_neg=f'/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results/{var}_NAO_neg_{abs(window[0])}_{abs(window[1])}_mean.nc'


    ivke_NAO_pos.to_netcdf(save_dir_pos)
    ivke_NAO_neg.to_netcdf(save_dir_neg)



#%%
if __name__ == "__main__":
    process_data('ivke')
