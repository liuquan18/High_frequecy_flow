# %%
import pandas as pd
import numpy as np
import seaborn as sns
import xarray as xr
import matplotlib.pyplot as plt
from src.plotting.jet_stream_plotting import plot_uhat

from src.composite.composite_NAO_WB import smooth, NAO_WB
from src.plotting.util import erase_white_line
import cartopy.crs as ccrs
from src.data_helper.read_NAO_extremes import (
    read_NAO_extremes_troposphere,
)
from src.data_helper.read_composite import read_comp_var, read_comp_var_dist
from matplotlib.ticker import FuncFormatter


# %%
wb_time_window = (-20, 10)  # days relative to NAO onset

# %%%
# read heat flux
vpetp_neg_first = read_comp_var_dist(
    "vpetp",
    "neg",
    1850,
    time_window = wb_time_window,
)
vpetp_pos_first = read_comp_var_dist(
    "vpetp",
    "pos",
    1850,
    time_window = wb_time_window,
)
vpetp_neg_last = read_comp_var_dist(
    "vpetp",
    "neg",
    2090,
    time_window = wb_time_window,
)
vpetp_pos_last = read_comp_var_dist(
    "vpetp",
    "pos",
    2090,
    time_window = wb_time_window,
)

# %%
# vsets
vsets_pos_first = read_comp_var_dist(
    "vsets",
    "pos",
    1850,
    time_window = wb_time_window,
)
vsets_neg_first = read_comp_var_dist(
    "vsets",
    "neg",
    1850,
    time_window = wb_time_window,
)
vsets_pos_last = read_comp_var_dist(
    "vsets",
    "pos",
    2090,
    time_window = wb_time_window,
)
vsets_neg_last = read_comp_var_dist(
    "vsets",
    "neg",
    2090,
    time_window = wb_time_window,
)

#%%

vpetp_pos_first = vpetp_pos_first.to_dataframe().reset_index()
vpetp_pos_last = vpetp_pos_last.to_dataframe().reset_index()
vpetp_neg_first = vpetp_neg_first.to_dataframe().reset_index()
vpetp_neg_last = vpetp_neg_last.to_dataframe().reset_index()
vsets_pos_first = vsets_pos_first.to_dataframe().reset_index()
vsets_pos_last = vsets_pos_last.to_dataframe().reset_index()
vsets_neg_first = vsets_neg_first.to_dataframe().reset_index()
vsets_neg_last = vsets_neg_last.to_dataframe().reset_index()    

#%%
fig, ax = plt.subplots(1,2,figsize = (10, 8), sharex=True, sharey=True)


# Set font size for axis labels and tick labels
for axis in ax:
    axis.tick_params(axis='both', which='major', labelsize=14)
    axis.tick_params(axis='both', which='minor', labelsize=12)
    axis.xaxis.label.set_size(14)
    axis.yaxis.label.set_size(14)

# positive (was axes[1], now axes[0])
sns.lineplot(
    x = 'time',
    y = 'vpetp',
    data=vpetp_pos_first,
    color="black",
    ax=ax[0],
)
sns.lineplot(
    x = 'time',
    y = 'vsets',
    data=vsets_pos_first,
    color="black",
    ax=ax[0],
    linestyle="--",
)

sns.lineplot(
    x = 'time',
    y = 'vpetp',
    data=vpetp_pos_last,
    color="red",
    ax=ax[0],
)
sns.lineplot(
    x = 'time',
    y = 'vsets',
    data=vsets_pos_last,
    color="red",
    ax=ax[0],
    linestyle="--",
)

# transient eddy heat flux
sns.lineplot(
    x = 'time',
    y = 'vpetp',
    data=vpetp_neg_first,
    color="black",
    ax=ax[1],
)
## steady eddy heat flux
sns.lineplot(
    x = 'time',
    y = 'vsets',
    data=vsets_neg_first,
    color="black",
    ax=ax[1],
    linestyle="--",
)

## read as last
sns.lineplot(
    x = 'time',
    y = 'vpetp',
    data=vpetp_neg_last,
    color="red",
    ax=ax[1],
)
sns.lineplot(
    x = 'time',
    y = 'vsets',
    data=vsets_neg_last,
    color="red",
    ax=ax[1],
    linestyle="--",
)

# add customed legend, solid line for transient, dashed line for steady, black for first10, red for last10
handles = [
    plt.Line2D([0], [0], color="black", linestyle="-", label="transient"),  
    plt.Line2D([0], [0], color="black", linestyle="--", label="steady"),
    plt.Line2D([0], [0], color="black", linestyle="-", label="first10"),
    plt.Line2D([0], [0], color="red", linestyle="-", label="last10"),
]

ax[0].legend(
    handles=handles,
    loc="lower left",
    frameon=False,
    fontsize=14,
)
ax[0].set_xlabel("")
ax[0].set_ylabel(r"eddy heat flux anomaly (K $m s^{-1}$)", fontsize=14)
ax[1].set_xlabel("")

# vline at x=0
ax[0].axvline(x=0, color="k", linestyle="dotted", linewidth=1)
ax[1].axvline(x=0, color="k", linestyle="dotted", linewidth=1)
fig.supxlabel("days relative to extreme NAO onset", fontsize=16)

plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eddy_heat_flux_lineplot.pdf",
    dpi = 500,
    transparent=True,
)

# %%
