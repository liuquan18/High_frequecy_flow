# %%
import xarray as xr
import pandas as pd
import numpy as np

import eventextreme.eventextreme as ee
import sys
import logging
import os

logging.basicConfig(level=logging.WARNING)


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
projected_pc_path = "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/pc_std/"

pos_extreme_save_path = "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/pos_extreme_events/"
neg_extreme_save_path = "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/neg_extreme_events/"

if rank == 0:
    if not os.path.exists(pos_extreme_save_path):
        os.makedirs(pos_extreme_save_path)

    if not os.path.exists(neg_extreme_save_path):
        os.makedirs(neg_extreme_save_path)


# %%

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
#%%
pc = xr.open_mfdataset(f"{projected_pc_path}*.nc", combine = 'by_coords').pc


#%%
pc = to_dataframe(pc)

#%%
extremes = ee.EventExtreme(pc, 'pc', independent_dim='plev', threshold_std = 1.2)

#%%
# extract extremes
positive_extremes = extremes.extract_positive_extremes
negative_extremes = extremes.extract_negative_extremes

# %%


positive_extremes.to_csv(
    f"{pos_extreme_save_path}/NAO_pc_pos_extremes.csv"
)

negative_extremes.to_csv(
    f"{neg_extreme_save_path}/NAO_pc_neg_extremes.csv"
)



# %%
