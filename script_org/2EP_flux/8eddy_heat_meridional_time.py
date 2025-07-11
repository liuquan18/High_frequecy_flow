#%%
import xarray as xr
import numpy as np
from metpy.units import units
import os
import sys

import metpy.calc as mpcalc
from src.data_helper.read_composite import read_comp_var
from src.dynamics.EP_flux import E_div

import logging
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#%%
def read_data(decade, phase, eddy = 'transient', **kwargs):
    """
    Read data for a given decade and phase
    """
    logging.info(f"Read data for {phase} phase in {decade}")
    equiv_theta = kwargs.get('equiv_theta', True)
    time_window = kwargs.get('time_window', 'all')
    method = kwargs.get('method', 'no_stat')

    if eddy == 'transient':
        upvp = read_comp_var(
            var = "upvp",phase = phase, decade = decade, name = "upvp", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
            time_window = time_window, method = method, erase_zero_line = True,
        )
        
        if equiv_theta:
            vptp = read_comp_var(
                var = "vpetp", phase = phase, decade = decade, name = "vpetp", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
                time_window = time_window, method = method, erase_zero_line = True,
            )
            

        else:
            vptp = read_comp_var(
                var = "vptp", phase = phase, decade = decade, name = "vptp", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
                time_window = time_window, method = method, erase_zero_line = True,
            )
        


    elif eddy == 'steady':
        upvp = read_comp_var(
            var = "usvs", phase = phase, decade = decade, name = "usvs", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
            time_window = time_window, method = method, erase_zero_line = True,
        )
        if equiv_theta:
            vptp = read_comp_var(
                var = "vsets", phase = phase, decade = decade, name = "vsets", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
                time_window = time_window, method = method, erase_zero_line = True,
            )
            
        
        else:
            vptp = read_comp_var(
                var = "vsts", phase = phase, decade = decade, name = "vsts", suffix = "", model_dir = 'MPI_GE_CMIP6_allplev',
                time_window = time_window, method = method, erase_zero_line = True,
            )
    else:
        raise ValueError("eddy must be either 'transient' or 'steady'", f"but got {eddy}")

    return upvp, vptp



# %%
def cal_E_div(decade, phase, eddy='transient', **kwargs):
    """
    Calculate the E-vector divergence for a given decade and phase
    """
    # Read data

    # Read data, just vptp is useful, M2 (or upvp here) is just for position
    M2, vptp = read_data(decade, phase, eddy=eddy, **kwargs)


    # Calculate the divergence of the E-vector
    logging.info(f"Calculate E-vector divergence for {phase} phase in {decade}")

    _, dvptpdy = E_div(M2, vptp, **kwargs)

    # save
    logging.info(f"Save data for {phase} phase in {decade}")
    save_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0EP_flux_distribution/"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # dM2dx.to_netcdf(os.path.join(save_dir, f"{eddy}_E_div_x_{phase}_{decade}.nc"))
    dvptpdy.to_netcdf(os.path.join(save_dir, f"{eddy}_eddy_heat_dy_{phase}_{decade}.nc"))
# %%
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
    cal_E_div(decade, phase, eddy=eddy)

# %%
# for phase in ['pos', 'neg']:
#     for decade in ['1850', '2090']:
#         for eddy in ['transient', 'steady']:
#             cal_E_div(decade, phase, eddy=eddy)
# %%
