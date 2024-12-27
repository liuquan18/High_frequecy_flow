#%%
import xarray as xr
import numpy as np
import pandas as pd
#%%
from src.moisture.longitudinal_contrast import read_data


# %%
decade = 1850
tas_extremes = read_data("tas", decade, (-30,30), False, suffix="extremes")
hus_extremes = read_data("hus", decade, (-30,30), False, suffix="extremes")
# %%
