#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from src.data_helper.read_variable import read_prime
#%%
jet_first = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_std_decmean/ua_std_monmean_ensmean_185005_185909.nc")
jet_last = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_std_decmean/ua_std_monmean_ensmean_209005_209909.nc")

#%%
jet_first = jet_first.mean(dim='time').sel(plev=25000)
jet_last = jet_last.mean(dim='time').sel(plev=25000)
# %%
baroclinicity_first = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/eady_growth_rate_std_decmean/eady_growth_rate_std_monmean_ensmean_185005_185909.nc")
baroclinicity_last = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/eady_growth_rate_std_decmean/eady_growth_rate_std_monmean_ensmean_209005_209909.nc")
# %%
baroclinicity_first = baroclinicity_first.mean(dim = 'time').sel(plev = 85000)
baroclinicity_last = baroclinicity_last.mean(dim = 'time').sel(plev = 85000)


# %%
# plotting
fig, ax = plt.subplots(2, 3, figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})

# --- First row: Jet ---
# First period
jet_first['std'].plot(
    ax=ax[0, 0], transform=ccrs.PlateCarree(), cmap='viridis',
    levels=np.arange(50, 251, 50),
    cbar_kwargs={'label': 'Jet Std (m/s)', 'orientation': 'horizontal'}
)
ax[0, 0].set_title('Jet 1850')
ax[0, 0].coastlines()
ax[0, 0].set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
ax[0, 0].gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)

# Last period
jet_last['std'].plot(
    ax=ax[0, 1], transform=ccrs.PlateCarree(), cmap='viridis',
    levels=np.arange(50, 251, 50),
    cbar_kwargs={'label': 'Jet Std (m/s)', 'orientation': 'horizontal'}
)
ax[0, 1].set_title('Jet 2090')
ax[0, 1].coastlines()
ax[0, 1].set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
ax[0, 1].gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)

# Difference
jet_diff = jet_last['std'] - jet_first['std']
jet_diff.plot(
    ax=ax[0, 2], transform=ccrs.PlateCarree(), cmap='RdBu_r',
    levels=np.arange(-50, 55, 5),
    cbar_kwargs={'label': 'Jet Diff (m/s)', 'orientation': 'horizontal'}
)
ax[0, 2].set_title('Jet Diff 2090 - 1850')
ax[0, 2].coastlines()
ax[0, 2].set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
ax[0, 2].gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)

# --- Second row: Baroclinicity ---
# First period
baroclinicity_first['std'].plot(
    ax=ax[1, 0], transform=ccrs.PlateCarree(), cmap='viridis',
    levels=np.arange(0, 3, 0.5)*1e-9,
    cbar_kwargs={'label': 'Baroclinicity (s⁻¹)', 'orientation': 'horizontal'}
)
ax[1, 0].set_title('Baroclinicity 1850')
ax[1, 0].coastlines()
ax[1, 0].set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
ax[1, 0].gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)

# Last period
baroclinicity_last['std'].plot(
    ax=ax[1, 1], transform=ccrs.PlateCarree(), cmap='viridis',
    levels=np.arange(0, 3, 0.5)*1e-9,
    cbar_kwargs={'label': 'Baroclinicity (s⁻¹)', 'orientation': 'horizontal'}
)
ax[1, 1].set_title('Baroclinicity 2090')
ax[1, 1].coastlines()
ax[1, 1].set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
ax[1, 1].gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)

# Difference
baroclinicity_diff = baroclinicity_last['std'] - baroclinicity_first['std']
baroclinicity_diff.plot(
    ax=ax[1, 2], transform=ccrs.PlateCarree(), cmap='RdBu_r',
    levels=np.linspace(-0.5e-9, 0.6e-9, 11),
    cbar_kwargs={'label': 'Difference (s⁻¹)', 'orientation': 'horizontal'}
)
ax[1, 2].set_title('Baroclinicity Diff 2090 - 1850')
ax[1, 2].coastlines()
ax[1, 2].set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
ax[1, 2].gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)

plt.tight_layout()

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0mean_flow/std_change_map.pdf", bbox_inches='tight', dpi=300)
# %%
