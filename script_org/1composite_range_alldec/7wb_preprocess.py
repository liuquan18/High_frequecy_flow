#%%
import xarray as xr
import numpy as np
import glob
import os

from src.data_helper.read_variable import read_prime_single_ens

# year 1850 and 2090, no sum over isen_level yet, replace the data with summed results
#%%
base_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_anticyclonic_allisen_daily/"

for decade in [1850, 2090]:
    for ens in range(1, 51):
        # find original file path
        files = glob.glob(base_dir + f"r{ens}i1p1f1/*{decade}*.nc")
        if len(files) == 0:
            print(f"No file found for decade {decade}, ens {ens}, skipping")
            continue
        file_path = files[0]

        # read, sum over isen_level, and save back
        ds = xr.open_dataset(file_path)
        if "isen_level" not in ds.dims:
            print(f"Decade {decade}, Ensemble {ens}, already summed, skipping")
            ds.close()
            continue
        ds_sum = ds.sum(dim="isen_level", skipna=True)
        ds.close()

        tmp_path = file_path + ".tmp"
        ds_sum.to_netcdf(tmp_path)
        os.replace(tmp_path, file_path)
        print(f"Decade {decade}, Ensemble {ens}, summed and saved to {file_path}")

# %%
