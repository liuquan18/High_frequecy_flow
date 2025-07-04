# %%
import xarray as xr
import numpy as np
import pandas as pd
import logging
import glob

import src.extremes.extreme_read as ext_read

logging.basicConfig(level=logging.INFO)


# %%
################## NAO composite during the event ######################
def during_NAO_composite(uhat, events):
    try:
        uhat["time"] = uhat.indexes["time"].to_datetimeindex()
    except AttributeError:
        pass

    uhat_extreme = []
    for i, event in events.iterrows():
        uhat_extreme.append(
            uhat.sel(time=slice(event["extreme_start_time"], event["extreme_end_time"]))
        )

    uhat_extreme = xr.concat(uhat_extreme, dim="time")

    # average over time
    uhat_extreme = uhat_extreme.mean(dim="time")

    return uhat_extreme


# %%
################# before the NAO composite ######################
# %%
def before_NAO_composite(NAO, data, lag=(-15, -5)):

    data_before_NAO = []
    for i, event in NAO.iterrows():
        event_date = pd.to_datetime(event.extreme_start_time)
        event_date_before_start = event_date + pd.Timedelta(days=lag[0])
        event_date_before_end = event_date + pd.Timedelta(days=lag[1])

        # -15 to -5 days before the event average

        # if 'ens' in the column
        if "ens" in data.dims:
            event_ens = int(event.ens)
            data_NAO_event = data.sel(
                time=slice(event_date_before_start, event_date_before_end),
                ens=event_ens,
            ).mean(dim="time")
        else:
            data_NAO_event = data.sel(
                time=slice(event_date_before_start, event_date_before_end)
            ).mean(dim="time")

        data_before_NAO.append(data_NAO_event)

    data_before_NAO = xr.concat(data_before_NAO, dim="event")

    return data_before_NAO


################# NAO composite -30 - 30 days ######################
# %%
def find_lead_lag_30days(events, base_plev=None, cross_plev=None):
    """
    Parameters
    ----------
    events : pandas dataframe
        extreme events
    base_plev : int
        base pressure level
    cross_plev : int
        number of pressure levels that the events should concurrently occur
    """

    start_times = []
    end_times = []
    try:
        events["extreme_start_time"] = pd.to_datetime(events["extreme_start_time"])
        events["extreme_end_time"] = pd.to_datetime(events["extreme_end_time"])
    except Exception:
        pass

    for base_event in events.itertuples():
        ref_time = base_event.extreme_start_time
        ref_time = pd.to_datetime(ref_time).normalize()  # normalize to remove time part

        count_startime = ref_time - pd.Timedelta(days=30)
        count_endtime = ref_time + pd.Timedelta(days=30)

        # select the rows where the time between "extreme_start_time" and "extreme_end_time" has an overlap with the time between "count_startime" and "count_endtime"
        overlapped_events_across_height = events[
            (events.extreme_start_time <= count_endtime)
            & (events.extreme_end_time >= count_startime)
        ]

        if (cross_plev is not None) and (
            len(overlapped_events_across_height.plev.unique()) < cross_plev
        ):
            continue

        start_times.append(count_startime)
        end_times.append(count_endtime)

    date_range = pd.DataFrame(
        {"extreme_start_time": start_times, "extreme_end_time": end_times}
    )

    return date_range


def date_range_composite(zg, date_range):
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
            time=slice(start_time, start_time + pd.Timedelta(days=61))
        )  
        sel_zg = sel_zg.isel(time = slice(None, 61)) # ensure we have 61 days
        if sel_zg.time.size < 61:
            if start_time < pd.Timestamp(f"{start_time.year}-05-01"):
                logging.info(
                    "start_time is before May 1st, filling the missing days with Nan"
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
                # change zeros to np.nan
                add_data = add_data.where(add_data != 0)

                sel_zg = xr.concat([add_data, sel_zg], dim="time")
            elif end_time > pd.Timestamp(f"{end_time.year}-09-30"):
                logging.info(
                    "end_time is after September 30th, filling the missing days with Nan"
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
                add_data = add_data.where(add_data != 0)
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


def range_NAO_composite_single_phase(
    variable, extremes, base_plev=None, cross_plev=None
):
    date_range = find_lead_lag_30days(extremes, base_plev, cross_plev)
    composite = None
    if not date_range.empty:
        composite = date_range_composite(variable, date_range)
    return composite


def range_NAO_composite(
    variable, pos_extremes, neg_extremes, base_plev=None, cross_plev=None
):

    # pos
    pos_composite = range_NAO_composite_single_phase(
        variable, pos_extremes, base_plev, cross_plev
    )

    # neg
    neg_composite = range_NAO_composite_single_phase(
        variable, neg_extremes, base_plev, cross_plev
    )
    return pos_composite, neg_composite
