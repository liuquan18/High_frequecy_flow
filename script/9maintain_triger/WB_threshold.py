#%%
import pandas as pd
import xarray as xr
import eventextreme.extreme_threshold as et
# %%
wb = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wavebreak_index/wb_first10/*.nc",combine = 'nested', concat_dim='ens')

wb.load()
# %%
wb = wb.wave_breaking_index
# %%
# spatial smoothing
wb = wb.rolling(lat=7, lon=7, center=True).mean()
#%%

wb_sel = wb.sel(lat = slice(40,50), lon = slice(310,320))

#%%
wb_threshold = wb_sel.mean(dim  = ('lat','lon')).quantile(0.95, dim = ('time', 'ens'))

# %%