# %%
import xarray as xr
import numpy as np
import pandas as pd
import logging
import glob

import src.extremes.extreme_read as ext_read

logging.basicConfig(level=logging.INFO)


# %%
def read_variable(
    variable: str, period: str, ens: int, plev: int = None, freq_label: str = None
):
    """
    Parameters
    ----------
    variable : str
        variable name
    period : str
        period name, first10 or last10
    ens : int
        ensemble number
    plev : int
        pressure level
    freq : str
        frequency label, default is None, hat, prime, prime_veryhigh, prime_intermedia
    """
    base_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{variable}_daily_global/{variable}_MJJAS_{period}"

    if freq_label is None:
        freq_label = "/"
    else:
        freq_label = f"_{freq_label}/"

    base_path = f"{base_path}{freq_label}"

    file = glob.glob(f"{base_path}{variable}_day_*r{ens}i1p1f1_gn_*.nc")[0]

    try:
        ds = xr.open_dataset(file)[variable]
    except KeyError:
        ds = xr.open_dataset(file)["ua"]  # case for momentum fluxes
    if plev is not None:
        ds = ds.sel(plev=plev)

    # convert datetime to pandas datetime
    try:
        ds["time"] = ds.indexes["time"].to_datetimeindex()
    except AttributeError:
        pass

    return ds


# %%
def lead_lag_30days(events, base_plev=None, cross_plev=1):

    start_times = []
    end_times = []

    if base_plev is not None:
        events = events[events["plev"] == base_plev]

    for base_event in events.itertuples():
        ref_time = base_event.extreme_end_time

        count_startime = ref_time - pd.Timedelta(days=30)
        count_endtime = ref_time + pd.Timedelta(days=31)

        # select the rows where the time between "extreme_start_time" and "extreme_end_time" has an overlap with the time between "count_startime" and "count_endtime"
        overlapped_events_across_height = events[
            (events.extreme_start_time <= count_endtime)
            & (events.extreme_end_time >= count_startime)
        ]

        if len(overlapped_events_across_height.plev.unique()) < cross_plev:
            continue

        start_times.append(count_startime)
        end_times.append(count_endtime)

    date_range = pd.DataFrame(
        {"extreme_start_time": start_times, "extreme_end_time": end_times}
    )

    return date_range


# %%
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
            time=slice(start_time, end_time)
        )  # note that xarray slice is inclusive on both sides
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


# %%[]
def event_composite(variable, pos_extremes, neg_extremes, base_plev=None, cross_plev=1):

    pos_date_range = lead_lag_30days(pos_extremes, base_plev, cross_plev)
    neg_date_range = lead_lag_30days(neg_extremes, base_plev, cross_plev)

    pos_composite = None
    neg_composite = None

    if not pos_date_range.empty:
        pos_composite = date_range_composite(variable, pos_date_range)

    if not neg_date_range.empty:
        neg_composite = date_range_composite(variable, neg_date_range)

    return pos_composite, neg_composite


# %%
def composite_single_ens(variable, period, ens, plev, freq_label=None):
    pos_extreme, neg_extreme = ext_read.read_extremes(period, 8, ens, plev=plev)
    variable_ds = read_variable(variable, period, ens, plev, freq_label)

    pos_comp, neg_comp = event_composite(variable_ds, pos_extreme, neg_extreme)
    return pos_comp, neg_comp


# %%
def composite_variable(variable, plev, freq_label, period, stat="mean"):
    pos_comps = []
    neg_comps = []

    for i in range(1, 51):
        pos_comp, neg_comp = composite_single_ens(variable, period, i, plev, freq_label)

        pos_comps.append(pos_comp)
        neg_comps.append(neg_comp)

    # exclude None from the list
    pos_comps = [x for x in pos_comps if x is not None]
    neg_comps = [x for x in neg_comps if x is not None]

    pos_comps = xr.concat(pos_comps, dim="event")
    neg_comps = xr.concat(neg_comps, dim="event")

    if stat == "mean":
        pos_comps = pos_comps.mean(dim="event")
        neg_comps = neg_comps.mean(dim="event")
    elif stat == "count":
        pos_comps = pos_comps.count(dim="event")
        neg_comps = neg_comps.count(dim="event")

    return pos_comps, neg_comps
