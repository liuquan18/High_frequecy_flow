#%%
import wavebreaking as wb
import numpy as np
import pandas as pd
import xarray as xr
import metpy.calc as mpcalc
import metpy.units as mpunits
import cartopy.crs as ccrs

# %%

ua_data = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/tmp/u.nc")
u = ua_data.ua
#%%
va_data = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/tmp/v.nc")
v = va_data.va
# %%
u = u.sel(plev = 25000, time = '1850-05-01')
v = v.sel(plev = 25000, time = '1850-05-01')
# %%
u = u * mpunits.units('m/s')
v = v * mpunits.units('m/s')
# %%
u = u.metpy.assign_crs(grid_mapping_name='latitude_longitude', earth_radius=6371229)
v = v.metpy.assign_crs(grid_mapping_name='latitude_longitude', earth_radius=6371229)
# %%
# calculate absolute vorticity
avor = mpcalc.absolute_vorticity(u, v)
# %%

avor.name = 'AV'
# %%
smoothed = wb.calculate_smoothed_field(data = avor,
                                       passes = 5)
# %%
cdoflux = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/E_N_MJJAS_first10_prime/E_N_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_18500501-18590931.nc")
# %%
cdoflux = cdoflux.sel(time = '1850-05-01', plev = 25000).ua
#%%
cdoflux['time'] = cdoflux.indexes['time'].to_datetimeindex()
cdoflux['lat'] = smoothed.lat
cdoflux['lon'] = smoothed.lon
# %%
mflux = wb.calculate_momentum_flux(u = u, v = v)

# %%
# calculate contours
contours = wb.calculate_contours(data=smoothed,
                                 contour_levels=[7.5* 1e-5 ,9.4* 1e-5, 11.2* 1e-5],
                                 periodic_add=120, # optional
                                 original_coordinates=False) # optional
#%%
# calculate overturnings
overturnings = wb.calculate_overturnings(data=smoothed,
                                         contour_levels=[7.5* 1e-5 ,9.4* 1e-5, 11.2* 1e-5],
                                         contours=contours, #optional
                                         range_group=5, # optional
                                         min_exp=5, # optional
                                         intensity=cdoflux, # optional
                                         periodic_add=120) # optional

# %%
events = overturnings

#%%
# mean_var to 1 if events.intensity is negative, to 2 if positive
events = events.assign(mean_var=(events.intensity < 0).astype(int) + 1)


# %%
# anticyclonic and cyclonic by intensity for the Northern Hemisphere
anticyclonic = events[events.intensity >= 0]
cyclonic = events[events.intensity < 0]


# %%
flag_array = wb.to_xarray(data = smoothed,
                          events = anticyclonic)
# %%
# import cartopy for projection

wb.plot_step(flag_data=flag_array,
             step="1850-05-01T12:00:00", #index or date
             data=smoothed, # optional
             contour_levels=np.arange(0,1,0.2), # optional
             proj=ccrs.PlateCarree(), # optional
             size=(12,8), # optional
             periodic=True, # optional
             labels=True,# optional
             levels=None, # optional
             cmap="Blues", # optional
             color_events="gold", # optional
             title="") # optional

# %%
import matplotlib.pyplot as plt
fig, ax = plt.subplots(subplot_kw=dict(projection=ccrs.PlateCarree()), figsize=(12, 8))
p = smoothed.isel(time = 0).plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap="Blues", levels=np.arange(-10,11,2)* 1e-5)
ax.coastlines()
f = flag_array.isel(time = 0).plot.contour(ax=ax, transform=ccrs.PlateCarree(), colors="gold", levels=[0, 1,2])
# %%
