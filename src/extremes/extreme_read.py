# %%
import xarray as xr
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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


def sel_event_above_duration(df, duration=5, by="extreme_duration"):
    """
    select the extreme events, which durates 5 days or more in June to August
    """

    # Convert start_time and end_time to datetime if they aren't already
    df.loc[:, "extreme_start_time"] = pd.to_datetime(df["extreme_start_time"])
    df.loc[:, "extreme_end_time"] = pd.to_datetime(df["extreme_end_time"])

    if by == "extreme_duration":
        # Apply the function to each row
        df.loc[:, "days_in_JJA"] = df.apply(
            lambda row: days_in_june_to_aug(
                row["extreme_start_time"], row["extreme_end_time"]
            ),
            axis=1,
        )

        # Filter rows where there are at least 5 days in June to August
        result = df[df["days_in_JJA"] >= duration]

    elif by == "sign_duration":
        result = df[df["sign_duration"] >= duration]

    else:
        raise ValueError('by should be either "extreme_duration" or "sign_duration"')
    return result


def sel_extreme_duration(df, duration=5):
    """
    select the extreme events, which durates 5 days or more in June to August
    """

    # Convert start_time and end_time to datetime if they aren't already
    df["extreme_start_time"] = pd.to_datetime(df["extreme_start_time"])
    df["extreme_end_time"] = pd.to_datetime(df["extreme_end_time"])
    # Apply the function to each row
    df["days_in_JJA"] = df.apply(
        lambda row: days_in_june_to_aug(
            row["extreme_start_time"], row["extreme_end_time"]
        ),
        axis=1,
    )

    # Filter rows where there are at least 5 days in June to August
    result = df[df["days_in_JJA"] == duration]
    return result


def days_in_june_to_aug(start, end):
    # Check if the event spans multiple years
    if start.year != end.year:
        return 0

    june1 = pd.Timestamp(start.year, 6, 1)
    sep1 = pd.Timestamp(start.year, 9, 1)

    overlap_start = max(start, june1)
    overlap_end = min(end, sep1)

    if overlap_start < overlap_end:
        return (overlap_end - overlap_start).days + 1
    return 0


# %%
def read_extremes_allens(period, start_duration=5):
    """
    parameters:
    period: str, 'first10' or 'last10'
    start_duration: int, above which (>=) duration the events are selected
    plev: int, pressure level in Pa
    """
    pos_extremes = []
    neg_extremes = []

    for i in range(1, 51):
        pos_extreme, neg_extreme = read_extremes(
            period, start_duration=start_duration, ens=i
        )

        pos_extreme["ens"] = i
        neg_extreme["ens"] = i

        pos_extremes.append(pos_extreme)
        neg_extremes.append(neg_extreme)

    pos_extremes = pd.concat(pos_extremes, axis=0, ignore_index=True)
    neg_extremes = pd.concat(neg_extremes, axis=0, ignore_index=True)
    return pos_extremes, neg_extremes


# %%
