#%%
import xarray as xr
import numpy as np
import glob
import sys
# %%
decade = sys.argv[1] # 1850
# %%
# calculate the mean and std from all members and time
all_pcs = xr.open_mfdataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NAO_pc_{dec}_trop_nonstd/*.nc", 
                            combine = 'nested', concat_dim = 'member')

#%%
mean = all_pcs.pc.mean(dim = ('time','member'))
std = all_pcs.pc.std(dim = ('time','member'))
# %%
# standardize every member and save to a new folder with same name
from_folder = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NAO_pc_{decade}_trop_nonstd/"
to_folder =  f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NAO_pc_{decade}_trop_std/"

for file in glob.glob(from_folder + "*.nc"):
    # outname = file replace "nonstd" with "std"
    outname=to_folder+file.split("/")[-1].replace("nonstd","std")

    pc = xr.open_dataset(file).pc
    pc = (pc - mean) / std

    pc.to_netcdf(outname)

# %%
