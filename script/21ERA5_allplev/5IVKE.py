# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)

# %%
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
model="ERA5_ano"
from_path = "/work/mh0033/m300883/High_frequecy_flow/data/${model}/vke_daily/"
to_path = "/work/mh0033/m300883/High_frequecy_flow/data/${model}/ivke_daily/"

if rank == 0:
    if not os.path.exists(to_path):
        os.makedirs(to_path)


# %%
all_files = glob.glob(from_path + "*.nc")
files_core = np.array_split(all_files, size)[rank]

# %%
def ivke(vke):
    d_vke_dp = vke.differentiate("plev")
    ivke = d_vke_dp.integrate("plev")
    ivke =  ivke / 9.81
    ivke.name = "ivke"
    return ivke


# %%
for i, file in enumerate(files_core):
    logging.info(f"rank {rank} Processing {i+1}/{len(files_core)}")
    ds = xr.open_dataset(file, chunks={"time": 1})
    ds = ds.sortby("plev", ascending=True)

    ds = ivke(ds["vke"])

    ds.to_netcdf(file.replace("vke", "ivke"))
    ds.close()
# %%
