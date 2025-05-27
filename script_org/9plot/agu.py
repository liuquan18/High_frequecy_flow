# %%
import pandas as pd
import numpy as np
import seaborn as sns
import xarray as xr
from src.extremes.extreme_read import read_extremes_allens
import matplotlib.pyplot as plt
from src.dynamics.jet_speed_and_location import jet_stream_anomaly, jet_event
from src.plotting.jet_stream_plotting import plot_uhat

from src.composite.composite_NAO_WB import smooth, NAO_WB
from src.plotting.util import erase_white_line
import cartopy.crs as ccrs

from src.data_helper.read_NAO_extremes import read_NAO_extremes_troposphere 
from src.data_helper.read_composite import read_comp_var
from cartopy.mpl.patch import geos_to_path
# %%

################ old jet, should be updated #############
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

# %%


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

####################################################
#%%
wb_time_window = (-15, 5)  # days relative to NAO onset
#%%
# read NAO extremes

pos_first = read_NAO_extremes_troposphere(1850, 'pos', dur_threshold=8)
neg_first = read_NAO_extremes_troposphere(1850, 'neg', dur_threshold=8)

pos_last = read_NAO_extremes_troposphere(2090, 'pos', dur_threshold=8)
neg_last = read_NAO_extremes_troposphere(2090, 'neg', dur_threshold=8)
#%%
pos_days_first = pos_first.groupby("plev")["extreme_duration"].sum().reset_index()
neg_days_first = neg_first.groupby("plev")["extreme_duration"].sum().reset_index()
pos_days_last = pos_last.groupby("plev")["extreme_duration"].sum().reset_index()
neg_days_last = neg_last.groupby("plev")["extreme_duration"].sum().reset_index()

#%%
pos_days_first['extreme_duration'] = pos_days_first['extreme_duration']/50
neg_days_first['extreme_duration'] = neg_days_first['extreme_duration']/50

pos_days_last['extreme_duration'] = pos_days_last['extreme_duration']/50
neg_days_last['extreme_duration'] = neg_days_last['extreme_duration']/50

# %%
awb_pos_first = read_comp_var(
    "wb_anticyclonic", "pos", 1850, name="flag", time_window=wb_time_window, method = 'no_stat'
)

cwb_neg_first = read_comp_var(
    "wb_cyclonic", "neg", 1850, name="flag", time_window=wb_time_window, method = 'no_stat'
)

awb_pos_last = read_comp_var(
    "wb_anticyclonic", "pos", 2090, name="flag", time_window=wb_time_window, method = 'no_stat'
)
cwb_neg_last = read_comp_var(
    "wb_cyclonic", "neg", 2090, name="flag", time_window=wb_time_window, method = 'no_stat'
)
# check the map
#%%
fig, axes = plt.subplots(
    2, 2, figsize=(20, 10), subplot_kw=dict(projection=ccrs.PlateCarree(-70))
)

awb_pos_first.sum(dim = 'ens').mean(dim = 'time').plot.contourf(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
)

cwb_neg_first.sum(dim = 'ens').mean(dim = 'time').plot.contourf(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
)



awb_pos_last.sum(dim = 'ens').mean(dim = 'time').plot.contourf(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
)
cwb_neg_last.sum(dim = 'ens').mean(dim = 'time').plot.contourf(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
)

# add box at the first column, first row, 40-60N, -10, 10 E
import matplotlib.patches as mpatches

# Define the box coordinates (longitude in 0-360 or -180-180 as per your data)
# Here, -10 to 10 E is equivalent to 350 to 10 if your data is 0-360, or just -10 to 10 if -180 to 180
box_lons = [-10, 10, 10, -10, -10]
box_lats = [40, 40, 60, 60, 40]

axes[0, 0].plot(
    box_lons,
    box_lats,
    transform=ccrs.PlateCarree(),
    color="k",
    linewidth=2,
    linestyle="--",
)

# add box at the second column, first row, 50-70N, -50, -40 W
box_lons = [310, 320, 320, 310, 310]
box_lats = [50, 50, 70, 70, 50]
axes[0, 1].plot(
    box_lons,
    box_lats,
    transform=ccrs.PlateCarree(),
    color="k",
    linewidth=2,
    linestyle="--",
)

# add gridlines
for ax in axes.flatten():
    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.coastlines()
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
plt.tight_layout()


#%%
# AWB 40-60N, -10, 10 E
awb_pos_NAL_first = awb_pos_first.sel(lat = slice(30, 60), lon = slice(300, 360)).mean(dim = ('lat','lon')).sum(dim = 'ens')
awb_pos_NAL_last = awb_pos_last.sel(lat = slice(30, 60), lon = slice(300, 360)).mean(dim = ('lat','lon')).sum(dim = 'ens')

cwb_neg_NAL_first = cwb_neg_first.sel(lat = slice(30, 60), lon = slice(300, 360)).mean(dim = ('lat','lon')).sum(dim = 'ens')
cwb_neg_NAL_last = cwb_neg_last.sel(lat = slice(30, 60), lon = slice(300, 360)).mean(dim = ('lat','lon')).sum(dim = 'ens')



#%%
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


line_ax2.set_xlim(-15, 5)
line_ax1.set_xlim(-15, 5)

line_ax2.set_ylim(0, 3)
line_ax1.set_ylim(0, 3)

line_ax2.set_ylabel("WB occurrence", fontsize=14)
line_ax2.set_ylabel("")
line_ax1.set_xlabel("days relative to onset of NAO extremes", fontsize=20)
line_ax2.set_xlabel("days relative to onset of NAO extremes", fontsize=20)

line_ax1.legend(frameon=False, loc="upper right")
line_ax1.set_ylabel("WB occurrence")
plt.tight_layout()

# no line at the top and right of the plot
for ax in [ax1, hist_ax2, hist_ax3, line_ax1, line_ax2]:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# # save as pdf without background
# plt.savefig(
#     "/work/mh0033/m300883/High_frequecy_flow/docs/plots/slides/agu/agu.pdf",
#     dpi=500,
#     transparent=True,
# )
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
