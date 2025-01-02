# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from src.moisture.longitudinal_contrast import read_data
from sklearn.linear_model import LinearRegression

# %%
first_tas = read_data("tas", 1850, (-90, 90), meridional_mean=False, chunks = {'time': -1})
first_hus = read_data("hus", 1850, (-90, 90), meridional_mean=False, chunks = {'time': -1})
first_hussat = read_data("hussat", 1850, (-90, 90), meridional_mean=False, chunks = {'time': -1})
first_data = xr.Dataset({"tas": first_tas, "hus": first_hus * 1000, 'hussat': first_hussat * 1000})

# %%

last_tas = read_data("tas", 2090, (-90, 90), meridional_mean=False, chunks = {'time': -1})
last_hus = read_data("hus", 2090, (-90, 90), meridional_mean=False, chunks = {'time': -1})
last_hussat = read_data("hussat", 2090, (-90, 90), meridional_mean=False, chunks = {'time': -1})
last_data = xr.Dataset({"tas": last_tas, "hus": last_hus * 1000, 'hussat': last_hussat * 1000})


#%%
first_data.load()
last_data.load()
#%%
lim_first = first_data.tas.quantile(0.1, dim = ('time', 'ens'))
first_data = first_data.where(first_data.tas >= lim_first, drop = True)

#%%
lim_last = last_data.tas.quantile(0.1, dim = ('time', 'ens'))
last_data = last_data.where(last_data.tas >= lim_last, drop = True)


#%%
first_ratio_hus = first_data.hus / first_data.tas
first_ratio_hus = first_ratio_hus.mean(dim = ('time', 'ens'))
# %%
last_ratio_hus = last_data.hus / last_data.tas
last_ratio_hus = last_ratio_hus.mean(dim = ('time', 'ens'))
# %%
first_ratio_hus.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_ratio_hus.nc")
# %%
last_ratio_hus.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_ratio_hus.nc")
# %%
first_ratio_hussat = first_data.hussat / first_data.tas
first_ratio_hussat = first_ratio_hussat.mean(dim = ('time', 'ens'))
# %%
last_ratio_hussat = last_data.hussat / last_data.tas
last_ratio_hussat = last_ratio_hussat.mean(dim = ('time', 'ens'))

# %%
first_ratio_hussat.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_ratio_hussat.nc")
last_ratio_hussat.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_ratio_hussat.nc")
# %%
