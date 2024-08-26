#%%
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec

# %%
from contrack import contrack
# %%
WB = contrack()
# %%
WB.read("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/momentum_fluxes_daily_global/momentum_fluxes_MJJAS_ano_first10_prime/momentum_fluxes_day_MPI-ESM1-2-LR_historical_r2i1p1f1_gn_18500501-18590931_ano.nc")
# convert Convert timedelta64 to a Supported Resolution: Convert the timedelta64 object to seconds (s) first, and then to hours (h).

WB.ds['time'] = WB.ds.indexes['time'].to_datetimeindex()

# %%
WB.set_up(force=True)
#%%
WB.run_contrack(
    variable='ua',
    threshold=150,
    gorl = '>=',
    overlap=0.5,
    persistence=5,
    twosided=True,
)
# %%
