# %%
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import logging
import cmocean

logging.basicConfig(level=logging.INFO)


# %%
def read_extreme_freq(var, decade):
    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily_extremes_decade_freq/"
    file = base_dir + f"{var}_extreme_dec_{decade}.nc"
    frequency_dec = xr.open_dataarray(file)
    return frequency_dec


# %%

first_vt_freq = read_extreme_freq("vt", 1850)
last_vt_freq = read_extreme_freq("vt", 2090)
# %%
first_va_freq = read_extreme_freq("va", 1850)
last_va_freq = read_extreme_freq("va", 2090)
# %%
fig, axes = plt.subplots(
    3, 2, figsize=(10, 7), subplot_kw={"projection": ccrs.PlateCarree(100)}
)

freq_plot = first_vt_freq.plot(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap=cmocean.cm.amp,
    levels=np.arange(0, 10, 1),
    add_colorbar=False,
)
axes[0, 0].set_title("thermal wind 1850")

first_va_freq.plot(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap=cmocean.cm.amp,
    levels=np.arange(0, 10, 1),
    add_colorbar=False,
)
axes[0, 1].set_title("wind 1850 (250 hPa)")

last_vt_freq.plot(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap=cmocean.cm.amp,
    levels=np.arange(0, 10, 1),
    add_colorbar=False,
)
axes[1, 0].set_title("thermal wind 2090")

last_va_freq.plot(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap=cmocean.cm.amp,
    levels=np.arange(0, 10, 1),
    add_colorbar=False,
)
axes[1, 1].set_title("wind 2090 (250 hPa)")

# difference between last and first
diff_vt = last_vt_freq - first_vt_freq
diff_va = last_va_freq - first_va_freq

diff_plot = diff_vt.plot(
    ax=axes[2, 0],
    transform=ccrs.PlateCarree(),
    cmap=cmocean.cm.balance,
    levels=np.arange(-5, 6, 1),
    add_colorbar=False,
)
axes[2, 0].set_title("thermal wind difference")

diff_va.plot(
    ax=axes[2, 1],
    transform=ccrs.PlateCarree(),
    cmap=cmocean.cm.balance,
    levels=np.arange(-5, 6, 1),
    add_colorbar=False,
)
axes[2, 1].set_title("wind difference (250 hPa)")

for ax in axes.flatten():
    ax.coastlines()
    ax.set_extent([-180, 180, 10, 90], crs=ccrs.PlateCarree())

# Add colorbars
cbar_freq = fig.colorbar(freq_plot, ax=axes[:, 0], orientation='horizontal', pad=0.05)
cbar_freq.set_label('extreme event requency (%)')

cbar_diff = fig.colorbar(diff_plot, ax=axes[:, 1], orientation='horizontal', pad=0.05)
cbar_diff.set_label('Difference (%)')

plt.tight_layout( rect=[0, 0.3, 1, 0.95])
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/v_wind/wind_extremes_freq_diff_firrst_last.png")

# %%
