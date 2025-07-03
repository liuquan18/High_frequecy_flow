#%%
import xarray as xr
import numpy as np
from src.data_helper.read_NAO_extremes import read_NAO_extreme_ERA5
from src.composite import composite
from src.data_helper import read_ERA5
import sys
import logging
logging.basicConfig(level=logging.INFO)
import importlib
importlib.reload(composite)
importlib.reload(read_ERA5)
read_prime_single_ens = read_ERA5.read_prime_ERA5
range_NAO_composite = composite.range_NAO_composite
range_NAO_composite_single_phase = composite.range_NAO_composite_single_phase


#%%
var = sys.argv[1] if len(sys.argv) > 1 else 'ua'
name = sys.argv[2] if len(sys.argv) > 2 else var
suffix = sys.argv[3] if len(sys.argv) > 3 else ''
plev = int(sys.argv[4]) if len(sys.argv) > 4 else None
# read NAO extremes

#%%
logging.info("reading NAO extremes")
pos_extreme = read_NAO_extreme_ERA5("pos", 5)# 7 days, the same for the others
neg_extreme = read_NAO_extreme_ERA5("neg", 5)
# read variable
logging.info(f"reading {var} for {name} at plev {plev}")
var_field = read_ERA5.read_prime_ERA5( var = var, name = name, suffix = suffix, plev =plev)

logging.info(f"composite {var}")
#%%
# select plev 
if not pos_extreme.empty:
    var_pos = range_NAO_composite_single_phase(var_field, pos_extreme)
else:
    var_pos = None

#%%
if not neg_extreme.empty:
    var_neg = range_NAO_composite_single_phase(var_field, neg_extreme)
else:
    var_neg = None


#%%
logging.info("saving results")
# save
var_pos.to_netcdf(f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0composite_distribution/{var}_pos_{name}{suffix}.nc")
var_neg.to_netcdf(f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0composite_distribution/{var}_neg_{name}{suffix}.nc")
logging.info(f"Saved {var}_pos_{name}{suffix}.nc and {var}_neg_{name}{suffix}.nc to /work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0composite_distribution/")
# %%
