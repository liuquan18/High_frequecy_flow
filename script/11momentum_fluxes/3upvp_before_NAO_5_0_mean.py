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

from src.data_helper.read_NAO_extremes import read_NAO_extremes
from src.composite.composite import before_NAO_composite
from src.data_helper.read_variable import read_prime

logging.basicConfig(level=logging.INFO)


# %%
def read_all_data(decade, var, **kwargs):
    logging.info("reading NAO extremes")
    # wave breaking
    NAO_pos = read_NAO_extremes(decade, "positive")
    NAO_neg = read_NAO_extremes(decade, "negative")

    logging.info("reading upvp")
    hf_data = read_prime(
        decade, var=var, suffix="_ano", **kwargs
    )  # change the suffix to read different data

    return NAO_pos, NAO_neg, hf_data


# %%
def process_data(decade, var):
    # read data
    NAO_pos, NAO_neg, data = read_all_data(decade, var=var, name="ua", plev=25000)

    # select data before NAO events, here 'var' is only for column name
    logging.info(f"selecting data for {decade} \n")
    upvp_NAO_pos = before_NAO_composite(NAO_pos, data, (-5, 0))
    upvp_NAO_neg = before_NAO_composite(NAO_neg, data, (-5, 0))

    logging.info(f"saving data for decade {decade} \n")
    save_dir_pos = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/upvp_NAO_pos_5_0_mean_{decade}.nc"
    save_dir_neg = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/upvp_NAO_neg_5_0_mean_{decade}.nc"

    upvp_NAO_pos.to_netcdf(save_dir_pos)
    upvp_NAO_neg.to_netcdf(save_dir_neg)


# %%

if __name__ == "__main__":
    # nodes for different decades
    decade = int(sys.argv[1]) if len(sys.argv) > 1 else 1850

    logging.info(f"processing decade {decade} \n")
    process_data(decade, "upvp")
