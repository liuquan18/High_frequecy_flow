# %%
import pandas as pd
from scipy import ndimage


# %%
def calculate_residue(pc, threshold):
    # add a new column in pc called 'threshold'
    pc = pc.groupby(["plev", pc["time"].dt.year])[["plev", "time", "pc"]].apply(
        lambda x: x.assign(
            threshold=threshold[threshold["plev"] == x["plev"].values[0]][
                "threshold"
            ].values,
            residual=x["pc"]
            - threshold[threshold["plev"] == x["plev"].values[0]]["threshold"].values,
        )
    )
    pc = pc.droplevel(level=[0, 1])
    return pc


# %%
def extract_pos_extremes(df, column = 'residual'):
    """
    extract exsecutively above zero events
    """
    # apply ndimage.median_filter to remove the single day anomaly data (with one day tolerance)
    df.loc[:, column] = ndimage.median_filter(df[column], size=3)
    # A grouper that increaments every time a non-positive value is encountered
    Grouper_pos = df.groupby(df.time.dt.year)[column].transform(
        lambda x: x.lt(0).cumsum()
    )

    # groupby the year and the grouper
    G = df[df[column] > 0].groupby([df.time.dt.year, Grouper_pos])

    # Get the statistics of the group
    Events = G.agg(
        start_time=pd.NamedAgg(column="time", aggfunc="min"),
        end_time=pd.NamedAgg(column="time", aggfunc="max"),
        sum=pd.NamedAgg(column=column, aggfunc="sum"),
        mean=pd.NamedAgg(column=column, aggfunc="mean"),
        max=pd.NamedAgg(column=column, aggfunc="max"),
        min=pd.NamedAgg(
            column=column, aggfunc="min"
        ),  # add mean to make sure the data are all positive
    ).reset_index()
    Events["duration"] = (Events["end_time"] - Events["start_time"]).dt.days + 1

    Events = Events[["start_time", "end_time", "duration", "sum", "mean", "max", "min"]]
    return Events


# %%
def add_pos_sign_times(df: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    """
    Add sign_start_time and sign_end_time to the events DataFrame.

    Parameters:
    df (pd.DataFrame): The original DataFrame with 'time' and 'pc' columns.
    events (pd.DataFrame): The DataFrame of extreme events with 'start_time' and 'end_time' columns.

    Returns:
    pd.DataFrame: The events DataFrame with added 'sign_start_time' and 'sign_end_time' columns.
    """
    # apply median_filter
    df["pc"] = ndimage.median_filter(df["pc"], size=3)

    # Create a column for positive values
    df["positive"] = df["pc"] > 0

    # Create a grouper that increments every time the sign changes
    sign_grouper = df.groupby(df.time.dt.year)["pc"].transform(
        lambda x: x.lt(0).cumsum()
    )

    # Grouby by year and the sign_grouper
    G = df[df["pc"] > 0].groupby([df.time.dt.year, sign_grouper])

    # get the sign_start_time and sign_end_time
    sign_times = G.agg(
        sign_start_time=pd.NamedAgg(column="time", aggfunc="min"),
        sign_end_time=pd.NamedAgg(column="time", aggfunc="max"),
    ).reset_index()

    # functions to find corresponding sign_start_time and sign_end_time

    def find_sign_times(row):
        mask = (sign_times["sign_start_time"] <= row["start_time"]) & (
            sign_times["sign_end_time"] >= row["end_time"]
        )
        if mask.any():
            return sign_times.loc[mask.idxmax(), ["sign_start_time", "sign_end_time"]]
        return pd.Series({"sign_start_time": pd.NaT, "sign_end_time": pd.NaT})

    # Apply the function to each row in events
    sign_times_for_events = events.apply(find_sign_times, axis=1)

    # Add the new columns to the events DataFrame
    events["sign_start_time"] = sign_times_for_events["sign_start_time"]
    events["sign_end_time"] = sign_times_for_events["sign_end_time"]
    events["sign_duration"] = (
        events["sign_end_time"] - events["sign_start_time"]
    ).dt.days + 1

    return events


# %%
def extract_neg_extremes(df,column='residual'):
    """
    extract exsecutively below zero events
    """
    # apply ndimage.median_filter to remove the single day anomaly data (with one day tolerance)
    df[column] = ndimage.median_filter(df[column], size=3)

    # A grouper that increaments every time a non-positive value is encountered
    Grouper_neg = df.groupby(df.time.dt.year)[column].transform(
        lambda x: x.gt(0).cumsum()
    )

    # groupby the year and the grouper
    G = df[df[column] < 0].groupby([df.time.dt.year, Grouper_neg])

    # Get the statistics of the group
    Events = G.agg(
        start_time=pd.NamedAgg(column="time", aggfunc="min"),
        end_time=pd.NamedAgg(column="time", aggfunc="max"),
        sum=pd.NamedAgg(column=column, aggfunc="sum"),
        mean=pd.NamedAgg(column=column, aggfunc="mean"),
        max=pd.NamedAgg(column=column, aggfunc="max"),
        min=pd.NamedAgg(
            column=column, aggfunc="min"
        ),  # add mean to make sure the data are all positive
    ).reset_index()
    Events["duration"] = (Events["end_time"] - Events["start_time"]).dt.days + 1

    Events = Events[["start_time", "end_time", "duration", "sum", "mean", "max", "min"]]
    return Events
