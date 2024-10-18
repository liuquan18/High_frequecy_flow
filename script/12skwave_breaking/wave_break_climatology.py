# %%
import xarray as xr
import wavebreaking as wb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from src.plotting.util import erase_white_line

# %%
period = "first10"
ens = 1
WB = "AWB"


# %%
def climatology(period, WB):
    E_arr = xr.open_mfdataset(
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/skader_wb_events/{WB}_array/{WB}_array_{period}/{WB}_{period}_r*.nc",
        combine="nested",
        concat_dim="ens",
    )
    E_arr = E_arr.flag
    Climatology = E_arr.mean(dim=("time", "ens"))
    return Climatology


# %%
first_AWB = climatology("first10", "AWB")
last_AWB = climatology("last10", "AWB")

first_CWB = climatology("first10", "CWB")
last_CWB = climatology("last10", "CWB")
# %%
first_AWB = erase_white_line(first_AWB)
last_AWB = erase_white_line(last_AWB)
first_CWB = erase_white_line(first_CWB)
last_CWB = erase_white_line(last_CWB)

# %%
f, axes = plt.subplots(
    2, 1, figsize=(7, 5), subplot_kw=dict(projection=ccrs.PlateCarree(-50))
)
first_AWB.plot.contourf(
    ax=axes[0],
    transform=ccrs.PlateCarree(),
    # cmap="Reds",
    levels=np.arange(0, 0.31, 0.03),
)

last_AWB.plot.contourf( 
    ax=axes[1],
    transform=ccrs.PlateCarree(),
    # cmap="Reds",
    levels=np.arange(0, 0.31, 0.03),
)

for ax in axes:
    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.coastlines()  # add coastlines

    # x-ticks and y-ticks
    ax.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(0, 91, 30), crs=ccrs.PlateCarree())

axes[0].set_title("AWB first 10 years")
axes[1].set_title("AWB last 10 years")

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/skader_WB/AWB_climatology.png")
# %%
# same for CWB
f, axes = plt.subplots(
    2, 1, figsize=(7, 5), subplot_kw=dict(projection=ccrs.PlateCarree(-50))
)
first_CWB.plot.contourf(
    ax=axes[0],
    transform=ccrs.PlateCarree(),
    # cmap="Blues",
    levels=np.arange(0, 0.11, 0.01),
)

last_CWB.plot.contourf(
    ax=axes[1],
    transform=ccrs.PlateCarree(),
    # cmap="Blues",
    levels=np.arange(0, 0.11, 0.01),
)

for ax in axes:
    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.coastlines()  # add coastlines
    # x-ticks and y-ticks
    ax.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(0, 91, 30), crs=ccrs.PlateCarree())

axes[0].set_title("CWB first 10 years")
axes[1].set_title("CWB last 10 years")

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/skader_WB/CWB_climatology.png")
# %%
