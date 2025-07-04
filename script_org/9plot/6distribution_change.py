# %%
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
# %%
# read NAO extremes

pos_first = read_NAO_extremes_troposphere(1850, "pos", dur_threshold=7)
neg_first = read_NAO_extremes_troposphere(1850, "neg", dur_threshold=7)

pos_last = read_NAO_extremes_troposphere(2090, "pos", dur_threshold=7)
neg_last = read_NAO_extremes_troposphere(2090, "neg", dur_threshold=7)
# %%
pos_days_first = pos_first.groupby("plev")["extreme_duration"].sum().reset_index()
neg_days_first = neg_first.groupby("plev")["extreme_duration"].sum().reset_index()
pos_days_last = pos_last.groupby("plev")["extreme_duration"].sum().reset_index()
neg_days_last = neg_last.groupby("plev")["extreme_duration"].sum().reset_index()

# %%
pos_days_first["extreme_duration"] = pos_days_first["extreme_duration"] / 50
neg_days_first["extreme_duration"] = neg_days_first["extreme_duration"] / 50

pos_days_last["extreme_duration"] = pos_days_last["extreme_duration"] / 50
neg_days_last["extreme_duration"] = neg_days_last["extreme_duration"] / 50
# %%
# read jet stream location extremes

jet_loc_first10_pos = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_distribution/jet_loc_first10_pos.csv"
)["jet_loc"]
jet_loc_first10_neg = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_distribution/jet_loc_first10_neg.csv"
)["jet_loc"]
jet_loc_last10_pos = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_distribution/jet_loc_last10_pos.csv"
)["jet_loc"]
jet_loc_last10_neg = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_distribution/jet_loc_last10_neg.csv"
)["jet_loc"]

# %%
awb_pos_first = read_comp_var(
    "wb_anticyclonic",
    "pos",
    1850,
    name="flag",
    time_window=wb_time_window,
    method="no_stat",
    comp_path="0composite_distribution",
)

cwb_neg_first = read_comp_var(
    "wb_cyclonic",
    "neg",
    1850,
    name="flag",
    time_window=wb_time_window,
    method="no_stat",
    comp_path="0composite_distribution",
)

awb_pos_last = read_comp_var(
    "wb_anticyclonic",
    "pos",
    2090,
    name="flag",
    time_window=wb_time_window,
    method="no_stat",
    comp_path="0composite_distribution",
)
cwb_neg_last = read_comp_var(
    "wb_cyclonic",
    "neg",
    2090,
    name="flag",
    time_window=wb_time_window,
    method="no_stat",
    comp_path="0composite_distribution",
)

# %%
# AWB 40-60N, -10, 10 E
awb_pos_NAL_first = (
    awb_pos_first.sel(lat=slice(30, 50), lon=slice(340, 360))
    .mean(dim=("lat", "lon"))
    .sum(dim="ens")
)
awb_pos_NAL_last = (
    awb_pos_last.sel(lat=slice(30, 50), lon=slice(340, 360))
    .mean(dim=("lat", "lon"))
    .sum(dim="ens")
)

# %%
cwb_neg_NAL_first = (
    cwb_neg_first.sel(lat=slice(50, 70), lon=slice(290, 310))
    .mean(dim=("lat", "lon"))
    .sum(dim="ens")
)
cwb_neg_NAL_last = (
    cwb_neg_last.sel(lat=slice(50, 70), lon=slice(290, 310))
    .mean(dim=("lat", "lon"))
    .sum(dim="ens")
)


# %%
first_NAO_pos_AWB = awb_pos_NAL_first
last_NAO_pos_AWB = awb_pos_NAL_last

first_NAO_neg_CWB = cwb_neg_NAL_first
last_NAO_neg_CWB = cwb_neg_NAL_last

# %%
# Merge the two dataframes and reshape for 'period' column
pos_extrems = pd.concat(
    [
        pos_days_first.assign(period="first10"),
        pos_days_last.assign(period="last10"),
    ],
    axis=0,
    ignore_index=True,
)
neg_extrems = pd.concat(
    [
        neg_days_first.assign(period="first10"),
        neg_days_last.assign(period="last10"),
    ],
    axis=0,
    ignore_index=True,
)

# reanem "extreme_duration" to "count"
pos_extrems.rename(columns={"extreme_duration": "count"}, inplace=True)
neg_extrems.rename(columns={"extreme_duration": "count"}, inplace=True)

# 'plev' to int and divided by 100
pos_extrems["plev"] = (pos_extrems["plev"] / 100).astype(int)
neg_extrems["plev"] = (neg_extrems["plev"] / 100).astype(int)

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


# %%
cm = 1 / 2.54  # centimeters in inches
fig = plt.figure(figsize=(36 * cm, 60 * cm))
# adjust hratio
plt.subplots_adjust(hspace=2 * cm, wspace=2 * cm)
gs = fig.add_gridspec(3, 2, height_ratios=[0.6, 0.6, 0.8])

# Set the default font size
plt.rcParams.update(
    {
        "font.size": 20,
        "xtick.labelsize": 20,
        "ytick.labelsize": 20,
        "axes.labelsize": 25,
        "axes.titlesize": 25,
    }
)

ax1 = fig.add_subplot(gs[0, :])

# neg as negative side of y-axis
_neg_extremes = neg_extrems.copy()
_neg_extremes["count"] = -_neg_extremes["count"]
sns.barplot(
    data=_neg_extremes,
    y="plev",
    x="count",
    hue="period",
    hue_order=["last10", "first10"],
    palette=["C1", "C0"],
    orient="h",
    ax=ax1,
    legend=False,
    alpha=0.5,
)
ax1.set_ylabel("Pressure Level (hPa)")

# pos as positive side of y-axis
sns.barplot(
    data=pos_extrems,
    y="plev",
    x="count",
    hue="period",
    orient="h",
    ax=ax1,
    hue_order=["last10", "first10"],
    palette=["C1", "C0"],
)

# Set x=0 in the middle
max_count = max(pos_extrems["count"].max(), -_neg_extremes["count"].min())
ax1.set_xlim(-max_count, max_count)

hist_ax2 = fig.add_subplot(gs[1, 1])
sns.histplot(
    jet_loc_first10_pos,
    label="first10_pos",
    color="k",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=hist_ax2,
)

sns.histplot(
    jet_loc_last10_pos,
    label="last10_pos",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=hist_ax2,
)

hist_ax3 = fig.add_subplot(gs[1, 0])
sns.histplot(
    jet_loc_first10_neg,
    label="first10",
    color="k",
    bins=np.arange(-30, 31, 2),  # Note: (20, 21, 1) would give better visualisation
    stat="count",
    ax=hist_ax3,
)

sns.histplot(
    jet_loc_last10_neg,
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=hist_ax3,
)

hist_ax3.legend()
hist_ax3.set_ylabel("eddy-driven jet stream count")
hist_ax2.set_ylabel("")

for ax in [hist_ax2, hist_ax3]:
    ax.axvline(x=0, color="k", linestyle="--", linewidth=2)
    ax.set_xlabel(r"Jet loc anomaly relative to climatology ($\degree$)", fontsize=20)

line_ax1 = fig.add_subplot(gs[2, 0])
line_ax2 = fig.add_subplot(gs[2, 1])

first_NAO_pos_AWB.plot(ax=line_ax2, alpha=0.5, color="k", linewidth=2, label="first10")
last_NAO_pos_AWB.plot(ax=line_ax2, alpha=0.5, color="r", linewidth=2, label="last10")

first_NAO_neg_CWB.plot(ax=line_ax1, alpha=0.5, color="k", linewidth=2, label="first10")
last_NAO_neg_CWB.plot(ax=line_ax1, alpha=0.5, color="r", linewidth=2, label="last10")

smooth(first_NAO_pos_AWB).plot(
    ax=line_ax2, color="k", linewidth=4, label="first10 5day-mean"
)
smooth(last_NAO_pos_AWB).plot(
    ax=line_ax2, color="r", linewidth=4, label="last10 5day-mean"
)

smooth(first_NAO_neg_CWB).plot(
    ax=line_ax1, color="k", linewidth=4, label="first10 5day-mean"
)
smooth(last_NAO_neg_CWB).plot(
    ax=line_ax1, color="r", linewidth=4, label="last10 5day-mean"
)


line_ax2.set_xlim(-20, 10)
line_ax1.set_xlim(-20, 10)

# line_ax2.set_ylim(0, 3)
# line_ax1.set_ylim(0, 3)

line_ax2.set_ylabel("WB occurrence", fontsize=14)
line_ax2.set_ylabel("")
line_ax1.set_xlabel("days relative to onset of NAO extremes", fontsize=20)
line_ax2.set_xlabel("days relative to onset of NAO extremes", fontsize=20)

line_ax1.legend(frameon=False, loc="upper left")
line_ax1.set_ylabel("WB occurrence")
plt.tight_layout()

# no line at the top and right of the plot
for ax in [ax1, hist_ax2, hist_ax3, line_ax1, line_ax2]:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# save as pdf without background
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0distribution_change/NAO_distribution_change.pdf",
    dpi=500,
    transparent=True,
)
# %%
cm = 1 / 2.54  # centimeters in inches
fig = plt.figure(figsize=(36 * cm, 30 * cm))
# adjust hratio
plt.subplots_adjust(hspace=2 * cm, wspace=2 * cm)
gs = fig.add_gridspec(3, 2, height_ratios=[0.6, 0.6, 0.8])

# Set the default font size
plt.rcParams.update(
    {
        "font.size": 20,
        "xtick.labelsize": 20,
        "ytick.labelsize": 20,
        "axes.labelsize": 25,
        "axes.titlesize": 25,
    }
)

ax1 = fig.add_subplot(gs[0, :])

# neg as negative side of y-axis
_neg_extremes = neg_extrems.copy()
_neg_extremes["count"] = -_neg_extremes["count"]
sns.barplot(
    data=_neg_extremes,
    y="plev",
    x="count",
    hue="period",
    hue_order=["last10", "first10"],
    palette=["C1", "C0"],
    orient="h",
    ax=ax1,
    legend=False,
    alpha=0.5,
)
ax1.set_ylabel("Pressure Level (hPa)")
# ytick labels to int and divided by 1000



# pos as positive side of y-axis
sns.barplot(
    data=pos_extrems,
    y="plev",
    x="count",
    hue="period",
    orient="h",
    ax=ax1,
    hue_order=["last10", "first10"],
    palette=["C1", "C0"],
)

# Set x=0 in the middle
max_count = max(pos_extrems["count"].max(), -_neg_extremes["count"].min())
ax1.set_xlim(-max_count, max_count)

# distribution of the transient eddy heat flux
hist_ax2 = fig.add_subplot(gs[1, 1])

sns.histplot(
    vpetp_pos_first.to_dataframe()["vpetp"],
    label="first10_pos",
    color="black",
    bins=np.arange(-20, 20.1, 0.5),
    stat="count",
    ax=hist_ax2,
    alpha=0.5,
)
sns.histplot(
    vpetp_pos_last.to_dataframe()["vpetp"],
    label="last10_pos",
    color="red",
    bins=np.arange(-20, 20.1, 0.5),
    stat="count",
    alpha=0.5,
    ax=hist_ax2,
)
hist_ax2.set_xlabel("Transient eddy heat flux anomaly (K m/s)", fontsize=20)
hist_ax2.set_ylabel("count", fontsize=20)


# negative side
hist_ax3 = fig.add_subplot(gs[1, 0])
sns.histplot(
    vpetp_neg_first.to_dataframe()["vpetp"],
    label="first10",
    color="black",
    bins=np.arange(-20, 20.1, 0.5),
    stat="count",
    ax=hist_ax3,
    alpha=0.5,
)
sns.histplot(
    vpetp_neg_last.to_dataframe()["vpetp"],
    label="last10",
    color="red",
    bins=np.arange(-20, 20.1, 0.5),
    stat="count",
    alpha=0.5,
    ax=hist_ax3,
)
hist_ax3.set_xlabel("Transient eddy heat flux anomaly (K m/s)", fontsize=20)


hist_ax3.legend()
hist_ax2.set_ylabel("")

# distribution of the steady eddy heat flux
hist_ax4 = fig.add_subplot(gs[2, 1])
sns.histplot(
    vsets_pos_first.to_dataframe()["vsets"],
    label="first10_pos",
    color="black",
    bins=np.arange(-20, 20.1, 0.5),
    stat="count",
    ax=hist_ax4,
    alpha=0.5,
)
sns.histplot(
    vsets_pos_last.to_dataframe()["vsets"],
    label="last10_pos",
    color="red",
    bins=np.arange(-20, 20.1, 0.5),
    stat="count",
    alpha=0.5,
    ax=hist_ax4,
)
hist_ax4.set_xlabel("Steady eddy heat flux anomaly (K m/s)", fontsize=20)


hist_ax5 = fig.add_subplot(gs[2, 0])
sns.histplot(
    vsets_neg_first.to_dataframe()["vsets"],
    label="first10",
    color="black",
    bins=np.arange(-20, 20.1, 0.5),
    stat="count",
    ax=hist_ax5,
    alpha=0.5,
)
sns.histplot(
    vsets_neg_last.to_dataframe()["vsets"],
    label="last10",
    color="red",
    bins=np.arange(-20, 20.1, 0.5),
    stat="count",
    alpha=0.5,
    ax=hist_ax5,
)
hist_ax5.set_xlabel("Steady eddy heat flux anomaly (K m/s)", fontsize=20)
hist_ax5.legend()


# no line at the top and right of the plot
for ax in [ax1, hist_ax2, hist_ax3, hist_ax4, hist_ax5]:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

for ax in [hist_ax2, hist_ax3, hist_ax4, hist_ax5]:
    ax.axvline(x=0, color="k", linestyle="--", linewidth=2)

plt.tight_layout()

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0distribution_change/NAO_distribution_change_heat_flux.pdf",
    dpi=500,
    transparent=True,
)


# %%
# Count the occurrence of positive vpetp values for pos_first
vpetp_pos_first_poscount =vpetp_pos_first.groupby("time").apply(
    lambda x: (x > 0).sum()
)

vpetp_pos_last_poscount = vpetp_pos_last.groupby("time").apply(
    lambda x: (x > 0).sum()
)
#%%
vpetp_neg_first_negcount = vpetp_neg_first.groupby("time").apply(
    lambda x: (x < 0).sum()
)
vpetp_neg_last_negcount = vpetp_neg_last.groupby("time").apply(
    lambda x: (x < 0).sum()
)
#%%
vsets_neg_first_poscount = vsets_neg_first.groupby("time").apply(
    lambda x: (x > 0).sum()
)
vsets_neg_last_poscount = vsets_neg_last.groupby("time").apply(
    lambda x: (x > 0).sum()
)

#%%
vsets_pos_first_negcount = vsets_pos_first.groupby("time").apply(
    lambda x: (x < 0).sum()
)
vsets_pos_last_negcount = vsets_pos_last.groupby("time").apply(
    lambda x: (x < 0).sum()
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
)
ax[0].set_xlabel("")
ax[0].set_ylabel(r"eddy heat flux anomaly (K $m s^{-1}$)", fontsize=20)
ax[1].set_xlabel("")

# vline at x=0
ax[0].axvline(x=0, color="k", linestyle="dotted", linewidth=1)
ax[1].axvline(x=0, color="k", linestyle="dotted", linewidth=1)
fig.supxlabel("days relative to extreme NAO onset", fontsize=20)

plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0distribution_change/eddy_heat_flux_timewindow_last.pdf",
    dpi = 500,
    transparent=True,
)


#%%

cm = 1 / 2.54  # centimeters in inches
fig = plt.figure(figsize=(36 * cm, 60 * cm))
# adjust hratio
plt.subplots_adjust(hspace=2 * cm, wspace=2 * cm)
gs = fig.add_gridspec(3, 2, height_ratios=[0.6, 0.6, 0.8])

# Set the default font size
plt.rcParams.update(
    {
        "font.size": 20,
        "xtick.labelsize": 20,
        "ytick.labelsize": 20,
        "axes.labelsize": 25,
        "axes.titlesize": 25,
    }
)

ax1 = fig.add_subplot(gs[0, :])

# neg as negative side of y-axis
_neg_extremes = neg_extrems.copy()
_neg_extremes["count"] = -_neg_extremes["count"]
sns.barplot(
    data=_neg_extremes,
    y="plev",
    x="count",
    hue="period",
    hue_order=["last10", "first10"],
    palette=["C1", "C0"],
    orient="h",
    ax=ax1,
    legend=False,
    alpha=0.5,
)
ax1.set_ylabel("Pressure Level (hPa)")

# pos as positive side of y-axis
sns.barplot(
    data=pos_extrems,
    y="plev",
    x="count",
    hue="period",
    orient="h",
    ax=ax1,
    hue_order=["last10", "first10"],
    palette=["C1", "C0"],
)

# Set x=0 in the middle
max_count = max(pos_extrems["count"].max(), -_neg_extremes["count"].min())
ax1.set_xlim(-max_count, max_count)

hist_ax2 = fig.add_subplot(gs[1, 1])
sns.histplot(
    jet_loc_first10_pos,
    label="first10_pos",
    color="k",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=hist_ax2,
)

sns.histplot(
    jet_loc_last10_pos,
    label="last10_pos",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=hist_ax2,
)

hist_ax3 = fig.add_subplot(gs[1, 0])
sns.histplot(
    jet_loc_first10_neg,
    label="first10",
    color="k",
    bins=np.arange(-30, 31, 2),  # Note: (20, 21, 1) would give better visualisation
    stat="count",
    ax=hist_ax3,
)

sns.histplot(
    jet_loc_last10_neg,
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=hist_ax3,
)

hist_ax3.legend()
hist_ax3.set_ylabel("eddy-driven jet stream count")
hist_ax2.set_ylabel("")

for ax in [hist_ax2, hist_ax3]:
    ax.axvline(x=0, color="k", linestyle="--", linewidth=2)
    ax.set_xlabel(r"Jet loc anomaly relative to climatology ($\degree$)", fontsize=20)

line_ax1 = fig.add_subplot(gs[2, 0])
line_ax2 = fig.add_subplot(gs[2, 1])

first_NAO_pos_AWB.plot(ax=line_ax2, alpha=0.5, color="k", linewidth=2, label="first10")
last_NAO_pos_AWB.plot(ax=line_ax2, alpha=0.5, color="r", linewidth=2, label="last10")

first_NAO_neg_CWB.plot(ax=line_ax1, alpha=0.5, color="k", linewidth=2, label="first10")
last_NAO_neg_CWB.plot(ax=line_ax1, alpha=0.5, color="r", linewidth=2, label="last10")

smooth(first_NAO_pos_AWB).plot(
    ax=line_ax2, color="k", linewidth=4, label="first10 5day-mean"
)
smooth(last_NAO_pos_AWB).plot(
    ax=line_ax2, color="r", linewidth=4, label="last10 5day-mean"
)

smooth(first_NAO_neg_CWB).plot(
    ax=line_ax1, color="k", linewidth=4, label="first10 5day-mean"
)
smooth(last_NAO_neg_CWB).plot(
    ax=line_ax1, color="r", linewidth=4, label="last10 5day-mean"
)


line_ax2.set_xlim(-20, 10)
line_ax1.set_xlim(-20, 10)

# line_ax2.set_ylim(0, 3)
# line_ax1.set_ylim(0, 3)

line_ax2.set_ylabel("WB occurrence", fontsize=14)
line_ax2.set_ylabel("")
line_ax1.set_xlabel("days relative to onset of NAO extremes", fontsize=20)
line_ax2.set_xlabel("days relative to onset of NAO extremes", fontsize=20)

line_ax1.legend(frameon=False, loc="upper left")
line_ax1.set_ylabel("WB occurrence")
plt.tight_layout()

# no line at the top and right of the plot
for ax in [ax1, hist_ax2, hist_ax3, line_ax1, line_ax2]:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)






# %%
first_NAO_pos_AWB, first_NAO_neg_AWB, first_NAO_pos_CWB, first_NAO_neg_CWB = NAO_WB(
    "first10", fldmean=False
)
last_NAO_pos_AWB, last_NAO_neg_AWB, last_NAO_pos_CWB, last_NAO_neg_CWB = NAO_WB(
    "last10", fldmean=False
)

# %%
first_NAO_pos_AWB = first_NAO_pos_AWB.sel(time=slice(-5, 5)).mean(dim="time")
last_NAO_pos_AWB = last_NAO_pos_AWB.sel(time=slice(-5, 5)).mean(dim="time")

first_NAO_pos_CWB = first_NAO_pos_CWB.sel(time=slice(-5, 5)).mean(dim="time")
last_NAO_pos_CWB = last_NAO_pos_CWB.sel(time=slice(-5, 5)).mean(dim="time")

first_NAO_neg_AWB = first_NAO_neg_AWB.sel(time=slice(-5, 5)).mean(dim="time")
last_NAO_neg_AWB = last_NAO_neg_AWB.sel(time=slice(-5, 5)).mean(dim="time")

first_NAO_neg_CWB = first_NAO_neg_CWB.sel(time=slice(-5, 5)).mean(dim="time")
last_NAO_neg_CWB = last_NAO_neg_CWB.sel(time=slice(-5, 5)).mean(dim="time")
# %%
# Set the default font size
plt.rcParams.update(
    {
        "font.size": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "axes.labelsize": 12,
        "axes.titlesize": 12,
    }
)

f, axes = plt.subplots(
    4, 1, figsize=(17 * cm, 14 * cm), subplot_kw=dict(projection=ccrs.PlateCarree(-70))
)
erase_white_line(first_NAO_pos_AWB).plot.contourf(
    ax=axes[0],
    transform=ccrs.PlateCarree(),
    levels=np.arange(10, 50, 5),
    extend="max",
    cbar_kwargs={
        "label": "count",
        "ticks": np.arange(10, 50, 10),
        "format": "%.0f",
        "shrink": 0.8,
        "pad": 0.05,
    },
)

erase_white_line(last_NAO_pos_AWB).plot.contourf(
    ax=axes[1],
    transform=ccrs.PlateCarree(),
    levels=np.arange(10, 50, 5),
    extend="max",
    cbar_kwargs={
        "ticks": np.arange(10, 50, 10),
        "format": "%.0f",
        "shrink": 0.8,
        "pad": 0.05,
        "label": "count",
    },
)

erase_white_line(first_NAO_neg_CWB).plot.contourf(
    ax=axes[2],
    transform=ccrs.PlateCarree(),
    levels=np.arange(2, 10, 1),
    extend="max",
    cbar_kwargs={
        "ticks": np.arange(2, 10, 2),
        "format": "%.0f",
        "shrink": 0.8,
        "pad": 0.05,
        "label": "count",
    },
)

erase_white_line(last_NAO_neg_CWB).plot.contourf(
    ax=axes[3],
    transform=ccrs.PlateCarree(),
    levels=np.arange(2, 10, 1),
    extend="max",
    cbar_kwargs={
        "ticks": np.arange(2, 10, 2),
        "format": "%.0f",
        "shrink": 0.8,
        "pad": 0.05,
        "label": "count",
    },
)

for ax in axes:
    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.coastlines()

plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/slides/agu/wb_spatial.pdf",
    dpi=500,
    transparent=True,
)

# %%
