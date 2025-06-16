#%%
import xarray as xr
import numpy as np
from src.data_helper.read_NAO_extremes import read_NAO_extremes_single_ens
from src.composite import composite
from src.data_helper import read_variable
import sys
import logging
logging.basicConfig(level=logging.INFO)
import importlib
import pandas as pd
importlib.reload(composite)
importlib.reload(read_variable)
read_prime_single_ens = read_variable.read_prime_single_ens
range_NAO_composite = composite.range_NAO_composite

#%%
import mpi4py.MPI as MPI
# %%
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()
#%%
def composite_single_ens(var, decade, ens, plev = 85000, dur_threshold = 5, **kwargs):
    # read NAO extremes
    pos_extreme = read_NAO_extremes_single_ens('pos', decade, ens, dur_threshold = dur_threshold)
    neg_extreme = read_NAO_extremes_single_ens('neg', decade, ens, dur_threshold = dur_threshold)

    # read variable
    var_field = read_prime_single_ens( decade, ens,var, **kwargs)

    if not pos_extreme.empty and not neg_extreme.empty:

        var_pos, var_neg = range_NAO_composite(var_field, pos_extreme, neg_extreme)

        # select the pressure level if provided
        var_pos = var_pos.sel(plev = plev) if plev is not None else var_pos
        var_neg = var_neg.sel(plev = plev) if plev is not None else var_neg

        # average over domain [-60, -10][40, 60N]
        var_pos = var_pos.sel(lon = slice(280, 360), lat = slice(40, 80))
        var_neg = var_neg.sel(lon = slice(280, 360), lat = slice(40, 80))
    else:
        var_pos = None
        var_neg = None
    return var_pos, var_neg
# %%
# %%
decade = int(sys.argv[1]) if len(sys.argv) > 1 else 1850
var = sys.argv[2] if len(sys.argv) > 2 else 'ua'
name = sys.argv[3] if len(sys.argv) > 3 else var
model_dir = sys.argv[4] if len(sys.argv) > 4 else 'MPI_GE_CMIP6'
suffix = sys.argv[5] if len(sys.argv) > 5 else ''

# report the input
logging.info(f"Rank {rank} of {size} is processing {var} for decade {decade}, model_dir {model_dir}, name {name}, suffix {suffix}")
# %%
members = np.arange(1, 51)  # all members
members_single = np.array_split(members, size)[rank]  # members on this core

# %%

theta_2PVU_poss = []
theta_2PVU_negs = []
for i, member in enumerate(members_single):
    print(f"Rank {rank}, member {member}/{members_single[-1]}")

    theta_2pvu_pos, theta_2pvu_neg = composite_single_ens(var, decade=decade, ens=member, name = name, suffix = suffix, model_dir=model_dir, plev = None)

    theta_2PVU_poss.append(theta_2pvu_pos)
    theta_2PVU_negs.append(theta_2pvu_neg)


# combine all members from all cores
theta_2PVU_poss = comm.gather(theta_2PVU_poss, root=0)
theta_2PVU_negs = comm.gather(theta_2PVU_negs, root=0)

# concatenate the results 
if rank == 0:

    # Flatten the gathered lists
    theta_2PVU_poss = [item for sublist in theta_2PVU_poss for item in sublist if item is not None]
    theta_2PVU_negs = [item for sublist in theta_2PVU_negs for item in sublist if item is not None]


    # concat the results
    theta_2PVU_poss = xr.concat(theta_2PVU_poss, dim='event')
    theta_2PVU_negs = xr.concat(theta_2PVU_negs, dim='event')

    # save the results
    save_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0composite_distribution/"

    theta_2PVU_poss.to_netcdf(f'{save_dir}{var}{suffix}_NAO_pos_{decade}.nc')
    theta_2PVU_negs.to_netcdf(f'{save_dir}{var}{suffix}_NAO_neg_{decade}.nc')