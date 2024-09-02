#%%
import xarray as xr
import numpy as np
# Any import of metpy will activate the accessors
import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.units import units

# %%
u = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_ano_first10/ua_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_18500501-18590931_ano.nc")
# %%
v = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_MJJAS_ano_first10/va_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_18500501-18590931_ano.nc")
# %%
u = u.ua.sel(plev=25000)
v = v.va.sel(plev=25000)
#%%
u = u.metpy.quantify()
v = v.metpy.quantify()
# %%
# Calculate the total deformation of the flow
div = mpcalc.divergence(u, v)
# %%
