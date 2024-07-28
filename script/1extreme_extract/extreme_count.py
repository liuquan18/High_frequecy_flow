# %%
import pandas as pd
import numpy as np
import seaborn as sns
from src.extremes.extreme_statistics import read_extremes_allens
import matplotlib.pyplot as plt


# %%
def combine_events(df, duration=13):
    """
    combine the events which durates more than 13 days
    """
    # Step 1: Split the dataframe
    df_up_to_13 = df[df.index <= duration]
    df_above_13 = df[df.index > duration]

    # Step 2: Sum the "duration" for rows > 13
    count_above_13 = df_above_13["count"].sum()
    mean_above_13 = np.average(
        df_above_13["mean"], weights=df_above_13.index
    )  # weighted average

    # Step 3: Create a new row and append it to df_up_to_13
    combine_row = pd.DataFrame(
        {
            "mean": [mean_above_13],
            "count": [count_above_13],
            "note": [f"above_{str(duration)}"],
        },
        index=[duration + 1],
    )  # should be ">duration" in plots

    df_final = pd.concat([df_up_to_13, combine_row])

    return df_final


# %%
def extreme_stat_allens(start_duration=5, duration_lim=8, plev=50000):
    first10_pos_extremes, first10_neg_extremes = read_extremes_allens(
        "first10", start_duration=start_duration
    )
    last10_pos_extremes, last10_neg_extremes = read_extremes_allens(
        "last10", start_duration=start_duration
    )

    # select the events with plev
    first10_pos_extremes = first10_pos_extremes[first10_pos_extremes["plev"] == plev]
    first10_neg_extremes = first10_neg_extremes[first10_neg_extremes["plev"] == plev]
    last10_pos_extremes = last10_pos_extremes[last10_pos_extremes["plev"] == plev]
    last10_neg_extremes = last10_neg_extremes[last10_neg_extremes["plev"] == plev]

    # statistics across ensemble members
    first10_pos = first10_pos_extremes.groupby("duration")["mean"].agg(
        ["mean", "count"]
    )
    first10_neg = first10_neg_extremes.groupby("duration")["mean"].agg(
        ["mean", "count"]
    )

    last10_pos = last10_pos_extremes.groupby("duration")["mean"].agg(["mean", "count"])
    last10_neg = last10_neg_extremes.groupby("duration")["mean"].agg(["mean", "count"])

    first10_pos = combine_events(first10_pos, duration=duration_lim)
    first10_neg = combine_events(first10_neg, duration=duration_lim)
    last10_pos = combine_events(last10_pos, duration=duration_lim)
    last10_neg = combine_events(last10_neg, duration=duration_lim)
    return first10_pos, first10_neg, last10_pos, last10_neg


# %%
def plot_extreme_stat(
    first10_pos, first10_neg, last10_pos, last10_neg, stat="count", duration_lim=7
):
    print(f"Plotting extreme statistics for {stat}")

    # Get the union of all durations
    all_durations = sorted(
        set(first10_pos.index)
        | set(last10_pos.index)
        | set(first10_neg.index)
        | set(last10_neg.index)
    )

    # Reindex all DataFrames to include all durations, filling missing values with 0
    first10_pos = first10_pos.reindex(all_durations, fill_value=0)
    last10_pos = last10_pos.reindex(all_durations, fill_value=0)
    first10_neg = first10_neg.reindex(all_durations, fill_value=0)
    last10_neg = last10_neg.reindex(all_durations, fill_value=0)

    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 8))

    # Set the width of each bar and the positions of the bars
    width = 0.35
    x = np.arange(len(all_durations))

    # Plot positive values
    ax.bar(
        x - width / 2,
        first10_pos[stat],
        width,
        label="First 10 years (positive)",
        color="black",
        alpha=0.7,
    )
    ax.bar(
        x + width / 2,
        last10_pos[stat],
        width,
        label="Last 10 years (positive)",
        color="red",
        alpha=0.7,
    )

    # Plot negative values
    if stat == "count":
        ax.bar(
            x - width / 2,
            -first10_neg[stat],
            width,
            label="First 10 years (negative)",
            color="black",
            alpha=0.3,
        )
        ax.bar(
            x + width / 2,
            -last10_neg[stat],
            width,
            label="Last 10 years (negative)",
            color="red",
            alpha=0.3,
        )
    elif stat == "mean":
        ax.bar(
            x - width / 2,
            first10_neg[stat],
            width,
            label="First 10 years (negative)",
            color="black",
            alpha=0.3,
        )
        ax.bar(
            x + width / 2,
            last10_neg[stat],
            width,
            label="Last 10 years (negative)",
            color="red",
            alpha=0.3,
        )

    # Set labels and title
    ax.set_xlabel("Duration")
    ax.set_ylabel(stat)
    ax.set_title("Count Distribution by Duration")

    # Set x-axis ticks
    ax.set_xticks(x)
    ax.set_xticklabels(all_durations, rotation=45)

    # Add legend
    ax.legend()

    # Add a horizontal line at y=0
    ax.axhline(y=0, color="k", linestyle="-", linewidth=0.5)

    # change the x-label "11" to ">10"
    labels = [item.get_text() for item in ax.get_xticklabels()]
    labels[-1] = f">{duration_lim}"
    ax.set_xticklabels(labels)

    # Adjust layout and display the plot
    plt.tight_layout()
    return fig, ax


# %%
def increase_by_percentage(first, last):
    first_count = first.loc[first["note"] == "above_7"]["count"].values[0]
    last_count = last.loc[last["note"] == "above_7"]["count"].values[0]
    increase = (last_count - first_count) / first_count * 100
    return increase


# %%
increase_bys_pos = {}
increase_bys_neg = {}
pos_extrems = []
neg_extrems = []

for plev in [100000, 85000, 70000, 50000, 25000]:
    first10_pos, first10_neg, last10_pos, last10_neg = extreme_stat_allens(
        start_duration=5, duration_lim=7, plev=plev
    )

    # fig, ax = plot_extreme_stat(first10_pos,first10_neg,last10_pos,last10_neg, stat = 'count')
    # plt.savefig(f"/work/mh0033/m300883/High_frequecy_flow/docs/plots/extremes_statistics/count_distribution_{plev}.png")

    # fig, ax = plot_extreme_stat(first10_pos,first10_neg,last10_pos,last10_neg, stat = 'mean')
    # plt.savefig(f"/work/mh0033/m300883/High_frequecy_flow/docs/plots/extremes_statistics/mean_distribution_{plev}.png")

    # increase_bys_pos[plev] = increase_by_percentage(first10_pos, last10_pos)
    # increase_bys_neg[plev] = increase_by_percentage(first10_neg, last10_neg)

    first10_pos_extremes = first10_pos[first10_pos["note"] == "above_7"][
        ["mean", "count"]
    ]
    first10_pos_extremes["plev"] = int(plev / 100)
    first10_pos_extremes["period"] = "first10"

    last10_pos_extremes = last10_pos[last10_pos["note"] == "above_7"][["mean", "count"]]
    last10_pos_extremes["plev"] = int(plev / 100)
    last10_pos_extremes["period"] = "last10"

    pos_extrems.append(first10_pos_extremes)
    pos_extrems.append(last10_pos_extremes)

    first10_neg_extremes = first10_neg[first10_neg["note"] == "above_7"][
        ["mean", "count"]
    ]
    first10_neg_extremes["plev"] = int(plev / 100)
    first10_neg_extremes["period"] = "first10"

    last10_neg_extremes = last10_neg[last10_neg["note"] == "above_7"][["mean", "count"]]
    last10_neg_extremes["plev"] = int(plev / 100)
    last10_neg_extremes["period"] = "last10"

    neg_extrems.append(first10_neg_extremes)
    neg_extrems.append(last10_neg_extremes)

pos_extrems = pd.concat(pos_extrems)
neg_extrems = pd.concat(neg_extrems)

# %%
fig, ax = plt.subplots(figsize=(15, 8))
# pos as positive side of y-axis
sns.barplot(
    data=pos_extrems,
    y="plev",
    x="count",
    hue="period",
    orient="h",
    ax=ax,
    hue_order=["first10", "last10"],
)

# neg as negative side of y-axis
_neg_extremes = neg_extrems.copy()
_neg_extremes["count"] = -_neg_extremes["count"]
sns.barplot(
    data=_neg_extremes,
    y="plev",
    x="count",
    hue="period",
    hue_order=["first10", "last10"],
    orient="h",
    ax=ax,
    alpha=0.5,
)
ax.set_ylabel("Pressure Level (hPa)")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/extremes_statistics/count_distribution_all.pdf"
)
# %%
# plot for mean
fig, ax = plt.subplots(figsize=(15, 8))
# pos as positive side of y-axis
sns.barplot(
    data=pos_extrems,
    y="plev",
    x="mean",
    hue="period",
    orient="h",
    ax=ax,
    hue_order=["first10", "last10"],
)

# neg as negative side of y-axis
sns.barplot(
    data=neg_extrems,
    y="plev",
    x="mean",
    hue="period",
    hue_order=["first10", "last10"],
    orient="h",
    ax=ax,
    alpha=0.5,
)
ax.set_ylabel("Pressure Level (hPa)")
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/extremes_statistics/mean_distribution_all.pdf"
)
# %%
