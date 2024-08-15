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
def extract_pos_extremes(df, column="residual"):
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
def extract_neg_extremes(df, column="residual"):
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


# %%
def find_sign_times(extremes, signs):
    """
    Find the sign_start_time and sign_end_time for each extreme event.

    Parameters:
    extremes (pd.DataFrame): The DataFrame containing the extreme events.
    signs (pd.DataFrame): The DataFrame containing the sign events.

    Returns:
    pd.DataFrame: The DataFrame containing the extreme events with sign_start_time and sign_end_time.
    """



    # select rows of signs, where the sign event is within the extreme event
    new_extremes = []
    for i, row in extremes.iterrows():
        sign_i = signs[
            (signs["plev"] == row["plev"])
            & (signs["start_time"] <= row["start_time"])
            & (signs["end_time"] >= row["end_time"])
        ]
        row["sign_start_time"] = sign_i["start_time"].values[0]
        row["sign_end_time"] = sign_i["end_time"].values[0]
        row["sign_duration"] = sign_i["duration"].values[0]
        new_extremes.append(row)
    new_extremes = pd.DataFrame(new_extremes)

    new_extremes.loc[:, "start_time"] = pd.to_datetime(new_extremes["start_time"])
    new_extremes.loc[:, "end_time"] = pd.to_datetime(new_extremes["end_time"])
    new_extremes.loc[:, 'sign_start_time'] = pd.to_datetime(new_extremes['sign_start_time'])
    new_extremes.loc[:, 'sign_end_time'] = pd.to_datetime(new_extremes['sign_end_time'])

    # find duplicated rows on 'sign_start_time' and 'sign_end_time', delete first one, and replace the 'start_time' with
    # smallest 'start_time' and 'end_time' with largest 'end_time'

    # group by 'sign_start_time' and 'sign_end_time'
    new_extremes = new_extremes.groupby(["sign_start_time", "sign_end_time"])[new_extremes.columns].apply(
        lambda x: x.assign(
            start_time=x["start_time"].min(),
            end_time=x["end_time"].max(),
            duration=(x["end_time"].max() - x["start_time"].min()).days + 1,
        )
    )

    new_extremes = new_extremes.reset_index(drop=True)
    new_extremes = new_extremes.drop_duplicates(subset=["sign_start_time", "sign_end_time"], ignore_index=True)


    return new_extremes
