# %%
import src.EP_flux.EP_flux as EP_flux_module
import importlib
import xarray as xr
import glob

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

#%%

def calculate_EP_flux(decade, equiv_theta=True, isentrope=True):
    """
    Calculate EP flux for a given decade and phase
    """
    # path
    logging.info (f"Read data for ensmean in {decade}")
    upvp_path = glob.glob(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/upvp_monthly_ensmean/*{decade}*.nc")[0]
    if equiv_theta:
        vptp_path = glob.glob(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vpetp_monthly_ensmean/*{decade}*.nc")[0]
        theta_path = glob.glob(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/equiv_theta_monthly_ensmean/*{decade}*.nc")[0]
    else:
        vptp_path = glob.glob(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vptp_monthly_ensmean/*{decade}*.nc")[0]
        theta_path = glob.glob(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/theta_monthly_ensmean/*{decade}*.nc")[0]

    # read data
    upvp = xr.open_dataset(upvp_path)
    vptp = xr.open_dataset(vptp_path)
    theta = xr.open_dataset(theta_path)
    try:
        upvp = upvp.ua
    except AttributeError:
        upvp = upvp.upvp
    try:
        vptp = vptp.vpetp
    except AttributeError:
        vptp = vptp.vptp
    try:
        theta = theta.etheta
    except AttributeError:
        theta = theta.theta

    # ensemble and time mean (different months)
    if 'time' in upvp.dims:
        upvp = upvp.mean(dim ='time')
    if 'time' in vptp.dims:
        vptp = vptp.mean(dim ='time')
    if 'time' in theta.dims:
        theta = theta.mean(dim ='time')

    # convert to hPa
    if upvp.plev.max() > 1000:
        logging.warning(
            "upvp is in Pa, convert to hPa"
        )
        upvp["plev"] = upvp["plev"] / 100
    if vptp.plev.max() > 1000:
        logging.warning(
            "vptp is in Pa, convert to hPa"
        )
        vptp["plev"] = vptp["plev"] / 100
    if theta.plev.max() > 1000:
        logging.warning(
            "theta is in Pa, convert to hPa"
        )
        theta["plev"] = theta["plev"] / 100

    
    # Determine save directory based on isentrope flag
    if isentrope:
        logging.info (f"Calculate EP flux on isentropes for ensmean in {decade}")
        save_dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0EP_flux_isen/"
    else:
        logging.info (f"Calculate EP flux for ensmean in {decade}")
        save_dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0EP_flux/"
    
    # Calculate EP flux
    F_phi, F_p, div = EP_flux_isen(vptp, upvp, theta, isentrope=isentrope)

    # Save data
    logging.info (f"Save data for ensmean in {decade}")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    F_phi.to_netcdf(os.path.join(save_dir, f"F_phi_{decade}_ensmean.nc"))
    F_p.to_netcdf(os.path.join(save_dir, f"F_p_{decade}_ensmean.nc"))
    div.to_netcdf(os.path.join(save_dir, f"div_{decade}_ensmean.nc"))
    
#%%
decade = sys.argv[1] # '1850' or '2090'
isentrope = sys.argv[2].lower() == 'true' # Convert string to boolean

#%%
if __name__ == "__main__":
    # Summary of the input
    logging.info(f"Decade: {decade}")
    logging.info(f"Isentrope: {isentrope}")
    
    # Calculate EP flux for NAO pos and neg phase
    calculate_EP_flux(decade, isentrope=isentrope)