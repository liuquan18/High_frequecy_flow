#%%
import pandas as pd
import xarray as xr
import numpy as np

import eventextreme.eventextreme as ee
import eventextreme.extreme_threshold as et
# %%
df_windows = []

for member in range(1, 51):
    print(f"processing member {member}")
    df_window = pd.read_csv(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/first10_OLR_daily_window/rlut_window_first10_r{member}.csv")
    df_window['ens'] = member

    df_windows.append(df_window)

#%%
# put all dataframes together
df_windows = pd.concat(df_windows, axis = 0)

#%%
# calculate the threshold
std_dim = ['time','window','ens']
pos_threshold = df_windows.groupby(['lat','lon'])[std_dim + ['rlut']].apply(et.threshold, type = 'pos')
pos_threshold = pos_threshold.droplevel(2).reset_index()

neg_threshold = df_windows.groupby(['lat','lon'])[std_dim + ['rlut']].apply(et.threshold, type = 'neg')
neg_threshold = neg_threshold.droplevel(2).reset_index()

#%%
pos_threshold.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_threshold/rlut_pos_threshold_first10_allens.csv', index = False)
neg_threshold.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_threshold/rlut_neg_threshold_first10_allens.csv', index = False)