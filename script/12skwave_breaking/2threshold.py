#%%
import xarray as xr
import numpy as np
# %%
from src.moisture.longitudinal_contrast import read_data
#%%
var = 'upvp'
# %%
first_upvp = read_data(var, 1850, (-90, 90), False, suffix='')
#%%
first_upvp.load()
# %%
vt_threshold = first_upvp.ua.sel(lat = slice(20, 60)).quantile([0.9, 0.1], dim = ('time', 'ens','lon','lat'))
# 84.34, -50.65
# %%
var = 'av'
# %%
first_avor = read_data(var, 1850, (-90, 90), False, suffix='_ano')

# %%
first_avor.load()
# %%
avor_threshold = first_avor.AV.sel(lat = slice(20, 60)).quantile(0.9, dim = ('time', 'ens','lon','lat'))
# %%
# 4.31473897e-05