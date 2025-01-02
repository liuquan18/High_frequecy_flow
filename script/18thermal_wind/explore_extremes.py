#%%
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from src.moisture.longitudinal_contrast import read_data
import logging
import sys
import os
import cartopy.crs as ccrs
logging.basicConfig(level=logging.INFO)
# %%
var = 'vt'
# %%
decade = 1850
# %%

vt_extremes_pos = read_data(var, decade, (-90,90), False, suffix='_extremes_pos')
vt_extremes_neg = read_data(var, decade, (-90,90), False, suffix='_extremes_neg')

# %%
def plot_data(data):
    fig, axes = plt.subplots(
        subplot_kw={"projection": ccrs.PlateCarree(100)}
    )
    data.flag.plot(ax = axes, transform=ccrs.PlateCarree(), cmap = 'coolwarm', levels = np.arange(1, 3,1), extend = 'max')
    axes.set_title("positive")
    axes.coastlines()
# %%
plot_data(vt_extremes_pos.isel(time = 10, ens = 3))
# %%
plot_data(vt_extremes_neg.isel(time = 0, ens = 3))
# %%
