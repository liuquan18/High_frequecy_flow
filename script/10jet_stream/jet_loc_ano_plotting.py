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
def read_data(period, same_clim = True, eddy = True):
    # climatology
    if eddy:
        loc_clim = xr.open_dataset(
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_{period}.nc"                                 
                                         ).lat
    else:
        loc_clim = xr.open_dataset(
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_allplev_{period}.nc"
                                         ).lat

    # anomaly
    ano_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/loc_anomaly/"
    clima_label = "sameclima" if same_clim else "diffclima"
    eddy_label = "eddy" if eddy else "noneddy"

    ano_path = f"{ano_dir}jet_stream_anomaly_{eddy_label}_{clima_label}_{period}.nc"



    loc_ano = xr.open_dataset(ano_path).lat_ano

    return loc_clim, loc_ano

#%%
same_clim = False
eddy = True

#%%
# for plot the anomaly of all samples
_, first10_ano_all = read_data("first10", same_clim = True, eddy = eddy)
_, last10_ano_all = read_data("last10", same_clim = True, eddy = eddy)


first10_clim, first10_ano = read_data("first10", same_clim = same_clim, eddy = eddy)
last10_clim, last10_ano = read_data("last10", same_clim = same_clim, eddy = eddy)

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
jet_loc_first10_pos = jet_event(first10_ano, first10_pos_events)
jet_loc_first10_neg = jet_event(first10_ano, first10_neg_events)
# %%
jet_loc_last10_pos = jet_event(last10_ano, last10_pos_events)
jet_loc_last10_neg = jet_event(last10_ano, last10_neg_events)

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
    first10_ano_all.values.flatten(),
    label="first10",
    color="k",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=hist_ax1,
)
sns.histplot(
    last10_ano_all.values.flatten(),
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
    bins=np.arange(-30, 31, 2), # Note: (20, 21, 1) would give bettern visualisation

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

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/jet_stream/jet_location_hist_map_eddy.png")
# %%
