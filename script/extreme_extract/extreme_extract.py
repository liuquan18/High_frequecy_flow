# %%
import xarray as xr
import pandas as pd
from src.extremes.extreme_extract import subtract_threshold
from src.extremes.extreme_extract import extract_pos_extremes
from src.extremes.extreme_extract import extract_neg_extremes
import mpi4py.MPI as MPI
import numpy as np
import sys
# %%

# nodes and cores
node = int(sys.argv[1])
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#%%
periods = ["first10", "last10"]
period = periods[node]

tags = ["1850_1859", "2091_2100"]
tag = tags[node]

#%%
projected_pc_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_{period}/"

pos_extreme_save_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/pos_extreme_events/pos_extreme_events_{period}/"
neg_extreme_save_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/neg_extreme_events/neg_extreme_events_{period}/"

#%%
members_all = list(range(1, 51))  # all members
members_single = np.array_split(members_all, size)[rank]  # members on this core

#%%
def calculate_residue(pc, threshold):
    residues = []
    for plev in pc.plev.values:
        residue = subtract_threshold(pc.sel(plev=plev), threshold[threshold['plev'] == plev])
        residue['plev'] = plev
        residues.append(residue)
    residues = pd.concat(residues, axis=0)
    return residues


#%%
for i, member in enumerate(members_single):
    print(f"Period {period}: Rank {rank}, member {member}/{members_single[-1]}")
    # read pc index
    pc = xr.open_dataset(
        f"{projected_pc_path}/troposphere_pc_MJJAS_ano_{tag}_r{member}.nc"
    ).pc

    # positive extremes
    # use the threshold from the first 10  all members
    pos_threshold = pd.read_csv(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/threshold/pos_threshold_first10_allens.csv"
    )
    pos_residues = calculate_residue(pc, pos_threshold)


    pos_extremes = pos_residues.groupby('plev')[['time','pc']].apply(extract_pos_extremes)
    pos_extremes = pos_extremes.reset_index()[['plev','start_time','end_time','duration','sum','mean','max','min']]
    pos_extremes.to_csv(f"{pos_extreme_save_path}/troposphere_pos_extreme_events_{tag}_r{member}.csv", index=False)


    # negative extremes
    # use the threshold from the first 10  all members
    neg_threshold = pd.read_csv(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/threshold/neg_threshold_first10_allens.csv"
    )
    neg_residues = calculate_residue(pc, neg_threshold)
    neg_extremes = neg_residues.groupby('plev')[['time','pc']].apply(extract_neg_extremes)
    neg_extremes = neg_extremes.reset_index()[['plev','start_time','end_time','duration','sum','mean','max','min']]
    neg_extremes.to_csv(f"{neg_extreme_save_path}/troposphere_neg_extreme_events_{tag}_r{member}.csv")