# %%
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


def calc_malr(temp):
    """
    Calculates the moist adiabatic lapse rate.
    # inputs are 1d vertical profiles of pressure and temperature :
    # p       pressure (Pa)
    # temp    temperature (K)
    Parameters:
    p : array-like
        Pressure (Pa)
    temp : array-like
        Temperature (K)

    Returns:
    dtemp_dp_ma : array-like
        Derivative of potential temperature with respect to pressure along a moist adiabat
    """
    p = [100000.0, 85000.0, 70000.0, 50000.0, 25000.0]
    # Constants
    Rd = 287.04  # gas constant for dry air [J/kg/K]
    Rv = 461.5  # gas constant for water vapor [J/kg/K]
    cpd = 1005.7  # specific heat dry air [J/kg/K]
    cpv = 1870  # specific heat water vapor [J/kg/K]
    g = 9.80665  # gravitational acceleration [m/s^2]
    gc_ratio = Rd / Rv

    # Saturation vapor pressure [Pa]
    Tc = temp - 273.15
    es = 611.20 * np.exp(17.67 * Tc / (Tc + 243.5))  # Bolton 1980 equation 10

    # Latent heat of condensation [J/kg]
    L = (2.501 - 0.00237 * Tc) * 1e6  # Bolton 1980 equation 2

    # Saturation mixing ratio
    rs = gc_ratio * es / (p - es)

    # Density
    temp_virtual = temp * (1.0 + rs / gc_ratio) / (1.0 + rs)
    rho = p / (Rd * temp_virtual)

    # Moist adiabatic lapse rate
    malr = (
        g
        / cpd
        * (1 + rs)
        / (1 + cpv / cpd * rs)
        * (1 + L * rs / (Rd * temp))
        / (1 + L**2 * rs * (1 + rs / gc_ratio) / (Rv * temp**2 * (cpd + rs * cpv)))
    )

    # Derivative of potential temperature wrt pressure along a moist adiabat
    dtemp_dp_ma = malr / g / rho

    return dtemp_dp_ma


# %%

# %%
ta = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zzz_tmp/ta_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc"
).ta
# %%
ta = ta.isel(time=slice(0, 4))
# %%
# apply_ufunc calc_malr to calculate moist adiabatic lapse rate
# along the vertical profile of temperature, p = ta.plev.values, for all lon,lat, and time
Malr = xr.apply_ufunc(
    calc_malr,
    ta,
    input_core_dims=[["plev"]],
    output_core_dims=[["plev"]],
)

# %%