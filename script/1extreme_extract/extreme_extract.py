# %%
import xarray as xr
import pandas as pd
import numpy as np

import eventextreme.eventextreme as ee
import sys
import logging

logging.basicConfig(level=logging.WARNING)


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
projected_pc_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_{period}/"

pos_extreme_save_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/pos_extreme_events/pos_extreme_events_{period}/"
neg_extreme_save_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/neg_extreme_events/neg_extreme_events_{period}/"

# %%
members_all = list(range(1, 51))  # all members
members_single = np.array_split(members_all, size)[rank]  # members on this core


def to_dataframe(pc):

    # exclude the data at 1st may to 3rd May, and the data during 28th Sep and 31st Sep
    mask_exclude = (
        (pc["time.month"] == 5) & (pc["time.day"] >= 1) & (pc["time.day"] <= 3)
    ) | ((pc["time.month"] == 9) & (pc["time.day"] >= 28) & (pc["time.day"] <= 30))
    mask_keep = ~mask_exclude

    pc = pc.where(mask_keep, drop=True)

    # convert to dataframe
    pc = pc.to_dataframe().reset_index()[["plev", "time", "pc"]]
    pc["time"] = pd.to_datetime(pc["time"].values)

    return pc


# %%
for i, member in enumerate(members_single):
    print(f"Period {period}: Rank {rank}, member {member}/{members_single[-1]}")
    
    
    # read pc index
    pc = xr.open_dataset(
        f"{projected_pc_path}/troposphere_pc_MJJAS_ano_{tag}_r{member}.nc"
    ).pc

    pc = to_dataframe(pc)

    # read thresholds 
    ## positive extremes
    pos_threshold = pd.read_csv(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NAO_threshold/pos_threshold_first10_allens.csv"
    )

    ## negative extremes
    neg_threshold = pd.read_csv(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NAO_threshold/neg_threshold_first10_allens.csv"
    )


    # extract extremes
    extremes = ee.EventExtreme(pc, 'pc', independent_dim='plev')

    # set thresholds
    extremes.set_positive_threshold(pos_threshold)
    extremes.set_negative_threshold(neg_threshold)



    # extract extremes
    positive_extremes = extremes.extract_positive_extremes
    negative_extremes = extremes.extract_negative_extremes




    positive_extremes.to_csv(
        f"{pos_extreme_save_path}troposphere_pos_extreme_events_{tag}_r{member}.csv",
        index=False,
    )

    negative_extremes.to_csv(
        f"{neg_extreme_save_path}troposphere_neg_extreme_events_{tag}_r{member}.csv",
        index=False,
    )


# %%
