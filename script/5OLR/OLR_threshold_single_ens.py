#%%
import pandas as pd
import xarray as xr
import numpy as np
from mpi4py import MPI
import sys
import logging
logging.basicConfig(level=logging.WARNING)

import eventextreme.extreme_threshold as et

#%%


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print(f"Rank {rank} out of {size} on node {MPI.Get_processor_name()}")

# %%
file_path="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/first10_OLR_daily_ano/"

# %%
members_all = list(range(1, 51))  # all members
members_single = np.array_split(members_all, size)[rank]  # members on this core
# %%
def dataframe_window(df):
    df_window = df.groupby(['lat','lon'])[['time','rlut']].apply(
        et.construct_window, window = 7,column_name = 'rlut'
    )
    df_window = df_window.droplevel(-1).reset_index()

    return df_window
# %%
for i, member in enumerate(members_single):
    print(f"Rank {rank} processing member {member}")
    olr = xr.open_dataset(f"{file_path}rlut_day_MPI-ESM1-2-LR_historical_r{member}i1p1f1_gn_18500501-18590930_ano.nc")
    olr = olr.rlut
    df = olr.to_dataframe()
    df = df.reset_index()

    df_window = dataframe_window(df)

    df_window.to_csv(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/first10_OLR_daily_window/rlut_window_first10_r{member}.csv", index = False)
    print(f"Rank {rank} finished processing member {member}")