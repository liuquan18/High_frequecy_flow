#%%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import logging
logging.basicConfig(level=logging.WARNING)
# %%
from src.extremes.extreme_read import read_extremes
# %%

# %%
def sel_uhat(uhat, events):
    try:
        uhat['time'] = uhat.indexes['time'].to_datetimeindex()
    except AttributeError:
        pass

    uhat_extreme = []
    for i, event in events.iterrows():
        uhat_extreme.append(uhat.sel(time=slice(event['extreme_start_time'], event['extreme_end_time'])))
    uhat_extreme = xr.concat(uhat_extreme, dim='time')
    return uhat_extreme

# %%
def extreme_uhat(period):
    basedir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_{period}_hat/'

    uhat_pos = []
    uhat_neg = []

    for ens in range(1,51):
        logging.info(f'Processing ensemble {ens}')

    # read extremes
        pos_extreme, neg_extreme = read_extremes(period, 8, ens, plev=25000)

    # read uhat 
        uhat_file = glob.glob(f'{basedir}*r{ens}i1p1f1*.nc')[0]
        uhat = xr.open_dataset(uhat_file).ua

    # average over plev below 700 hPa
        uhat = uhat.sel(plev=slice( None, 70000)).mean(dim='plev')

        if not pos_extreme.empty:
            uhat_pos.append(sel_uhat(uhat, pos_extreme))

        if not neg_extreme.empty:
            uhat_neg.append(sel_uhat(uhat, neg_extreme))

    uhat_pos = xr.concat(uhat_pos, dim='ens')
    uhat_neg = xr.concat(uhat_neg, dim='ens')

    return uhat_pos, uhat_neg
# %%
uhat_pos_first10, uhat_neg_first10 = extreme_uhat('first10')
uhat_pos_last10, uhat_neg_last10 = extreme_uhat('last10')
# %%
