# %%
import xarray as xr
import numpy as np
# %%
origin = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_first10_prime/ua_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_18500501-18590931.nc")
ano = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_ano_first10_prime/ua_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_18500501-18590931_ano.nc")
# %%
