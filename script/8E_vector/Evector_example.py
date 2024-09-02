#%%
import xarray as xr
import numpy as np
import pandas as pd

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.util import add_cyclic_point
# %%
# M
M = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_M_daily_global/E_M_MJJAS_ano_first10_prime/E_M_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_18500501-18590931_ano.nc")
# %%
# N
N = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/E_N_MJJAS_ano_first10_prime/E_N_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_18500501-18590931_ano.nc")
# %%
M = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_M_daily_global/E_M_MJJAS_ano_last10_prime/E_M_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_20910501-21000931_ano.nc")
N = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/E_N_MJJAS_ano_last10_prime/E_N_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_20910501-21000931_ano.nc")

#%%
M = M.ua.sel(plev=25000)
N = N.ua.sel(plev=25000)
#%%
## E vector
# E = (-2M, -N) = (M_2, -N)
E_M = -2*M
E_N = -N
#%%
E_S = np.sqrt(E_M**2 + E_N**2)
# %%
# vector plot of E
E_M_plot = E_M.mean(dim='time')
E_N_plot = E_N.mean(dim='time')
E_S_plot = E_S.mean(dim='time')

# %%
lon = E_M_plot.lon.values
lat = E_M_plot.lat.values
# %%
skip = 3
levels = np.arange(500, 2500, 500)
fig, ax = plt.subplots(subplot_kw=dict(projection=ccrs.PlateCarree(-120)))
ax.coastlines(color = 'grey', linewidth = 0.5)
ax.contourf(lon, lat, E_S_plot, transform=ccrs.PlateCarree(), levels = levels)

ax.quiver(lon[::skip], lat[::skip], E_M_plot[::skip,::skip], E_N_plot[::skip,::skip], scale = 1000)
ax.set_extent([-180, 180, 0, 90], ccrs.PlateCarree())
# %%
