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
importlib.reload(composite)
importlib.reload(read_variable)
read_prime_single_ens = read_variable.read_prime_single_ens
range_NAO_composite = composite.range_NAO_composite
range_NAO_composite_single_phase = composite.range_NAO_composite_single_phase
#%%
import mpi4py.MPI as MPI
# %%
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()
#%%
def composite_single_ens(var, decade, ens, plev = None, method = 'sum', **kwargs):
    
    # read NAO extremes
    pos_extreme = read_NAO_extremes_single_ens('pos', decade, ens, dur_threshold=8)
    neg_extreme = read_NAO_extremes_single_ens('neg', decade, ens, dur_threshold=8)
    # read variable
    var_field = read_prime_single_ens( decade, ens,var, **kwargs)
    
    # select plev 
    if not pos_extreme.empty:
        pos_extreme = pos_extreme[pos_extreme['plev'] == plev] if plev is not None else pos_extreme
        # postive composite
        var_pos = range_NAO_composite_single_phase(var_field, pos_extreme)
        var_pos = var_pos.sum(dim='event') # sum over the event
    else:
        var_pos = None
    if not neg_extreme.empty:
        neg_extreme = neg_extreme[neg_extreme['plev'] == plev] if plev is not None else neg_extreme
        # negative composite
        var_neg = range_NAO_composite_single_phase(var_field, neg_extreme)
        var_neg = var_neg.sum(dim='event')  # sum over the event
    else:
        var_neg = None
    return var_pos, var_neg
# %%
decade = int(sys.argv[1]) if len(sys.argv) > 1 else 1850
var = sys.argv[2] if len(sys.argv) > 2 else 'ua'
name = sys.argv[3] if len(sys.argv) > 3 else var
suffix = sys.argv[4] if len(sys.argv) > 4 else ''
# %%
members = np.arange(1, 51)  # all members
members_single = np.array_split(members, size)[rank]  # members on this core

# %%

theta_2PVU_poss = []
theta_2PVU_negs = []
for i, member in enumerate(members_single):
    print(f"Rank {rank}, member {member}/{members_single[-1]}")

    theta_2pvu_pos, theta_2pvu_neg = composite_single_ens(var, decade=decade, ens=member, name = name, suffix = suffix)

    theta_2PVU_poss.append(theta_2pvu_pos)
    theta_2PVU_negs.append(theta_2pvu_neg)


# combine all members from all cores
theta_2PVU_poss = comm.gather(theta_2PVU_poss, root=0)
theta_2PVU_negs = comm.gather(theta_2PVU_negs, root=0)

# concatenate the results 
if rank == 0:

    # Flatten the gathered lists
    theta_2PVU_poss = [item for sublist in theta_2PVU_poss for item in sublist]
    theta_2PVU_negs = [item for sublist in theta_2PVU_negs for item in sublist]

    theta_2PVU_poss = xr.concat(theta_2PVU_poss, dim='ens', coords = 'all')
    theta_2PVU_negs = xr.concat(theta_2PVU_negs, dim='ens', coords = 'all')

    # save the results
    theta_2PVU_poss.to_netcdf(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_distribution/{var}{suffix}_NAO_pos_{decade}.nc')
    theta_2PVU_negs.to_netcdf(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_distribution/{var}{suffix}_NAO_neg_{decade}.nc')
# %%
