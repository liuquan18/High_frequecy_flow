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
def jet_location(NAO, jet):
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

    # Assign 1 at the maximum value along 'lat', 0 elsewhere
    jet_loc = (jet_composite == jet_composite.max(dim="lat")).astype(int)

    jet_loc_occur = jet_loc.sum(dim="event")
    return jet_loc_occur


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
            jet_loc_pos = jet_location(NAO_pos, jet)
            NAO_pos_jet_locs.append(jet_loc_pos)

        if not NAO_neg.empty:
            jet_loc_neg = jet_location(NAO_neg, jet)
            NAO_neg_jet_locs.append(jet_loc_neg)

    NAO_pos_jet_locs = xr.concat(NAO_pos_jet_locs, dim="ens").sum(dim="ens")
    NAO_neg_jet_locs = xr.concat(NAO_neg_jet_locs, dim="ens").sum(dim="ens")
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
first_pos_jet.plot.contourf(
    x="time",
    y="lat",
    ax=axes[0, 0],
    label="pos-first10",
    levels=np.arange(5, 31, 5),
    extend="max",
)
first_neg_jet.plot.contourf(
    x="time",
    y="lat",
    ax=axes[1, 0],
    label="neg-first10",
    levels=np.arange(5, 31, 5),
    extend="max",
)

last_pos_jet.plot.contourf(
    x="time",
    y="lat",
    ax=axes[0, 1],
    label="pos-last10",
    levels=np.arange(5, 31, 5),
    extend="max",
)
last_neg_jet.plot.contourf(
    x="time",
    y="lat",
    ax=axes[1, 1],
    label="neg-last10",
    levels=np.arange(5, 31, 5),
    extend="max",
)

for ax in axes[:, 0].flat:
    # hline at mean, mean+-std
    ax.axhline(first_jet_mean, color="k", linestyle="--")
    ax.axhline(first_jet_mean + first_jet_std, color="k", linestyle=":")
    ax.axhline(first_jet_mean - first_jet_std, color="k", linestyle=":")

for ax in axes[:, 1].flat:
    # hline at mean, mean+-std
    ax.axhline(last_jet_mean, color="k", linestyle="--")
    ax.axhline(last_jet_mean + last_jet_std, color="k", linestyle=":")
    ax.axhline(last_jet_mean - last_jet_std, color="k", linestyle=":")


for ax in axes.flat:
    ax.set_ylim(35, 63)
    ax.set_xlim(-15, 10)
    ax.set_title(ax.get_label())
    ax.set_ylabel("Latitude")
    ax.set_xlabel("Days relative to NAO onset day")
    # ax.axvline(0, color="k", linestyle="--")

axes[0, 0].set_title("pos-first10")
axes[0, 1].set_title("pos-last10")
axes[1, 0].set_title("neg-first10")
axes[1, 1].set_title("neg-last10")

plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/background_jet/NA_jet250_loc_lat_day.png"
)

# %%
