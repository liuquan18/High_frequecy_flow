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
def composite_before_NAO(NAO, WB, lag_days=[-10, -1], WB_type="precusor_WB"):
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
            NAO_pos_AWB = composite_before_NAO(NAO_pos, AWB, WB_type="precusor_WB")
            NAO_pos_CWB = composite_before_NAO(NAO_pos, CWB, WB_type="non_precusor_WB")

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
            NAO_neg_AWB = composite_before_NAO(NAO_neg, AWB, WB_type="non_precusor_WB")
            NAO_neg_CWB = composite_before_NAO(NAO_neg, CWB, WB_type="precusor_WB")

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
NAO["WB_diff"] = NAO["precusor_WB"] - NAO["non_precusor_WB"]


# %%

# %%
fig, axes = plt.subplots(
    3, 1, height_ratios=[0.3, 1, 0.3], sharex=False, figsize=(6, 8)
)

kde_during = sns.kdeplot(data=NAO, x="jet_loc_during", hue="period", common_norm=True, ax=axes[0], legend=True)
kde_during.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)

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
# add legend

scatter.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)

sns.kdeplot(data=NAO, x="jet_loc_before", hue="period", common_norm=True, ax=axes[2], legend=False)


for ax in axes:
    ax.set_xlim(35, 65)
# %%
