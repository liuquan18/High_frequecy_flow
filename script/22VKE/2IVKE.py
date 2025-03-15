#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import sys
import logging
logging.basicConfig(level=logging.INFO)
# %%
member = sys.argv[1]
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
from_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/vke_daily/r{member}i1p1f1/'
to_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ivke_daily/r{member}i1p1f1/'

if rank == 0:
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    logging.info(f"This node is processing ensemble member {member}")


#%%
all_files = glob.glob(from_path + "*.nc")
files_core = np.array_split(all_files, size)[rank]

# %%
def ivke(vke):
    # vke = vke.sortby('plev', ascending=False) # make sure plev is in descending order, p_B is larger than p_T
    d_vke_dp = vke.differentiate('plev')
    ivke = d_vke_dp.integrate('plev')
    ivke = ivke / 9.81
    ivke.name = 'ivke'
    return ivke
# %%
for i, file in enumerate(files_core):
    logging.info(f"rank {rank} Processing {i+1}/{len(files_core)}")
    ds = xr.open_dataset(file)
    ds = ds.sortby('plev', ascending=True)

    ds = ivke(ds['vke'])
    
    ds.to_netcdf(file.replace('vke', 'ivke'))
    ds.close()
# %%
