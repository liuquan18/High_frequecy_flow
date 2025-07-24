#%%
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
# %%
from src.data_helper.read_variable import read_prime
# %%
theta_hat_first = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/theta_hat_monthly_ensmean/theta_hat_monmean_ensmean_185005_185909.nc")
# %%
theta_hat_last = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/theta_hat_monthly_ensmean/theta_hat_monmean_ensmean_209005_209909.nc")
# %%
theta_hat_first = theta_hat_first['theta'].sel(plev = 85000).mean(dim = 'time')
# %%
theta_hat_last = theta_hat_last['theta'].sel(plev = 85000).mean(dim = 'time')
# %%
fig, axes = plt.subplots(1, 3, figsize=(18, 6), subplot_kw={'projection': ccrs.PlateCarree()})

# Northern Hemisphere extent
extent = [-180, 180, 0, 90]
# Set common vmin and vmax for consistent color mapping
vmin = min(theta_hat_first.min().item(), theta_hat_last.min().item())
vmax = max(theta_hat_first.max().item(), theta_hat_last.max().item())

# First period
im0 = axes[0].pcolormesh(
    theta_hat_first['lon'], theta_hat_first['lat'], theta_hat_first,
    transform=ccrs.PlateCarree(), cmap='RdBu_r', vmin=vmin, vmax=vmax
)
axes[0].set_title('1850-1859')
axes[0].set_extent(extent, crs=ccrs.PlateCarree())
axes[0].coastlines()

# Last period
im1 = axes[1].pcolormesh(
    theta_hat_last['lon'], theta_hat_last['lat'], theta_hat_last,
    transform=ccrs.PlateCarree(), cmap='RdBu_r', vmin=vmin, vmax=vmax
)
axes[1].set_title('2090-2099')
axes[1].set_extent(extent, crs=ccrs.PlateCarree())
axes[1].coastlines()

# Difference
diff = theta_hat_last - theta_hat_first
im2 = axes[2].pcolormesh(
    diff['lon'], diff['lat'], diff,
    transform=ccrs.PlateCarree(), cmap='coolwarm'
)
axes[2].set_title('Difference')
axes[2].set_extent(extent, crs=ccrs.PlateCarree())
axes[2].coastlines()

# Colorbars
fig.colorbar(im0, ax=axes[0], orientation='horizontal', fraction=0.046, pad=0.08, label = r"$\Theta$ (K)")
fig.colorbar(im1, ax=axes[1], orientation='horizontal', fraction=0.046, pad=0.08, label = r"$\Theta$ (K)")
fig.colorbar(im2, ax=axes[2], orientation='horizontal', fraction=0.046, pad=0.08, label = r"$\Delta$ $\Theta$ (K)")

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0mean_flow/T_hat_plot.png", dpi=300)

# %%
