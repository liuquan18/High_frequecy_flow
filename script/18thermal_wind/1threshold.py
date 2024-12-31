# %%
import xarray as xr
import numpy as np

from src.moisture.longitudinal_contrast import read_data

# %%
first_vt = read_data("vt", 1850, (-90, 90), False, suffix='_ano')

# %%
vt_threshold = first_vt.sel(lat = slice(20, 60)).quantile([0.99, 0.01], dim = ('time', 'ens','lon','lat'))

# %%
