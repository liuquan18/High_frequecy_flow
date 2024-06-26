#%%
import xarray as xr
import numpy as np
# %%
ex = xr.open_dataset("/pool/data/CMIP6/data/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r10i1p1f1/day/zg/gn/v20190710/zg_day_MPI-ESM1-2-LR_historical_r10i1p1f1_gn_18500101-18691231.nc")
# %%
ex  = xr.open_dataset("/pool/data/CMIP6/data/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/ssp585/r10i1p1f1/day/zg/gn/v20190710/zg_day_MPI-ESM1-2-LR_ssp585_r10i1p1f1_gn_20150101-20341231.nc")
# %%
ex = xr.open_dataset("/pool/data/CMIP6/data/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r10i1p1f1/Omon/tos/gn/v20190710/tos_Omon_MPI-ESM1-2-LR_historical_r10i1p1f1_gn_185001-186912.nc")
# %%
ex2 = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/scripts/tmp/ex2.nc")
# %%
