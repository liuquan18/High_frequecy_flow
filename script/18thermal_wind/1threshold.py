# %%
import xarray as xr
import numpy as np

from src.moisture.longitudinal_contrast import read_data
#%%
var = 'vt'
# %%
first_vt = read_data(var, 1850, (-90, 90), False, suffix='_ano')
#%%
first_vt.load()
# %%
vt_threshold = first_vt.sel(lat = slice(20, 60)).quantile([0.9, 0.1], dim = ('time', 'ens','lon','lat'))

# %%
var = 'va'
first_va = read_data(var, 1850, (-90, 90), False, suffix='_ano')
first_va = first_va.sel(plev = 25000)
# %%
first_va.load()
# %%
va_threshold = first_va.sel(lat = slice(20, 60)).quantile([0.9, 0.1], dim = ('time', 'ens','lon','lat'))
# %%
