#%%
import xarray as xr
import numpy as np

from src.dynamics.theta_on_pv import theta_on_2pvu
from src.data_helper.read_variable import read_prime_single_ens
# %%
import logging
import os
import glob
import sys

logging.basicConfig(level=logging.INFO)





# %%
node = sys.argv[1]
ens = int(node)
logging.info(f"Processing ensemble {ens}")
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
# %%
ua_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily/r{ens}i1p1f1/"
va_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily/r{ens}i1p1f1/"
theta_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/theta_daily/r{ens}i1p1f1/"

# save path
theta_2pvu_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/theta_2pvu_daily/r{ens}i1p1f1/"
if rank == 0:
    if not os.path.exists(theta_2pvu_path):
        os.makedirs(theta_2pvu_path)

# %%
all_decades = np.arange(1850, 2100, 10)
single_decades = np.array_split(all_decades, size)[rank]
# %%
for i, dec in enumerate(single_decades):
    logging.info(f"rank {rank} Processing {i+1}/{len(single_decades)}")

    # read data
    ua_file = glob.glob(ua_path + f"*{dec}*.nc")
    va_file = glob.glob(va_path + f"*{dec}*.nc")
    theta_file = glob.glob(theta_path + f"*{dec}*.nc")

    ua = xr.open_dataset(ua_file[0]).ua
    va = xr.open_dataset(va_file[0]).va
    theta = xr.open_dataset(theta_file[0]).theta

    # calculate theta on 2PVU
    theta_2pvu = theta_on_2pvu(theta, ua, va)

    # save data
    theta_2pvu.to_netcdf(
        theta_2pvu_path + f"theta_2pvu_day_MPI-ESM1-2-LR_r{ens}i1p1f1_gn_{dec[0]}0502-{dec[-1]+9}0930.nc"
    )