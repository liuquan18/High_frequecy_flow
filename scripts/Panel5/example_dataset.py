#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
# %%
import src.blocking.block_index as block_index


# %%
# ens range from 0069 to 0100
for ens in range(86,101):
    print(ens)
    month = ["Jun", "Jul", "Aug"]
    files_globes = []
    for mm in month:
        odir = f"/work/mh0033/m300883/Tel_MMLE/data/MPI_GE_onepct_30_daily/zg_{mm}/"
        files_globe = glob.glob(odir + f"*{ens}*.nc")
        files_globe.sort()
        files_globes.append(files_globe)
    zg_JJA = xr.open_mfdataset(files_globes[0])
    zg_JJA = zg_JJA.isel(time = slice(0,30))
    zg_JJA.to_netcdf(f"/work/mh0033/m300883/High_frequecy_flow/data/example_blocking_event/zg{ens}_first30.nc")

#%%
