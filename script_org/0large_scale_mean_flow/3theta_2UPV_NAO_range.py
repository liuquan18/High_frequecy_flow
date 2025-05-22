#%%
import xarray as xr
import numpy as np
from src.data_helper.read_NAO_extremes import read_NAO_extremes_single_ens
from src.composite import composite
from src.data_helper import read_variable
import sys
from src.dynamics.theta_on_pv import theta_on_2pvu
import logging
logging.basicConfig(level=logging.INFO)
import importlib
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
def composite_single_ens(var, decade, ens, plev = None, **kwargs):
    
    # read NAO extremes
    pos_extreme = read_NAO_extremes_single_ens('pos', decade, ens)
    neg_extreme = read_NAO_extremes_single_ens('neg', decade, ens)

    # read variable
    name = kwargs.get('name', var)  # default name is the same as var')
    var_field = read_prime_single_ens(var, decade, ens, name = name, plev = plev, **kwargs)

    if not pos_extreme.empty and not neg_extreme.empty:

        var_pos, var_neg = range_NAO_composite(var_field, pos_extreme, neg_extreme)

        # average over the event
        var_pos = var_pos.mean(dim='event')
        var_neg = var_neg.mean(dim='event')

    return var_pos, var_neg
# %%
decade = int(sys.argv[1]) if len(sys.argv) > 1 else 1850
# %%
members = np.arange(1, 51)  # all members
members_single = np.array_split(members, size)[rank]  # members on this core

# %%

theta_2PVUs = []
for i, member in enumerate(members_single):
    print(f"Rank {rank}, member {member}/{members_single[-1]}")

    ua_pos, ua_neg = composite_single_ens('ua', decade, member, suffix = '')

    va_pos, va_neg = composite_single_ens('va', decade, member, suffix = '')

    theta_pos, theta_neg = composite_single_ens('theta', decade, member, suffix = '')

    #  drop na along time dimension
    theta_2PVU_pos = theta_on_2pvu(theta_pos, ua_pos, va_pos)
# %%
