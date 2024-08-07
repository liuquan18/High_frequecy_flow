# %%
import xarray as xr
import numpy as np
import pandas as pd
import logging

from src.extremes.extreme_read import sel_event_above_duration
from src.extremes.extreme_read import read_extremes
logging.basicConfig(level=logging.INFO)


# %%
def lead_lag_30days(events, base_plev=25000, cross_plev=1):

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


# %%
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

        sel_zg = zg.sel(
            time=slice(start_time, end_time)
        )  # note that xarray slice is inclusive on both sides
        if sel_zg.time.size < 61:
            if start_time < pd.Timestamp(f"{start_time.year}-05-01"):
                logging.info(
                    "start_time is before May 1st, filling the missing days with zeros"
                )
                missing_days = 61 - sel_zg.time.size
                add_data = sel_zg.isel(time=slice(None, missing_days)).copy()
                try:
                    add_data["time"] = pd.date_range(
                        end=f"{start_time.year}-05-01", periods=missing_days, freq="D"
                    )
                except OverflowError:
                    add_data["time"] = [start_time]
                # change values of add_data to 0
                add_data = xr.zeros_like(add_data)
                sel_zg = xr.concat([add_data, sel_zg], dim="time")
            elif end_time > pd.Timestamp(f"{end_time.year}-09-30"):
                logging.info(
                    "end_time is after September 30th, filling the missing days with zeros"
                )
                missing_days = 61 - sel_zg.time.size
                add_data = sel_zg.isel(time=slice(-1 * missing_days, None)).copy()
                try:
                    add_data["time"] = pd.date_range(
                        f"{end_time.year}-10-01", periods=missing_days, freq="D"
                    )
                except OverflowError:
                    add_data["time"] = [end_time]
                add_data = xr.zeros_like(add_data)
                sel_zg = xr.concat([sel_zg, add_data], dim="time")

        # now change the time coordinate as lag-days
        sel_zg["time"] = np.arange(-30, 31, 1)

        # put them together
        composite.append(sel_zg)
    try:
        composite = xr.concat(composite, dim="event")
    except ValueError:
        pass
    return composite


# %%[]
