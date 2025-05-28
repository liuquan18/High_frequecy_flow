# %%
import src.dynamics.EP_flux as EP_flux_module
import importlib

importlib.reload(EP_flux_module)
from src.dynamics.EP_flux import (  # noqa: E402
    EP_flux,
    eff_stat_stab_xr,
    read_data_all,
    plev_to_isentrope
)


import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

import sys
import os

#%%
def EP_flux_isen(vptp, upvp, theta=None, isentrope=False):
    """
    vptp: v't'
    upvp: u'v'
    theta: ensemble mean of (equivalent) potential temperature
    """

    stat_stab = eff_stat_stab_xr(theta)
    # change from /ha to /hpa
    stat_stab = stat_stab * 100

    # EP flux
    F_phi, F_p, div = EP_flux(
        vptp,
        upvp,
        stat_stab,
    ) # the plev is already in hPa

    if isentrope:
        # theta must given
        if theta is None:
            logging.error("theta must be given if isentrope is True")
        else:
            # check if theta is in hPa
            if theta.plev.max() > 1000:
                logging.warning(
                    "theta is in Pa, convert to hPa"
                )
                theta["plev"] = theta["plev"] / 100
        # convert to isentropes
        F_phi = plev_to_isentrope(F_phi, theta, var_name="F_phi", theta_name="etheta")
        F_p = plev_to_isentrope(F_p, theta, var_name="F_p", theta_name="etheta")
        div = plev_to_isentrope(div, theta, var_name="div", theta_name="etheta")

    return F_phi, F_p, div

def calculate_EP_flux(decade, phase, ano=False, equiv_theta=True, isentrope=True, eddy='transient'):
    """
    Calculate EP flux for a given decade and phase
    """
    # Read data
    logging.info (f"Read data for {phase} phase in {decade}")
    upvp, vptp, theta = read_data_all(decade, phase, ano=ano, equiv_theta=equiv_theta, eddy=eddy)

    # Determine save directory based on isentrope flag
    if isentrope:
        logging.info (f"Calculate EP flux on isentropes for {phase} phase in {decade}")
        save_dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0EP_flux_isen/"
    else:
        logging.info (f"Calculate EP flux for {phase} phase in {decade}")
        save_dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0EP_flux/"
    
    # Calculate EP flux
    F_phi, F_p, div = EP_flux_isen(vptp, upvp, theta, isentrope=isentrope)

    # Save data
    logging.info (f"Save data for {phase} phase in {decade}")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    F_phi.to_netcdf(os.path.join(save_dir, f"{eddy}_F_phi_{phase}_{decade}_ano{ano}.nc"))
    F_p.to_netcdf(os.path.join(save_dir, f"{eddy}_F_p_{phase}_{decade}_ano{ano}.nc"))
    div.to_netcdf(os.path.join(save_dir, f"{eddy}_div_{phase}_{decade}_ano{ano}.nc"))
    
#%%
phase = sys.argv[1] # 'pos' or 'neg'
decade = sys.argv[2] # '1850' or '2090'
isentrope = sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else False  # Convert string to boolean
if isentrope:
    logging.warning("Isentrope should be calculated after False manually, this is not implemented yet.")
eddy = sys.argv[4]
ano = sys.argv[5].lower() == 'true' if len(sys.argv) > 5 else False  # Convert string to boolean, default is False

#%%
if __name__ == "__main__":
    # Summary of the input
    logging.info(f"Phase: {phase}")
    logging.info(f"Decade: {decade}")
    logging.info(f"Isentrope: {isentrope}")
    logging.info(f"Eddy: {eddy}")
    logging.info(f"Anomaly: {ano}")
    
    # Calculate EP flux for NAO pos and neg phase
    calculate_EP_flux(decade, phase, ano=ano, equiv_theta=True, isentrope=isentrope, eddy=eddy)
