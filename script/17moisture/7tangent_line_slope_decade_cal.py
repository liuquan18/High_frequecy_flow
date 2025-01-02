#%%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import os
import glob
import logging
from src.moisture.longitudinal_contrast import read_data

logging.basicConfig(level=logging.INFO)
# %%

box_EAA = [-35, 140, 20,60] # [lon_min, lon_max, lat_min, lat_max] Eurasia and Africa
box_NAM = [-145, -70, 20, 60] # [lon_min, lon_max, lat_min, lat_max] North America
box_NAL = [-70, -35, 20, 60] # [lon_min, lon_max, lat_min, lat_max] North Atlantic
box_NPO = [140, -145, 20, 60] # [lon_min, lon_max, lat_min, lat_max] North Pacific
# %%
#%%
# nodes for different decades
node = sys.argv[1]

#%%

decade = int(node)
logging.info(f"processing decade {decade}")
# %%
tas = read_data("tas", decade, (20,60), False, suffix='_std')
hus = read_data("hus", decade, (20,60), False, suffix='_std')
hussat = read_data("hussat", decade, (20,60), False, suffix='_std')
data = xr.Dataset({"tas": tas, "hus": hus*1000, "hussat": hussat*1000})
# %%
# select the data where the tas is above the 10th percentile
data.load()
tas_lim = data.tas.quantile(0.1, dim = ('time', 'ens'))
data = data.where(data.tas >= tas_lim, drop = True)
# %%
ratio_hus = data.hus / data.tas
ratio_hussat = data.hussat / data.tas

#%%
ratio_hus_mean = ratio_hus.mean(dim = ('time', 'ens'))
ratio_hussat_mean = ratio_hussat.mean(dim = ('time', 'ens'))
#%%
ratio = xr.Dataset({"hus": ratio_hus, "hussat": ratio_hussat})
# %%
file_name = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/husDBtas_hussatDBtas_dec/moist_tas_ratio_{decade}.nc"

ratio.to_netcdf(file_name)

# %%
