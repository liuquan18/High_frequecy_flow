# %%
import xarray as xr
import pandas as pd
import numpy as np
import sys
import glob
import eventextreme.eventextreme as ee
import logging
import src.compute.slurm_cluster as scluster

logging.basicConfig(level=logging.WARNING)
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

print(f"node {node}, rank {rank}, size {size}")


# %%
periods = ["first10", "last10"]
period = periods[node]

tags = ["1850_1859", "2091_2100"]
tag = tags[node]

# %%
OLR_ano_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/{period}_OLR_daily_ano/"

pos_extreme_save_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_extremes_pos/OLR_extremes_pos_{period}/"
neg_extreme_save_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_extremes_neg/OLR_extremes_neg_{period}/"
# %%
threshold = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_threshold/OLR_threshold_allens/threshold_allens.nc"
)

# %%
pos_threshold = threshold.pos_thr
neg_threshold = threshold.neg_thr
# %%
pos_threshold = pos_threshold.to_dataframe(name="threshold").reset_index()
neg_threshold = neg_threshold.to_dataframe(name="threshold").reset_index()

# %%
# add spatial dimension
pos_threshold["spatial"] = pos_threshold.groupby(["lat", "lon"]).ngroup()
neg_threshold["spatial"] = neg_threshold.groupby(["lat", "lon"]).ngroup()
# %%
members_all = list(range(1, 51))  # all members
members_single = np.array_split(members_all, size)[rank]  # members on this core


# %%
def to_dataframe(pc):

    # exclude the data at 1st may to 3rd May, and the data during 28th Sep and 31st Sep
    mask_exclude = (
        (pc["time.month"] == 5) & (pc["time.day"] >= 1) & (pc["time.day"] <= 3)
    ) | ((pc["time.month"] == 9) & (pc["time.day"] >= 28) & (pc["time.day"] <= 30))
    mask_keep = ~mask_exclude

    pc = pc.where(mask_keep, drop=True)

    # convert to dataframe
    pc = pc.to_dataframe().reset_index()
    pc["spatial"] = pc.groupby(["lat", "lon"]).ngroup()
    pc["time"] = pd.to_datetime(pc["time"].values)

    return pc


# %%
client, cluster = scluster.init_dask_slurm_cluster(scale = 2, processes=20, walltime="08:00:00", memory="200GB")

print("rank {rank} client {client} cluster {cluster}")

for i, member in enumerate(members_single):
    print(f"period {period} Processing member {member} on node {node}...")
#%%
    # read OLR nc file
    olr_file = glob.glob(f"{OLR_ano_path}rlut*r{member}i1p1f1*ano.nc")[0]
    OLR_ano = xr.open_dataset(olr_file).rlut
#%%
    OLR_df = to_dataframe(OLR_ano)

    df = OLR_df[["time", "spatial", "rlut"]]

    solver = ee.EventExtreme(df, column_name="rlut")

    # positive
    solver.set_positive_threshold(pos_threshold[["spatial", "threshold", "dayofyear"]])
    pos_extremes = solver.extract_positive_extremes

    # negative
    solver.set_negative_threshold(neg_threshold[["spatial", "threshold", "dayofyear"]])
    neg_extremes = solver.extract_negative_extremes

    # add coords of lat lon
    coords = pos_threshold[pos_threshold["dayofyear"] == 124][
        ["spatial", "lat", "lon"]
    ]  # select one day to get the coords
    pos_extremes = pos_extremes.merge(coords, on="spatial", how="inner")
    neg_extremes = neg_extremes.merge(coords, on="spatial", how="inner")

    # save the extremes
    pos_extremes.to_csv(
        f"{pos_extreme_save_path}OLR_extremes_pos_{tag}_r{member}.csv", index=False
    )

    print("positive extremes saved")
    neg_extremes.to_csv(
        f"{neg_extreme_save_path}OLR_extremes_neg_{tag}_r{member}.csv", index=False
    )
    print("negative extremes saved")
# %%
