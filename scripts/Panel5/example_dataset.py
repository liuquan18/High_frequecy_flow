#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
# %%
import src.blocking.block_index as block_index


# %%
ens = '0080'

#%%
month = ["Jun", "Jul", "Aug"]
files_globes = []
for mm in month:
    odir = f"/work/mh0033/m300883/Tel_MMLE/data/MPI_GE_onepct_30_daily/zg_{mm}/"
    files_globe = glob.glob(odir + f"*ens_{ens}*.nc")
    files_globe.sort()
    files_globes.append(files_globe)
# %%
zg_JJA = xr.open_mfdataset(files_globes[0])
# %%
example_zg = zg_JJA.isel(time = slice(0,30))
# %%
example_zg.to_netcdf(f"/work/mh0033/m300883/High_frequecy_flow/data/example_blocking_event/zg{ens}_first30.nc")
# %%
