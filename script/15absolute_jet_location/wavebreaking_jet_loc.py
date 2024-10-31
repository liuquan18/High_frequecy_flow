# %%
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import seaborn as sns


# %%
from src.composite.composite_NAO_WB import read_wb, lag_lead_composite
import src.composite.composite as comp
from src.extremes.extreme_read import read_extremes  # NAO extremes


# %%
def jet_stream_abs(period, ens, plev=None):

    if plev is None:  # eddy-driven jet
        plev_label = ""
    else:
        plev_label = "_allplev"  # select plev later
    # Load data
    jet_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream{plev_label}_{period}/"
    jet_file = glob.glob(f"{jet_path}*r{ens}i1p1f1*.nc")[0]

    jet = xr.open_dataset(jet_file).ua
    jet["time"] = jet.indexes["time"].to_datetimeindex()

    try:
        jet = jet.sel(plev=plev)
    except KeyError:
        pass

    # drop dim lon
    jet = jet.isel(lon=0)

    jet_loc = jet.lat[jet.argmax(dim="lat")]
    jet_loc["ens"] = ens

    # maximum jet speed
    jet_max = jet.max(dim="lat")
    jet_max["ens"] = ens

    return jet_loc, jet_max


# %%
def composite_during_NAO(NAO, jet, label="jet_loc"):
    NAO_jet_composites = []
    for event_id, event in NAO.iterrows():

        NAO_jet_comp = jet.sel(
            time=slice(event["extreme_start_time"], event["extreme_end_time"])
        ).mean(dim="time")

        # tag the composite with the start time and ensemble number, named as 'event'
        NAO_jet_comp["event"] = event_id
        NAO_jet_composites.append(NAO_jet_comp)

    NAO_jet_composites = xr.concat(NAO_jet_composites, dim="event")
    NAO_jet_composites = NAO_jet_composites.to_dataframe(label)
    return NAO_jet_composites[[label]]


# %%
def composite_before_NAO(NAO, WB, lag_days=[-10, -1], WB_type="AWB"):
    NAO_wb_composites = []

    for event_id, event in NAO.iterrows():
        on_set_day = event["extreme_start_time"]

        WB_comp = WB.sel(
            time=slice(
                on_set_day + pd.Timedelta(days=lag_days[0]),
                on_set_day + pd.Timedelta(days=lag_days[1]),
            )
        ).mean(dim="time")

        WB_comp["event"] = event_id
        NAO_wb_composites.append(WB_comp)

    NAO_wb_composites = xr.concat(NAO_wb_composites, dim="event")
    NAO_wb_composites = NAO_wb_composites.to_dataframe(WB_type)
    return NAO_wb_composites[[WB_type]]


# %%
def event_composite(period, jet_plev=None):

    NAO_pos_composites = []
    NAO_neg_composites = []

    for ens in range(1, 51):

        jet_loc, jet_speed = jet_stream_abs(period, ens, jet_plev)
        NAO_pos, NAO_neg = read_extremes(period, 8, ens, 25000)

        AWB = read_wb(period, ens, "AWB", True)
        CWB = read_wb(period, ens, "CWB", True)

        if not NAO_pos.empty:

            NAO_pos.index.name = "event"
            NAO_pos["ens"] = ens

            NAO_pos_jet_loc = composite_during_NAO(
                NAO_pos, jet_loc, label="jet_loc_during"
            )
            NAO_pos_jet_speed = composite_during_NAO(
                NAO_pos, jet_speed, label="jet_speed_during"
            )
            NAO_pos_jet_loc_before = composite_before_NAO(
                NAO_pos, jet_loc, lag_days=[-10, -1], WB_type="jet_loc_before"
            )
            NAO_pos_jet_speed_before = composite_before_NAO(
                NAO_pos, jet_speed, lag_days=[-10, -1], WB_type="jet_speed_before"
            )
            NAO_pos_AWB = composite_before_NAO(NAO_pos, AWB,lag_days= [-5,5], WB_type="AWB")
            NAO_pos_CWB = composite_before_NAO(NAO_pos, CWB,lag_days= [-5,5], WB_type="CWB")

            NAO_pos_composite = (
                NAO_pos.join(NAO_pos_jet_loc, on="event")
                .join(NAO_pos_jet_speed, on="event")
                .join(NAO_pos_jet_loc_before, on="event")
                .join(NAO_pos_jet_speed_before, on="event")
                .join(NAO_pos_AWB, on="event")
                .join(NAO_pos_CWB, on="event")
            )
            NAO_pos_composites.append(NAO_pos_composite)

        if not NAO_neg.empty:

            NAO_neg.index.name = "event"
            NAO_neg["ens"] = ens

            NAO_neg_jet_loc = composite_during_NAO(
                NAO_neg, jet_loc, label="jet_loc_during"
            )
            NAO_neg_jet_speed = composite_during_NAO(
                NAO_neg, jet_speed, label="jet_speed_during"
            )
            NAO_neg_jet_loc_before = composite_before_NAO(
                NAO_neg, jet_loc, lag_days=[-10, -1], WB_type="jet_loc_before"
            )
            NAO_neg_jet_speed_before = composite_before_NAO(
                NAO_neg, jet_speed, lag_days=[-10, -1], WB_type="jet_speed_before"
            )
            NAO_neg_AWB = composite_before_NAO(NAO_neg, AWB,lag_days=[-5,5], WB_type="AWB")
            NAO_neg_CWB = composite_before_NAO(NAO_neg, CWB, lag_days = [-5,5], WB_type="CWB")

            NAO_neg_composite = (
                NAO_neg.join(NAO_neg_jet_loc, on="event")
                .join(NAO_neg_jet_speed, on="event")
                .join(NAO_neg_jet_loc_before, on="event")
                .join(NAO_neg_jet_speed_before, on="event")
                .join(NAO_neg_AWB, on="event")
                .join(NAO_neg_CWB, on="event")
            )
            NAO_neg_composites.append(NAO_neg_composite)

    NAO_pos_composites = pd.concat(NAO_pos_composites, axis=0)
    NAO_neg_composites = pd.concat(NAO_neg_composites, axis=0)

    return NAO_pos_composites, NAO_neg_composites


# %%
first_NAO_pos, first_NAO_neg = event_composite("first10", None)
# %%
last_NAO_pos, last_NAO_neg = event_composite("last10", None)

# %%
first_NAO_neg["period"] = "first10"
last_NAO_neg["period"] = "last10"

first_NAO_pos["period"] = "first10"
last_NAO_pos["period"] = "last10"

# %%
# merge first and last
NAO_pos = pd.concat([first_NAO_pos, last_NAO_pos], axis=0)
NAO_neg = pd.concat([first_NAO_neg, last_NAO_neg], axis=0)

# %%
NAO_pos["phase"] = "pos"
NAO_neg["phase"] = "neg"

# merge pos and neg
NAO = pd.concat([NAO_pos, NAO_neg], axis=0)
NAO["WB_diff"] = NAO["AWB"] - NAO["CWB"]
#%%
# construct a column called 'percusor', the value equals column 'AWB' is 'phase' is 'pos', otherwise 'CWB'
NAO['precusor'] = NAO['AWB']
NAO.loc[NAO['phase'] == 'neg', 'precusor'] = NAO.loc[NAO['phase'] == 'neg', 'CWB']
#%%
# save 
# NAO.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/abs_jet_loc_NAO.csv", index=True)
# read NAO
# NAO = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/abs_jet_loc_NAO.csv", index_col=0)

# %%
# read climatology
first_jet_loc_clim = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_first10.nc")
last_jet_loc_clim = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_last10.nc")

first_jet_loc_clim = first_jet_loc_clim.lat.mean(dim ='month')
last_jet_loc_clim = last_jet_loc_clim.lat.mean(dim ='month')
# %%
def set_legend_properties(ax):
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)

fig, axes = plt.subplots(
    3, 1, height_ratios=[0.3, 1, 0.3], sharex=False, figsize=(8, 8)
)

# KDE plot during NAO event
kde_plot_during_NAO = sns.kdeplot(data=NAO, x="jet_loc_during", hue="period", common_norm=True, ax=axes[0], legend=True)
set_legend_properties(axes[0])
axes[0].set_xlabel("Jet location during NAO event")



# Scatter plot
scatter = sns.scatterplot(
    data=NAO,
    x="jet_loc_during",
    y="WB_diff",
    hue="period",
    size="extreme_duration",
    legend=True,
    style="phase",
    sizes=(20, 200),
    ax=axes[1],
)
set_legend_properties(scatter)
axes[1].set_xlabel("Jet location during NAO event")
axes[1].set_ylabel("AWB - CWB averaged on [-5, 5] days")


# KDE plot before NAO event
kde_before = sns.kdeplot(data=NAO, x="jet_loc_before", hue="period", common_norm=True, ax=axes[2], legend=False)
axes[2].set_xlabel("Jet location averaged on [-10, -1] days")

# Calculate mean jet location before NAO event
jet_loc_before = NAO.groupby('period')['jet_loc_before'].mean()

# Add vertical lines at mean of period
for period, color in zip(['first10', 'last10'], ['C0', 'C1']):
    x = jet_loc_before[period]
    kde_line = kde_before.get_lines()[1 if period == 'first10' else 0]
    kde_x, kde_y = kde_line.get_data()
    y = kde_y[np.argmin(np.abs(kde_x - x))]
    axes[2].plot([x, x], [0, y], color=color, label=period)

# Add vertical lines at climatology
axes[2].axvline(first_jet_loc_clim.values, color="C0", linestyle="--", label='first10 climatology')
axes[2].axvline(last_jet_loc_clim.values, color="C1", linestyle="--", label='last10 climatology')

set_legend_properties(axes[2])

# Set x-axis limits
for ax in axes:
    ax.set_xlim(35, 65)

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/background_jet/WB_jet_background.png", dpi=300)

# %%
fig, axes = plt.subplots(
    3, 1, height_ratios=[0.3, 1, 0.3], sharex=False, figsize=(8, 8)
)

# KDE plot during NAO event
kde_during = sns.kdeplot(data=NAO, x="jet_loc_during", hue="period", common_norm=True, ax=axes[0], legend=True)
sns.move_legend(axes[0], "upper left", bbox_to_anchor=(1.05, 1))
axes[0].set_xlabel("Jet location during NAO event")



# Scatter plot
scatter = sns.scatterplot(
    data=NAO,
    x="jet_loc_during",
    y="precusor",
    hue="period",
    size="extreme_duration",
    legend=True,
    style="phase",
    sizes=(20, 200),
    ax=axes[1],
)
scatter.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
axes[1].set_xlabel("Jet location during NAO event")
axes[1].set_ylabel("precusor WB occurrence averaged on [-5, 5] days")
axes[1].set_ylim(-0.08, 0.41)


# KDE plot before NAO event
kde_before = sns.kdeplot(data=NAO, x="jet_loc_before", hue="period", common_norm=True, ax=axes[2], legend=False)
axes[2].set_xlabel("Jet location averaged on [-10, -1] days")

# Calculate mean jet location before NAO event
jet_loc_before = NAO.groupby('period')['jet_loc_before'].mean()

# Add vertical lines at mean of period
for period, color in zip(['first10', 'last10'], ['C0', 'C1']):
    x = jet_loc_before[period]
    kde_line = kde_before.get_lines()[1 if period == 'first10' else 0]
    kde_x, kde_y = kde_line.get_data()
    y = kde_y[np.argmin(np.abs(kde_x - x))]
    axes[2].plot([x, x], [0, y], color=color, label=period)

# Add vertical lines at climatology
axes[2].axvline(first_jet_loc_clim.values, color="C0", linestyle="--", label='first10 climatology')
axes[2].axvline(last_jet_loc_clim.values, color="C1", linestyle="--", label='last10 climatology')

axes[2].legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)

# Set x-axis limits
for ax in axes:
    ax.set_xlim(35, 65)
plt.tight_layout()

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/background_jet/WB_precursor_jet_background.png", dpi=300)

# %%
