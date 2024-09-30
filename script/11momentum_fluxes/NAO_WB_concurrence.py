#%%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
# %%
from src.extremes.extreme_read import read_extremes
from eventextreme.extreme_threshold import subtract_threshold
import src.composite.composite as comp

# %%
import importlib
importlib.reload(comp)

#%%
def read_upvp(period, ens):
    base_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_{period}/'
    file=glob.glob(base_dir+f'*r{ens}i*.nc')[0]
    upvp = xr.open_dataset(file).ua.squeeze()
    upvp['time'] = upvp.indexes['time'].to_datetimeindex()
    return upvp


# %%
def WB_composite(period, ens):
    upvp = read_upvp(period, ens)
    AWB = xr.where(upvp > 1, 1, 0)
    CWB = xr.where(upvp < -1, 1, 0)
    NAO_pos, NAO_neg = read_extremes(period, 8, ens, 25000)
    if NAO_pos.empty:
        NAO_pos_AWB = None
        NAO_pos_CWB = None
    else:
        NAO_pos_range = comp.lead_lag_30days(NAO_pos, base_plev=25000, cross_plev=1)
        NAO_pos_AWB = comp.date_range_composite(AWB, NAO_pos_range)
        NAO_pos_CWB = comp.date_range_composite(CWB, NAO_pos_range)

        # calculate the ocurrence during the events
        NAO_pos_AWB = NAO_pos_AWB.sum(dim = 'event')
        NAO_pos_CWB = NAO_pos_CWB.sum(dim = 'event')

    if NAO_neg.empty:
        NAO_neg_AWB = None
        NAO_neg_CWB = None
    else:
        NAO_neg_range = comp.lead_lag_30days(NAO_neg, base_plev=25000, cross_plev=1)
        NAO_neg_AWB = comp.date_range_composite(AWB, NAO_neg_range)
        NAO_neg_CWB = comp.date_range_composite(CWB, NAO_neg_range)
        # calculate the ocurrence during the events
        NAO_neg_AWB = NAO_neg_AWB.sum(dim = 'event')
        NAO_neg_CWB = NAO_neg_CWB.sum(dim = 'event')

    return NAO_pos_AWB, NAO_neg_AWB, NAO_pos_CWB, NAO_neg_CWB
# %%
def WB_occurrence_period(period):
    pos_AWBs = []
    neg_AWBs = []

    pos_CWBs = []
    neg_CWBs = []

    for ens in range(1,51):
        NAO_pos_AWB, NAO_neg_AWB, NAO_pos_CWB, NAO_neg_CWB = WB_composite(period, ens)

        if NAO_pos_AWB is not None:
            pos_AWBs.append(NAO_pos_AWB)
        if NAO_neg_AWB is not None:
            neg_AWBs.append(NAO_neg_AWB)
        if NAO_pos_CWB is not None:
            pos_CWBs.append(NAO_pos_CWB)
        if NAO_neg_CWB is not None:
            neg_CWBs.append(NAO_neg_CWB)


    pos_AWBs = xr.concat(pos_AWBs, dim = 'ens').sum(dim = 'ens')
    neg_AWBs = xr.concat(neg_AWBs, dim = 'ens').sum(dim = 'ens')
    pos_CWBs = xr.concat(pos_CWBs, dim = 'ens').sum(dim = 'ens')
    neg_CWBs = xr.concat(neg_CWBs, dim = 'ens').sum(dim = 'ens')

    return pos_AWBs, neg_AWBs, pos_CWBs, neg_CWBs

#%%
first_pos_AWBs, first_neg_AWBs, first_pos_CWBs, first_neg_CWBs = WB_occurrence_period("first10")

# %%
last_pos_AWBs, last_neg_AWBs, last_pos_CWBs, last_neg_CWBs = WB_occurrence_period("last10")

#%%
def smooth(arr, days = 5):
    arr_smooth = arr.rolling(time = days).mean(dim = 'time')
    return arr_smooth


# %%
fig, axes = plt.subplots(2,2, figsize = (12,8))
first_pos_AWBs.plot(ax = axes[0,0])
last_pos_AWBs.plot(ax = axes[0,0])

first_pos_CWBs.plot(ax = axes[1,0])
last_pos_CWBs.plot(ax = axes[1,0])


first_neg_AWBs.plot(ax = axes[0,1])
last_neg_AWBs.plot(ax = axes[0,1])

first_neg_CWBs.plot(ax = axes[1,1])
last_neg_CWBs.plot(ax = axes[1,1])

# %%
fig, axes = plt.subplots(1,2,figsize = (12,8))
first_pos_AWBs.plot(ax = axes[0], alpha = 0.5,  color = 'b')
last_pos_AWBs.plot(ax = axes[0], alpha = 0.5, color = 'r')

first_neg_CWBs.plot(ax = axes[1], alpha = 0.5, color = 'b')
last_neg_CWBs.plot(ax = axes[1], alpha = 0.5,  color = 'r')

smooth(first_pos_AWBs).plot(ax = axes[0], color = 'b', linewidth = 3, label = 'first10')
smooth(last_pos_AWBs).plot(ax = axes[0], color = 'r', linewidth = 3, label = 'last10')

smooth(first_neg_CWBs).plot(ax = axes[1], color = 'b', linewidth = 3, label = 'first10')
smooth(last_neg_CWBs).plot(ax = axes[1], color = 'r', linewidth = 3, label = 'last10')

axes[0].set_title("AWB occurrence during NAO positive")
axes[1].set_title("CWB occurrence during NAO negative")

axes[0].set_xlim(-21,21)
axes[1].set_xlim(-21, 21)

axes[0].set_ylabel("WB occurrence", fontsize = 14)
axes[0].set_ylabel("")
axes[1].set_xlabel("days after NAO extremes", fontsize = 14)
axes[0].set_xlabel("days after NAO extremes", fontsize = 14)

axes[1].legend()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/pos_AWB_neg_CWB_occurrence.png", dpi = 300)
# %%
# pos_CWB, neg_AWB
fig, axes = plt.subplots(1,2,figsize = (12,8))
first_pos_CWBs.plot(ax = axes[0], alpha = 0.5,  color = 'b')
last_pos_CWBs.plot(ax = axes[0], alpha = 0.5, color = 'r')

first_neg_AWBs.plot(ax = axes[1], alpha = 0.5, color = 'b')
last_neg_AWBs.plot(ax = axes[1], alpha = 0.5,  color = 'r')

smooth(first_pos_CWBs).plot(ax = axes[0], color = 'b', linewidth = 3, label = 'first10')
smooth(last_pos_CWBs).plot(ax = axes[0], color = 'r', linewidth = 3, label = 'last10')

smooth(first_neg_AWBs).plot(ax = axes[1], color = 'b', linewidth = 3, label = 'first10')
smooth(last_neg_AWBs).plot(ax = axes[1], color = 'r', linewidth = 3, label = 'last10')

axes[0].set_title("CWB occurrence during NAO positive")
axes[1].set_title("AWB occurrence during NAO negative")

axes[0].set_xlim(-21,21)
axes[1].set_xlim(-21, 21)

axes[0].set_ylabel("WB occurrence", fontsize = 14)
axes[0].set_ylabel("")
axes[1].set_xlabel("days after NAO extremes", fontsize = 14)
axes[0].set_xlabel("days after NAO extremes", fontsize = 14)

axes[1].legend()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/pos_CWB_neg_AWB_occurrence.png", dpi = 300)
# %%
