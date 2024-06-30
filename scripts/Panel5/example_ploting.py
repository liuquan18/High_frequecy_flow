#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
# %%
BE = xr.open_dataset("/work/mh0033/m300883/Tel_MMLE/data/MPI_GE_onepct_30_daily/block_event/onepct_1850-1999_ens_0069.gph500.nc")

#%%
BE = BE['IB index']
#%%
BE_sel = BE.isel(time = slice(0,30))

#%%
BE_sel.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/example_blocking_event/ex69_first30.nc")
#%%
days = pd.date_range('1850-06-04','1850-06-30',freq = 'D')

#%%

BE = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/example_blocking_event/ex69_first30.nc")
#%%
def BE_time_int(BE):
    hours = pd.date_range(BE.time[0].values,BE.time[-1].values,periods=BE.time.shape[0]*2)
#%%
    BE_int = BE['IB index'].interp(time = hours, method = 'linear')
#%%
    BE_sum = BE_int.sum(dim = ('lat','lon'))
#%%
# find the time when BE_sum is maximum
    time_max = BE_sum.sel(time = BE_sum == BE_sum.max(), method = 'nearest').time
# divide the hours into 2 parts, before and after the time_max
# Create a boolean mask
    mask = hours.values < time_max.values

# Get the hours before time_max
    hours_before = hours[mask]

# Get the hours after time_max
    hours_after = hours[~mask]
    return BE_int,hours_before,hours_after

BE_int, hours_before, hours_after = BE_time_int(BE)
# %%
fig, axes = plt.subplots(1, 1, figsize=(10, 10), subplot_kw={'projection': ccrs.Orthographic(-20,60)})
cmap_before = plt.cm.get_cmap('Reds', len(hours_before))
cmap_after = plt.cm.get_cmap('Blues', len(hours_after))

for i,hour in enumerate(hours_before):
    # Calculate the color index
    color_index = i / len(hours_before)

    # Get the color from the colormap
    color = cmap_before(color_index)
    BE_int.sel(time=hour, method = 'nearest').plot.contour(ax=axes, 
                                                      transform=ccrs.PlateCarree(), 
                                                      colors = [color],
                                                      levels=[0,0.5,1.5], )
    

for i,hour in enumerate(hours_after):
    # Calculate the color index
    color_index = i / len(hours_after)

    # Get the color from the colormap
    color = cmap_after(color_index)
    BE_int.sel(time=hour, method = 'nearest').plot.contour(ax=axes, 
                                                      transform=ccrs.PlateCarree(), 
                                                      colors = [color],
                                                      levels=[0,0.5,1.5], )
# %%
