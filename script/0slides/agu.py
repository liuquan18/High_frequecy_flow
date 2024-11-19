# %%
import pandas as pd
import numpy as np
import seaborn as sns
import xarray as xr
from src.extremes.extreme_read import read_extremes_allens
import matplotlib.pyplot as plt
from src.jet_stream.jet_speed_and_location import jet_stream_anomaly, jet_event
from src.jet_stream.jet_stream_plotting import plot_uhat

from src.composite.composite_NAO_WB import smooth, NAO_WB
from src.plotting.util import erase_white_line
import cartopy.crs as ccrs




# %%
#### extreme count
def combine_events(df, duration=13):
    """
    combine the events which durates more than 13 days
    """
    # Step 1: Split the dataframe
    df_up_to_13 = df[df.index <= duration]
    df_above_13 = df[df.index > duration]

    # Step 2: Sum the "extreme_duration" for rows > 13
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
    first10_pos = first10_pos_extremes.groupby("extreme_duration")["mean"].agg(
        ["mean", "count"]
    )
    first10_neg = first10_neg_extremes.groupby("extreme_duration")["mean"].agg(
        ["mean", "count"]
    )

    last10_pos = last10_pos_extremes.groupby("extreme_duration")["mean"].agg(
        ["mean", "count"]
    )
    last10_neg = last10_neg_extremes.groupby("extreme_duration")["mean"].agg(
        ["mean", "count"]
    )

    first10_pos = combine_events(first10_pos, duration=duration_lim)
    first10_neg = combine_events(first10_neg, duration=duration_lim)
    last10_pos = combine_events(last10_pos, duration=duration_lim)
    last10_neg = combine_events(last10_neg, duration=duration_lim)
    return first10_pos, first10_neg, last10_pos, last10_neg



# %%
increase_bys_pos = {}
increase_bys_neg = {}
pos_extrems = []
neg_extrems = []

for plev in [100000, 85000, 70000, 50000, 25000]:
    first10_pos, first10_neg, last10_pos, last10_neg = extreme_stat_allens(
        start_duration=5, duration_lim=7, plev=plev
    )

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
pos_extrems = pos_extrems.sort_values(by="period", ascending=True)
neg_extrems = neg_extrems.sort_values(by="period", ascending=True)

#%%


# %%
##### jet stream
def read_anomaly(period, same_clim=True, eddy=True):

    # anomaly
    ano_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/loc_anomaly/"
    clima_label = "sameclima" if same_clim else "diffclima"
    eddy_label = "eddy" if eddy else "noneddy"

    ano_path = f"{ano_dir}jet_stream_anomaly_{eddy_label}_{clima_label}_{period}.nc"

    loc_ano = xr.open_dataset(ano_path).lat_ano

    return loc_ano



same_clim = False
eddy = True

first10_ano = read_anomaly("first10", same_clim=same_clim, eddy=eddy)
last10_ano = read_anomaly("last10", same_clim=same_clim, eddy=eddy)


first10_pos_events, first10_neg_events = read_extremes_allens("first10", 8)
last10_pos_events, last10_neg_events = read_extremes_allens("last10", 8)


# select 250 hPa only
first10_pos_events = first10_pos_events[first10_pos_events["plev"] == 25000]
first10_neg_events = first10_neg_events[first10_neg_events["plev"] == 25000]

last10_pos_events = last10_pos_events[last10_pos_events["plev"] == 25000]
last10_neg_events = last10_neg_events[last10_neg_events["plev"] == 25000]


jet_loc_first10_pos = jet_event(first10_ano, first10_pos_events)
jet_loc_first10_neg = jet_event(first10_ano, first10_neg_events)

jet_loc_last10_pos = jet_event(last10_ano, last10_pos_events)
jet_loc_last10_neg = jet_event(last10_ano, last10_neg_events)


#%%%% wave breaking
first_NAO_pos_AWB, first_NAO_neg_AWB, first_NAO_pos_CWB, first_NAO_neg_CWB = NAO_WB('first10')
last_NAO_pos_AWB, last_NAO_neg_AWB, last_NAO_pos_CWB, last_NAO_neg_CWB = NAO_WB('last10')
# %%

# %%
cm = 1/2.54  # centimeters in inches
fig = plt.figure(figsize=(36*cm, 60*cm))
# adjust hratio
plt.subplots_adjust(hspace=2*cm, wspace=2*cm)
gs = fig.add_gridspec(3, 2, height_ratios=[0.6, 0.6, 0.8])

# Set the default font size
plt.rcParams.update({
    'font.size': 20,
    'xtick.labelsize': 20,
    'ytick.labelsize': 20,
    'axes.labelsize': 25,
    'axes.titlesize': 25
})

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
hist_ax2.set_ylabel('')

for ax in [hist_ax2, hist_ax3]:
    ax.axvline(x=0, color="k", linestyle="--", linewidth=2)
    ax.set_xlabel(r"Jet loc anomaly relative to climatology ($\degree$)", fontsize = 20)

line_ax1 = fig.add_subplot(gs[2, 0])
line_ax2 = fig.add_subplot(gs[2, 1])

first_NAO_pos_AWB.plot(ax=line_ax2, alpha=0.5, color='k', linewidth=2, label='first10')
last_NAO_pos_AWB.plot(ax=line_ax2, alpha=0.5, color='r', linewidth=2, label='last10')

first_NAO_neg_CWB.plot(ax=line_ax1, alpha=0.5, color='k',linewidth=2, label='first10')
last_NAO_neg_CWB.plot(ax=line_ax1, alpha=0.5, color='r', linewidth=2, label='last10')

smooth(first_NAO_pos_AWB).plot(ax=line_ax2, color='k', linewidth=4, label='first10 5day-mean')
smooth(last_NAO_pos_AWB).plot(ax=line_ax2, color='r', linewidth=4, label='last10 5day-mean')

smooth(first_NAO_neg_CWB).plot(ax=line_ax1, color='k', linewidth=4, label='first10 5day-mean')
smooth(last_NAO_neg_CWB).plot(ax=line_ax1, color='r', linewidth=4, label='last10 5day-mean')



line_ax2.set_xlim(-21, 21)
line_ax1.set_xlim(-21, 21)

line_ax2.set_ylim(10, 33)
line_ax1.set_ylim(0, 10)

line_ax2.set_ylabel("WB occurrence", fontsize=14)
line_ax2.set_ylabel("")
line_ax1.set_xlabel("days relative to onset of NAO extremes", fontsize=20)
line_ax2.set_xlabel("days relative to onset of NAO extremes", fontsize=20)

line_ax1.legend(frameon = False, loc = 'upper right')
line_ax1.set_ylabel('WB occurrence')
plt.tight_layout()

# no line at the top and right of the plot
for ax in [ax1, hist_ax2, hist_ax3, line_ax1, line_ax2]:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


# save as pdf without background
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/slides/agu/agu.pdf", dpi=500, transparent=True)
# %%

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
plt.rcParams.update({
    'font.size': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'axes.labelsize': 12,
    'axes.titlesize': 12
})

f, axes = plt.subplots(4,1, figsize=(17*cm, 14*cm),subplot_kw=dict(projection=ccrs.PlateCarree(-70)))
erase_white_line(first_NAO_pos_AWB).plot.contourf(
    ax=axes[0], transform=ccrs.PlateCarree(), levels=np.arange(10, 50, 5), extend="max", 
    cbar_kwargs={'label': 'count', 'ticks': np.arange(10, 50, 10), 'format': '%.0f', 'shrink': 0.8, 'pad': 0.05}
)

erase_white_line(last_NAO_pos_AWB).plot.contourf(
    ax=axes[1], transform=ccrs.PlateCarree(), levels=np.arange(10, 50, 5), extend="max", 
    cbar_kwargs={'ticks': np.arange(10, 50, 10), 'format': '%.0f', 'shrink': 0.8, 'pad': 0.05, 'label': 'count'}
)

erase_white_line(first_NAO_neg_CWB).plot.contourf(
    ax=axes[2], transform=ccrs.PlateCarree(), levels=np.arange(2, 10, 1), extend="max", 
    cbar_kwargs={'ticks': np.arange(2, 10, 2), 'format': '%.0f', 'shrink': 0.8, 'pad': 0.05, 'label': 'count'}
)

erase_white_line(last_NAO_neg_CWB).plot.contourf(
    ax=axes[3], transform=ccrs.PlateCarree(), levels=np.arange(2, 10, 1), extend="max", 
    cbar_kwargs={'ticks': np.arange(2, 10, 2), 'format': '%.0f', 'shrink': 0.8, 'pad': 0.05, 'label': 'count'}
)

for ax in axes:
    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.coastlines()

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/slides/agu/wb_spatial.pdf", dpi=500, transparent=True)

# %%
