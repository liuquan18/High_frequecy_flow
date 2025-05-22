#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature

# %%
from src.data_helper.read_variable import read_MPI_GE_uhat

# %%
def read_theta_2pvu(decade, phase, time_window = (-10, 5)):
    basedir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_range/theta_2pvu_NAO_{phase}_{decade}.nc"
    ds = xr.open_dataset(basedir).__xarray_dataarray_variable__
    ds = ds.sel(time=slice(*time_window))
    ds = ds.mean(dim=("time", "ens"))
    return ds
#%%
def read_wb(decade, wb_type, phase):
    basedir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_range/{wb_type}_{phase}_{decade}.nc"
    ds = xr.open_dataset(basedir)
    ds = ds.mean(dim=( "ens"))
    return ds
# %%
# u hat
uhat_first, uhat_last = read_MPI_GE_uhat()

# %%
theta_pos_first = read_theta_2pvu(1850, "pos")
theta_pos_last = read_theta_2pvu(2090, "pos")

theta_neg_first = read_theta_2pvu(1850, "neg")
theta_neg_last = read_theta_2pvu(2090, "neg")
# %%
AWB_pos_first = read_wb(1850, "AWB", "pos")
# %%
