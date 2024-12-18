#%%
import xarray as xr
import numpy as np
import sys
import os
import glob
import logging
import mpi4py.MPI as MPI

logging.basicConfig(level=logging.INFO)
# %%
start_year = int(sys.argv[1])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()

#%%
files_tag=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/daily/projected_pc_decade_nonstd/r*i1p1f1/NAO_{start_year}-{start_year+9}_r*i1p1f1_nonstd.nc"
files = glob.glob(files_tag)
#%%
# check if files length==50
if rank == 0:
    if len(files) != 50:
        logging.ERROR(f"Files length is not 50, but {len(files)}")
        sys.exit()



# %%
# calculate the mean and std from all members and time
all_pcs = xr.open_mfdataset(files, combine = 'nested', concat_dim = 'member')

#%%
mean = all_pcs.pc.mean(dim = ('time','member'))
std = all_pcs.pc.std(dim = ('time','member'))
# %%
# standardize every member and save to a new folder with same name
files_single = np.array_split(files, size)[rank]  # files on this core

for file in files_single:
    out_file = file.replace("nonstd", "std")
    # make dir if not exist
    if rank == 0:
        if not os.path.exists(os.path.dirname(out_file)):
            os.makedirs(os.path.dirname(out_file))

    pc = xr.open_dataset(file).pc
    pc = (pc - mean) / std

    pc.to_netcdf(out_file)


# %%
