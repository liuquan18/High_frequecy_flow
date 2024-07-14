#%%
import xarray as xr
import pandas as pd
from src.extremes.extreme_threshold import threshold, construct_window

#%%
pc = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_first10/troposphere_pc_MJJAS_ano_1850_1859_r*.nc",
                       combine = 'nested', concat_dim = 'ens')
# %%
df = pc.to_dataframe().reset_index()
# %%
df_window = df.groupby(['plev','ens'])[['time','pc']].apply(construct_window, window = 7)
# %%
df_window = df_window.reset_index()[['plev','ens','time','window','pc']]
# %%
pos_threshold = df_window.groupby('plev')[['ens','time','window','pc']].apply(threshold, type = 'pos')
neg_threshold = df_window.groupby('plev')[['ens','time','window','pc']].apply(threshold, type = 'neg')
#%%
pos_threshold = pos_threshold.reset_index()[['plev','dayofyear','threshold']]
neg_threshold = neg_threshold.reset_index()[['plev','dayofyear','threshold']]

# %%
pos_threshold.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/threshold/pos_threshold_first10_allens.csv', index = False)
neg_threshold.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/threshold/neg_threshold_first10_allens.csv', index = False)
# %%
