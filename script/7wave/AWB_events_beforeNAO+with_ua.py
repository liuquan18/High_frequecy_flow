#%%
import xarray as xr
import numpy as np
import pandas as pd
import logging
import glob
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
#%%
logging.basicConfig(level=logging.INFO)

# %%
import src.composite.composite as composite
import src.extremes.extreme_read as ext_read
import src.composite.composite_plot as composite_plot
import src.ConTrack.track_statistic as ts
# %%
first_AWB = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/WB_before_NAO/AWB_before_NAO_first10.csv")
last_AWB = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/WB_before_NAO/AWB_before_NAO_last10.csv")
# %%
first_eof = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/WB_before_NAO/va_eof_first10.nc")
last_eof = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/WB_before_NAO/va_eof_last10.nc")
# %%
first_eof = first_eof.eof.isel(mode = 0, decade = 0)
last_eof = last_eof.eof.isel(mode = 0, decade = 0)
# %%
levels = np.arange(-4, 4.1, 0.5)

fig, ax = plt.subplots(2, 1, figsize=(10,5), subplot_kw=dict(projection=ccrs.PlateCarree(-120)))
ts.plot_tracks(first_AWB, ax[0])
ax[0].set_title('AWB events before NAO+ events in the First 10 years ')

first_eof.plot.contourf(ax=ax[0], transform=ccrs.PlateCarree(),  cmap='RdBu_r', alpha = 0.7, levels = levels)

ts.plot_tracks(last_AWB, ax[1])
ax[1].set_title('AWB events before NAO+ events in the Last 10 years ')
ax[1].set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
last_eof.plot.contourf(ax=ax[1], transform=ccrs.PlateCarree(),  cmap='RdBu_r', alpha = 0.7, levels = levels)


ax[1].set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])
for ax in [ax[0], ax[1]]:
    ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/AWB_before_NAO.png")
# %%


first_CWB= pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/WB_before_NAO/CWB_before_NAO_first10.csv")
# %%
