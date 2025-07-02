#%%
import src.dynamics.EP_flux as EP_flux_module
import importlib
import sys
import os
from src.data_helper.read_composite import read_comp_var_ERA5

import logging
importlib.reload(EP_flux_module)
from src.dynamics.EP_flux import (  # noqa: E402
    EP_flux,
    eff_stat_stab_xr,
)



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

#%%
def read_data_all(phase, equiv_theta = True, eddy='transient', time_window='all', method='no_stat'):
    """
    Read data for a given phase
    """
    logging.info(f"Reading data for {phase} phase")
    if eddy == 'transient':
        upvp = read_comp_var_ERA5('upvp', phase, time_window=time_window, method=method, equiv_theta=equiv_theta,)
        if equiv_theta:
            vptp = read_comp_var_ERA5('vpetp', phase, time_window=time_window, method=method, equiv_theta=equiv_theta)
        else:
            vptp = read_comp_var_ERA5('vptp', phase, time_window=time_window, method=method, equiv_theta=equiv_theta)
    elif eddy == 'steady':
        upvp = read_comp_var_ERA5('usvs', phase, time_window=time_window, method=method, equiv_theta=equiv_theta)
        if equiv_theta:
            vptp = read_comp_var_ERA5('vsets', phase, time_window=time_window, method=method, equiv_theta=equiv_theta)
        else:
            vptp = read_comp_var_ERA5('vsts', phase, time_window=time_window, method=method, equiv_theta=equiv_theta)

    ta = read_comp_var_ERA5('ta_hat', phase, time_window=time_window, name = 'var130', method=method, equiv_theta=equiv_theta)

    return upvp, vptp, ta


#%%
def calculate_EP_flux(phase, ano=False, equiv_theta=True, eddy='transient'):
    """
    Calculate EP flux for a given and phase
    """
    # Read data
    logging.info (f"Read data for {phase} phase")
    upvp, vptp, ta = read_data_all(phase, equiv_theta=equiv_theta, eddy=eddy, time_window = 'all', method = 'no_stat')

    logging.info (f"Calculate {eddy} EP flux for {phase} phase")
    save_dir="/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/"

    # Calculate EP flux
    stat_stab = eff_stat_stab_xr(ta)
    F_phi, F_p, div_phi, div_p = EP_flux(vptp, upvp, stat_stab)

    # Save data
    logging.info (f"Save data for {phase} phase")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    F_phi.to_netcdf(os.path.join(save_dir, f"{eddy}_F_phi_{phase}_ano{ano}.nc"))
    F_p.to_netcdf(os.path.join(save_dir, f"{eddy}_F_p_{phase}_ano{ano}.nc"))
    div_phi.to_netcdf(os.path.join(save_dir, f"{eddy}_div_phi_{phase}_ano{ano}.nc"))
    div_p.to_netcdf(os.path.join(save_dir, f"{eddy}_div_p_{phase}_ano{ano}.nc"))


# %%
for phase in ['pos', 'neg']:
    for eddy in ['transient', 'steady']:
        calculate_EP_flux(phase, ano=False, equiv_theta=True, eddy=eddy)
        calculate_EP_flux(phase, ano=True, equiv_theta=True, eddy=eddy)
# %%
