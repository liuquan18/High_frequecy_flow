# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# %%
from src.extremes.extreme_read import read_extremes_allens

# %%
first10_pos_extremes, first10_neg_extremes = read_extremes_allens(
    "first10", start_duration=8
)  # start from 5 days to have more events

last10_pos_extremes, last10_neg_extremes = read_extremes_allens(
    "last10", start_duration=8
)


# %%
# select ens and plev, where there are more than one extreme event in one year
def events_above_once(events):
    return events[
        events.groupby([events.start_time.dt.year, "ens", "plev"])["mean"].transform(
            "size"
        )
        > 1
    ]


# %%
def collect_swing(events):
    events = events.sort_values("start_time")

    pp = []  # positive + positive
    nn = []  # negative + negative
    pn = []  # positive + negative
    np = []  # negative + positive

    # more than one extreme event
    for i in range(len(events) - 1):
        first = events.iloc[i]
        second = events.iloc[i + 1]

        # occurrence of events more than twice
        pp_ = []
        nn_ = []
        pn_ = []
        np_ = []

        if first.extreme_type == "pos" and second.extreme_type == "pos":
            pp_ = update_swing(pp_, first, second)
        elif first.extreme_type == "neg" and second.extreme_type == "neg":
            nn_ = update_swing(nn_, first, second)
        elif first.extreme_type == "pos" and second.extreme_type == "neg":
            pn_ = update_swing(pn_, first, second)
        elif first.extreme_type == "neg" and second.extreme_type == "pos":
            np_ = update_swing(np_, first, second)

        pp_ = pd.DataFrame(pp_)
        nn_ = pd.DataFrame(nn_)
        pn_ = pd.DataFrame(pn_)
        np_ = pd.DataFrame(np_)

        pp.append(pp_)
        nn.append(nn_)
        pn.append(pn_)
        np.append(np_)

    pp = pd.concat(pp, axis=0)
    nn = pd.concat(nn, axis=0)
    pn = pd.concat(pn, axis=0)
    np = pd.concat(np, axis=0)
    
    swing = pd.concat([pp, nn, pn, np], axis=0, keys = ["pos_pos", "neg_neg", "pos_neg", "neg_pos"])

    return swing


# %%
def update_swing(swing, first, second):
    swing.append(
        {
            "first_start_time": first.start_time,
            "first_end_time": first.end_time,
            "first_duration": first.duration,
            "second_start_time": second.start_time, 
            "second_end_time": second.end_time,
            "second_duration": second.duration,
            "gap_duration": (second.start_time - first.end_time).days,
        }
    )
    return swing


# %%
def collect_noswing(events):

    return events[
        events.groupby([events.start_time.dt.year, "ens", "plev"])["mean"].transform(
            "size"
        )
        == 1
    ]

# %%

first_extremes = pd.concat(
    [first10_pos_extremes, first10_neg_extremes], axis=0, keys=["pos", "neg"]
)
last_extremes = pd.concat(
    [last10_pos_extremes, last10_neg_extremes], axis=0, keys=["pos", "neg"]
)

# %%
first_extremes = (
    first_extremes.reset_index()
    .drop(columns="level_1")
    .rename(columns={"level_0": "extreme_type"})
)
last_extremes = (
    last_extremes.reset_index()
    .drop(columns="level_1")
    .rename(columns={"level_0": "extreme_type"})
)
# %%
### swings 
first_above_once = events_above_once(first_extremes)
first_swings = first_above_once.groupby([first_above_once.start_time.dt.year, "ens", "plev"])[
    [
        "extreme_type",
        "start_time",
        "end_time",
        "duration",
    ]
].apply(collect_swing)
first_swings = first_swings.reset_index().drop(columns="level_4").rename(columns={'level_3': 'swing_type'})


last_above_once = events_above_once(last_extremes)
last_swings = last_above_once.groupby([last_above_once.start_time.dt.year, "ens", "plev"])[
    [
        "extreme_type",
        "start_time",
        "end_time",
        "duration",
    ]
].apply(collect_swing)
last_swings = last_swings.reset_index().drop(columns="level_4").rename(columns={'level_3': 'swing_type'})
# %%
#### no swings
first_noswings = collect_noswing(first_extremes)
last_no_swings = collect_noswing(last_extremes)
# %%
#### statistics of swings (variability) ######
