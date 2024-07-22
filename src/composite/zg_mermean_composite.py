# %%
import xarray as xr
import numpy as np
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)

from src.extremes.extreme_statistics import sel_event_above_duration


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
def lead_lag_time(events, base_plev=25000, cross_plev=1):

    start_times = []
    end_times = []

    for base_event in events[events["plev"] == base_plev].itertuples():
        ref_time = base_event.end_time

        count_startime = ref_time - pd.Timedelta(days=30)
        count_endtime = ref_time + pd.Timedelta(days=30)

        # select the rows where the time between "start_time" and "end_time" has an overlap with the time between "count_startime" and "count_endtime"
        overlapped_events_across_height = events[
            (events.start_time <= count_endtime) & (events.end_time >= count_startime)
        ]

        if len(overlapped_events_across_height.plev.unique()) < cross_plev:
            continue

        start_times.append(count_startime)
        end_times.append(count_endtime)

    date_range = pd.DataFrame({"start_time": start_times, "end_time": end_times})

    return date_range

#%%
def composite_zg_mermean(zg, date_range):
    """
    parameters:
    zg: xarray dataset
        zonal mean geopotential height
    date_range: pandas dataframe
        start_time and end_time for the composite
    """
    composite = []
    for start_time, end_time in date_range.itertuples(index=False):
        duration = end_time - start_time
        sel_zg = zg.sel(time=slice(start_time, end_time )) # note that xarray slice is inclusive on both sides
        sel_zg['time'] = np.arange(-30, 31,1)
        if duration.days != (len(sel_zg.time) -1):
            logging.warning(f"Duration of the extreme event is {duration.days + 1}, not equal to 61 days")
            continue
        composite.append(
            sel_zg
        )
    try:
        composite = xr.concat(composite, dim="event")
    except ValueError:
        pass
    return composite

