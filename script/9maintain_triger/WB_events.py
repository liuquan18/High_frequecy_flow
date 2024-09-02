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

logging.basicConfig(level=logging.WARNING)
# %%
import src.ConTrack.contrack as ct

# %%
import importlib

importlib.reload(ct)
# %%
# %%
try:
    node = int(sys.argv[1])
except ValueError:
    logging.warning("no node number provided, using default node 0")
    node = 0

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
index_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wavebreak_index/wb_{period}/"
event_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wavebreak_events/wavebreak_events_{period}/"
flag_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wavebreak_events/wavebreak_flag_{period}/"
# %%
members_all = list(range(1, 51))  # all members
members_single = np.array_split(members_all, size)[rank]  # members on this core
#%%
# %%
def wb_event(file: str,  persistence: int = 5):
    WB = ct.contrack()
    WB.read(file)

    # apply median filter to the data along time
    WB.ds = WB.ds.rolling(time=3, center=True).median()

    # spatial smoothing
    WB.ds = WB.ds.rolling(lat=5, lon=5, center=True).mean()

    WB.set_up(force=True)

    WB.run_contrack(
        variable="wave_breaking_index",
        threshold=20,
        gorl=">=",
        overlap=0.5,
        persistence=persistence,
        twosided=True,
    )

    WB["flag"].to_netcdf(flag_dir + file.split("/")[-1])

    # life cycle
    WB_df = WB.run_lifecycle(flag="flag", variable="wave_breaking_index")

    # save
    WB_df.to_csv(
        event_dir
        + file.split("/")[-1].replace("wb_", "wb_events_").replace(".nc", ".csv"),
        index=False,
    )
    return WB_df


# %%
for i, ens in enumerate(members_single):
    logging.warning(f"Period {period}: Rank {rank}, member {i+1}/{len(members_single)}")

    file = glob.glob(f"{index_dir}wb_*r{ens}i1p1f1*.nc")[0]

    WB_df = wb_event(file, persistence=5)

# %%
