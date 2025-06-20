# %%
import src.dynamics.EP_flux as EP_flux_module
import importlib
import sys
import os

import logging
importlib.reload(EP_flux_module)
from src.dynamics.EP_flux import (  # noqa: E402
    EP_flux,
    eff_stat_stab_xr,
)

from src.data_helper.read_variable import read_climatology

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

#%%


def calculate_EP_flux(decade, equiv_theta=True, eddy='transient'):
    """
    Calculate EP flux for a given decade and phase
    """
    model_dir = "MPI_GE_CMIP6_allplev"
    # Read data
    logging.info (f"Read data for {decade}")

    # read temperature to compute static stability
    if eddy == 'transient':
        upvp = read_climatology(var = 'upvp',decade = decade, model_dir=model_dir)
        if equiv_theta:
            vptp = read_climatology(var = 'vpetp', decade = decade, model_dir=model_dir)
        else:
            vptp = read_climatology(var = 'vptp', decade = decade, model_dir=model_dir)

        ta = read_climatology(var = 'ta_hat', decade = decade, name = 'ta')
    elif eddy == 'steady':
        upvp = read_climatology(var = 'usvs', decade = decade, model_dir=model_dir)
        if equiv_theta:
            vptp = read_climatology(var = 'vsets', decade = decade, model_dir=model_dir)
        else:
            vptp = read_climatology(var = 'vsts', decade = decade, model_dir=model_dir)
        ta = read_climatology(var = 'ta_hat', decade = decade, name = 'ta')
    
    logging.info (f"Calculate {eddy} EP flux {decade}")
    save_dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0EP_flux/"

    # Calculate EP flux
    stat_stab = eff_stat_stab_xr(ta)
    F_phi, F_p, div_phi, div_p = EP_flux(vptp, upvp, stat_stab)

    # Save data
    logging.info (f"Save data for clima phase in {decade}")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    F_phi.to_netcdf(os.path.join(save_dir, f"{eddy}_F_phi_clima_{decade}.nc"))
    F_p.to_netcdf(os.path.join(save_dir, f"{eddy}_F_p_clima_{decade}.nc"))
    div_phi.to_netcdf(os.path.join(save_dir, f"{eddy}_div_phi_clima_{decade}.nc"))
    div_p.to_netcdf(os.path.join(save_dir, f"{eddy}_div_p_clima_{decade}.nc"))

#%%
for eddy in ['transient', 'steady']:
    for dec in [1850, 2090]:
        calculate_EP_flux(decade=dec, eddy=eddy, equiv_theta=True)
        logging.info(f"Finished calculating EP flux for {eddy} phase in {dec}")
# %%
