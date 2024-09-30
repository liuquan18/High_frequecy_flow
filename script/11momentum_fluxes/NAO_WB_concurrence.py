#%%
import xarray as xr
import pandas as pd
import numpy as np
import glob
# %%
from src.extremes.extreme_read import read_extremes
from eventextreme.extreme_threshold import subtract_threshold
import src.composite.composite as comp

# %%
import importlib
importlib.reload(comp)


# %%
def construct_df(events):
    
    df = pd.DataFrame(index = pd.date_range(start = '1850-05-01', end = '2100-09-30', freq = 'D'), columns = ['WB'], data = 0)

    if len(events) >0 :
        for i, event in events.iterrows():
            start_time = event['extreme_start_time']
            end_time = event['extreme_end_time']
            df.loc[start_time:end_time, 'WB'] = 1

    xarr = df.to_xarray()
    xarr = xarr.rename({'index':'time'})
    
    return xarr

#%%
def read_wbs(period, ens):
    awb_file = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_AWB/AWB_{period}/AWB_{period}_r{ens}.csv"
    cwb_file = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_CWB/CWB_{period}/CWB_{period}_r{ens}.csv"
    awbs = pd.read_csv(awb_file)
    cwbs = pd.read_csv(cwb_file)

    AWB = construct_df(awbs)
    CWB = construct_df(cwbs)

    return AWB, CWB


# %%
def WB_composite(period, ens):
    AWB, CWB = read_wbs(period, ens)
    NAO_pos, NAO_neg = read_extremes(period, 8, ens, 25000)
    if NAO_pos.empty:
        NAO_pos_AWB = None
        NAO_pos_CWB = None
    else:
        NAO_pos_range = comp.lead_lag_30days(NAO_pos, base_plev=25000, cross_plev=1)
        NAO_pos_AWB = comp.date_range_composite(AWB, NAO_pos_range)
        NAO_pos_CWB = comp.date_range_composite(CWB, NAO_pos_range)

    if NAO_neg.empty:
        NAO_neg_AWB = None
        NAO_neg_CWB = None
    else:
        NAO_neg_range = comp.lead_lag_30days(NAO_neg, base_plev=25000, cross_plev=1)
        NAO_neg_AWB = comp.date_range_composite(AWB, NAO_neg_range)
        NAO_neg_CWB = comp.date_range_composite(CWB, NAO_neg_range)

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


    pos_AWBs = xr.concat(pos_AWBs, dim = 'ens')
    neg_AWBs = xr.concat(neg_AWBs, dim = 'ens')
    pos_CWBs = xr.concat(pos_CWBs, dim = 'ens')
    neg_CWBs = xr.concat(neg_CWBs, dim = 'ens')

    return pos_AWBs, neg_AWBs, pos_CWBs, neg_CWBs

#%%
first_pos_AWBs, first_neg_AWBs, first_pos_CWBs, first_neg_CWBs = WB_occurrence_period("first10")
# %%
last_pos_AWBs, last_neg_AWBs, last_pos_CWBs, last_neg_CWBs = WB_occurrence_period("last10")