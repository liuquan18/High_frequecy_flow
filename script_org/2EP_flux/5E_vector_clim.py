# %%
import src.dynamics.EP_flux as EP_flux_module
import importlib
import sys
import os

import logging
importlib.reload(EP_flux_module)
from src.dynamics.EP_flux import (  # noqa: E402
    E_div
)

from src.data_helper.read_variable import read_climatology

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

#%%

def cal_E_div(decade, eddy='transient', **kwargs):
    """
    Calculate the E-vector divergence for a given decade and phase
    """
    # Read data
    logging.info(f"Read data for climatology in {decade}")

    if eddy == 'transient':
        M2 = read_climatology(var = 'M2_prime', decade = decade, model_dir='MPI_GE_CMIP6_allplev', name = 'M2')
        upvp = read_climatology(var = 'upvp', decade = decade, model_dir='MPI_GE_CMIP6_allplev')
    else:
        M2 = read_climatology(var = 'M2_steady', decade = decade, model_dir='MPI_GE_CMIP6_allplev', name = 'M2')
        upvp = read_climatology(var = 'usvs', decade = decade, model_dir='MPI_GE_CMIP6_allplev')
    # Calculate the divergence of the E-vector
    logging.info(f"Calculate E-vector divergence for climatology in {decade}")

    dM2dx, dupvpdy = E_div(M2, upvp, **kwargs)

    # save
    logging.info(f"Save data for climatolgoy in {decade}")
    save_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0EP_flux/"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    dM2dx.to_netcdf(os.path.join(save_dir, f"{eddy}_E_div_x_clima_{decade}.nc"))
    dupvpdy.to_netcdf(os.path.join(save_dir, f"{eddy}_E_div_y_clima_{decade}.nc"))

#%%
for eddy in ['transient', 'steady']:
    for dec in [1850, 2090]:
        cal_E_div(decade=dec, eddy=eddy)
        logging.info(f"Finished calculating E vector for {eddy} phase in {dec}")
# %%
