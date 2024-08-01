# %%
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from src.extremes.extreme_read import read_extremes_allens

# %%
from matplotlib.patches import Patch


# %%


def after_events(events, base_plev=25000, start_point="end_time", cross_plev=1):
    """
    parameters:
        events: events dataframe
        events_container: a zero container for count of concurrent events
        base_plev: the plev to set referent time
        start_point: the point to set referent time, start_time or end_time
        cross_plev: how many plevs must cross
    """
    events_container = pd.DataFrame(
        columns=list(range(-30, 31)),
        index=[25000, 50000, 70000, 85000, 100000],
        data=0,
    )

    ref_index = events[events["plev"] == base_plev].columns.get_loc(start_point)
    # loop over all the events in the base_plev

    for base_event in events[events["plev"] == base_plev].itertuples(index=False):
        ref_time = base_event[ref_index]

        # select the events that happens after the base_startime
        if start_point == "start_time":
            after_events = events[events[start_point] >= ref_time]
            concurrent_events = after_events
        else:
            before_events = events[events[start_point] <= ref_time]
            concurrent_events = before_events

        # if there is no overlap with events in other plevs, continue
        if len(concurrent_events.plev.unique()) <= cross_plev:
            continue

        # loop over all the events in the overlapped_events and update the count in container
        for event in concurrent_events.itertuples():
            event_startday = np.max([(event.start_time - ref_time).days, -30])
            event_endday = np.min([(event.end_time - ref_time).days +1, 30])
            events_container.loc[event.plev, event_startday:event_endday] += 1

    return events_container


# %%
def plot_concurrent_bar(first10_df, last10_df, ax, vmin=15, vmax=85):

    # Define color maps
    # Custom normalization class
    blue_cmap = plt.cm.Blues
    orange_cmap = plt.cm.Oranges

    # set the color as 'none' between [0-0.2]
    # Define a function to map values to colors
    def value_to_color(value, cmap, vmin=15, vmax=85):
        if value < vmin:
            return "none"
        elif value > vmax:
            return cmap(1.0)
        else:
            return cmap((value - vmin) / (vmax - vmin))

    # Get the pressure levels and lag days
    pressure_levels = first10_df.index
    lag_days = first10_df.columns

    # Plot the data
    for i, level in enumerate(pressure_levels):
        for j, lag in enumerate(lag_days):
            # Plot first10 years data (upper bar)
            # Plot first10 years data (upper bar)
            # Add text annotations
            if j in range(26, 50, 1):
                first10_value = first10_df.loc[level, lag]
                first10_color = value_to_color(first10_value, blue_cmap, vmin, vmax)

                ax.bar(
                    j,
                    0.4,
                    bottom=i + 0.3,
                    width=1.0,
                    color=first10_color,
                    edgecolor="grey",
                    linewidth=0.3,
                )

                # Plot last10 years data (lower bar)
                last10_value = last10_df.loc[level, lag]
                last10_color = value_to_color(last10_value, orange_cmap, vmin, vmax)
                ax.bar(
                    j,
                    0.4,
                    bottom=i - 0.1,
                    width=1.0,
                    color=last10_color,
                    edgecolor="grey",
                    linewidth=0.3,
                )

                ax.text(
                    j,
                    i + 0.5,
                    str(first10_df.loc[level, lag]),
                    ha="center",
                    va="center",
                    fontsize=8,
                )
                ax.text(
                    j,
                    i + 0.1,
                    str(last10_df.loc[level, lag]),
                    ha="center",
                    va="center",
                    fontsize=8,
                )

    # Customize the plot
    ax.set_ylabel("Pressure Levels / hPa")

    # Set tick labels
    ax.set_xticks(range(len(lag_days)))
    ax.set_xticklabels(lag_days, rotation=45, ha="right")
    ax.set_yticks(np.arange(len(pressure_levels)) + 0.3)
    ax.set_yticklabels((pressure_levels.values / 100).astype(int))
    ax.set_xlim(25, 50)
    # reverse the y-axis
    ax.invert_yaxis()

# %%
# first10
first10_pos_events, first10_neg_events = read_extremes_allens("first10", 8)
last10_pos_events, last10_neg_events = read_extremes_allens("last10", 8)

#%%
cross_plev = 4
# %%
first10_pos_events_container = first10_pos_events.groupby("ens")[
    ["plev", "start_time", "end_time", "duration"]
].apply(after_events, base_plev=100000, start_point="start_time", cross_plev=cross_plev)
first10_pos_events_container = first10_pos_events_container.groupby(level=1).sum()
# %%
first10_neg_events_container = first10_neg_events.groupby("ens")[
    ["plev", "start_time", "end_time", "duration"]
].apply(after_events, base_plev=100000, start_point="start_time", cross_plev=cross_plev)
first10_neg_events_container = first10_neg_events_container.groupby(level=1).sum()
# %%
last10_pos_events_container = last10_pos_events.groupby("ens")[
    ["plev", "start_time", "end_time", "duration"]
].apply(after_events, base_plev=100000, start_point="start_time", cross_plev=cross_plev)
last10_pos_events_container = last10_pos_events_container.groupby(level=1).sum()
# %%
last10_neg_events_container = last10_neg_events.groupby("ens")[
    ["plev", "start_time", "end_time", "duration"]
].apply(after_events, base_plev=100000, start_point="start_time", cross_plev=cross_plev)
last10_neg_events_container = last10_neg_events_container.groupby(level=1).sum()

# %%
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
plot_concurrent_bar(
    first10_pos_events_container, last10_pos_events_container, ax1, vmin=5, vmax=20
)
plot_concurrent_bar(
    first10_neg_events_container, last10_neg_events_container, ax2, vmin=5, vmax=20
)

# Add a legend
legend_elements = [
    Patch(facecolor=plt.cm.Blues(0.7), edgecolor="white", label="First 10 Years"),
    Patch(facecolor=plt.cm.Oranges(0.7), edgecolor="white", label="Last 10 Years"),
]
plt.legend(handles=legend_elements, loc="lower right")

plt.tight_layout()
plt.savefig(
    f"/work/mh0033/m300883/High_frequecy_flow/docs/plots/extremes_statistics/events_evolution_cross_plev{cross_plev}.pdf"
)


# %%
