# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import matplotlib.colors as mcolors

import proplot as pplt

# %%
import src.blocking.block_index as block_index
import src.blocking.block_event as block_event


# %%


def detect_blocking(zg):
    Z = zg.geopoth.squeeze()
    Z = erase_white_line(Z)
    blocks_ind = block_index.IB_index(Z, LLB_filter=True)

    blocks_event = block_event.blocking_event_index(blocks_ind)
    blocks_sm = blocks_event.rolling(lat=2, lon=2, center=True).mean()
    return blocks_sm


# %%
# function to erase the white line
def erase_white_line(data):
    """
    erase the white line aroung 180 degree.
    """
    data = data.transpose(..., "lon")  # make the lon as the last dim
    dims = data.dims  # all the dims
    res_dims = tuple(dim for dim in dims if dim != "lon")  # dims apart from lon
    res_coords = [data.coords[dim] for dim in res_dims]  # get the coords

    # add one more longitude to the data
    data_value, lons = add_cyclic_point(data, coord=data.lon, axis=-1)

    # make the lons as index
    lon_dim = xr.IndexVariable(
        "lon", lons, attrs={"standard_name": "longitude", "units": "degrees_east"}
    )

    # the new coords with changed lon
    new_coords = res_coords + [lon_dim]  # changed lon but new coords

    new_data = xr.DataArray(data_value, coords=new_coords, name=data.name)

    return new_data


# %%
def BE_time_int(BE, folder=5):
    hours = pd.date_range(
        BE.time[0].values, BE.time[-1].values, periods=BE.time.shape[0] * folder
    )
    BE_int = BE.interp(time=hours, method="slinear")
    return BE_int


# %%
def block_draw(ens):
    zg = xr.open_dataset(
        f"/work/mh0033/m300883/High_frequecy_flow/data/example_blocking_event/zg{ens}_first30.nc"
    )
    blocks_sm = detect_blocking(zg)
    BE_int = BE_time_int(blocks_sm)
    return BE_int


# %%
# BE_L = block_draw(69)
# %%
BE_L = block_draw(74)

# %%
# BE_R = block_draw(75) # same west
# %%
BE_R = block_draw(82)  # local increase
# %%
# BE_R = block_draw(90) # two directions
# #%%
# BE_R = block_draw(94) # going down
# #%%
# BE_R = block_draw(95) #
# %%
BE_left = BE_L  # .isel(time = slice(10,70))
BE_right = BE_R  # .isel(time = slice(0,55))

fig, axes = plt.subplots(
    1,
    2,
    figsize=(180 / 25.4, 90 / 25.4),
    subplot_kw={"projection": ccrs.Orthographic(-20, 60)},
)
cmap = pplt.Colormap("Reds")
for i, hour in enumerate(BE_left.time):
    # Calculate the color index
    color_index = i / len(BE_left.time)

    # Get the color from the colormap
    color = cmap(color_index)

    axes[0].contour(
        BE_left.lon,
        BE_left.lat,
        BE_left.sel(time=hour, method="nearest"),
        transform=ccrs.PlateCarree(),
        colors=[color],
        linewidths=1,
        levels=[0, 0.5, 1.5],
    )
    axes[1].contour(
        BE_right.lon,
        BE_right.lat,
        BE_right.sel(time=hour, method="nearest"),
        transform=ccrs.PlateCarree(),
        colors=[color],
        linewidths=1,
        levels=[0, 0.5, 1.5],
    )

for ax in axes:
    ax.coastlines(linewidth=0.5, color="grey7")
    ax.set_global()
    ax.gridlines(color="grey4", linestyle="-", linewidth=0.5)
    ax.set_title("")
# Create a new axes for the colorbar
cbar_ax = fig.add_axes([0.25, 0.05, 0.55, 0.03])

# Create a Normalize instance
norm = mcolors.Normalize(vmin=0, vmax=30)

# Create a ScalarMappable instance
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

# Create the colorbar
cbar = fig.colorbar(sm, cax=cbar_ax, orientation="horizontal")
cbar.ax.xaxis.grid(True, which='major', color='black', linestyle='-',linewidth=2)


# Set the colorbar ticks
cbar.set_ticks(np.arange(0, 31, 5))
# no xmin ticks
cbar.ax.tick_params(axis='x', which='both', length=0)
# add text at the end of the colorbar
cbar.ax.text(31.1, 0.5, 'Days', va='center', ha='left')

# fig.tight_layout()

# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/panel/Bloking_event.pdf")
# %%
