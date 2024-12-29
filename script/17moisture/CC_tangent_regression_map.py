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
first_slope.plot(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2.5, 4, 0.1),
    extend='both',
)

first_tangent.plot(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2.5, 4, 0.1),
    extend='both',
)

(first_slope - first_tangent).plot(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-1, 1.1, 0.1),
    extend='both',
)

last_slope.plot(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2.5, 4, 0.1),
    extend='both',
)

last_tangent.plot(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-2.5, 4, 0.1),
    extend='both',
)
(last_slope - last_tangent).plot(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-1, 1.1, 0.1),
    extend='both',
)

(last_slope - first_slope).plot(
    ax=axes[2, 0],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-1, 1.1, 0.1),
    extend='both',
)

(last_tangent - first_tangent).plot(
    ax=axes[2, 1],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-1, 1.1, 0.1),
    extend='both',
)

((last_slope - last_tangent) - (first_slope - first_tangent)).plot(
    ax=axes[2, 2],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=np.arange(-1, 1.1, 0.1),
    extend='both',
)

for ax in axes.flat:
    ax.coastlines()

plt.tight_layout()

# %%
