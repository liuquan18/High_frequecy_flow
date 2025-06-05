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
    read_data_all,
)



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

#%%


def calculate_EP_flux(decade, phase, ano=False, equiv_theta=True, eddy='transient'):
    """
    Calculate EP flux for a given decade and phase
    """
    # Read data
    logging.info (f"Read data for {phase} phase in {decade}")
    upvp, vptp, ta = read_data_all(decade, phase, equiv_theta=equiv_theta, eddy=eddy)

    logging.info (f"Calculate {eddy} EP flux for {phase} phase in {decade}")
    save_dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0EP_flux/"

    # Calculate EP flux
    stat_stab = eff_stat_stab_xr(ta)
    F_phi, F_p, div_phi, div_p = EP_flux(vptp, upvp, stat_stab)

    # Save data
    logging.info (f"Save data for {phase} phase in {decade}")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    F_phi.to_netcdf(os.path.join(save_dir, f"{eddy}_F_phi_{phase}_{decade}_ano{ano}.nc"))
    F_p.to_netcdf(os.path.join(save_dir, f"{eddy}_F_p_{phase}_{decade}_ano{ano}.nc"))
    div_phi.to_netcdf(os.path.join(save_dir, f"{eddy}_div_phi_{phase}_{decade}_ano{ano}.nc"))
    div_p.to_netcdf(os.path.join(save_dir, f"{eddy}_div_p_{phase}_{decade}_ano{ano}.nc"))

#%%
phase = sys.argv[1] # 'pos' or 'neg'
decade = sys.argv[2] # '1850' or '2090'
eddy = sys.argv[3]
ano = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else False  # Convert string to boolean, default is False

#%%
if __name__ == "__main__":
    # Summary of the input
    logging.info(f"Phase: {phase}")
    logging.info(f"Decade: {decade}")
    logging.info(f"Eddy: {eddy}")
    logging.info(f"Anomaly: {ano}")
    
    # Calculate EP flux for NAO pos and neg phase
    calculate_EP_flux(decade, phase, ano=ano, equiv_theta=True, eddy=eddy)

# %%
