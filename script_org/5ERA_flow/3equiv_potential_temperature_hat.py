#%%
import xarray as xr
import numpy as np
import os
import sys
import logging
import glob
import pandas as pd
logging.basicConfig(level=logging.INFO)
# %%
import src.dynamics.EP_flux as EP_flux
import importlib
importlib.reload(EP_flux)

# %%
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # [0,1,2,3,4,5,6,7,8,9]
    size = comm.Get_size()  # 10
    logging.info(f"Running on rank {rank} of {size} total ranks.")
except:
    logging.warning("::: Warning: Proceeding without mpi4py! :::")
    rank = 0
    size = 1
#%%
# from temperature to potential temperature
ta_path = '/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/ta_hat_daily/'
q_path = '/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/hus_hat_daily/'
to_path = '/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/equiv_theta_hat_daily/'

if rank == 0:
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    logging.info("This node is processing equivalent potential temperature hat")

# %%
all_decs = np.arange(1979, 2024)
dec_core = np.array_split(all_decs, size)[rank]

# %%
for i, dec in enumerate (dec_core):
    logging.info(f"rank {rank} Processing decade {dec} {i+1}/{len(dec_core)}")
    ta_file = glob.glob(ta_path + f"*{dec}*.nc")
    q_file = glob.glob(q_path + f"*{dec}*.nc")
    ta_file = ta_file[0]
    q_file = q_file[0]
    basename = os.path.basename(ta_file)
    # replace the 'ta' in basename with 'theta'
    basename = basename.replace('ta', 'equiv_theta')
    to_file = os.path.join(to_path, basename)

    t = xr.open_dataset(ta_file).var130
    q = xr.open_dataset(q_file).var133

    # change the time to datetime64[ns]
    # Convert time values like 19790501.979167 to datetime64[ns] with daily frequency
    if not np.issubdtype(t['time'].dtype, np.datetime64):
        t_dates = pd.to_datetime(t['time'].astype(int).astype(str), format='%Y%m%d')
        t['time'] = t_dates
        q['time'] = t_dates  # Ensure q has the same time index
    else:
        t_dates = t['time']
        q['time'] = t_dates

    # make sure the time dimension is the same
    if t.shape[0] != q.shape[0]:
        logging.warning(f"::: Warning: time dimension of {ta_file} and {q_file} do not match! :::")
        continue

    # calculate equivalent potential temperature
    ds = EP_flux.equivalent_potential_temperature(t, q, p='plev', p0=1e5)
    # save to netcdf
    ds.to_netcdf(to_file)
    ds.close()