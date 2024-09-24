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

# %%

jet_speed_first10_ano, jet_loc_first10_ano = jet_stream_anomaly("first10")

# %%
jet_speed_last10_ano, jet_loc_last10_ano = jet_stream_anomaly("last10")


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


# %%
# plot jet location anomaly
fig, axes = plt.subplots(3, 1, figsize=(10, 10))

# jet location anomaly
sns.histplot(
    jet_loc_first10_ano.values.flatten(),
    label="first10",
    color="b",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=axes[0],
)
sns.histplot(
    jet_loc_last10_ano.values.flatten(),
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=axes[0],
)

axes[0].set_title("Jet location anomaly all")

sns.histplot(
    jet_loc_first10_pos,
    label="first10_pos",
    color="b",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=axes[1],
)

sns.histplot(
    jet_loc_last10_pos,
    label="last10_pos",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=axes[1],
)
axes[1].set_title("Jet location anomaly positive NAO")


sns.histplot(
    jet_loc_first10_neg,
    label="first10",
    color="b",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=axes[2],
)

sns.histplot(
    jet_loc_last10_neg,
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=axes[2],
)
axes[2].set_title("Jet location anomaly negative NAO")
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/jet_stream/jet_loc_anomaly.png"
)
# %%
# jet speed
jet_speed_first10_pos = jet_event(jet_speed_first10_ano, first10_pos_events)
jet_speed_first10_neg = jet_event(jet_speed_first10_ano, first10_neg_events)

jet_speed_last10_pos = jet_event(jet_speed_last10_ano, last10_pos_events)
jet_speed_last10_neg = jet_event(jet_speed_last10_ano, last10_neg_events)
# %%
# plot jet speed anomaly
fig, axes = plt.subplots(3, 1, figsize=(10, 10))

# jet speed anomaly
sns.histplot(
    jet_speed_first10_ano.values.flatten(),
    label="first10",
    color="b",
    bins=np.arange(-5, 5.2, 0.5),
    stat="density",
    ax=axes[0],
)

sns.histplot(
    jet_speed_last10_ano.values.flatten(),
    label="last10",
    color="r",
    bins=np.arange(-5, 5.2, 0.5),
    stat="density",
    alpha=0.5,
    ax=axes[0],
)


axes[0].set_title("Jet speed anomaly all")

sns.histplot(
    jet_speed_first10_pos,
    label="first10_pos",
    color="b",
    bins=np.arange(-5, 5.2, 0.5),
    stat="density",
    ax=axes[1],
)

sns.histplot(
    jet_speed_last10_pos,
    label="last10_pos",
    color="r",
    bins=np.arange(-5, 5.2, 0.5),
    stat="density",
    alpha=0.5,
    ax=axes[1],
)

axes[1].set_title("Jet speed anomaly positive NAO")

sns.histplot(
    jet_speed_first10_neg,
    label="first10",
    color="b",
    bins=np.arange(-5, 5.2, 0.5),
    stat="density",
    ax=axes[2],
)

sns.histplot(
    jet_speed_last10_neg,
    label="last10",
    color="r",
    bins=np.arange(-5, 5.2, 0.5),
    stat="density",
    alpha=0.5,
    ax=axes[2],
)

axes[2].set_title("Jet speed anomaly negative NAO")

# %%
# plot location histgram and composite mean map together
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
uhat_climatology = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/ua_Amon_MPI-ESM1-2-LR_HIST_climatology_185005-185909.nc"
)
uhat_climatology = uhat_climatology.ua.sel(plev=slice(None, 70000)).mean(dim="plev")

uhat_climatology = uhat_climatology.sel(time=slice("1859-06-01", "1859-08-31")).mean(
    dim="time"
)
# %%
fig, axes = plt.subplots(
    1, 3, figsize=(15, 6), subplot_kw={"projection": ccrs.Orthographic(-20, 60)}
)

plot_uhat(axes[0], uhat_climatology)
axes[0].set_title("Climatology")


plot_uhat(axes[1], uhat_pos_first10)
axes[1].set_title("Positive NAO")

plot_uhat(axes[2], uhat_neg_first10)
axes[2].set_title("Negative NAO")

for ax in axes:
    # Add gridlines
    gl = ax.gridlines(draw_labels=False, dms=True, x_inline=False, y_inline=False)

    # Optionally, adjust gridline appearance
    gl.xlines = True
    gl.ylines = True


plt.tight_layout(pad=1.3)
