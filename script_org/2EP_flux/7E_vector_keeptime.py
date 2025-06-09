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
# %%
def cal_E_div(decade, phase, eddy='transient', **kwargs):
    """
    Calculate the E-vector divergence for a given decade and phase
    """
    # Read data
    logging.info(f"Read data for {phase} phase in {decade}")

    if eddy == 'transient':
        M2 = read_comp_var('M2_prime', phase, decade, time_window='all', method = 'no_stat', name = 'M2', model_dir = 'MPI_GE_CMIP6_allplev')
        upvp = read_comp_var('upvp', phase, decade, time_window='all', method = 'no_stat', name = 'upvp', model_dir = 'MPI_GE_CMIP6_allplev')
    else:
        M2 = read_comp_var('M2_steady', phase, decade, time_window='all', method = 'no_stat', name = 'M2', model_dir = 'MPI_GE_CMIP6_allplev')
        upvp = read_comp_var('usvs', phase, decade, time_window='all', method = 'no_stat', name = 'usvs', model_dir = 'MPI_GE_CMIP6_allplev')

    # Calculate the divergence of the E-vector
    logging.info(f"Calculate E-vector divergence for {phase} phase in {decade}")

    dM2dx, dupvpdy = E_div(M2, upvp, **kwargs)

    # save
    logging.info(f"Save data for {phase} phase in {decade}")
    save_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0EP_flux_distribution/"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    dM2dx.to_netcdf(os.path.join(save_dir, f"{eddy}_E_div_x_{phase}_{decade}.nc"))
    dupvpdy.to_netcdf(os.path.join(save_dir, f"{eddy}_E_div_y_{phase}_{decade}.nc"))
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
