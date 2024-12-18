#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
# %%

variance = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_bandvar_first10/va_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_1850-05-01-1859-09-30.nc")
# %%
var = variance.__xarray_dataarray_variable__.mean(dim="time")
# %%
# map of var
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree( central_longitude=-120))
var.plot(ax=ax, transform=ccrs.PlateCarree())
ax.coastlines()
# gridlines
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
plt.show()

# %%
