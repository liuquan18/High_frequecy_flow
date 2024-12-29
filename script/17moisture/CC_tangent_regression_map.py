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

# %%
first_slope = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_hus_tas_slope.nc"
).__xarray_dataarray_variable__
# %%
last_slope = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_hus_tas_slope.nc"
).__xarray_dataarray_variable__
# %%
first_tangent = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_tas_dqs_dT.nc"
).tas*1000
# %%
last_tangent = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_tas_dqs_dT.nc"
).tas*1000
# %%
fig, axes = plt.subplots(
    3, 3, figsize=(12, 8), subplot_kw={"projection": ccrs.PlateCarree(100)}
)

# rows for 'slope', 'tangent', 'slope - tangent'
# columns for 'first', 'last', 'difference'
slope = first_slope.plot(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
)

first_tangent.plot(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
    )

(first_slope - first_tangent).plot(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
)

last_slope.plot(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
)

last_tangent.plot(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
)
(last_slope - last_tangent).plot(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
)

(last_slope - first_slope).plot(
    ax=axes[2, 0],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
)

(last_tangent - first_tangent).plot(
    ax=axes[2, 1],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
)

((last_slope - last_tangent) - (first_slope - first_tangent)).plot(
    ax=axes[2, 2],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2, 2.1, 0.1),
    extend='both',
    add_colorbar = False
)

for ax in axes.flat:
    ax.coastlines()

axes[0, 0].set_title("1850-1859 slope")
axes[0, 1].set_title("1850-1859 tangent")
axes[0, 2].set_title("slope - tangent")
axes[1, 0].set_title("2090-2099 slope")
axes[1, 1].set_title("2090-2099 tangent")
axes[1, 2].set_title("slope - tangent")
axes[2, 0].set_title("2090-2099 - 1850-1859")
axes[2, 1].set_title("2090-2099 - 1850-1859")
axes[2, 2].set_title("slope - tangent")
# add colorbar at the bottom
cax = fig.add_axes([0.15, 0.01, 0.7, 0.02])
plt.colorbar(slope, ax=axes, orientation='horizontal', label='slope / tangent', cax=cax)

plt.tight_layout()

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/slope_tangent_diff_map.png")
# %%
