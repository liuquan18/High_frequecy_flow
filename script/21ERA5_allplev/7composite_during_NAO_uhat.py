#%%
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
from src.data_helper.read_variable import read_prime_ERA5
from src.composite.composite_during import sel_var
logging.basicConfig(level=logging.INFO)


# %%
logging.info("reading NAO extremes")
NAO_pos = read_NAO_extreme_ERA5('pos', 3) # the number is too small for 5 days
NAO_neg = read_NAO_extreme_ERA5('neg', 3)

logging.info("reading uhat")
hf_data = read_prime_ERA5(var = 'ua_hat', name = 'var131', plev = None)  # change the suffix to read different data
#%%
uhat_pos = sel_var(hf_data, NAO_pos)
# %%
uhat_neg = sel_var(hf_data, NAO_neg)
# %%
logging.info("saving data for \n")
save_dir_pos=f'/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results/ua_hat_NAO_pos_during_mean.nc'
save_dir_neg=f'/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results/ua_hat_NAO_neg_during_mean.nc'
# %%
uhat_pos.to_netcdf(save_dir_pos)
uhat_neg.to_netcdf(save_dir_neg)
# %%
