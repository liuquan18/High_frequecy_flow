#%%
import pandas as pd
import xarray as xr
import eventextreme.extreme_threshold as et
# %%
wb = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wavebreak_index/wb_first10/*.nc",combine = 'nested', concat_dim='ens')
# %%
wb = wb.wave_breaking_index
# %%
# spatial smoothing
wb = wb.rolling(lat=7, lon=7, center=True).mean()
#%%
df = wb.to_dataframe().reset_index()
#%%
df = df.drop(columns = 'plev')
# %%
df_window = df.groupby(['ens','lat','lon'])[['time','wave_breaking_index']].apply(et.construct_window, window = 7, column_name = 'wave_breaking_index')

# %%
