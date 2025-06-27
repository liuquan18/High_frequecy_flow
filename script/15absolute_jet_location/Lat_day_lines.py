# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import src.composite.composite as comp
from src.extremes.extreme_read import read_extremes  # NAO extremes


# %%
# read jet
def read_jet(period, ens, plev=None):

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

    return jet


# %%
def jet_location(NAO, jet, ens):
    """
    calculate the occurrence of jet as a function of days relative to NAO onset day

    Parameters
    ----------
    NAO : pandas.DataFrame
        NAO extremes
    jet : pandas.DataFrame
        jet array
    """

    NAO_range = comp.find_lead_lag_30days(NAO, base_plev=25000)
    jet_composite = comp.date_range_composite(jet, NAO_range)
    jet_composite["event"] = ens * 1000 + jet_composite["event"].astype(int)

    # jet location as the lat where the value is in the maximum
    jet_loc = jet_composite.groupby("event").apply(_jet_loc)

    return jet_loc


def _jet_loc(jet_composite):
    try:
        jet_loc = jet_composite.lat[jet_composite.argmax(dim="lat")]
        # drop dim lat
        jet_loc = jet_loc.drop("lat")
    except ValueError:
        # jet_composite contains nan, remove nan and try again
        jet_loc_container = xr.full_like(jet_composite.isel(lat=0), np.nan)
        jet_composite = jet_composite.dropna(dim="time", how="any")
        jet_loc = jet_composite.lat[jet_composite.argmax(dim="lat")]
        jet_loc = jet_loc.combine_first(jet_loc_container)
        try:
            jet_loc = jet_loc.drop("lat")
        except ValueError:
            pass

    return jet_loc


# %%
def composite_jet_loc(period, plev=None, smooth=None):

    jets_climat_locs = []
    NAO_pos_jet_locs = []
    NAO_neg_jet_locs = []

    for ens in range(1, 51):
        NAO_pos, NAO_neg = read_extremes(period, 8, ens, 25000)
        jet = read_jet(period, ens, plev)

        jets_climat_locs.append(jet)

        if not NAO_pos.empty:
            jet_loc_pos = jet_location(NAO_pos, jet, ens)
            NAO_pos_jet_locs.append(jet_loc_pos)

        if not NAO_neg.empty:
            jet_loc_neg = jet_location(NAO_neg, jet, ens)
            NAO_neg_jet_locs.append(jet_loc_neg)

    NAO_pos_jet_locs = xr.concat(NAO_pos_jet_locs, dim="event")
    NAO_neg_jet_locs = xr.concat(NAO_neg_jet_locs, dim="event")
    jets_climat_locs = xr.concat(jets_climat_locs, dim="ens")
    jets_climat_locs = jets_climat_locs.lat[jets_climat_locs.argmax(dim="lat")]
    jet_climat_mean = jets_climat_locs.mean(dim=("ens", "time"))
    jet_climat_std = jets_climat_locs.std(dim=("ens", "time"))

    if smooth is not None:
        NAO_pos_jet_locs = NAO_pos_jet_locs.rolling(time=smooth, center=True).mean()
        NAO_neg_jet_locs = NAO_neg_jet_locs.rolling(time=smooth, center=True).mean()

    return NAO_pos_jet_locs, NAO_neg_jet_locs, jet_climat_mean, jet_climat_std


# %%
first_pos_jet, first_neg_jet, first_jet_mean, first_jet_std = composite_jet_loc(
    "first10", 25000, smooth=3
)
last_pos_jet, last_neg_jet, last_jet_mean, last_jet_std = composite_jet_loc(
    "last10", 25000, smooth=3
)


# %%
fig, axes = plt.subplots(2, 2, figsize=(10, 6))

first_pos_jet.plot.line(
    x="time",
    ax=axes[0, 0],
    label="pos-first10",
    add_legend=False,
    color="grey",
    linewidth=1,
)
first_pos_jet.mean(dim="event").plot.line(
    x="time", ax=axes[0, 0], label="mean", color="k"
)
# 25% to 75%
axes[0, 0].fill_between(
    first_pos_jet.time,
    first_pos_jet.quantile(0.75, dim="event"),
    first_pos_jet.quantile(0.25, dim="event"),
    color="r",
    alpha=0.5,
    zorder=10,
)

last_pos_jet.plot.line(
    x="time",
    ax=axes[0, 1],
    label="pos-last10",
    add_legend=False,
    color="grey",
    linewidth=1,
)
axes[0, 1].fill_between(
    last_pos_jet.time,
    last_pos_jet.quantile(0.75, dim="event"),
    last_pos_jet.quantile(0.25, dim="event"),
    color="r",
    alpha=0.5,
    zorder=10,
)

last_pos_jet.mean(dim="event").plot.line(
    x="time", ax=axes[0, 1], label="mean", color="k"
)

first_neg_jet.plot.line(
    x="time",
    ax=axes[1, 0],
    label="neg-first10",
    add_legend=False,
    color="grey",
    linewidth=1,
)

first_neg_jet.mean(dim="event").plot.line(
    x="time", ax=axes[1, 0], label="mean", color="k"
)

axes[1, 0].fill_between(
    first_neg_jet.time,
    first_neg_jet.quantile(0.75, dim="event"),
    first_neg_jet.quantile(0.25, dim="event"),
    color="r",
    alpha=0.5,
    zorder=10,
)

last_neg_jet.plot.line(
    x="time",
    ax=axes[1, 1],
    label="neg-last10",
    add_legend=False,
    color="grey",
    linewidth=1,
)
last_neg_jet.mean(dim="event").plot.line(
    x="time", ax=axes[1, 1], label="mean", color="k"
)

axes[1, 1].fill_between(
    last_neg_jet.time,
    last_neg_jet.quantile(0.75, dim="event"),
    last_neg_jet.quantile(0.25, dim="event"),
    color="r",
    alpha=0.5,
    zorder=10,
)

for ax in axes.flat:
    ax.set_ylim(30, 65)
    ax.set_xlim(-15, 15)

# plot climatology
axes[0, 0].axhline(first_jet_mean, color="k", linestyle="--")
axes[0, 0].fill_between(
    first_pos_jet.time,
    first_jet_mean - first_jet_std,
    first_jet_mean + first_jet_std,
    color="k",
    alpha=0.5,
)

axes[0, 1].axhline(last_jet_mean, color="k", linestyle="--")
axes[0, 1].fill_between(
    last_pos_jet.time,
    last_jet_mean - last_jet_std,
    last_jet_mean + last_jet_std,
    color="k",
    alpha=0.5,
)

axes[1, 0].axhline(first_jet_mean, color="k", linestyle="--")
axes[1, 0].fill_between(
    first_neg_jet.time,
    first_jet_mean - first_jet_std,
    first_jet_mean + first_jet_std,
    color="k",
    alpha=0.5,
)

axes[1, 1].axhline(last_jet_mean, color="k", linestyle="--")
axes[1, 1].fill_between(
    last_neg_jet.time,
    last_jet_mean - last_jet_std,
    last_jet_mean + last_jet_std,
    color="k",
    alpha=0.5,
)

# %%
# %%
fig, axes = plt.subplots(2, 2, figsize=(10, 6))

first_pos_jet.plot.line(
    x="time",
    ax=axes[0, 0],
    label="pos-first10",
    add_legend=False,
    color="grey",
    linewidth=1,
)
first_pos_jet.mean(dim="event").plot.line(
    x="time", ax=axes[0, 0], label="mean", color="k"
)
# +1 to -1 std
axes[0, 0].fill_between(
    first_pos_jet.time,
    first_pos_jet.mean(dim="event") + first_pos_jet.std(dim="event"),
    first_pos_jet.mean(dim="event") - first_pos_jet.std(dim="event"),
    color="r",
    alpha=0.5,
    zorder=10,
)

last_pos_jet.plot.line(
    x="time",
    ax=axes[0, 1],
    label="pos-last10",
    add_legend=False,
    color="grey",
    linewidth=1,
)
axes[0, 1].fill_between(
    last_pos_jet.time,
    last_pos_jet.mean(dim="event") + last_pos_jet.std(dim="event"),
    last_pos_jet.mean(dim="event") - last_pos_jet.std(dim="event"),
    color="r",
    alpha=0.5,
    zorder=10,
)

last_pos_jet.mean(dim="event").plot.line(
    x="time", ax=axes[0, 1], label="mean", color="k"
)

first_neg_jet.plot.line(
    x="time",
    ax=axes[1, 0],
    label="neg-first10",
    add_legend=False,
    color="grey",
    linewidth=1,
)

first_neg_jet.mean(dim="event").plot.line(
    x="time", ax=axes[1, 0], label="mean", color="k"
)

axes[1, 0].fill_between(
    first_neg_jet.time,
    first_neg_jet.mean(dim="event") + first_neg_jet.std(dim="event"),
    first_neg_jet.mean(dim="event") - first_neg_jet.std(dim="event"),
    color="r",
    alpha=0.5,
    zorder=10,
)

last_neg_jet.plot.line(
    x="time",
    ax=axes[1, 1],
    label="neg-last10",
    add_legend=False,
    color="grey",
    linewidth=1,
)
last_neg_jet.mean(dim="event").plot.line(
    x="time", ax=axes[1, 1], label="mean", color="k"
)

axes[1, 1].fill_between(
    last_neg_jet.time,
    last_neg_jet.mean(dim="event") + last_neg_jet.std(dim="event"),
    last_neg_jet.mean(dim="event") - last_neg_jet.std(dim="event"),
    color="r",
    alpha=0.5,
    zorder=10,
)

for ax in axes.flat:
    ax.set_ylim(30, 71)
    ax.set_xlim(-15, 15)

# plot climatology
axes[0, 0].axhline(first_jet_mean, color="k", linestyle="--")
axes[0, 0].fill_between(
    first_pos_jet.time,
    first_jet_mean - first_jet_std,
    first_jet_mean + first_jet_std,
    color="k",
    alpha=0.5,
)

axes[0, 1].axhline(last_jet_mean, color="k", linestyle="--")
axes[0, 1].fill_between(
    last_pos_jet.time,
    last_jet_mean - last_jet_std,
    last_jet_mean + last_jet_std,
    color="k",
    alpha=0.5,
)

axes[1, 0].axhline(first_jet_mean, color="k", linestyle="--")
axes[1, 0].fill_between(
    first_neg_jet.time,
    first_jet_mean - first_jet_std,
    first_jet_mean + first_jet_std,
    color="k",
    alpha=0.5,
)

axes[1, 1].axhline(last_jet_mean, color="k", linestyle="--")
axes[1, 1].fill_between(
    last_neg_jet.time,
    last_jet_mean - last_jet_std,
    last_jet_mean + last_jet_std,
    color="k",
    alpha=0.5,
)

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/background_jet/tracks_jet_lines.png"
)

# %%
