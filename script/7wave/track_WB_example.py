#%%
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec

# %%
import src.ConTrack.contrack as ct
#%%
import importlib
importlib.reload(ct)
# %%
WB = ct.contrack()
# %%
WB.read("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/momentum_fluxes_daily_global/momentum_fluxes_MJJAS_ano_first10_prime/momentum_fluxes_day_MPI-ESM1-2-LR_historical_r2i1p1f1_gn_18500501-18590931_ano.nc")
# convert Convert timedelta64 to a Supported Resolution: Convert the timedelta64 object to seconds (s) first, and then to hours (h).

WB.ds['time'] = WB.ds.indexes['time'].to_datetimeindex()
WB.ds = WB.ds.sel(plev = 25000).drop('plev')

# %%
WB.set_up(force=True)
#%%
WB.run_contrack(
    variable='ua',
    threshold=50,
    gorl = '>=',
    overlap=0.5,
    persistence=3,
    twosided=True,
)
# %%
fig, ax = plt.subplots(figsize=(7, 5), subplot_kw={'projection': ccrs.NorthPolarStereo()})
(xr.where(WB['flag']>1,1,0).sum(dim='time')/WB.ntime*100).plot(levels=np.arange(0,1,0.2), cmap='Oranges', extend = 'max', transform=ccrs.PlateCarree())
(xr.where(WB['flag']>1,1,0).sum(dim='time')/WB.ntime*100).plot.contour(colors='grey', linewidths=0.8, levels=np.arange(0,1,0.2),  transform=ccrs.PlateCarree())
ax.set_extent([-180, 180, 30, 90], crs=ccrs.PlateCarree())
ax.coastlines()
plt.show()

# %%
WB_df = WB.run_lifecycle(flag = 'flag', variable='ua')
# %%
# plotting blocking track (center of mass) and genesis
f, ax = plt.subplots(1, 1, figsize=(7,5), subplot_kw=dict(projection=ccrs.NorthPolarStereo()))
ax.set_extent([-180, 180, 30, 90], crs=ccrs.PlateCarree()); ax.coastlines()
ax.coastlines() # add coastlines

#need to split each blocking track due to longitude wrapping (jumping at map edge)
for bid in np.unique(np.asarray(WB_df['Flag'])): #select blocking id
    lons = np.asarray(WB_df['Longitude'].iloc[np.where(WB_df['Flag']==bid)])
    lats = np.asarray(WB_df['Latitude'].iloc[np.where(WB_df['Flag']==bid)])

    # cosmetic: sometimes there is a gap near map edge where track is split:
    lons[lons >= 355] = 359.9
    lons[lons <= 3] = 0.1
    segment = np.vstack((lons,lats))

    #move longitude into the map region and split if longitude jumps by more than "threshold"
    lon0 = 0 #center of map
    bleft = lon0-0.
    bright = lon0+360
    segment[0,segment[0]> bright] -= 360
    segment[0,segment[0]< bleft]  += 360
    threshold = 180  # CHANGE HERE
    isplit = np.nonzero(np.abs(np.diff(segment[0])) > threshold)[0]
    subsegs = np.split(segment,isplit+1,axis=+1)

    #plot the tracks
    for seg in subsegs:
        x,y = seg[0],seg[1]
        ax.plot(x ,y,c = 'm',linewidth=1, transform=ccrs.PlateCarree())
    #plot the starting points
    ax.scatter(lons[0],lats[0],s=11,c='m', zorder=10, edgecolor='black', transform=ccrs.PlateCarree())

# %%
