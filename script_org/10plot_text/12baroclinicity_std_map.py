#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from src.data_helper.read_variable import read_prime
# %%
first_baroclinicity = read_prime(1850, "eady_growth_rate", model_dir = "MPI_GE_CMIP6_allplev", suffix = '_ano')
# %%
last_baroclinicity = read_prime(2090, "eady_growth_rate", model_dir = "MPI_GE_CMIP6_allplev", suffix = '_ano')
# %%
std_first = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/eady_growth_rate_std_decmean/eady_growth_rate_std_monmean_ensmean_185005_185909.nc")
# %%
std_last = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/eady_growth_rate_std_decmean/eady_growth_rate_std_monmean_ensmean_209005_209909.nc")
# %%
std_first = std_first.mean(dim = 'time').sel(plev = 85000)
std_last = std_last.mean(dim = 'time').sel(plev = 85000)
# %%
# plotting
fig, ax = plt.subplots(1, 3, figsize=(18, 6), subplot_kw={'projection': ccrs.PlateCarree()})

# First period
std_first['std'].plot(
    ax=ax[0], transform=ccrs.PlateCarree(), cmap='viridis',
    levels=np.arange(0, 3, 0.5)*1e-9,
    cbar_kwargs={'label': 'Baroclinicity (s⁻¹)', 'orientation': 'horizontal'}
)
ax[0].set_title('Baroclinicity 1850')
ax[0].coastlines()
ax[0].set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
ax[0].gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)

# Last period
std_last['std'].plot(
    ax=ax[1], transform=ccrs.PlateCarree(), cmap='viridis',
    levels=np.arange(0, 3, 0.5)*1e-9,
    cbar_kwargs={'label': 'Baroclinicity (s⁻¹)', 'orientation': 'horizontal'}
)
ax[1].set_title('Baroclinicity 2090')
ax[1].coastlines()
ax[1].set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
ax[1].gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)

# Difference
diff = std_last['std'] - std_first['std']
diff.plot(
    ax=ax[2], transform=ccrs.PlateCarree(), cmap='RdBu_r',
    levels=np.linspace(-1e-9, 1e-9, 11),
    cbar_kwargs={'label': 'Difference (s⁻¹)', 'orientation': 'horizontal'}
)
ax[2].set_title('Difference 2090 - 1850')
ax[2].coastlines()
ax[2].set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
ax[2].gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)

plt.tight_layout()

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0mean_flow/std_change_map.pdf", bbox_inches='tight', dpi=300)
# %%
