# %%
import xarray as xr
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from src.extremes.extreme_statistics import (
    read_extremes_allens,
    sel_event_above_duration,
)


# %%
def read_extremes(period: str, start_duration: int, ens: int):
    """
    parameters:
    period: str
        period of the extremes, first10 or last10
    start_duration: int
        >= which duration the extremes are selected
    """
    pos_extreme_path = (
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/pos_extreme_events/"
    )
    neg_extreme_path = (
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/neg_extreme_events/"
    )

    tags = {"first10": "1850_1859", "last10": "2091_2100"}
    tag = tags[period]

    pos_extreme = pd.read_csv(
        f"{pos_extreme_path}pos_extreme_events_{period}/troposphere_pos_extreme_events_{tag}_r{ens}.csv"
    )
    neg_extreme = pd.read_csv(
        f"{neg_extreme_path}neg_extreme_events_{period}/troposphere_neg_extreme_events_{tag}_r{ens}.csv"
    )

    # select the extremes with durations longer than or equal to start_duration
    pos_extreme = sel_event_above_duration(pos_extreme, duration=start_duration)
    neg_extreme = sel_event_above_duration(neg_extreme, duration=start_duration)
    return pos_extreme, neg_extreme


# %%


def concurrent_events(pos_extreme, events_container):
    for base_event in pos_extreme[pos_extreme["plev"] == 25000].itertuples():
        ref_time = base_event.end_time

        count_startime = ref_time - pd.Timedelta(days=30)
        count_endtime = ref_time + pd.Timedelta(days=30)

        # select the rows where the time between "start_time" and "end_time" has an overlap with the time between "count_startime" and "count_endtime"
        overlapped_events = pos_extreme[
            (pos_extreme.start_time <= count_endtime)
            & (pos_extreme.end_time >= count_startime)
        ]

        # loop over all the events in the overlapped_events and update the count in container
        for event in overlapped_events.itertuples():
            event_startday = np.max([(event.start_time - ref_time).days, -30])
            event_endday = np.min([(event.end_time - ref_time).days, 30])
            events_container.loc[event.plev, event_startday:event_endday] += 1


# %%
first10_pos_events_container = pd.DataFrame(
    columns=list(range(-30, 31)),
    index=[25000, 50000, 70000, 85000, 100000],
    data=0,
)

first10_neg_events_container = pd.DataFrame(
    columns=list(range(-30, 31)),
    index=[25000, 50000, 70000, 85000, 100000],
    data=0,
)

last10_pos_events_container = pd.DataFrame(
    columns=list(range(-30, 31)),
    index=[25000, 50000, 70000, 85000, 100000],
    data=0,
)

last10_neg_events_container = pd.DataFrame(
    columns=list(range(-30, 31)),
    index=[25000, 50000, 70000, 85000, 100000],
    data=0,
)

# %%
# first10

for ens in range(1, 51):
    pos_extreme, neg_extreme = read_extremes("first10", 8, ens)
    concurrent_events(pos_extreme, first10_pos_events_container)
    concurrent_events(neg_extreme, first10_neg_events_container)
# %%
for ens in range(1, 51):
    pos_extreme, neg_extreme = read_extremes("last10", 8, ens)
    concurrent_events(pos_extreme, last10_pos_events_container)
    concurrent_events(neg_extreme, last10_neg_events_container)
# %%
