#%%
import xarray as xr
import numpy as np
import glob
# %%
period = "last10"
# %%
# calculate the mean and std from all members and time
all_pcs = xr.open_mfdataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/daily/projected_pc_{period}_nonstd/troposphere*.nc", 
                            combine = 'nested', concat_dim = 'member')

#%%
mean = all_pcs.pc.mean(dim = ('time','member'))
std = all_pcs.pc.std(dim = ('time','member'))
# %%
# standardize every member and save to a new folder with same name
from_folder = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/daily/projected_pc_{period}_nonstd/"
to_folder = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_{period}/"

for file in glob.glob(from_folder + "*.nc"):
    member = file.split("_")[-2]
    pc = xr.open_dataset(file).pc
    pc = (pc - mean) / std

    pc.to_netcdf(to_folder + file.split("/")[-1][:-10]+".nc")

# %%
