# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %%
from src.extremes.extreme_read import read_extremes_allens
from src.extremes.extreme_swing import events_above_once, collect_swing, collect_noswing

# %%
import src.extremes.extreme_swing as es
import importlib

importlib.reload(es)

# %%
import logging

logging.basicConfig(level=logging.INFO)
# %%
first10_pos_extremes, first10_neg_extremes = read_extremes_allens(
    "first10", start_duration=5
)  # start from 5 days to have more events

last10_pos_extremes, last10_neg_extremes = read_extremes_allens(
    "last10", start_duration=5
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
first_swings = first_above_once.groupby(
    [first_above_once.start_time.dt.year, "ens", "plev"]
)[
    [
        "extreme_type",
        "event_start_time",
        "event_end_time",
        "event_duration",
    ]
].apply(
    collect_swing
)

first_swings = (
    first_swings.reset_index()
    .drop(columns="level_4")
    .rename(columns={"level_3": "swing_type"})
)


# %%
last_above_once = events_above_once(last_extremes)
last_swings = last_above_once.groupby(
    [last_above_once.start_time.dt.year, "ens", "plev"]
)[
    [
        "extreme_type",
        "event_start_time",
        "event_end_time",
        "event_duration",
    ]
].apply(
    collect_swing
)
last_swings = (
    last_swings.reset_index()
    .drop(columns="level_4")
    .rename(columns={"level_3": "swing_type"})
)
# %%


# %%
#### statistics of swings (variability) ######
def count_swints(swings, percentage=True):
    swings_stat = pd.DataFrame(
        columns=np.arange(-90, 91, 1),
        index=["pos_", "pos_pos", "pos_neg", "neg_", "neg_pos", "neg_neg"],
        data=0,
    )

    # swings
    for swing_type in ["pos_pos", "pos_neg", "neg_pos", "neg_neg"]:
        swings_onetype = swings[swings.swing_type == swing_type]

        for i, swing in swings_onetype.iterrows():

            first_start = -swing.first_duration
            first_end = 0

            second_start = swing.gap_duration
            second_end = swing.second_duration + swing.gap_duration

            swings_stat.loc[swing_type, first_start : first_end - 1] += 1
            swings_stat.loc[swing_type, second_start : second_end - 1] += 1

    swings_stat.loc["pos_", :] = (
        swings_stat.loc["pos_pos", :] + swings_stat.loc["pos_neg", :]
    )
    swings_stat.loc["neg_", :] = (
        swings_stat.loc["neg_pos", :] + swings_stat.loc["neg_neg", :]
    )

    if percentage:
        swings_stat.iloc[1:3] = (
            swings_stat.iloc[1:3].div(swings_stat.loc["pos_", :], axis=1) * 100
        )
        swings_stat.iloc[4:6] = (
            swings_stat.iloc[4:6].div(swings_stat.loc["neg_", :], axis=1) * 100
        )

    # make negative values negative
    swings_stat.loc["pos_neg", 1:] = -swings_stat.loc["pos_neg", 1:]
    swings_stat.loc["neg_pos", :-1] = -swings_stat.loc["neg_pos", :-1]
    swings_stat.loc["neg_neg", :] = -swings_stat.loc["neg_neg", :]

    return swings_stat


# %%
first_swings_stat = count_swints(
    first_swings[first_swings.plev == 50000], percentage=False
)
first_swings_stat_perc = count_swints(
    first_swings[first_swings.plev == 50000], percentage=True
)

# %%
last_swings_stat = count_swints(
    last_swings[last_swings.plev == 50000], percentage=False
)
last_swings_stat_perc = count_swints(
    last_swings[last_swings.plev == 50000], percentage=True
)
# %%
# Set up the plot


def plot_swings(swings, swings_perc, vmin, vmax):
    fig, ax = plt.subplots(figsize=(20, 5))

    # Define color maps
    blue_cmap = plt.cm.Blues
    orange_cmap = plt.cm.Oranges

    def value2color(value, cmap, vmin=5, vmax=30):
        abs_value = abs(value)
        if abs_value < vmin:
            return "none"
        # elif abs_value > vmax:
        #     return cmap(1)
        else:
            normalized_value = (abs_value - vmin) / (vmax - vmin)
        return cmap(normalized_value)

    extreme_types = ["neg_pos", "neg_neg", "neg_", "pos_neg", "pos_pos", "pos_"]
    lag_days = np.arange(-90, 91, 1)

    # shading and text for the swing data
    for i in [0, 1, 3, 4]:
        row = extreme_types[i]
        for j, lag in enumerate(lag_days):
            value = swings.loc[row, lag]
            perc = swings_perc.loc[row, lag]
            color = (
                value2color(perc, blue_cmap, vmin, vmax)
                if perc < 0
                else value2color(perc, orange_cmap, vmin, vmax)
            )
            if lag in range(-14, 70, 1):
                ax.bar(
                    lag, 0.4, bottom=i + 0.3, width=1.0, color=color, edgecolor="black"
                )
                ax.text(
                    lag, i + 0.5, str(int(value)), ha="center", va="center", fontsize=8
                )

    # only text for "pos_"  and "neg_"
    for i in [2, 5]:
        row = extreme_types[i]
        for j, lag in enumerate(lag_days):
            value = swings.loc[row, lag]
            if lag in range(-14, 70, 1):
                ax.bar(
                    lag,
                    0.4,
                    bottom=i + 0.3,
                    width=1.0,
                    color="white",
                    edgecolor="black",
                )
                ax.text(
                    lag, i + 0.5, str(int(value)), ha="center", va="center", fontsize=8
                )

    ax.set_xlim(-15, 70)
    # make y_ticks higher than index of extreme_types
    ax.set_yticks(np.arange(0.5, 6, 1))
    ax.set_yticklabels(extreme_types)
    ax.set_xlabel("Lag days")
    ax.set_title("Visualization of Swing Data")

    # vertical line at x = 0
    ax.axvline(x=0, color="red", linewidth=1, linestyle="--")
    # text at left of the line, up at the top to indicate "first event"
    ax.text(-1, 6.2, "First event", ha="right", va="top", fontsize=8)
    # text at right of the line, up at the top to indicate "second event"
    ax.text(3, 6.2, "Second event", ha="left", va="top", fontsize=8)

    plt.tight_layout()


# %%
plot_swings(first_swings_stat, first_swings_stat, 1, 15)
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/extremes_statistics/first10_swings_500hPa.pdf"
)
# %%
plot_swings(last_swings_stat, last_swings_stat, 1, 15)
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/extremes_statistics/last10_swings_500hPa.pdf"
)
# %%
