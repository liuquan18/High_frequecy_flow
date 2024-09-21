# %%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import logging

logging.basicConfig(level=logging.INFO)
import seaborn as sns

import matplotlib.pyplot as plt

from src.extremes.extreme_read import read_extremes_allens

# %%
def _jet_stream_anomaly(ens, period, climatology, stat = 'loc'):
    # Load data
    jet_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_{period}/"
    jet_file = glob.glob(f"{jet_path}*r{ens}i1p1f1*.nc")[0]

    jet = xr.open_dataset(jet_file).ua
    # drop dim lon
    jet = jet.isel(lon=0)

    if stat == 'speed':

        # maximum westerly wind speed of the resulting profile is then identified and this is defined as the jet speed.
        jet_speed = jet.max(dim="lat")
        jet_speed_ano = jet_speed.groupby("time.month") - climatology

        return jet_speed_ano

    elif stat == 'loc':
            
        # The jet latitude is defined as the latitude at which this maximum is found.
        jet_loc = jet.lat[jet.argmax(dim="lat")]

        jet_loc_ano = jet_loc.groupby("time.month") - climatology

        if jet_loc_ano.min() < -50:
            logging.warning(
                f"Jet latitude anomaly is below -40 for ens {ens} in period {period}\n"
            )
        
        return jet_loc_ano



# %%
def jet_stream_anomaly(period):

    # climatology only use the first10 years
    jet_speed_clim = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_speed_climatology_first10.nc"
    ).ua
    jet_loc_clim = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_first10.nc"
    ).lat

    jet_speed_ano = []
    jet_loc_ano = []

    for ens in range(1, 51):
        loc_ano = _jet_stream_anomaly(
            ens, period, jet_loc_clim, stat="loc"
        )
        loc_ano["ens"] = ens

        speed_ano = _jet_stream_anomaly(
            ens, period, jet_speed_clim, stat="speed"
        )
        speed_ano["ens"] = ens

        jet_speed_ano.append(speed_ano)
        jet_loc_ano.append(loc_ano)

    jet_speed_ano = xr.concat(jet_speed_ano, dim="ens")
    jet_loc_ano = xr.concat(jet_loc_ano, dim="ens")

    return jet_speed_ano, jet_loc_ano


# %%

jet_speed_first10_ano, jet_loc_first10_ano = jet_stream_anomaly("first10")

# %%
jet_speed_last10_ano, jet_loc_last10_ano = jet_stream_anomaly("last10")
# %%
# jet location anomaly
sns.histplot(
    jet_loc_first10_ano.values.flatten(),
    label="first10",
    color="b",
    bins=np.arange(-30, 31, 2),
    stat="count",
)
sns.histplot(
    jet_loc_last10_ano.values.flatten(),
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
)
plt.legend()
# %%
sns.histplot(
    jet_speed_first10_ano.values.flatten(),
    label="first10",
    color="b",
    bins=np.arange(-5, 5.2, 0.5),
    stat="density",
)
sns.histplot(
    jet_speed_last10_ano.values.flatten(),
    label="last10",
    color="r",
    bins=np.arange(-5, 5.2, 0.5),
    stat="density",
    alpha=0.5,
)
# %%
def jet_loc_extremeNAO(NAO, jet_loc):
    jet_loc_negs = []
    jet_loc_poss = []

    for ens in range(1, 51):
        NAO_ens = NAO.sel(ens=ens)

        # negative NAO extreme months
        NAO_neg = NAO_ens.where(NAO_ens < -1.5, drop=True)
        jet_loc_neg = jet_loc.sel(
        ens=ens,
        time=(
            jet_loc.time.dt.year.isin(NAO_neg.time.dt.year)
            & jet_loc.time.dt.month.isin(NAO_neg.time.dt.month)
        ),
    )

        NAO_pos = NAO_ens.where(NAO_ens > 1.5, drop=True)
        jet_loc_pos = jet_loc.sel(
        ens=ens,
        time=(
            jet_loc.time.dt.year.isin(NAO_pos.time.dt.year)
            & jet_loc.time.dt.month.isin(NAO_pos.time.dt.month)
        ),
    )

        if jet_loc_neg.time.size == 0:
            continue # empty array
        else:
            jet_loc_negs.append(jet_loc_neg.values)

        if jet_loc_pos.time.size == 0:
            continue
        else:
            jet_loc_poss.append(jet_loc_pos.values)

    # flat the list
    jet_loc_negs = np.concatenate(jet_loc_negs)
    jet_loc_poss = np.concatenate(jet_loc_poss)

    return jet_loc_negs, jet_loc_poss

#%%
first10_pos_events, first10_neg_events = read_extremes_allens("first10", 8)
last10_pos_events, last10_neg_events = read_extremes_allens("last10", 8)


# %%
def jet_loc_event(jet_locs, events, average = True):
    # change time to tiemstamp
    try:
        jet_locs['time'] = jet_locs.indexes['time'].to_datetimeindex()
    except AttributeError:
        pass
    # iterate over all events
    jet_locs_event = []
    for idx, event in events.iterrows():
        jet_loc = jet_locs.sel(
            time = slice (event.extreme_start_time, event.extreme_end_time),
            ens = event.ens
        )

        if average:
            jet_loc = jet_loc.mean(dim='time')
        # to numpy array
        jet_loc = jet_loc.values
        jet_locs_event.append(jet_loc)
    try:
        jet_locs_event = np.concatenate(jet_locs_event)
    except ValueError:
        jet_locs_event = np.array(jet_locs_event)
    return jet_locs_event
# %%
jet_loc_first10_pos = jet_loc_event(jet_loc_first10_ano, first10_pos_events)
jet_loc_first10_neg = jet_loc_event(jet_loc_first10_ano, first10_neg_events)
# %%
jet_loc_last10_pos = jet_loc_event(jet_loc_last10_ano, last10_pos_events)
jet_loc_last10_neg = jet_loc_event(jet_loc_last10_ano, last10_neg_events)
# %%
# plot jet location anomaly
fig, axes = plt.subplots(3,1, figsize=(10, 10))

# jet location anomaly
sns.histplot(
    jet_loc_first10_ano.values.flatten(),
    label="first10",
    color="b",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax = axes[0]
)
sns.histplot(
    jet_loc_last10_ano.values.flatten(),
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax = axes[0]
)

axes[0].set_title("Jet location anomaly all")

sns.histplot(
    jet_loc_first10_pos,
    label="first10_pos",
    color="b",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=axes[1]
)

sns.histplot(
    jet_loc_last10_pos,
    label="last10_pos",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=axes[1]
)
axes[1].set_title("Jet location anomaly positive NAO")


sns.histplot(
    jet_loc_first10_neg,
    label="first10",
    color="b",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=axes[2]
)

sns.histplot(
    jet_loc_last10_neg,
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=axes[2]
)
axes[2].set_title("Jet location anomaly negative NAO")
# %%
