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
                          cmap='viridis', vmin=2, vmax=15,
                          extend = 'max',
                          cbar_kwargs={'label': 'AWB', 'orientation': 'horizontal', 
                                       'shrink': 0.7, 'pad': 0.05, 'aspect': 20,
                                       'format': '%.0f'})

awbs_last_mean.flag.plot(ax=axes[0, 1], transform=ccrs.PlateCarree(),
                         cmap='viridis', vmin=2, vmax=15,
                        extend = 'max',
                         cbar_kwargs={'label': 'AWB', 'orientation': 'horizontal',
                                      'shrink': 0.7, 'pad': 0.05, 'aspect': 20,
                                      'format': '%.0f'})

# difference
awbs_diff = awbs_last_mean.flag - awbs_first_mean.flag
awbs_diff.plot(ax=axes[0, 2], transform=ccrs.PlateCarree(),
               cmap='coolwarm', vmin=-5, vmax=5,
               cbar_kwargs={'label': 'AWB Difference', 'orientation': 'horizontal',
                            'shrink': 0.7, 'pad': 0.05, 'aspect': 20,
                            'format': '%.0f'})

# cwbs
cwbs_first_mean.flag.plot(ax=axes[1, 0], transform=ccrs.PlateCarree(),
                          cmap='viridis', vmin=2, vmax=15,
                          extend = 'max',
                          cbar_kwargs={'label': 'CWB', 'orientation': 'horizontal',
                                       'shrink': 0.7, 'pad': 0.05, 'aspect': 20,
                                       'format': '%.0f'})

cwbs_last_mean.flag.plot(ax=axes[1, 1], transform=ccrs.PlateCarree(),
                         cmap='viridis', vmin=2, vmax=15,
                            extend = 'max',
                         cbar_kwargs={'label': 'CWB', 'orientation': 'horizontal',
                                      'shrink': 0.7, 'pad': 0.05, 'aspect': 20,
                                      'format': '%.0f'})

# difference
cwbs_diff = cwbs_last_mean.flag - cwbs_first_mean.flag
cwbs_diff.plot(ax=axes[1, 2], transform=ccrs.PlateCarree(),
               cmap='coolwarm', vmin=-5, vmax=5,
               cbar_kwargs={'label': 'CWB Difference', 'orientation': 'horizontal',
                            'shrink': 0.7, 'pad': 0.05, 'aspect': 20,
                            'format': '%.0f'})

for x in axes.flatten():
    x.coastlines()
    x.set_global()
    x.gridlines()
   
plt.tight_layout()
# save
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0wavebreaking/awbs_cwbs_alllats_change_map.png",)
# %%
fig, axes = plt.subplots(1, 2, figsize=(10, 5),
                         subplot_kw={'projection': ccrs.Orthographic(-30, 70)})

awbs_diff.plot(ax=axes[0], transform=ccrs.PlateCarree(),
               cmap='coolwarm', vmin=-5, vmax=5,extend = 'both',
               cbar_kwargs={'label': 'AWB Difference', 'orientation': 'horizontal',
                            'shrink': 0.6, 'pad': 0.05, 'aspect': 20,
                            'format': '%.0f'})

axes[0].coastlines()
axes[0].set_global()
axes[0].gridlines()

cwbs_diff.plot(ax=axes[1], transform=ccrs.PlateCarree(),
               cmap='coolwarm', vmin=-5, vmax=5,extend = 'both',
               cbar_kwargs={'label': 'CWB Difference', 'orientation': 'horizontal',
                            'shrink': 0.6, 'pad': 0.05, 'aspect': 20,
                            'format': '%.0f'})
axes[1].coastlines()
axes[1].set_global()
axes[1].gridlines()

# a, b
for i, ax in enumerate(axes):
    ax.text(0.1, 0.98, f"{chr(97 + i)}", transform=ax.transAxes,
            fontsize=14, fontweight='bold', va='bottom', ha='right')

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0wavebreaking/awbs_cwbs_diff_map.pdf",
            bbox_inches='tight', dpi=300)
# %%
