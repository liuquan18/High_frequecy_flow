# %%
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from src.extremes.extreme_statistics import sel_event_above_duration

#%%
from matplotlib.patches import Patch
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

def concurrent_events(events, events_container, base_plev = 25000, cross_plev = 1):
    """
    parameters:
        events: events dataframe
        events_container: a zero container for count of concurrent events
        base_plev: the plev to set referent time
        cross_plev: how many plevs must cross
    """
    for base_event in events[events["plev"] == base_plev].itertuples():
        ref_time = base_event.end_time

        count_startime = ref_time - pd.Timedelta(days=30)
        count_endtime = ref_time + pd.Timedelta(days=30)

        # select the rows where the time between "start_time" and "end_time" has an overlap with the time between "count_startime" and "count_endtime"
        overlapped_events = events[
            (events.start_time <= count_endtime)
            & (events.end_time >= count_startime)
        ]

        # if there is no overlap with events in other plevs, continue
        if len(overlapped_events.plev.unique()) <= cross_plev:
            continue

        # loop over all the events in the overlapped_events and update the count in container
        for event in overlapped_events.itertuples():
            event_startday = np.max([(event.start_time - ref_time).days, -30])
            event_endday = np.min([(event.end_time - ref_time).days, 30])
            events_container.loc[event.plev, event_startday:event_endday] += 1


# %%
first10_pos_events_container = pd.DataFrame(
    columns=list(range(-30, 31)),
    index=[25000, 50000, 70000, 85000, 100000],
    data=0,
)

last10_pos_events_container = pd.DataFrame(
    columns=list(range(-30, 31)),
    index=[25000, 50000, 70000, 85000, 100000],
    data=0,
)

#%%
first10_neg_events_container = pd.DataFrame(
    columns=list(range(-30, 31)),
    index=[25000, 50000, 70000, 85000, 100000],
    data=0,
)

last10_neg_events_container = pd.DataFrame(
    columns=list(range(-30, 31)),
    index=[25000, 50000, 70000, 85000, 100000],
    data=0,
)

# %%
# first10

for ens in range(1, 51):
    pos_extreme, neg_extreme = read_extremes("first10", 8, ens)
    concurrent_events(pos_extreme, first10_pos_events_container, cross_plev=3)
    concurrent_events(neg_extreme, first10_neg_events_container, cross_plev=3)
# %%
for ens in range(1, 51):
    pos_extreme, neg_extreme = read_extremes("last10", 8, ens)
    concurrent_events(pos_extreme, last10_pos_events_container, cross_plev=3)
    concurrent_events(neg_extreme, last10_neg_events_container, cross_plev=3)
                     
# %%
def plot_concurrent_bar(first10_df, last10_df, ax, vmin = 15, vmax = 85):

    # Define color maps
    # Custom normalization class
    blue_cmap = plt.cm.Blues
    orange_cmap = plt.cm.Oranges

    # set the color as 'none' between [0-0.2]
    # Define a function to map values to colors
    def value_to_color(value, cmap, vmin = 15, vmax = 85):
        if value < vmin:
            return 'none'
        elif value > vmax:
            return cmap(1.0)
        else:
            return cmap(value  / (vmax-vmin))

    # Get the pressure levels and lag days
    pressure_levels = first10_df.index
    lag_days = first10_df.columns

    # Plot the data
    for i, level in enumerate(pressure_levels):
        for j, lag in enumerate(lag_days):
            # Plot first10 years data (upper bar)
                    # Plot first10 years data (upper bar)
            first10_value = first10_df.loc[level, lag]
            first10_color = value_to_color(first10_value, blue_cmap, vmin, vmax)

            ax.bar(j, 0.4, bottom=i+0.3, width=1.,
                    color=first10_color, edgecolor='grey', linewidth=0.3)           
             
            # Plot last10 years data (lower bar)
            last10_value = last10_df.loc[level, lag]
            last10_color = value_to_color(last10_value, orange_cmap, vmin, vmax)
            ax.bar(j, 0.4, bottom=i-0.1, width=1., 
                color=last10_color, edgecolor='grey', linewidth=0.3)

            
            # Add text annotations
            if j in range(11, 40, 1):
                ax.text(j, i+0.5, str(first10_df.loc[level, lag]), ha='center', va='center', fontsize=8)
                ax.text(j, i+0.1, str(last10_df.loc[level, lag]), ha='center', va='center', fontsize=8)

    # Customize the plot
    ax.set_ylabel("Pressure Levels / hPa")

    # Set tick labels
    ax.set_xticks(range(len(lag_days)))
    ax.set_xticklabels(lag_days, rotation=45, ha='right')
    ax.set_yticks(np.arange(len(pressure_levels))+0.3)
    ax.set_yticklabels((pressure_levels.values/100).astype(int))
    ax.set_xlim(10,40)
    # reverse the y-axis
    ax.invert_yaxis()


#%%
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(10, 10))
plot_concurrent_bar(first10_pos_events_container, last10_pos_events_container, ax1, vmin = 10, vmax = 50)
plot_concurrent_bar(first10_neg_events_container, last10_neg_events_container, ax2, vmin = 10, vmax = 50)

# Add a legend
legend_elements = [Patch(facecolor=plt.cm.Blues(0.7), edgecolor='white', label='First 10 Years'),
                Patch(facecolor=plt.cm.Oranges(0.7), edgecolor='white', label='Last 10 Years')]
plt.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/extremes_statistics/events_evolution_cross_plev.pdf")


# %%
