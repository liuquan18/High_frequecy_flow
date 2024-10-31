# %%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from src.composite.composite_NAO_WB import NAO_WB
from src.plotting.util import erase_white_line

# %%
first_NAO_pos_AWB, first_NAO_neg_AWB, first_NAO_pos_CWB, first_NAO_neg_CWB = NAO_WB(
    "first10", fldmean=False
)
last_NAO_pos_AWB, last_NAO_neg_AWB, last_NAO_pos_CWB, last_NAO_neg_CWB = NAO_WB(
    "last10", fldmean=False
)

# %%
first_NAO_pos_AWB.sel(time=slice(-5, 5)).mean(dim="time").plot()
# %%
last_NAO_pos_AWB.sel(time=slice(-5, 5)).mean(dim="time").plot()

# %%
first_NAO_pos_AWB = first_NAO_pos_AWB.sel(time=slice(-5, 5)).mean(dim="time")
last_NAO_pos_AWB = last_NAO_pos_AWB.sel(time=slice(-5, 5)).mean(dim="time")

first_NAO_pos_CWB = first_NAO_pos_CWB.sel(time=slice(-5, 5)).mean(dim="time")
last_NAO_pos_CWB = last_NAO_pos_CWB.sel(time=slice(-5, 5)).mean(dim="time")

first_NAO_neg_AWB = first_NAO_neg_AWB.sel(time=slice(-5, 5)).mean(dim="time")
last_NAO_neg_AWB = last_NAO_neg_AWB.sel(time=slice(-5, 5)).mean(dim="time")

first_NAO_neg_CWB = first_NAO_neg_CWB.sel(time=slice(-5, 5)).mean(dim="time")
last_NAO_neg_CWB = last_NAO_neg_CWB.sel(time=slice(-5, 5)).mean(dim="time")
# %%
f, axes = plt.subplots(
    2, 1, figsize=(7, 5), subplot_kw=dict(projection=ccrs.PlateCarree(-70))
)
erase_white_line(first_NAO_pos_AWB).plot.contourf(
    ax=axes[0], transform=ccrs.PlateCarree(), levels=np.arange(10, 50, 5), extend="max"
)

erase_white_line(last_NAO_pos_AWB).plot.contourf(
    ax=axes[1], transform=ccrs.PlateCarree(), levels=np.arange(10, 50, 5), extend="max"
)

axes[0].set_title("AWB NAO+ first10")
axes[1].set_title("AWB NAO+ last10")

for ax in axes:
    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.coastlines()

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/skader_WB/AWB_NAO_pos_map.png",
    dpi=300,
)
# %%
f, axes = plt.subplots(
    2, 1, figsize=(7, 5), subplot_kw=dict(projection=ccrs.PlateCarree(-70))
)
erase_white_line(first_NAO_neg_CWB).plot.contourf(
    ax=axes[0], transform=ccrs.PlateCarree(), levels=np.arange(2, 10, 1), extend="max"
)

erase_white_line(last_NAO_neg_CWB).plot.contourf(
    ax=axes[1], transform=ccrs.PlateCarree(), levels=np.arange(2, 10, 1), extend="max"
)

axes[0].set_title("CWB NAO- first10")
axes[1].set_title("CWB NAO- last10")

for ax in axes:
    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.coastlines()

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/skader_WB/CWB_NAO_neg_map.png",
    dpi=300,
)

# %%
fig, axes = plt.subplots(
    2,1, figsize = (12,8), subplot_kw=dict(projection=ccrs.PlateCarree(-70))
)

erase_white_line(first_NAO_pos_CWB).plot.contourf(
    ax=axes[0], transform=ccrs.PlateCarree(), levels=np.arange(3, 15, 1), extend="max"
)

erase_white_line(last_NAO_pos_CWB).plot.contourf(
    ax=axes[1], transform=ccrs.PlateCarree(), levels=np.arange(3, 15, 1), extend="max"
)

axes[0].set_title("CWB NAO+ first10")
axes[1].set_title("CWB NAO+ last10")

for ax in axes:
    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.coastlines()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/skader_WB/CWB_NAO_pos_map.png",
    dpi=300,
)
# %%
fig, axes = plt.subplots(
    2,1, figsize = (12,8), subplot_kw=dict(projection=ccrs.PlateCarree(-70))
)

erase_white_line(first_NAO_neg_AWB).plot.contourf(
    ax=axes[0], transform=ccrs.PlateCarree(), levels=np.arange(3, 20, 1), extend="max"
)

erase_white_line(last_NAO_neg_AWB).plot.contourf(
    ax=axes[1], transform=ccrs.PlateCarree(), levels=np.arange(3, 20, 1), extend="max"
)

axes[0].set_title("AWB NAO- first10")
axes[1].set_title("AWB NAO- last10")

for ax in axes:
    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.coastlines()
    
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/skader_WB/AWB_NAO_neg_map.png",
    dpi=300,
)
# %%
