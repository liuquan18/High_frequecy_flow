#%%
import src.dynamics.EP_flux as EP_flux_module
import importlib
import sys
import xarray as xr
import os
from src.data_helper.read_composite import read_comp_var_ERA5

import numpy as np
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

phase= sys.argv[1] if len(sys.argv) > 1 else 'pos'
eddy = sys.argv[2] if len(sys.argv) > 2 else 'transient'
logging.info(f"Calculating EP flux for {phase} phase and {eddy} eddy")
#%%

logging.info(f"Reading data for {phase} phase")
if eddy == 'transient':
    vptp = read_comp_var_ERA5('vpetp', phase, time_window='all', method='no_stat')
elif eddy == 'steady':
    vptp = read_comp_var_ERA5('vsets', phase, time_window='all', method='no_stat')
dthdp = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/stat_stab_{phase}.nc",
                            )['stat_stab']

vptp.load()
dthdp.load()
#%%
logging.info (f"Calculate {eddy} EP flux for {phase} phase")
save_dir="/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/"

# constants
a0    = 6371000.  # earth radius in m
Omega = 7.292e-5 #[1/s]

# geometry
coslat = np.cos(np.deg2rad(vptp['lat']))
sinlat = np.sin(np.deg2rad(vptp['lat']))
R      = 1./(a0*coslat)
f      = 2*Omega*sinlat


# absolute vorticity
fhat = f

# v't'/theta_p
vertEddy = vptp / dthdp

if 'time' in vptp.dims and dthdp.time.size == 0:
    logging.warning ("vptp and ta has different time dimensions. Using the time step of vptp.")
    dthdp['time'] = vptp['time']
    vertEddy = vptp / dthdp

# compute vertical component
ep2_cart = fhat*vertEddy # [1/s*m.hPa/s] = [m.hPa/s2]

# Similarly, we want acceleration = 1/a.coshpi*a.cosphi*d/dp[ep2_cart] [m/s2]
div2 = ep2_cart.differentiate('plev',edge_order=2) # [m/s2]
div2 = div2*86400
div2.name = 'div2'
div2.attrs['units'] = 'm/s/day'
div2.attrs['long_name'] = 'divergence of Vertical component of Eliassen-Palm flux'
original_dims = vptp.dims
div2 = div2.transpose(*original_dims)
#%%
div2.to_netcdf(os.path.join(save_dir, f"{eddy}_div_p_{phase}_ano.nc"))
