#%%
import xarray as xr
import numpy as np
from metpy.units import units
import os
import sys
import metpy
import metpy.calc as mpcalc
from src.data_helper.read_variable import read_prime_single_ens
import glob
import logging
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#%%
simulations = sys.argv[1] # 'vco2_4xco2_land', 'vco2_4xco2_ocean', 'vco2_4xco2_all'

#%%
def second_derivative_heat(vptp):
    """
    Calculate the second derivative of heat flux with respect to latitude
    """

    # metpy
    vptp = vptp.metpy.assign_crs(
            grid_mapping_name='latitude_longitude',
            earth_radius=6371229.0
        )
    vptp = vptp * units('K m s-1')
    
    # Calculate the second derivative with respect to latitude
    dx, dy = mpcalc.lat_lon_grid_deltas(vptp.lon, vptp.lat)
    # second derivative on y
    d2vptpdy2 = mpcalc.second_derivative(vptp, dy=dy, axis=2)

    d2vptpdy2.name = 'eddy_heat_d2y2'

    d2vptpdy2 = d2vptpdy2.metpy.dequantify()
    d2vptpdy2 = d2vptpdy2.drop_vars('metpy_crs')

    return d2vptpdy2

#%%
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


#%%
for i, member in enumerate(ens_core):
    logging.info(f"rank {rank} Processing ensemble member {member} {i+1}/{len(ens_core)}")

    
    v_hat_path = f"/scratch/m/m300883/{simulations}/v_hat_monmean/ens_{member}/"
    etheta_hat_path = f"/scratch/m/m300883/{simulations}/equiv_theta_hat_monmean/ens_{member}/"
    to_path = f"/scratch/m/m300883/{simulations}/second_heat_monmean/ens_{member}/"

    if 'mlo' in simulations:
            v_hat_path = f"/scratch/m/m300883/{simulations}/v_hat_monmean/mlo_{member}/"
            etheta_hat_path = f"/scratch/m/m300883/{simulations}/equiv_theta_hat_monmean/mlo_{member}/"
            to_path = f"/scratch/m/m300883/{simulations}/second_heat_monmean/mlo_{member}/"

    if not os.path.exists(to_path):
        os.makedirs(to_path)
    logging.info(f"This node is processing ensemble member {member}")

    v_hat_file = glob.glob(v_hat_path + "*.nc")
    etheta_hat_file = glob.glob(etheta_hat_path + "*.nc")
    v_hat_file = v_hat_file[0]
    etheta_hat_file = etheta_hat_file[0]
    basename = os.path.basename(v_hat_file)
    # replace the 'v' in basename with 'second_heat'
    basename = basename.replace("v_", "second_heat_")
    to_file = os.path.join(to_path, basename)

    v_hat = xr.open_dataset(v_hat_file).v_hat
    etheta_hat = xr.open_dataset(etheta_hat_file).etheta_hat

    # calculate eddy heat flux
    vptp = v_hat * etheta_hat

    logging.info("   calculating second derivative of heat flux...")
    d2vptpdy2 = second_derivative_heat(vptp)

    ds = d2vptpdy2.to_dataset(name="eddy_heat_d2y2")

    # save to netcdf
    ds.to_netcdf(to_file)
    ds.close()