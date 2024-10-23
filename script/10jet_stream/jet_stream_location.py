# %%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import logging

import seaborn as sns

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from src.extremes.extreme_read import read_extremes_allens
from src.jet_stream.jet_speed_and_location import jet_stream_anomaly, jet_event
from src.jet_stream.jet_stream_plotting import plot_uhat

logging.basicConfig(level=logging.INFO)
#%%

# climatology only use the first10 years
jet_speed_clim = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_speed_climatology_first10.nc"
).ua
jet_loc_clim = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_first10.nc"
).lat

# %%
def jet_stream_anomaly_period(period):

    jet_speed_ano = []
    jet_loc_ano = []

    for ens in range(1, 51):
        # Load data
        jet_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_{period}/"
        jet_file = glob.glob(f"{jet_path}*r{ens}i1p1f1*.nc")[0]

        jet = xr.open_dataset(jet_file).ua
        # drop dim lon
        jet = jet.isel(lon=0)

        loc_ano = jet_stream_anomaly(
            jet, jet_loc_clim, stat="loc"
        )
        loc_ano["ens"] = ens

        speed_ano = jet_stream_anomaly(
            jet, jet_speed_clim, stat="speed"
        )
        speed_ano["ens"] = ens

        jet_speed_ano.append(speed_ano)
        jet_loc_ano.append(loc_ano)

    jet_speed_ano = xr.concat(jet_speed_ano, dim="ens")
    jet_loc_ano = xr.concat(jet_loc_ano, dim="ens")

    return jet_speed_ano, jet_loc_ano


# %%
############## jet location hist #####################
jet_speed_first10_ano, jet_loc_first10_ano = jet_stream_anomaly_period("first10")

# %%
jet_speed_last10_ano, jet_loc_last10_ano = jet_stream_anomaly_period("last10")


# %%
first10_pos_events, first10_neg_events = read_extremes_allens("first10", 8)
last10_pos_events, last10_neg_events = read_extremes_allens("last10", 8)

# %%
# select 250 hPa only
first10_pos_events = first10_pos_events[first10_pos_events["plev"] == 25000]
first10_neg_events = first10_neg_events[first10_neg_events["plev"] == 25000]

last10_pos_events = last10_pos_events[last10_pos_events["plev"] == 25000]
last10_neg_events = last10_neg_events[last10_neg_events["plev"] == 25000]

# %%
jet_loc_first10_pos = jet_event(jet_loc_first10_ano, first10_pos_events)
jet_loc_first10_neg = jet_event(jet_loc_first10_ano, first10_neg_events)
# %%
jet_loc_last10_pos = jet_event(jet_loc_last10_ano, last10_pos_events)
jet_loc_last10_neg = jet_event(jet_loc_last10_ano, last10_neg_events)

#################### jet composite map ####################
# %%
uhat_climatology = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/ua_Amon_MPI-ESM1-2-LR_HIST_climatology_185005-185909.nc"
)
uhat_climatology = uhat_climatology.ua.sel(plev=slice(None, 70000)).mean(dim="plev")

uhat_climatology = uhat_climatology.sel(time=slice("1859-06-01", "1859-08-31")).mean(
    dim="time"
)

uhat_pos_first10 = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/jetstream_MJJAS_first10_pos.nc"
).ua

uhat_neg_first10 = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/jetstream_MJJAS_first10_neg.nc"
).ua

uhat_pos_last10 = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/jetstream_MJJAS_last10_pos.nc"
).ua

uhat_neg_last10 = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/jetstream_MJJAS_last10_neg.nc"
).ua


# %%
# %%
# plot location histgram and composite mean map together

# %%
def generate_intermediate_points(start, end, num_points):
    return list(
        zip(
            np.linspace(start[0], end[0], num_points),
            np.linspace(start[1], end[1], num_points),
        )
    )

def add_box(map_ax):
    # Define the corners of the box aligned with lat/lon
    lon_min, lon_max = -60, 0
    lat_min, lat_max = 15, 75

    # Number of intermediate points (increase for smoother curves)
    num_points = 100

    # Generate points for each edge of the box
    left_edge = generate_intermediate_points(
        (lon_min, lat_min), (lon_min, lat_max), num_points
    )
    top_edge = generate_intermediate_points(
        (lon_min, lat_max), (lon_max, lat_max), num_points
    )
    right_edge = generate_intermediate_points(
        (lon_max, lat_max), (lon_max, lat_min), num_points
    )
    bottom_edge = generate_intermediate_points(
        (lon_max, lat_min), (lon_min, lat_min), num_points
    )

    # Combine all edges
    box = left_edge + top_edge + right_edge + bottom_edge

    # Separate longitudes and latitudes
    lons, lats = zip(*box)

    # Plot the smooth box
    map_ax.plot(lons, lats, color="k", linewidth=2, transform=ccrs.PlateCarree())

# %%
fig = plt.figure(figsize=(20, 14))

gs = fig.add_gridspec(2, 3)


map_ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.Orthographic(-20, 60))
plot_uhat(map_ax1, uhat_climatology)
map_ax1.set_title("Climatology")


map_ax2 = fig.add_subplot(gs[0, 1], projection=ccrs.Orthographic(-20, 60))
plot_uhat(map_ax2, uhat_pos_first10)
map_ax2.set_title("Positive NAO")

map_ax3 = fig.add_subplot(gs[0, 2], projection=ccrs.Orthographic(-20, 60))
plot_uhat(map_ax3, uhat_neg_first10)
map_ax3.set_title("Negative NAO")
# add bounding box at -60,0 lon, and 15,75 lat
add_box(map_ax1)

# Add gridlines
for ax in [map_ax1, map_ax2, map_ax3]:
    # Add gridlines
    gl = ax.gridlines(draw_labels=False, dms=True, x_inline=False, y_inline=False)

    # Optionally, adjust gridline appearance
    gl.xlines = True
    gl.ylines = True


## histgram
hist_ax1 = fig.add_subplot(gs[1, 0])
# jet location anomaly
sns.histplot(
    jet_loc_first10_ano.values.flatten(),
    label="first10",
    color="k",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=hist_ax1,
)
sns.histplot(
    jet_loc_last10_ano.values.flatten(),
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=hist_ax1,
)

hist_ax1.set_title("Jet location anomaly all")


hist_ax2 = fig.add_subplot(gs[1, 1])
sns.histplot(
    jet_loc_first10_pos,
    label="first10_pos",
    color="k",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=hist_ax2,
)

sns.histplot(
    jet_loc_last10_pos,
    label="last10_pos",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=hist_ax2,
)
hist_ax2.set_title("Jet location anomaly positive NAO")


hist_ax3 = fig.add_subplot(gs[1, 2])
sns.histplot(
    jet_loc_first10_neg,
    label="first10",
    color="k",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=hist_ax3,
)

sns.histplot(
    jet_loc_last10_neg,
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=hist_ax3,
)
hist_ax3.set_title("Jet location anomaly negative NAO")
hist_ax3.legend()

# vertical line for hist axes
for ax in [hist_ax1, hist_ax2, hist_ax3]:
    ax.axvline(x=0, color="k", linestyle="--")

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/jet_stream/jet_location_hist_map.png")
# %%
