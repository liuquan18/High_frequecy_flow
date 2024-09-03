# %%
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec
import glob
import logging
import sys
import os

logging.basicConfig(level=logging.WARNING)
# %%
import src.ConTrack.contrack as ct

# %%
import importlib

importlib.reload(ct)
# %%
# %%
try:
    node = int(sys.argv[0])
except ValueError:
    logging.warning("no node number provided, using default node 0")
    node = 0

# %%
try:
    break_type = str(sys.argv[1])
except IndexError:
    logging.warning("no break type provided, using default AWB")
    break_type = "AWB"


# %%
# nodes and cores
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # [0,1,2,3,4,5,6,7,8,9]
    size = comm.Get_size()  # 10
except:
    logging.warning("::: Warning: Proceeding without mpi4py! :::")
    rank = 0
    size = 1

# %%
periods = ["first10", "last10"]
period = periods[node]

tags = ["1850_1859", "2091_2100"]
tag = tags[node]

# %%


# %%
index_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wavebreak_index/wb_{period}/"
event_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wavebreak_events/{break_type}_events_{period}/"
flag_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wavebreak_events/{break_type}_flag_{period}/"

# %%
# mkdir if not exist
if not os.path.exists(event_dir):
    os.makedirs(event_dir)
if not os.path.exists(flag_dir):
    os.makedirs(flag_dir)

# %%
members_all = list(range(1, 51))  # all members
members_single = np.array_split(members_all, size)[rank]  # members on this core


# %%
# %%
def wb_event(ds, persistence: int = 5, threshold: int = 15, gorl: str = ">="):
    WB = ct.contrack()
    WB.ds = ds

    # apply median filter to the data along time
    WB.ds = WB.ds.rolling(time=3, center=True).median()

    # spatial smoothing
    WB.ds = WB.ds.rolling(lat=3, lon=3, center=True).mean()

    WB.set_up(force=True)

    WB.run_contrack(
        variable="wave_breaking_index",
        threshold=threshold,
        gorl=gorl,
        overlap=0.5,
        persistence=persistence,
        twosided=True,
    )
    return WB.ds


# %%
def event_cycle(ds):
    WB = ct.contrack()
    WB.ds = ds
    WB.set_up(force=True)
    # life cycle
    WB_df = WB.run_lifecycle(flag="flag", variable="wave_breaking_index")

    WB_xr = xr.DataArray(WB_df)
    return WB_xr


# %%
for i, ens in enumerate(members_single):
    logging.warning(f"Period {period}: Rank {rank}, member {i+1}/{len(members_single)}")

    threshold = 15 if break_type == "AWB" else -15
    gorl = ">=" if break_type == "AWB" else "<="

    file = glob.glob(f"{index_dir}wb_*r{ens}i1p1f1*.nc")[0]

    ds = xr.open_dataset(file)
    ds = ds.groupby("time.year").apply(
        wb_event, persistence=5, threshold=threshold, gorl=gorl
    )

    # save the flag
    ds["flag"].to_netcdf(flag_dir + file.split("/")[-1])

    WB_xr = ds.groupby("time.year").apply(event_cycle)
    WB_df = []
    for year in WB_xr["year"].values:
        wb_df = WB_xr.sel(year=year).values
        wb_df = pd.DataFrame(
            wb_df,
            columns=["Flag", "Date", "Longitude", "Latitude", "Intensity", "Size"],
        )
        # change value of 'Flag' to 'year'+'Flag'
        wb_df["Flag"] = (
            year * 1000 + wb_df["Flag"]
        )  # different year may have the same flag
        WB_df.append(wb_df)
    WB_df = pd.concat(WB_df)
    # dropna
    WB_df = WB_df.dropna()

    # save life cycle
    WB_df.to_csv(
        event_dir
        + file.split("/")[-1].replace("wb_", "wb_events_").replace(".nc", ".csv"),
        index=False,
    )

# %%
