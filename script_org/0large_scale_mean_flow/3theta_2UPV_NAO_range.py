#%%
import xarray as xr
import numpy as np
from src.data_helper.before_extreme import read_NAO_extremes_single_ens
from src.composite import composite
from src.data_helper import read_variable

import logging
logging.basicConfig(level=logging.INFO)
import importlib
importlib.reload(composite)
importlib.reload(read_variable)
read_prime_single_ens = read_variable.read_prime_single_ens
range_NAO_composite = composite.range_NAO_composite
#%%
def composite_single_ens(var, decade, ens, plev, freq_label=None, **kwargs):
    
    # read NAO extremes
    pos_extreme = read_NAO_extremes_single_ens('pos', decade, ens)
    neg_extreme = read_NAO_extremes_single_ens('neg', decade, ens)

    # read variable
    name = kwargs.get('name', var)  # default name is the same as var')
    var_field = read_prime_single_ens(var, decade, ens, name = name, plev = plev)

    if not pos_extreme.empty and not neg_extreme.empty:

        var_pos, var_neg = range_NAO_composite(var_field, pos_extreme, neg_extreme)

