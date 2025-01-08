# %%
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


from src.moisture.longitudinal_contrast import read_data

# # %%
# first_tas = read_data("tas", 1850, (-90, 90), False)
# first_hus = read_data("hus", 1850, (-90, 90), False)
# first_hussat = read_data("hussat", 1850, (-90, 90), False)
# first_data = xr.Dataset({"tas": first_tas, "hus": first_hus, 'hussat': first_hussat})

# # %%

# last_tas = read_data("tas", 2090, (-90, 90), False)
# last_hus = read_data("hus", 2090, (-90, 90), False)
# last_hussat = read_data("hussat", 2090, (-90, 90), False)
# last_data = xr.Dataset({"tas": last_tas, "hus": last_hus, 'hussat': last_hussat})
# # %%
# first_mean = first_data.mean(dim = ('time', 'ens'))
# last_mean = last_data.mean(dim = ('time', 'ens'))

# #%%
# first_mean.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_mean.nc")
# last_mean.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_mean.nc")
# #%%
# # #%%
# first_data.load()
# last_data.load()
# first_qu95 = first_data.quantile(0.95, dim = ('time', 'ens'))
# last_qu95 = last_data.quantile(0.95, dim = ('time', 'ens'))

# first_qu95.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_qu95.nc")
# last_qu95.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_qu95.nc")

# %%
first_mean = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_mean.nc"
)
last_mean = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_mean.nc"
)
# %%
# change unit
first_mean["hus"] = first_mean.hus * 1000
first_mean["hussat"] = first_mean.hussat * 1000

last_mean["hus"] = last_mean.hus * 1000
last_mean["hussat"] = last_mean.hussat * 1000


#%%

diff_mean = last_mean - first_mean


# %%
temp_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/temp_seq.txt"
)
temp_cmap_seq = mcolors.ListedColormap(temp_cmap_seq, name="temp_div")

temp_cmap_div = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/temp_div.txt"
)
temp_cmap_div = mcolors.ListedColormap(temp_cmap_div, name="temp_div")

prec_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_seq.txt"
)
prec_cmap_seq = mcolors.ListedColormap(prec_cmap_seq, name="prec_div")

prec_cmap_div = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_div.txt"
)
prec_cmap_div = mcolors.ListedColormap(prec_cmap_div, name="prec_div")
#%%
temp_levels = np.arange(0,21,1)
hus_levels = np.arange(0,6,0.5)

temp_levels_div = np.arange(-5,6,0.5)
hus_levels_div = np.arange(-1.5,1.6,0.1)


# %%
fig, axes = plt.subplots(
    3, 3, figsize=(12, 6), subplot_kw={"projection": ccrs.PlateCarree(100)}
)
axes[0, 0].set_title("1850-1859")
axes[0, 1].set_title("1850-1859")
axes[0, 2].set_title("1850-1859")

axes[1, 0].set_title("2090-2099")
axes[1, 1].set_title("2090-2099")
axes[1, 2].set_title("2090-2099")

axes[2, 0].set_title("2090-2099 - 1850-1859")
axes[2, 1].set_title("2090-2099 - 1850-1859")
axes[2, 2].set_title("2090-2099 - 1850-1859")

first_mean.tas.plot(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_seq,
    cbar_kwargs={"label": "T (K)", "shrink": 0.6},
    levels=temp_levels,
    extend='max',
)
axes[0, 0].set_title("1850-1859")
axes[0, 0].coastlines()
axes[0, 0].set_global()

first_mean.hussat.plot(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_seq,
    cbar_kwargs={"label": r"$q^*$ (g/kg)", "shrink": 0.6},
    levels=hus_levels*2,
    extend='max',
)
axes[0, 1].set_title("1850-1859")
axes[0, 1].coastlines()
axes[0, 1].set_global()

first_mean.hus.plot(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_seq,
    cbar_kwargs={"label": r"$q$ (g/kg)", "shrink": 0.6},
    levels=hus_levels,
    extend='max',
)
axes[0, 2].set_title("1850-1859")
axes[0, 2].coastlines()
axes[0, 2].set_global()

last_mean.tas.plot(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_seq,
    cbar_kwargs={"label": "T (K)", "shrink": 0.6},
    levels=temp_levels,
    extend='max',
)
axes[1, 0].set_title("2090-2099")
axes[1, 0].coastlines()
axes[1, 0].set_global()

last_mean.hussat.plot(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_seq,
    cbar_kwargs={"label": r"$q^*$ (g/kg)", "shrink": 0.6},
    levels=hus_levels*2,
    extend='max',
)
axes[1, 1].set_title("2090-2099")
axes[1, 1].coastlines()
axes[1, 1].set_global()

last_mean.hus.plot(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_seq,
    cbar_kwargs={"label": r"$q$ (g/kg)", "shrink": 0.6},
    levels=hus_levels,
    extend='max',
)
axes[1, 2].set_title("2090-2099")
axes[1, 2].coastlines()
axes[1, 2].set_global()

# difference between last and first
diff_mean.tas.plot(
    ax=axes[2, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    cbar_kwargs={"label": "T (K)", "shrink": 0.6},
    levels=temp_levels_div,
    extend='both',
)
axes[2, 0].set_title("2090-2099 - 1850-1859")
axes[2, 0].coastlines()
axes[2, 0].set_global()

diff_mean.hussat.plot(
    ax=axes[2, 1],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_div,
    cbar_kwargs={"label": r"$q^*$ (g/kg)", "shrink": 0.6},
    levels=hus_levels_div*2,
    extend='both',
)
axes[2, 1].set_title("2090-2099 - 1850-1859")
axes[2, 1].coastlines()
axes[2, 1].set_global()

diff_mean.hus.plot(
    ax=axes[2, 2],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_div,
    cbar_kwargs={"label": r"$q$ (g/kg)", "shrink": 0.6},
    levels=hus_levels_div,
    extend='both',
)
axes[2, 2].set_title("2090-2099 - 1850-1859")
axes[2, 2].coastlines()
axes[2, 2].set_global()

# latitude ticks
for ax in axes.flatten():
    ax.set_yticks(np.arange(-60, 76, 30), crs=ccrs.PlateCarree())
    ax.set_ylabel("Latitude")
    ax.yaxis.set_major_formatter(cartopy.mpl.ticker.LatitudeFormatter())
    # Set longitude ticks and labels
    ax.set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels(['180°', '120°W', '60°W', '0°', '60°E', '120°E'])
    ax.set_yticks(np.arange(-60, 76, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels(['60°S', '30°S', '0°', '30°N', '60°N'])
    ax.set_ylabel("Latitude")
    ax.yaxis.set_major_formatter(cartopy.mpl.gridliner.LATITUDE_FORMATTER)

axes[1, 1].set_xlabel("Longitude")

draw_box(axes[0, 0], (60, 30))

# a, b, c labels for each subplots
for i, ax in enumerate(axes.flatten()):
    ax.text(
        -0.1,
        1.0,
        chr(97 + i),
        transform=ax.transAxes,
        size=12,
        weight="bold",
    )
    ax.set_ylabel('')
    ax.set_xlabel('')

plt.tight_layout(w_pad=-1)
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/first_last_clim.pdf", dpi=300)

#%%
first_qu95 = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_qu95.nc"
)
last_qu95 = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_qu95.nc"
)

first_qu95["hus"] = first_qu95.hus * 1000
first_qu95['hussat'] = first_qu95.hussat * 1000

last_qu95["hus"] = last_qu95.hus * 1000
last_qu95['hussat'] = last_qu95.hussat * 1000
diff_qu95 = last_qu95 - first_qu95



# %%
# same for qu95
fig, axes = plt.subplots(
    3, 3, figsize=(15, 10), subplot_kw={"projection": ccrs.PlateCarree(100)}
)
first_qu95.tas.plot(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_seq,
    cbar_kwargs={"label": "Temperature (K)"},
    levels=temp_levels,
    extend='max',
)
axes[0, 0].set_title("1850-1859")
axes[0, 0].coastlines()
axes[0, 0].set_global()

last_qu95.tas.plot(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_seq,
    cbar_kwargs={"label": "Temperature (K)"},
    levels=temp_levels,
    extend='max',
)
axes[1, 0].set_title("2090-2099")
axes[1, 0].coastlines()
axes[1, 0].set_global()

first_qu95.hus.plot(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_seq,
    cbar_kwargs={"label": "Specific Humidity (g/kg)"},
    levels=hus_levels,
    extend='max',
)
axes[0, 1].set_title("1850-1859")
axes[0, 1].coastlines()
axes[0, 1].set_global()

last_qu95.hus.plot(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_seq,
    cbar_kwargs={"label": "Specific Humidity (g/kg)"},
    levels=hus_levels,
    extend='max',
)
axes[1, 1].set_title("2090-2099")
axes[1, 1].coastlines()
axes[1, 1].set_global()

first_qu95.hussat.plot(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_seq,
    cbar_kwargs={"label": "saturate specific Humidity (g/kg)"},
    levels=hus_levels*2,
    extend='max',
)
axes[0, 2].set_title("1850-1859")
axes[0, 2].coastlines()
axes[0, 2].set_global()

last_qu95.hussat.plot(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_seq,
    cbar_kwargs={"label": "saturate specific Humidity (g/kg)"},
    levels=hus_levels*2,
    extend='max',
)
axes[1, 2].set_title("2090-2099")
axes[1, 2].coastlines()
axes[1, 2].set_global()

# difference between last and first for qu95
diff_qu95.tas.plot(
    ax=axes[2, 0],
    transform=ccrs.PlateCarree(),
    cmap=temp_cmap_div,
    cbar_kwargs={"label": "Temperature (K)"},
    levels=temp_levels_div,
    extend='both',
)
axes[2, 0].set_title("2090-2099 - 1850-1859")
axes[2, 0].coastlines()
axes[2, 0].set_global()

diff_qu95.hus.plot(
    ax=axes[2, 1],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_div,
    cbar_kwargs={"label": "Specific Humidity (g/kg)"},
    levels=hus_levels_div,
    extend='both',
)
axes[2, 1].set_title("2090-2099 - 1850-1859")
axes[2, 1].coastlines()
axes[2, 1].set_global()

diff_qu95.hussat.plot(
    ax=axes[2, 2],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_div,
    cbar_kwargs={"label": "saturate specific Humidity (g/kg)"},
    levels=hus_levels_div*2,
    extend='both',
)
axes[2, 2].set_title("2090-2099 - 1850-1859")
axes[2, 2].coastlines()
axes[2, 2].set_global()

# latitude ticks
for ax in axes.flatten():
    ax.set_yticks(np.arange(-60, 76, 30), crs=ccrs.PlateCarree())
    ax.set_ylabel("Latitude")
    ax.yaxis.set_major_formatter(cartopy.mpl.gridliner.LATITUDE_FORMATTER)
    # Set longitude ticks and labels
    ax.set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels(['180°W', '120°W', '60°W', '0°', '60°E', '120°E'])
    ax.set_yticks(np.arange(-60, 76, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels(['60°S', '30°S', '0°', '30°N', '60°N'])
    ax.set_ylabel("Latitude")
    ax.yaxis.set_major_formatter(cartopy.mpl.gridliner.LATITUDE_FORMATTER)

axes[1, 1].set_xlabel("Longitude")
draw_box(axes[0, 0], (60, 30))

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/first_last_clim_qu95.png")
# %%
