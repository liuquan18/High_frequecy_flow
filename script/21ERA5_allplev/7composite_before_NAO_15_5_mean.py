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

from src.data_helper.read_NAO_extremes import read_NAO_extreme_ERA5
from src.composite.composite import before_NAO_composite
from src.data_helper.read_ERA5 import read_prime_ERA5

logging.basicConfig(level=logging.INFO)


# %%
def read_all_data(var, **kwargs):
    logging.info("reading NAO extremes")
    NAO_pos = read_NAO_extreme_ERA5("pos", 4)  # the number is too small for 5 days
    NAO_neg = read_NAO_extreme_ERA5("neg", 4)

    logging.info(f"reading {var}")
    hf_data = read_prime_ERA5(
        var=var, model="ERA5_allplev", **kwargs
    )  # change the suffix to read different data

    # anomaly
    hf_data = hf_data - hf_data.mean(dim="time")

    return NAO_pos, NAO_neg, hf_data


# %%
def process_data(var, name="ivke", plev=None, window=(-15, -5), model="ERA5_allplev"):
    # read data
    NAO_pos, NAO_neg, data = read_all_data(var=var, name=name, plev=plev, suffix="_ano")

    # select the NAO_pos and NAO_neg from 1979 on
    NAO_pos = NAO_pos.where(
        pd.to_datetime(NAO_pos.extreme_start_time).dt.year >= 1979
    ).dropna(axis=0)
    NAO_neg = NAO_neg.where(
        pd.to_datetime(NAO_neg.extreme_start_time).dt.year >= 1979
    ).dropna(axis=0)

    # select data before NAO events, here 'var' is only for column name
    logging.info(f"selecting data for {var}")
    ivke_NAO_pos = before_NAO_composite(NAO_pos, data, window)
    ivke_NAO_neg = before_NAO_composite(NAO_neg, data, window)

    logging.info(f"saving data for {var}")
    save_dir_pos = f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results/{model}_{var}_NAO_pos_{abs(window[0])}_{abs(window[1])}_mean.nc"
    save_dir_neg = f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results/{model}_{var}_NAO_neg_{abs(window[0])}_{abs(window[1])}_mean.nc"

    ivke_NAO_pos.to_netcdf(save_dir_pos)
    ivke_NAO_neg.to_netcdf(save_dir_neg)


# %%
if __name__ == "__main__":
    process_data("ivke", name="ivke", plev=None, window=(-15, -5))
    process_data("upvp", name="var131", plev=25000, window=(-5, 0))
    process_data("ieke", name="ieke", plev=None, window=(-15, -5))

# %%
