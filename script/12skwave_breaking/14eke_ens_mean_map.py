#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line
import matplotlib.colors as mcolors
import cartopy
#%%
import src.plotting.util as util
import importlib
importlib.reload(util)
from src.plotting.util import lon2x

# %%
ensmean_first = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_ensmean_50000_1850.nc")
ensmean_last = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_ensmean_50000_2090.nc")
# %%
ensmean_first = ensmean_first.eke
ensmean_last = ensmean_last.eke
#%%
ensmean_first = ensmean_first.mean(dim = 'time').squeeze()
ensmean_last = ensmean_last.mean(dim = 'time').squeeze()
#%%
ensmean_first.compute()
ensmean_last.compute()
#%%
ensmean_first = erase_white_line(ensmean_first)
ensmean_last = erase_white_line(ensmean_last)

#%%
NAO_pos_first = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_NAO_pos_15_5_mean_1850.nc")
NAO_neg_first = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_NAO_neg_15_5_mean_1850.nc")

NAO_pos_last = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_NAO_pos_15_5_mean_2090.nc")
NAO_neg_last = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/eke_NAO_neg_15_5_mean_2090.nc")
#%%
NAO_pos_first = NAO_pos_first.eke
NAO_neg_first = NAO_neg_first.eke

NAO_pos_last = NAO_pos_last.eke
NAO_neg_last = NAO_neg_last.eke

#%%
NAO_pos_first = NAO_pos_first.mean(dim = 'event').squeeze()
NAO_neg_first = NAO_neg_first.mean(dim = 'event').squeeze()

NAO_pos_last = NAO_pos_last.mean(dim = 'event').squeeze()
NAO_neg_last = NAO_neg_last.mean(dim = 'event').squeeze()
#%%
NAO_pos_first.compute()
NAO_neg_first.compute()

NAO_pos_last.compute()
NAO_neg_last.compute()
#%%
NAO_pos_first = erase_white_line(NAO_pos_first)
NAO_neg_first = erase_white_line(NAO_neg_first)

NAO_pos_last = erase_white_line(NAO_pos_last)
NAO_neg_last = erase_white_line(NAO_neg_last)
#%%
def remove_zonalmean(arr):
    arr = arr - arr.mean(dim = 'lon')
    return arr
#%%
# ensmean_first = remove_zonalmean(ensmean_first)
# ensmean_last = remove_zonalmean(ensmean_last)

NAO_pos_first = remove_zonalmean(NAO_pos_first)
NAO_neg_first = remove_zonalmean(NAO_neg_first)

NAO_pos_last = remove_zonalmean(NAO_pos_last)
NAO_neg_last = remove_zonalmean(NAO_neg_last)

#%%
# %%
fig, axes = plt.subplots(3, 3, figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree(-90)})

# ens mean
ensmean_first.plot.contourf(ax=axes[0, 0], transform=ccrs.PlateCarree(), cmap='Reds', levels=np.arange(0, 35, 5), extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})
ensmean_last.plot.contourf(ax=axes[1, 0], transform=ccrs.PlateCarree(), cmap='Reds', levels=np.arange(0, 35, 5), extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})
cbar = (ensmean_last - ensmean_first).plot.contourf(ax=axes[2, 0], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=np.arange(-15, 20, 5),extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})


# NAO neg
NAO_neg_first.plot.contourf(ax=axes[0, 1], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=np.arange(-3, 3.5, 0.5), extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})
NAO_neg_last.plot.contourf(ax=axes[1, 1], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=np.arange(-3, 3.5, 0.5), extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6 })
cbar = (NAO_neg_last - NAO_neg_first).plot.contourf(ax=axes[2, 1], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=np.arange(-3, 3.5, 0.5), extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})

# NAO pos
NAO_pos_first.plot.contourf(ax=axes[0, 2], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=np.arange(-3, 3.5, 0.5), extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})
NAO_pos_last.plot.contourf(ax=axes[1, 2], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=np.arange(-3, 3.5, 0.5), extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})
(NAO_pos_last - NAO_pos_first).plot.contourf(ax=axes[2, 2], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=np.arange(-3, 3.5, 0.5), extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})

for ax in axes.flatten():
    ax.coastlines()
    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.axhline(20, color='k', lw=0.5, ls='dotted')
    ax.axhline(60, color='k', lw=0.5, ls='dotted')

# latitude ticks
for i, ax in enumerate(axes.flatten()):
    ax.set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())

    if i % 3 == 0:
        ax.set_yticks([20, 60], crs=ccrs.PlateCarree())
        ax.set_ylabel("Latitude")
        ax.yaxis.set_major_formatter(cartopy.mpl.ticker.LatitudeFormatter())
    else:
        ax.set_yticks([])
    
    if i // 3 == 2:
        ax.set_xticklabels(['180°', '120°W', '60°W', '0°', '60°E', '120°E'])
    else:
        ax.set_xticks([])

    ax.set_xlabel("")
    ax.set_ylabel("")

plt.tight_layout(w_pad = 0.5, h_pad = 1.1)

# add a, b, c, d, e, f
plt.figtext(0.04, 0.95, "a", fontsize=12, fontweight='bold')
plt.figtext(0.04, 0.63, "b", fontsize=12, fontweight='bold')
plt.figtext(0.04, 0.31, "c", fontsize=12, fontweight='bold')

plt.figtext(0.36, 0.95, "d", fontsize=12, fontweight='bold')
plt.figtext(0.36, 0.63, "e", fontsize=12, fontweight='bold')
plt.figtext(0.36, 0.31, "f", fontsize=12, fontweight='bold')

plt.figtext(0.68, 0.95, "g", fontsize=12, fontweight='bold')
plt.figtext(0.68, 0.63, "h", fontsize=12, fontweight='bold')
plt.figtext(0.68, 0.31, "i", fontsize=12, fontweight='bold')


# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/eke_maps.pdf", dpi = 300)
# %%
fig, axes = plt.subplots(3, 2, figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree(-90)})


# ens mean
ensmean_first.plot.contourf(ax=axes[0, 0], transform=ccrs.PlateCarree(), cmap='Reds', levels=np.arange(0, 35, 5), extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})
ensmean_last.plot.contourf(ax=axes[1, 0], transform=ccrs.PlateCarree(), cmap='Reds', levels=np.arange(0, 35, 5), extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})
cbar = (ensmean_last - ensmean_first).plot.contourf(ax=axes[2, 0], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=np.arange(-15, 20, 5),extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})



(NAO_pos_first - NAO_neg_first).plot.contourf(ax=axes[0, 1], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=np.arange(-3, 3.5, 0.5), extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})
(NAO_pos_last - NAO_neg_last).plot.contourf(ax=axes[1, 1], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=np.arange(-3, 3.5, 0.5), extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})
((NAO_pos_last - NAO_neg_last) - (NAO_pos_first - NAO_neg_first)).plot.contourf(ax=axes[2, 1], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=np.arange(-3, 3.5, 0.5), extend = 'both', cbar_kwargs={'label': r'$m^2/s^2$', 'orientation': 'horizontal', 'shrink':0.6})

for ax in axes.flatten():
    ax.coastlines()
    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.axhline(20, color='k', lw=0.5, ls='dotted')
    ax.axhline(60, color='k', lw=0.5, ls='dotted')

axes[2,1].axvline(x=lon2x(-145, axes[2,1]), ymin=0.22, ymax=0.65, color='k', lw=0.5, ls='dotted')
axes[2,1].axvline(x=lon2x(140, axes[2,1]), ymin=0.22, ymax=0.65, color='k', lw=0.5, ls='dotted')
axes[2,1].axvline(x=lon2x(-30, axes[2,1]), ymin=0.22, ymax=0.65, color='k', lw=0.5, ls='dotted')
axes[2,1].axvline(x=lon2x(-70, axes[2,1]), ymin=0.22, ymax=0.65, color='k', lw=0.5, ls='dotted')

# latitude ticks
for i, ax in enumerate(axes.flatten()):
    ax.set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())

    if i % 2 == 0:
        ax.set_yticks([20, 60], crs=ccrs.PlateCarree())
        ax.set_ylabel("Latitude")
        ax.yaxis.set_major_formatter(cartopy.mpl.ticker.LatitudeFormatter())
    else:
        ax.set_yticks([])
    
    if i // 2 == 2:
        ax.set_xticklabels(['180°', '120°W', '60°W', '0°', '60°E', '120°E'])
    else:
        ax.set_xticks([])

    ax.set_xlabel("")
    ax.set_ylabel("")
# add a, b, c, d
plt.figtext(0.04, 0.95, "a", fontsize=12, fontweight='bold')
plt.figtext(0.04, 0.63, "b", fontsize=12, fontweight='bold')
plt.figtext(0.04, 0.31, "c", fontsize=12, fontweight='bold')

plt.figtext(0.52, 0.95, "d", fontsize=12, fontweight='bold')
plt.figtext(0.52, 0.63, "e", fontsize=12, fontweight='bold')
plt.figtext(0.52, 0.31, "f", fontsize=12, fontweight='bold')

plt.tight_layout(w_pad = 0.5, h_pad = 1.1)
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/eke_NAO_diff_maps.pdf", dpi = 300)
# %%
