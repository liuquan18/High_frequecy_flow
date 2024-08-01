# %%
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from src.extremes.extreme_read import read_extremes_allens
from src.extremes.extreme_plots import plot_stacked_events
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
plot_stacked_events(
    first10_pos_events_container, last10_pos_events_container, ax1, vmin=5, vmax=20
)
plot_stacked_events(
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
