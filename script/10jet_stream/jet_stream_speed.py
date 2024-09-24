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
