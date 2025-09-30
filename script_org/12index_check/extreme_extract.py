# %%
import xarray as xr
import pandas as pd
import numpy as np

import eventextreme.eventextreme as ee
import sys
import logging
import os
import glob

logging.basicConfig(level=logging.WARNING)


# %%
# nodes for different ensemble members
node = sys.argv[1]
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
member = node
projected_pc_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0NAO_index_eofs/r{member}i1p1f1/"

pos_extreme_save_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0extreme_events_decades/positive_extreme_events_decades/r{member}i1p1f1/"
neg_extreme_save_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0extreme_events_decades/negative_extreme_events_decades/r{member}i1p1f1/"


if rank == 0:
    logging.info(f"Processing ensemble member {node}")

    if not os.path.exists(pos_extreme_save_path):
        os.makedirs(pos_extreme_save_path)

    if not os.path.exists(neg_extreme_save_path):
        os.makedirs(neg_extreme_save_path)


# %%
all_pc_files = glob.glob(projected_pc_path + "*.nc")
# %%
single_pc_files = np.array_split(all_pc_files, size)[rank]


# %%
def to_dataframe(pc):

    # exclude the data at 1st may to 3rd May, and the data during 28th Sep and 31st Sep
    mask_exclude = (
        (pc["time.month"] == 5) & (pc["time.day"] >= 1) & (pc["time.day"] <= 3)
    ) | ((pc["time.month"] == 9) & (pc["time.day"] >= 28) & (pc["time.day"] <= 30))
    mask_keep = ~mask_exclude

    pc = pc.where(mask_keep, drop=True)

    # convert to dataframe
    pc = pc.to_dataframe().reset_index()[["time", "pc"]]
    pc["time"] = pd.to_datetime(pc["time"].values)

    return pc


# %%
for i, pc_file in enumerate(single_pc_files):
    print(f"Rank {rank}, {i+1}/{len(single_pc_files)}")

    # read pc index
    pc = xr.open_dataset(pc_file).pseudo_pcs
    pc.name = "pc"

    # convert to datetime
    pc['time'] = pc.indexes['time'].to_datetimeindex()

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

    # select plev from thershold
    pos_threshold = pos_threshold[pos_threshold["plev"] == 50000]
    neg_threshold = neg_threshold[neg_threshold["plev"] == 50000]

    # extract extremes
    extremes = ee.EventExtreme(pc, "pc", independent_dim=None, threshold_std=1.5)

    # # set thresholds
    # extremes.set_positive_threshold(pos_threshold)
    # extremes.set_negative_threshold(neg_threshold)

    # extract extremes
    positive_extremes = extremes.extract_positive_extremes
    negative_extremes = extremes.extract_negative_extremes


    # save to csv
    file_name_prefix = pc_file.split("/")[-1].split(".")[0]
    pos_name = pos_extreme_save_path + file_name_prefix[:-3] + "pos_extreme_events.csv"
    neg_name = neg_extreme_save_path + file_name_prefix[:-3] + "neg_extreme_events.csv"

    positive_extremes.to_csv(
        pos_name,
        index=False,
    )

    negative_extremes.to_csv(
        neg_name,
        index=False,
    )


