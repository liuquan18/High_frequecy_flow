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
    3, 3, figsize=(14, 8), subplot_kw={"projection": ccrs.PlateCarree(100)}
)

tangent_level_seq = np.arange(-2, 2.1, 0.1)
tangent_level_diff = np.arange(-2, 2.1, 0.1)/2

# rows for 'slope', 'tangent', 'slope - tangent'
# columns for 'first', 'last', 'difference'
plot_first = first_hus_tas.plot(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=tangent_level_seq,
    extend='both',
    add_colorbar = False
)

first_hussat_tas.plot(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=tangent_level_seq,
    extend='both',
    add_colorbar = False
    )

(first_hus_tas - first_hussat_tas).plot(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=tangent_level_seq,
    extend='both',
    add_colorbar = False
)
plot_last = last_hus_tas.plot(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=tangent_level_seq,
    extend='both',
    add_colorbar = False
)

last_hussat_tas.plot(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=tangent_level_seq,
    extend='both',
    add_colorbar = False
)

(last_hus_tas - last_hussat_tas).plot(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=tangent_level_seq,
    extend='both',
    add_colorbar = False
)

plot_last_first = (last_hus_tas - first_hus_tas).plot(
    ax=axes[2, 0],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=tangent_level_diff,
    extend='both',
    add_colorbar = False
)

(last_hussat_tas - first_hussat_tas).plot(
    ax=axes[2, 1],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=tangent_level_diff,
    extend='both',
    add_colorbar = False
)

((last_hus_tas - last_hussat_tas) - (first_hus_tas - first_hussat_tas)).plot(
    ax=axes[2, 2],
    transform=ccrs.PlateCarree(),
    cmap="coolwarm",
    levels=tangent_level_diff,
    extend='both',
    add_colorbar = False
)


def lon2x(longitude):
    """
    Convert longitude to corresponding x-coordinates.
    """
    x_coord = axes[2, 2].projection.transform_point(longitude, 0, ccrs.PlateCarree())[0]

    return x_coord

def lat2y(latitude):
    """
    Convert latitude to corresponding y-coordinates.
    """
    y_coord = axes[2, 2].projection.transform_point(0, latitude, ccrs.PlateCarree())[1]

    return y_coord
# for the axes[2,2]
# add hlines at y = 30 and y = 60
axes[2,2].axhline(y=lat2y(20), color='black', linestyle='dotted')
axes[2,2].axhline(y=lat2y(60), color='black', linestyle='dotted')

axes[2,2].axvline(x=lon2x(-145), ymin=0.62, ymax=0.86, color='black', linestyle='dotted')
axes[2,2].axvline(x=lon2x(140), ymin=0.62, ymax=0.86, color='black', linestyle='dotted')
axes[2,2].axvline(x=lon2x(-35), ymin=0.62, ymax=0.86, color='black', linestyle='dotted')
axes[2,2].axvline(x=lon2x(-70), ymin=0.62, ymax=0.86, color='black', linestyle='dotted')

for ax in axes.flat:
    ax.coastlines()

# add x-ticks for the last row
for ax in axes[2, :]:
    ax.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
    lon_formatter = cartopy.mpl.ticker.LongitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.set_xlabel("")
# add y-ticks for the first column
for ax in axes[:, 0]:
    ax.set_yticks(np.arange(-90, 91, 30), crs=ccrs.PlateCarree())
    lat_formatter = cartopy.mpl.ticker.LatitudeFormatter()
    ax.yaxis.set_major_formatter(lat_formatter)
    ax.set_ylabel("")

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
cbar_ax1 = fig.add_axes([0.92, 0.7, 0.02, 0.2])
cbar_ax2 = fig.add_axes([0.92, 0.4, 0.02, 0.2])
cbar_ax3 = fig.add_axes([0.92, 0.1, 0.02, 0.2])

cbar1 = fig.colorbar(plot_first, cax=cbar_ax1, orientation='vertical', label='g/kg/K')
cbar2 = fig.colorbar(plot_last, cax=cbar_ax2, orientation='vertical', label='g/kg/K')
cbar3 = fig.colorbar(plot_last_first, cax=cbar_ax3, orientation='vertical', label='g/kg/K')

# Reduce the number of ticks
cbar1.set_ticks(np.arange(-2, 2.1, 1))
cbar2.set_ticks(np.arange(-2, 2.1, 1))
cbar3.set_ticks(np.arange(-1, 1.1, 0.5))

plt.tight_layout(rect=[0, 0, 0.9, 1])

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/tangent_hus_shus.png")
# %%
