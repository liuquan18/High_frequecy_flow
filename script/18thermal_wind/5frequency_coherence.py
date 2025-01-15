#%%
import xarray as xr
import numpy as np
from scipy import signal
# %%
vt = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vt_daily_ano/r1i1p1f1/vt_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930_ano.nc")
# %%
v = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_ano/r1i1p1f1/va_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930_ano.nc")
# %%
vt = vt.vt.sel(time = '1850')
v = v.va.sel(time = '1850')
# %%
