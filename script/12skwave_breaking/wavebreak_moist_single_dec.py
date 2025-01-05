#%%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import src.composite.composite as comp

# %%
def read_wb(period, ens, WB, NAO_region = False):
    base_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/skader_wb_events/{WB}_array/{WB}_array_{period}/'
    file=glob.glob(base_dir+f'*r{ens}*.nc')[0]
    wb = xr.open_dataset(file).flag.squeeze()
    try:
        wb['time'] = wb.indexes['time'].to_datetimeindex()
    except AttributeError:
        pass

    if NAO_region:
        # lonlatbox, -90,40,30,60
        # change longitude to -180,180
        wb = wb.assign_coords(lon=(wb.lon+ 180) % 360 - 180)
        wb = wb.sortby(wb.lon)
        wb = wb.sel(lon=slice(-90, 40), lat=slice(30, 60))


    return wb
#%%
ens = 1
period = 'first10'
# %%
AWB = read_wb(period, ens, 'AWB', NAO_region=True)
# %%
