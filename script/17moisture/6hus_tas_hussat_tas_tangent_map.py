#%%
import xarray as xr
import numpy as np
import sys
import os
import glob
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import logging
import matplotlib.colors as mcolors
from src.moisture.plot_utils import draw_box
#%%
first_hus_tas = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_ratio_hus.nc"
).__xarray_dataarray_variable__
# %%
last_hus_tas = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_ratio_hus.nc"
).__xarray_dataarray_variable__

#%%
first_hussat_tas = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_ratio_hussat.nc"
).__xarray_dataarray_variable__

last_hussat_tas = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_ratio_hussat.nc"
).__xarray_dataarray_variable__
# %%
fig, axes = plt.subplots(
    3, 3, figsize=(12, 8), subplot_kw={"projection": ccrs.PlateCarree(100)}
)

# rows for 'slope', 'tangent', 'slope - tangent'
# columns for 'first', 'last', 'difference'
plot_first = first_hus_tas.plot(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
)

first_hussat_tas.plot(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
    )

(first_hus_tas - first_hussat_tas).plot(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
)
plot_last = last_hus_tas.plot(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
)

last_hussat_tas.plot(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
)

plot_last_first = (last_hus_tas - last_hussat_tas).plot(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
)

(last_hus_tas - first_hus_tas).plot(
    ax=axes[2, 0],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1)/2,
    extend='both',
    add_colorbar = False
)

(last_hussat_tas - first_hussat_tas).plot(
    ax=axes[2, 1],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1)/2,
    extend='both',
    add_colorbar = False
)

((last_hus_tas - last_hussat_tas) - (first_hus_tas - first_hussat_tas)).plot(
    ax=axes[2, 2],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1)/2,
    extend='both',
    add_colorbar = False
)

for ax in axes.flat:
    ax.coastlines()

axes[0, 0].set_title("1850-1859 hus")
axes[0, 1].set_title("1850-1859 hussat")
axes[0, 2].set_title("hus - hussat")
axes[1, 0].set_title("2090-2099 hus")
axes[1, 1].set_title("2090-2099 hussat")
axes[1, 2].set_title("hus - hussat")
axes[2, 0].set_title("2090-2099 - 1850-1859")
axes[2, 1].set_title("2090-2099 - 1850-1859")
axes[2, 2].set_title("hus - hussat")

# add colorbars
cbar_ax1 = fig.add_axes([1.01, 0.7, 0.02, 0.2])
cbar_ax2 = fig.add_axes([1.01, 0.4, 0.02, 0.2])
cbar_ax3 = fig.add_axes([1.01, 0.1, 0.02, 0.2])

fig.colorbar(plot_first, cax=cbar_ax1, orientation='vertical', label='g/kg/K')
fig.colorbar(plot_last, cax=cbar_ax2, orientation='vertical', label='g/kg/K')
fig.colorbar(plot_last_first, cax=cbar_ax3, orientation='vertical', label='g/kg/K')

plt.tight_layout()

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/tangent_hus_shus.png")
# %%
