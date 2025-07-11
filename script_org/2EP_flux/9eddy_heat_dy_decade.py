#%%
# %%
import src.dynamics.EP_flux as EP_flux_module
import importlib
import sys
import os
import numpy as np

import logging
importlib.reload(EP_flux_module)
from src.dynamics.EP_flux import (  # noqa: E402
    EP_flux,
    eff_stat_stab_xr,
)
from src.data_helper.read_variable import read_prime_single_ens
from src.dynamics.EP_flux import E_div


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

#%%
def read_data_all_dec(decade, ens, eddy = 'transient', equiv_theta = True, **kwargs):
    """
    Read data for all members in a given decade
    """
    if eddy == 'transient':
        N = 'upvp'
        if equiv_theta:
            P = 'vpetp'
        else:
            P = 'vptp'
    elif eddy == 'steady':
        N = 'usvs'
        if equiv_theta:
            P = 'vsets'
        else:
            P = 'vpts'



    upvp = read_prime_single_ens(decade, ens, N, name = N,**kwargs) 
    vptp = read_prime_single_ens(decade, ens, P, name = P, **kwargs)

    
    return upvp, vptp


#%%



# %%
def cal_E_div(decade, ens, equiv_theta = True, eddy='transient',  suffix = ''):
    """
    Calculate the E-vector divergence for a given decade and phase
    """
    # Read data
    # Read data, just vptp is useful, M2 (or upvp here) is just for position
    M2, vptp = read_data_all_dec(decade, ens, eddy=eddy, model_dir='MPI_GE_CMIP6_allplev', suffix=suffix)


    # Calculate the divergence of the E-vector
    logging.info(f"Calculate E-vector divergence fo in {decade}")

    _, dvptpdy = E_div(M2, vptp)

    # save
    logging.info(f"Save data for in {decade}")
    save_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/eddy_heat_dy/r{ens}i1p1f1/"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # dM2dx.to_netcdf(os.path.join(save_dir, f"{eddy}_E_div_x_{phase}_{decade}.nc"))
    dvptpdy.to_netcdf(os.path.join(save_dir, f"{eddy}_eddy_heat_dy_{decade}_r{ens}i1pf1.nc"))
# %%

# %%
node = sys.argv[1]
ens = int(node)
# %%
#%%
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # [0,1,2,3,4,5,6,7,8,9]
    size = comm.Get_size()  # 10
except:
    logging.warning("::: Warning: Proceeding without mpi4py! :::")
    rank = 0
    size = 1
#%%
all_decades = np.arange(1850, 2100, 10)
single_decades = np.array_split(all_decades, size)[rank]
# %%
for i,dec in enumerate(single_decades):
    logging.info(f"rank {rank} Processing {i+1}/{len(single_decades)}")

    # calculate EP flux
    logging.info(f"Calculate transient eddy for {dec} of ens {ens}")

    cal_E_div(decade=dec, ens=ens, eddy='transient', suffix='')

    logging.info(f"Calculate steady eddy for {dec} of ens {ens}")
    cal_E_div(decade=dec, ens=ens, eddy='steady', suffix='')