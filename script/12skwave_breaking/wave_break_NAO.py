#%%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.extremes.extreme_read import read_extremes
import src.composite.composite as comp

# %%
def read_wb(period, ens, WB):
    base_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/skader_wb_events/{WB}_array/{WB}_array_{period}/'
    file=glob.glob(base_dir+f'*r{ens}*.nc')[0]
    wb = xr.open_dataset(file).flag.squeeze()
    try:
        wb['time'] = wb.indexes['time'].to_datetimeindex()
    except AttributeError:
        pass


    # lonlatbox, -90,40,30,60
    # change longitude to -180,180
    wb = wb.assign_coords(lon=(wb.lon+ 180) % 360 - 180)
    wb = wb.sortby(wb.lon)
    wb = wb.sel(lon=slice(-90, 40), lat=slice(30, 60))

    wb = wb.mean(dim = ('lat', 'lon'))

    return wb
# %%
def lag_lead_composite(NAO, WB):
    '''
    calculate the occurrence of WB as a function of days relative to NAO onset day

    Parameters
    ----------
    NAO : pandas.DataFrame
        NAO extremes
    WB : pandas.DataFrame
        WB array
    '''

    NAO_range = comp.lead_lag_30days(NAO, base_plev=25000)
    WB_composite = comp.date_range_composite(WB, NAO_range)

    WB_composite = WB_composite.sum(dim = 'event')

    return WB_composite

#%%
def NAO_WB(period):
    NAO_pos_AWB = []
    NAO_neg_AWB = []

    NAO_pos_CWB = []
    NAO_neg_CWB = []

    for ens in range(1, 51):
        AWB = read_wb(period, ens, 'AWB')
        CWB = read_wb(period, ens, 'CWB')

        NAO_pos, NAO_neg = read_extremes(period, 8, ens, 25000)
        if not NAO_pos.empty:
            NAO_pos_AWB.append(lag_lead_composite(NAO_pos, AWB))
            NAO_pos_CWB.append(lag_lead_composite(NAO_pos, CWB))
            
        if not NAO_neg.empty:
            NAO_neg_AWB.append(lag_lead_composite(NAO_neg, AWB))
            NAO_neg_CWB.append(lag_lead_composite(NAO_neg, CWB))


    NAO_pos_AWB = xr.concat(NAO_pos_AWB, dim = 'ens').sum(dim = 'ens')
    NAO_neg_AWB = xr.concat(NAO_neg_AWB, dim = 'ens').sum(dim = 'ens')
    NAO_pos_CWB = xr.concat(NAO_pos_CWB, dim = 'ens').sum(dim = 'ens')
    NAO_neg_CWB = xr.concat(NAO_neg_CWB, dim = 'ens').sum(dim = 'ens')

    return NAO_pos_AWB, NAO_neg_AWB, NAO_pos_CWB, NAO_neg_CWB
#%%
def smooth(arr, days = 5):
    arr_smooth = arr.rolling(time = days).mean(dim = 'time')
    return arr_smooth

# %%
first_NAO_pos_AWB, first_NAO_neg_AWB, first_NAO_pos_CWB, first_NAO_neg_CWB = NAO_WB('first10')
last_NAO_pos_AWB, last_NAO_neg_AWB, last_NAO_pos_CWB, last_NAO_neg_CWB = NAO_WB('last10')
# %%
fig, axes = plt.subplots(1,2,figsize = (12,8))
first_NAO_pos_AWB.plot(ax = axes[0], alpha = 0.5,  color = 'b')
last_NAO_pos_AWB.plot(ax = axes[0], alpha = 0.5, color = 'r')

first_NAO_neg_CWB.plot(ax = axes[1], alpha = 0.5, color = 'b')
last_NAO_neg_CWB.plot(ax = axes[1], alpha = 0.5,  color = 'r')

smooth(first_NAO_pos_AWB).plot(ax = axes[0], color = 'b', linewidth = 3, label = 'first10')
smooth(last_NAO_pos_AWB).plot(ax = axes[0], color = 'r', linewidth = 3, label = 'last10')

smooth(first_NAO_neg_CWB).plot(ax = axes[1], color = 'b', linewidth = 3, label = 'first10')
smooth(last_NAO_neg_CWB).plot(ax = axes[1], color = 'r', linewidth = 3, label = 'last10')

axes[0].set_title("AWB occurrence during NAO positive")
axes[1].set_title("CWB occurrence during NAO negative")

axes[0].set_xlim(-21,21)
axes[1].set_xlim(-21, 21)

axes[0].set_ylabel("WB occurrence", fontsize = 14)
axes[0].set_ylabel("")
axes[1].set_xlabel("days after NAO extremes", fontsize = 14)
axes[0].set_xlabel("days after NAO extremes", fontsize = 14)

axes[1].legend()
# %%
# pos NAO - CWB, neg NAO - AWB
fig, axes = plt.subplots(1,2,figsize = (12,8))
first_NAO_pos_CWB.plot(ax = axes[0], alpha = 0.5,  color = 'b')
last_NAO_pos_CWB.plot(ax = axes[0], alpha = 0.5, color = 'r')

first_NAO_neg_AWB.plot(ax = axes[1], alpha = 0.5, color = 'b')
last_NAO_neg_AWB.plot(ax = axes[1], alpha = 0.5,  color = 'r')

smooth(first_NAO_pos_CWB).plot(ax = axes[0], color = 'b', linewidth = 3, label = 'first10')
smooth(last_NAO_pos_CWB).plot(ax = axes[0], color = 'r', linewidth = 3, label = 'last10')

smooth(first_NAO_neg_AWB).plot(ax = axes[1], color = 'b', linewidth = 3, label = 'first10')
smooth(last_NAO_neg_AWB).plot(ax = axes[1], color = 'r', linewidth = 3, label = 'last10')

axes[0].set_title("CWB occurrence during NAO positive")
axes[1].set_title("AWB occurrence during NAO negative")

axes[0].set_xlim(-21,21)
axes[1].set_xlim(-21, 21)

axes[0].set_ylabel("WB occurrence", fontsize = 14)
axes[0].set_ylabel("")
axes[1].set_xlabel("days after NAO extremes", fontsize = 14)
axes[0].set_xlabel("days after NAO extremes", fontsize = 14)

axes[1].legend()
# %%
