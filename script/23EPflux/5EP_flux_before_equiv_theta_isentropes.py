# %%
import src.EP_flux.EP_flux as EP_flux_module
import importlib

importlib.reload(EP_flux_module)
from src.EP_flux.EP_flux import (  # noqa: E402
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
def EP_flux_isen(vptp, upvp, theta=None, isentrope=True):
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

def calculate_EP_flux(decade, phase, ano=False, equiv_theta=True, isentrope=True):
    """
    Calculate EP flux for a given decade and phase
    """
    # Read data
    upvp, vptp, theta = read_data_all(decade, phase, ano=ano, equiv_theta=equiv_theta)


    if isentrope:
        # Calculate EP flux
        F_phi, F_p, div = EP_flux_isen(vptp, upvp, theta)
        save_dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0EP_flux_isen/"
    else:
        # Calculate EP flux
        F_phi, F_p, div = EP_flux(vptp, upvp)
        save_dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0EP_flux/"

    # save data
    F_phi.to_netcdf(save_dir + f"F_phi_{phase}_{decade}.nc")
    F_p.to_netcdf(save_dir + f"F_p_{phase}_{decade}.nc")
    div.to_netcdf(save_dir + f"div_{phase}_{decade}.nc")
    
#%%
phase = sys.argv[1] # 'pos' or 'neg'
decade = sys.argv[2] # '1850' or '2090'

if __name__ == "__main__":
    # Calculate EP flux for NAO pos and neg phase
    calculate_EP_flux(decade, phase, ano=True, equiv_theta=True, isentrope=True)
    logging.info(f"EP flux for {phase} phase in {decade} calculated")
