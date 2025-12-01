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
all_ens = [f"{i:02d}" for i in range(1, 24)]
ens_core = np.array_split(all_ens, size)[rank]

# %%
for i, member in enumerate(ens_core):
    logging.info(f"rank {rank} Processing ensemble member {member} {i+1}/{len(ens_core)}")

    # from temperature to potential temperature
    ta_path = f"/scratch/m/m300883/{simulations}/t_monmean/ens_{member}/"
    q_path = f"/scratch/m/m300883/{simulations}/q_monmean/ens_{member}/"
    to_path = f"/scratch/m/m300883/{simulations}/equiv_theta_monmean/ens_{member}/"

    if rank == 0:
        if not os.path.exists(to_path):
            os.makedirs(to_path)
        logging.info(f"This node is processing ensemble member {member}")

    ta_file = glob.glob(ta_path + "*.nc")
    q_file = glob.glob(q_path + "*.nc")
    ta_file = ta_file[0]
    q_file = q_file[0]
    basename = os.path.basename(ta_file)
    # replace the 'ta' in basename with 'theta'
    basename = basename.replace("t_", "equiv_theta_")
    to_file = os.path.join(to_path, basename)

    t = xr.open_dataset(ta_file).t
    q = xr.open_dataset(q_file).q
    # make sure the time dimension is the same
    if t.shape[0] != q.shape[0]:
        logging.warning(
            f"::: Warning: time dimension of {ta_file} and {q_file} do not match! :::"
        )
        continue

    # calculate equivalent potential temperature
    ds = EP_flux.equivalent_potential_temperature(t, q, p="plev", p0=1e5)
    # save to netcdf
    ds.to_netcdf(to_file)
    ds.close()
