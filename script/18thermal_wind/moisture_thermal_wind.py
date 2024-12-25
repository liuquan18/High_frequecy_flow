#%%
import xarray as xr
import numpy as np
import pandas as pd

import metpy.calc as mpcalc
from metpy.units import units
import metpy.constants as mpconstants


# %%

# variables


# f     coriolis parameter          mpcalc.coriolis_parameter(lat)         's^-1'
# a     earth radius                mpconstants.earth_avg_radius            'm'


# $(\partial T / \partial P) s^*$   
#       moist adiabatic lapse rate  mpcalc.moist_lapse_rate(pressure, temperature)  'K / Pa'


# c_p  Specific heat at constant pressure for water vapor mpconstants.wv_specific_heat_press  'J/kg/K'
# \theta_e^* equivalent potential temperature mpcalc.equivalent_potential_temperature(pressure, temperature, dewpoint)  'K'

# $$
# s^* = c_p \ln \theta_e^* 

# where c_p is the specific heat of air at constant pressure
# \theta_e^* is the equivalent potential temperature

# $$



#%%
