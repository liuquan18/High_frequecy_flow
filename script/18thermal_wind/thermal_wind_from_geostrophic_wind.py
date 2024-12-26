# %%
import xarray as xr
import numpy as np
import pandas as pd

import metpy.calc as mpcalc
from metpy.units import units
import metpy.constants as mpconstants

# %%
zg = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily_global/zg_MJJAS_first10/zg_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_18500501-18590931.nc").zg
# %%
zg = zg.isel(time = 0)
#%%
zg = zg.metpy.assign_crs(
    grid_mapping_name='latitude_longitude',
    earth_radius=6371229.0
)
#%%
zg = zg.metpy.quantify()
#%%
u_g, v_g = mpcalc.geostrophic_wind(zg)
# %%
v_g = v_g.sortby('plev', ascending=True)
#%%
d_vg_dp = v_g.differentiate('plev')
# %%
# thermal wind 
v_t = d_vg_dp.sum('plev')
# %%
