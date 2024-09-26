#%%
import xarray as xr
import pandas as pd
from eventextreme.extreme_threshold import threshold
from eventextreme.extreme_threshold import construct_window
#%%
pc = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_first10/*.nc",
                       combine = 'nested', concat_dim = 'ens')
pc.load()
pc['time'] = pc.indexes['time'].to_datetimeindex()
# %%
pc = pc.ua.squeeze()
df = pc.to_dataframe().reset_index()
# %%
df_window = df.groupby(['ens'])[['time','ua']].apply(construct_window,column_name = 'ua', window = 7)
# %%
df_window = df_window.droplevel(1).reset_index()

# %%
# calculate the threshold from both 'time', 'window', and 'ens' dimension.
pos_threshold = threshold(df_window, column_name = 'ua', relative_thr=1, extreme_type = 'pos')

#%%
neg_threshold = threshold(df_window, column_name = 'ua', relative_thr=1, extreme_type = 'neg')
# %%
pos_threshold.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_threshold/AWB_threshold_first10_allens.csv', index = False)
neg_threshold.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_threshold/CWB_threshold_first10_allens.csv', index = False)
# %%
