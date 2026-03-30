# %%
import numpy as np
import xarray as xr
import glob
import matplotlib.pyplot as plt
import tqdm
from metpy.calc import first_derivative
from metpy.units import units

# %%
base_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/vsts_space_time_spectra_daily/"


# %%
def dec_mean(ens, decade):
    wb_dir = f"{base_dir}r{ens}i1p1f1/dec_{decade}/*.nc"
    wb_files = glob.glob(wb_dir)

    wb_data = xr.open_mfdataset(
        wb_files, combine="nested", parallel=True, concat_dim="year"
    )
    wb_data = wb_data.mean(dim="year")
    save_dir = (
        f"/scratch/m/m300883/MPI_GE_CMIP6/vsts_space_time_spectra_daily/r{ens}i1p1f1/"
    )
    wb_data["ens"] = ens
    wb_data.to_netcdf(f"{save_dir}vsts_kp_kn_dec_{decade}_r{ens}i1p1f1.nc")


# %%
for ens in tqdm.tqdm(range(1, 51)):
    dec_mean(ens, 1850)
    dec_mean(ens, 2090)

# #%%
# def read_dec(decade):
#     wb_dir = "/scratch/m/m300883/MPI_GE_CMIP6/vsts_space_time_spectra_daily/r*i1p1f1/"

#     wb_files = glob.glob(wb_dir+"*.nc")

#     wb_data = xr.open_mfdataset(
#         wb_files, combine="nested", parallel=True, concat_dim="ens"
#     )
#     wb_data = wb_data.mean(dim="ens")
#     wb_data["decade"] = decade
#     return wb_data.compute()

# # %%
# vsts_1850 = read_dec(1850)
# vsts_2090 = read_dec(2090)
