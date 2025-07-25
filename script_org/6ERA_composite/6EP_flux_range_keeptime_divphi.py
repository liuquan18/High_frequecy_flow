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
    upvp = read_comp_var_ERA5('upvp', phase, time_window='all', method='no_stat', )
elif eddy == 'steady':
    upvp = read_comp_var_ERA5('usvs', phase, time_window='all', method='no_stat',)

#%%

# constants
a0    = 6371000.  # earth radius in m
Omega = 7.292e-5 #[1/s]

# geometry
coslat = np.cos(np.deg2rad(upvp['lat']))
sinlat = np.sin(np.deg2rad(upvp['lat']))
R      = 1./(a0*coslat)
f      = 2*Omega*sinlat


# absolute vorticity
fhat = f

ep1_cart = -upvp

div1 = coslat*(np.rad2deg(ep1_cart).differentiate('lat',edge_order=2)) \
        - 2*sinlat*ep1_cart
# Now, we want acceleration, which is div(F)/a.cosphi [m/s2]
div1 = R*div1 # [m/s2]
div1 = div1*86400
div1.name = 'div'
div1.attrs['units'] = 'm/s/day'
div1.attrs['long_name'] = 'divergence of Horizonaltal component of Eliassen-Palm flux'
original_dims = upvp.dims

div1 = div1.transpose(*original_dims)


logging.info (f"Calculate {eddy} EP flux for {phase} phase")
save_dir="/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/"
div1.to_netcdf(os.path.join(save_dir, f"{eddy}_div_phi_{phase}_ano.nc"))
