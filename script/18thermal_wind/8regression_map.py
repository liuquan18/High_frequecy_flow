#%%
import xarray as xr
import numpy as np
import pandas as pd

import sys
from scipy.stats import linregress
import matplotlib.pyplot as plt 
import seaborn as sns
import cartopy.crs as ccrs

#%%
var1 = 'tas'
var1_ds = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var1}_daily_std/r1i1p1f1/{var1}_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc")
var1_ds = var1_ds[var1]
if var1 == 'hus':
    var1_ds = var1_ds * 1000 # unit conversion from kg/kg to g/kg
# %%
vp = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vp/r1i1p1f1/vp_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc").va
# %%
vp = vp.sel(plev = slice(100000, 85000)).mean(dim = 'plev')
# %%
# calculate the regression
slope = xr.apply_ufunc(
    lambda x, y: linregress(x, y)[0],  # Extract the slope
    vp, var1_ds,
    input_core_dims=[['time'], ['time']],
    vectorize=True,
    dask='parallelized',
    output_dtypes=[float]
)

# intercept = xr.apply_ufunc(
#     lambda x, y: linregress(x, y)[1],  # Extract the intercept
#     var1_ds, vp,
#     input_core_dims=[['time'], ['time']],
#     vectorize=True,
#     dask='parallelized',
#     output_dtypes=[float]
# )

# r_value = xr.apply_ufunc(
#     lambda x, y: linregress(x, y)[2],  # Extract the r_value
#     var1_ds, vp,
#     input_core_dims=[['time'], ['time']],
#     vectorize=True,
#     dask='parallelized',
#     output_dtypes=[float]
# )

# p_value = xr.apply_ufunc(
#     lambda x, y: linregress(x, y)[3],  # Extract the p_value
#     var1_ds, vp,
#     input_core_dims=[['time'], ['time']],
#     vectorize=True,
#     dask='parallelized',
#     output_dtypes=[float]
# )

std_err = xr.apply_ufunc(
    lambda x, y: linregress(x, y)[4],  # Extract the std_err
    vp, var1_ds,
    input_core_dims=[['time'], ['time']],
    vectorize=True,
    dask='parallelized',
    output_dtypes=[float]
)

# %%
# plot the map of slope
fig, ax = plt.subplots(1, 1, figsize=(10, 5), subplot_kw={'projection': ccrs.PlateCarree(-90)})
slope.plot(ax=ax, levels = np.arange(-0.04, 0.045, 0.005),
           transform=ccrs.PlateCarree(), cmap='RdBu_r', cbar_kwargs={'label': 'Slope'})
ax.coastlines()
# %%
