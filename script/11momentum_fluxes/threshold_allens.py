#%%
import xarray as xr
import pandas as pd
from eventextreme.extreme_threshold import threshold
from eventextreme.extreme_threshold import construct_window
#%%
pc = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_first10/*.nc",
                       combine = 'nested', concat_dim = 'ens')
# %%
pc = pc.ua.squeeze()
df = pc.to_dataframe().reset_index()
# %%
df_window = df.groupby(['ens'])[['time','ua']].apply(construct_window, window = 7)
# %%
df_window = df_window.droplevel(2).reset_index()

# %%
# calculate the threshold from both 'time', 'window', and 'ens' dimension.

std_dim = ['time','window','ens']
pos_threshold = df_window.groupby('plev')[std_dim + ['ua']].apply(threshold, type = 'pos')
pos_threshold = pos_threshold.droplevel(1).reset_index()
#%%
neg_threshold = df_window.groupby('plev')[std_dim + ['ua']].apply(threshold, type = 'neg')
neg_threshold = neg_threshold.droplevel(1).reset_index()

# %%
pos_threshold.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/threshold/pos_threshold_first10_allens.csv', index = False)
neg_threshold.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/threshold/neg_threshold_first10_allens.csv', index = False)
# %%
