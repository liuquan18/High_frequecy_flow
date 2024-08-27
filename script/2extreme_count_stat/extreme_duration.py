#%%
import pandas as pd
import numpy as np
import seaborn as sns
from src.extremes.extreme_read import read_extremes_allens
from src.extremes.extreme_plots import plot_stacked_events
import matplotlib.pyplot as plt

from matplotlib.patches import Patch

# %%
first10_pos_events, first10_neg_events = read_extremes_allens("first10", 8)
last10_pos_events, last10_neg_events = read_extremes_allens("last10", 8)


# %%
def stack_events(events):
    container = pd.DataFrame(columns= np.arange(-30,31,1),
                              index = [100000,85000,70000,50000,25000],
                                data = 0)
    for idx, event in events.iterrows():
        container.loc[event["plev"], 0: event['extreme_duration']+1] += 1
    return container
# %%
first_10_pos_container = stack_events(first10_pos_events)
first_10_neg_container = stack_events(first10_neg_events)
last_10_pos_container = stack_events(last10_pos_events)
last_10_neg_container = stack_events(last10_neg_events)
# %%
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
plot_stacked_events(
    first_10_pos_container, last_10_pos_container, ax1, vmin=10, vmax=90
)
plot_stacked_events(
    first_10_neg_container, last_10_neg_container, ax2, vmin=10, vmax=90
)


# Add a legend
legend_elements = [
    Patch(facecolor=plt.cm.Blues(0.7), edgecolor="white", label="First 10 Years"),
    Patch(facecolor=plt.cm.Oranges(0.7), edgecolor="white", label="Last 10 Years"),
]
plt.legend(handles=legend_elements, loc="lower right")

plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/extremes_statistics/events_durations.png"
)
# %%
