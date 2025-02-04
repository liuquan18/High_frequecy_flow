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
logging.info(f"This node is working on year {start_year} - {start_year+9}")

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()

#%%
files_tag=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NAO_pc_decade_nonstd/r*i1p1f1/NAO_{start_year}-{start_year+9}_r*i1p1f1_nonstd.nc"
files = glob.glob(files_tag)
#%%
# check if files length==50
if rank == 0:
    if len(files) != 50:
        logging.ERROR(f"Files length is not 50, but {len(files)}")
        sys.exit()

    import os

    # Base directory where the folders will be created
    base_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NAO_pc_decade_std"

    # Create folders with names r{number}i1p1f1 where number ranges from 1 to 50
    for number in range(1, 51):
        folder_name = f"r{number}i1p1f1"
        folder_path = os.path.join(base_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")



# %%
# calculate the mean and std from all members and time
all_pcs = xr.open_mfdataset(files, combine = 'nested', concat_dim = 'member')

#%%
mean = all_pcs.pc.mean(dim = ('time','member'))
std = all_pcs.pc.std(dim = ('time','member'))
# %%
# standardize every member and save to a new folder with same name
files_single = np.array_split(files, size)[rank]  # files on this core

for i, file in enumerate(files_single):
    logging.info(f"Rank {rank} {i+1}/{len(files_single)}")

    out_file = file.replace("nonstd", "std")

    pc = xr.open_dataset(file).pc
    pc = (pc - mean) / std

    pc.to_netcdf(out_file)


# %%
