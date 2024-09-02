# %%
import xarray as xr
import numpy as np
import pandas as pd
from cartopy.util import add_cyclic_point

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
# %%
#%%
def read_WB(period):
    WB_flat_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wavebreak_events/wavebreak_flag_{period}/"
    # 
    WB_flag = xr.open_mfdataset(f"{WB_flat_dir}*.nc", combine = 'nested', concat_dim = 'ens')
    # 
    WB_flag_com = WB_flag.stack(com = ('ens','time'))
    #
    WB_flag_com = erase_white_line(WB_flag_com.flag)
    #
    WB_flag_com = WB_flag_com.to_dataset(name = 'flag')
    return WB_flag_com


#%%
def erase_white_line(data):
    """
    erase the white line aroung 180 degree.
    """
    data = data.transpose(..., "lon")  # make the lon as the last dim
    dims = data.dims  # all the dims
    res_dims = tuple(dim for dim in dims if dim != "lon")  # dims apart from lon
    res_coords = [data.coords[dim] for dim in res_dims]  # get the coords

    # add one more longitude to the data
    data_value, lons = add_cyclic_point(data, coord=data.lon, axis=-1)

    # make the lons as index
    lon_dim = xr.IndexVariable(
        "lon", lons, attrs={"standard_name": "longitude", "units": "degrees_east"}
    )

    # the new coords with changed lon
    new_coords = res_coords + [lon_dim]  # changed lon but new coords

    new_data = xr.DataArray(data_value, coords=new_coords, name=data.name)

    return new_data

# %%
first_WB = read_WB('first10')
last_WB = read_WB('last10')


#%%
def plot_map(WB_flag_com, ax):
    p = (xr.where(WB_flag_com['flag']>1,1,0).sum(dim='com')/WB_flag_com.com.size*100).plot(ax = ax, levels=np.arange(0,0.21,0.02), cmap='Oranges', extend = 'max', transform=ccrs.PlateCarree(), add_colorbar = False)
    (xr.where(WB_flag_com['flag']>1,1,0).sum(dim='com')/WB_flag_com.com.size*100).plot.contour(ax = ax, colors='grey', linewidths=0.8, levels=np.arange(0,0.21,0.02),  transform=ccrs.PlateCarree(), add_colorbar = False)
    ax.set_extent([-180, 180, 30, 90], crs=ccrs.PlateCarree())
    ax.coastlines()

    return ax, p
# %%
fig, ax = plt.subplots(figsize=(15, 8), ncols=2, nrows = 1, subplot_kw={'projection': ccrs.NorthPolarStereo()})
_, p = plot_map(first_WB, ax[0])
plot_map(last_WB, ax[1])

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(p, cax=cbar_ax, orientation="horizontal")

ax[0].set_title('First 10 years')
ax[1].set_title('Last 10 years')

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/Scherrer_wave_break_climatology.png")
# %%
