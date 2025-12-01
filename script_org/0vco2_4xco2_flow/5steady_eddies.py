# %%
import xarray as xr
import numpy as np
import os
import sys
import logging
import glob

logging.basicConfig(level=logging.INFO)
# %%
import src.dynamics.EP_flux as EP_flux
import importlib

importlib.reload(EP_flux)
# %%
simulations = sys.argv[1] # 'vco2_4xco2_land', 'vco2_4xco2_ocean', 'vco2_4xco2_all'
var = sys.argv[2]  # 'etheta'
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
all_ens = [f"{i:02d}" for i in range(1, 25)]
ens_core = np.array_split(all_ens, size)[rank]

# %%
for i, member in enumerate(ens_core):
    logging.info(f"rank {rank} Processing ensemble member {member} {i+1}/{len(ens_core)}")

    # from temperature to potential temperature
    thetae_path = f"/scratch/m/m300883/{simulations}/{var}_monmean/ens_{member}/"
    to_path = f"/scratch/m/m300883/{simulations}/{var}_hat_monmean/ens_{member}/"

    if 'mlo' in simulations:
        thetae_path = f"/scratch/m/m300883/{simulations}/{var}_monmean/mlo_{member}/"
        to_path = f"/scratch/m/m300883/{simulations}/{var}_hat_monmean/mlo_{member}/"

    if not os.path.exists(to_path):
        os.makedirs(to_path)
    logging.info(f"This node is processing ensemble member {member}")

    thetae_file = glob.glob(thetae_path + "*.nc")
    thetae_file = thetae_file[0]
    basename = os.path.basename(thetae_file)
    # replace the 'ta' in basename with 'theta'
    basename = basename.replace("t_", "equiv_theta_")
    to_file = os.path.join(to_path, basename)

    variable_name = var
    if var == 'equiv_theta':
        variable_name = 'etheta'

    thetae = xr.open_dataset(thetae_file)[variable_name]


    # calculate equivalent potential temperature
    thetae_mean = thetae.mean(dim='lon')
    thetae_hat = thetae - thetae_mean

    ds = thetae_hat.to_dataset(name="etheta_hat")

    # save to netcdf
    ds.to_netcdf(to_file)
    ds.close()
