#%%
import xarray as xr
import pandas as pd
from src.extremes.extreme_threshold import threshold, construct_window

#%%
pc = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_first10/*.nc",
                       combine = 'nested', concat_dim = 'ens')
# %%
df = pc.to_dataframe().reset_index()
# %%
df_window = df.groupby('ens')[['time','pc']].apply(construct_window, window = 7)
# %%
df_window = df_window.reset_index()[['ens','time','window','pc']]
# %%
pos_threshold, neg_threshold = threshold(df_window)
# %%
pos_threshold.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/threshold/pos_threshold_first10_allens.csv', index = False)
neg_threshold.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/threshold/neg_threshold_first10_allens.csv', index = False)
# %%