# %%
import xarray as xr
import pandas as pd
import numpy as np
from src.extremes import extreme_read
import seaborn as sns
import matplotlib.pyplot as plt

# Reload the module
import importlib

importlib.reload(extreme_read)
# %%
from src.extremes.extreme_read import sel_extreme_duration


# %%
def sel_pc_duration(events, pc):

    if len(events) == 0:
        sel_pcs = None
    else:
        sel_pcs = []
        for i in range(len(events)):
            sel_pc = pc.sel(
                time=slice(events.start_time.iloc[i], events.end_time.iloc[i])
            )
            sel_pc = sel_pc.assign_coords(
                duration_index=("time", np.arange(1, sel_pc.sizes["time"] + 1))
            )
            sel_pc_df = sel_pc.to_dataframe().reset_index()[["duration_index", "pc"]]
            sel_pc_df["extreme_duration"] = events.duration.iloc[i]
            sel_pc_df = sel_pc_df.set_index(["extreme_duration", "duration_index"])
            sel_pcs.append(sel_pc_df)

        sel_pcs = pd.concat(sel_pcs, axis=1).sort_index()
    return sel_pcs


# %%
def event_pc(period, duration, plev=50000):

    # for reading path
    pc_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/"
    pos_extreme_path = (
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/pos_extreme_events/"
    )
    neg_extreme_path = (
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/neg_extreme_events/"
    )

    tags = {"first10": "1850_1859", "last10": "2091_2100"}
    tag = tags[period]

    pos_extremes = []
    neg_extremes = []
    pos_pcs = []
    neg_pcs = []

    for i in range(50):
        pc = xr.open_dataset(
            f"{pc_path}projected_pc_{period}/zg_JJA_ano_{tag}_r{i+1}.nc"
        ).pc
        pos_extreme = pd.read_csv(
            f"{pos_extreme_path}pos_extreme_events_{period}/troposphere_pos_extreme_events_{tag}_r{i+1}.csv"
        )
        neg_extreme = pd.read_csv(
            f"{neg_extreme_path}neg_extreme_events_{period}/troposphere_neg_extreme_events_{tag}_r{i+1}.csv"
        )

        # select plev and delete the 'plev' column
        pos_extreme = pos_extreme[pos_extreme["plev"] == plev][
            [
                "extreme_start_time",
                "extreme_end_time",
                "extreme_duration",
                "mean",
                "sum",
                "max",
                "min",
            ]
        ]

        neg_extreme = neg_extreme[neg_extreme["plev"] == plev][
            [
                "extreme_start_time",
                "extreme_end_time",
                "extreme_duration",
                "mean",
                "sum",
                "max",
                "min",
            ]
        ]

        pos_extreme = sel_extreme_duration(pos_extreme, duration=duration)
        neg_extreme = sel_extreme_duration(neg_extreme, duration=duration)

        pos_pc = sel_pc_duration(pos_extreme, pc)
        neg_pc = sel_pc_duration(neg_extreme, pc)

        pos_extremes.append(pos_extreme)
        neg_extremes.append(neg_extreme)
        if pos_pc is not None:
            pos_pcs.append(pos_pc)
        if neg_pc is not None:
            neg_pcs.append(neg_pc)

    pos_extremes = pd.concat(pos_extremes, axis=0)
    neg_extremes = pd.concat(neg_extremes, axis=0)
    pos_pcs = (
        pd.concat(pos_pcs, axis=1)
        if pos_pcs
        else pd.DataFrame().dropna(axis=0, how="all")
    )
    neg_pcs = (
        pd.concat(neg_pcs, axis=1)
        if neg_pcs
        else pd.DataFrame().dropna(axis=0, how="all")
    )

    # only select the rows with the same duration
    try:
        pos_pcs = pos_pcs.loc[duration, :]
        neg_pcs = neg_pcs.loc[duration, :]
        # some post process on dataframe, column values and index name
        pos_pcs.columns = [f"pc_{i+1}" for i in range(len(pos_pcs.columns))]
        pos_pcs.columns.name = "realization"

        neg_pcs.columns = [f"pc_{i+1}" for i in range(len(neg_pcs.columns))]
        neg_pcs.columns.name = "realization"

    except KeyError:
        print(f"No data for duration: {duration}")
        # empty dataframe
        pos_pcs = pd.DataFrame()
        neg_pcs = pd.DataFrame()

    return pos_extremes, neg_extremes, pos_pcs, neg_pcs


# %%
fig, axes = plt.subplots(ncols=3, nrows=4, sharex=False, sharey=True, figsize=(15, 20))

# plot the duration from 5 to 17 days
duration = 5
for ax in axes.flat:
    _, _, first10_pos_pcs, first10_neg_pcs = event_pc("first10", duration, plev=50000)
    _, _, last10_pos_pcs, last10_neg_pcs = event_pc("last10", duration, plev=50000)

    try:
        first10_pos_pcs.plot.line(ax=ax, color="k", alpha=0.5, legend=False)
        last10_pos_pcs.plot.line(ax=ax, color="r", alpha=0.5, legend=False)

        first10_neg_pcs.plot.line(ax=ax, color="k", alpha=0.5, legend=False)
        last10_neg_pcs.plot.line(ax=ax, color="r", alpha=0.5, legend=False)
    except KeyError or TypeError:
        print(f"No data for duration: {duration}")
        pass
    duration += 1

# plt.savefig('/work/mh0033/m300883/High_frequecy_flow/docs/plots/extreme_pc_features/pc_duration_5_15.png')


# %%
