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
#%%

# %%
def process_data(phase, equiv_theta=True):
    
    ta = read_comp_var_ERA5('ta_hat', phase, time_window='all', name = 'var130', method='no_stat', equiv_theta=True)
    
    # rechunk
    ta = ta.load()
    
    stat_stab = eff_stat_stab_xr(ta)
    stat_stab.name = 'stat_stab'

    #save
    stat_stab.to_netcdf(f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/stat_stab_{phase}.nc")
# %%
phase = sys.argv[1] if len(sys.argv) > 1 else "pos"

logging.info(f"Processing data for {phase} phase")
process_data(phase, equiv_theta=True)