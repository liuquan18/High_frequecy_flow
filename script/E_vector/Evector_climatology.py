#%%
import xarray as xr
import numpy as np
import pandas as pd

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.util import add_cyclic_point

# %%
def read_data(period):

    M_file=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_climatology/E_M_climatology_{period}_prime/E_M_climatology_{period}_prime.nc"
    N_file=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_climatology/E_N_climatology_{period}_prime/E_N_climatology_{period}_prime.nc"

    M = xr.open_dataset(M_file)
    N = xr.open_dataset(N_file)

    M = M.ua.sel(plev=25000)
    N = N.ua.sel(plev=25000)

    E_M = -2*M
    E_N = -N



    if period == 'first10':
        u_hat_mean = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_season_global/ua_Amon_MPI-ESM1-2-LR_HIST_ensmean_185005-185909.nc")
    else:
        u_hat_mean = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_season_global/ua_Amon_MPI-ESM1-2-LR_HIST_ensmean_209105-210009.nc")
    
    u_hat_mean = u_hat_mean.ua.sel(plev=25000)


    return E_M, E_N, u_hat_mean
# %%
def plot_E(E_M, E_N, u_hat, ax):

    E_M = E_M.isel(time = 0)
    E_N = E_N.isel(time = 0)
    u_hat = u_hat.mean(dim='time')

    lon = E_M.lon.values
    lat = E_M.lat.values

    skip = 3
    
    ax.coastlines(color = 'grey', linewidth = 0.5)
    lines = u_hat.plot.contourf(ax=ax, levels = np.arange(10,30,5),kwargs=dict(inline=True),alpha = 0.5, extend = 'max', add_colorbar = False)

    arrows = ax.quiver(lon[::skip], lat[::skip], E_M[::skip,::skip], E_N[::skip,::skip], scale = 1000)

    ax.set_extent([-180, 180, 0, 90], ccrs.PlateCarree())

    ax.quiverkey(arrows, X=0.9, Y=1.05, U=25, label=r'$25 m^2/s^2$', labelpos='E')

    return ax, lines, arrows

    
# %%
first10_E_M, first10_E_N, first10_u_hat = read_data('first10')
# %%
last10_E_M, last10_E_N, last10_u_hat = read_data('last10')
# %%
fig, ax = plt.subplots(2, 1, figsize = (10,8), subplot_kw=dict(projection=ccrs.PlateCarree(-120)))
plot_E(first10_E_M, first10_E_N,  first10_u_hat, ax[0])
ax[0].set_title('First 10 years')
_, p,_ = plot_E(last10_E_M, last10_E_N,  last10_u_hat, ax[1])
ax[1].set_title('Last 10 years')

# add colorbar
fig.colorbar(p, ax = [ax[0], ax[1]], orientation = 'horizontal', label = 'u (m/s)', pad = 0.1, aspect = 50)

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/E_vector/E_vector_climatology.png")
# %%
