#%%
import xarray as xr
import numpy as np
import os
import sys
import logging
import glob
import pandas as pd
logging.basicConfig(level=logging.INFO)
# %%
import src.dynamics.EP_flux as EP_flux
import importlib
importlib.reload(EP_flux)
# %%
ta_file = "/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/ta_monthly_mean/ta_monthly_05_09.nc"
q_file = "/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/hus_monthly_mean/hus_monthly_05_09.nc"
to_path = "/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/equiv_theta_monthly_mean/"
to_file = "/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/equiv_theta_monthly_mean/equiv_theta_monthly_05_09.nc"

if not os.path.exists(to_path):
    os.makedirs(to_path)
    logging.info("This node is processing equivalent potential temperature monthly mean")

t = xr.open_dataset(ta_file).var130
q = xr.open_dataset(q_file).var133

# change the time to datetime64[ns]
# Convert time values like 19790501.979167 to datetime64[ns] with daily frequency
if not np.issubdtype(t['time'].dtype, np.datetime64):
    t_dates = pd.to_datetime(t['time'].astype(int).astype(str), format='%Y%m%d')
    t['time'] = t_dates
    q['time'] = t_dates  # Ensure q has the same time index
else:
    t_dates = t['time']
    q['time'] = t_dates



# calculate equivalent potential temperature
ds = EP_flux.equivalent_potential_temperature(t, q, p='plev', p0=1e5)
# save to netcdf
ds.to_netcdf(to_file)
ds.close()
# %%
