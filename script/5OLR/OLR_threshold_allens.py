#%%
import pandas as pd
import xarray as xr
import numpy as np
import glob
import eventextreme.eventextreme as ee
import eventextreme.extreme_threshold as et
# %%
df_windows = []
base_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_threshold/"
files = glob.glob(f"{base_dir}*.nc")

#%%
thresholds = xr.open_mfdataset(files, combine = 'nested', concat_dim = 'ens')

#%%
threshold_allens = thresholds.mean(dim = 'ens')


#%%
threshold_allens.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_threshold/OLR_threshold_allens/threshold_allens.nc")
# %%
