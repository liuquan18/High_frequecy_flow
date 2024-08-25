#%%
import xarray as xr
import numpy as np
import pandas as pd
import logging
import glob
import os
#%%
logging.basicConfig(level=logging.INFO)

# %%
import src.composite.composite as composite
import src.extremes.extreme_read as ext_read
#%%
import importlib
importlib.reload(composite)
importlib.reload(ext_read)
# %%
ens = 1
variable = "zg"
plev = 25000
freq_label = None
period = "first10"
# %%
def composite_single_ens(variable, period, ens, plev, freq_label = None):
    pos_extreme, neg_extreme = ext_read.read_extremes(period, 8, ens, plev = plev)
    variable_ds = composite.read_variable(variable, period, ens, plev, freq_label)
    pos_comp, neg_comp = composite.event_composite(variable_ds, pos_extreme, neg_extreme)
    return pos_comp, neg_comp

# %%
pos_comps = []
neg_comps = []

for i in range(1, 51):
    pos_comp, neg_comp = composite_single_ens(variable, period, i, plev, freq_label)

    pos_comps.append(pos_comp)
    neg_comps.append(neg_comp)

# exclude None from the list
pos_comps = [x for x in pos_comps if x is not None]
neg_comps = [x for x in neg_comps if x is not None]

pos_comps = xr.concat(pos_comps, dim = "event")
neg_comps = xr.concat(neg_comps, dim = "event")
# %%
