#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
# %%
awbs_first = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_anticyclonic_daily/r*i1p1f1/*1850.nc",
                               combine = 'nested', concat_dim = 'ens')
awbs_last = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_anticyclonic_daily/r*i1p1f1/*2090.nc",
                               combine = 'nested', concat_dim = 'ens')
# %%
awbs_first_mean = awbs_first.sum(dim = ('time')).mean(dim = ('ens'))
awbs_last_mean = awbs_last.sum(dim = ('time')).mean(dim = ('ens'))
#%%
cwbs_first = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_cyclonic_daily/r*i1p1f1/*1850.nc",
                               combine = 'nested', concat_dim = 'ens')
cwbs_last = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_cyclonic_daily/r*i1p1f1/*2090.nc",
                               combine = 'nested', concat_dim = 'ens')
#%%
cwbs_first_mean = cwbs_first.sum(dim = ('time')).mean(dim = ('ens'))
cwbs_last_mean = cwbs_last.sum(dim = ('time')).mean(dim = ('ens'))


# %%
fig, axes = plt.subplots(2, 3, figsize=(12, 10),
                       subplot_kw={'projection': ccrs.Orthographic(-60, 70)})
awbs_first_mean.flag.plot(ax=axes[0, 0], transform=ccrs.PlateCarree(),
                          cmap='viridis', vmin=0, vmax=15,
                          cbar_kwargs={'label': 'AWB Flag'})

awbs_last_mean.flag.plot(ax=axes[0, 1], transform=ccrs.PlateCarree(),
                         cmap='viridis', vmin=0, vmax=15,
                         cbar_kwargs={'label': 'AWB Flag'})

# difference
awbs_diff = awbs_last_mean.flag - awbs_first_mean.flag
awbs_diff.plot(ax=axes[0, 2], transform=ccrs.PlateCarree(),
               cmap='coolwarm', vmin=-5, vmax=5,
               cbar_kwargs={'label': 'AWB Flag Difference'})

# cwbs
cwbs_first_mean.flag.plot(ax=axes[1, 0], transform=ccrs.PlateCarree(),
                          cmap='viridis', vmin=0, vmax=15,
                          cbar_kwargs={'label': 'CWB Flag'})    

cwbs_last_mean.flag.plot(ax=axes[1, 1], transform=ccrs.PlateCarree(),
                         cmap='viridis', vmin=0, vmax=15,
                         cbar_kwargs={'label': 'CWB Flag'}) 

# difference
cwbs_diff = cwbs_last_mean.flag - cwbs_first_mean.flag
cwbs_diff.plot(ax=axes[1, 2], transform=ccrs.PlateCarree(),
               cmap='coolwarm', vmin=-5, vmax=5,
               cbar_kwargs={'label': 'CWB Flag Difference'})

for x in axes.flatten():
    x.coastlines()
    x.set_global()
    x.gridlines(draw_labels=True, xlocs=None, ylocs=np.arange(-80, 91, 20))
    # x.set_extent([-180, 180, -20, 90], crs=ccrs.PlateCarree())
   
plt.tight_layout()
# save
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0wavebreaking/awbs_cwbs_alllats_change_map.png",)
# %%
