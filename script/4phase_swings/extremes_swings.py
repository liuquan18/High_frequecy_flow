# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# %%
from src.extremes.extreme_read import read_extremes_allens
from src.extremes.extreme_swing import events_above_once, collect_swing, collect_noswing

# %%
first10_pos_extremes, first10_neg_extremes = read_extremes_allens(
    "first10", start_duration=8
)  # start from 5 days to have more events

last10_pos_extremes, last10_neg_extremes = read_extremes_allens(
    "last10", start_duration=8
)


# %%
# concatenate positive and negative extremes
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
