# %%
import xarray as xr
import numpy as np
import pandas as pd

import metpy.calc as mpcalc
from metpy.units import units
import metpy.constants as mpconstants

# %%
def factor(arr):
    """
    calculate 1/facos(lat) for a given latitude

    """
    lat = arr.lat
    cosine = np.cos(lat)
    f = mpcalc.coriolis_parameter(lat * units.degree_north)
    a = mpconstants.earth_avg_radius

    return 1 / (f * a * cosine)  # units second/meter
#%%
def calc_malr_1d(temp, p):
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
    temp = temp * units.kelvin
    p = p * units.pascal

    # Constants
    Rd = 287.04 * units.joule / (units.kilogram * units.kelvin)  # gas constant for dry air
    Rv = 461.5 * units.joule / (units.kilogram * units.kelvin)  # gas constant for water vapor
    cpd = 1005.7 * units.joule / (units.kilogram * units.kelvin)  # specific heat dry air
    cpv = 1870 * units.joule / (units.kilogram * units.kelvin)  # specific heat water vapor
    g = 9.80665 * units.meter / units.second**2  # gravitational acceleration
    gc_ratio = Rd / Rv

    # Saturation vapor pressure [Pa]
    Tc = temp/units.kelvin - 273.15
    es = 611.20 * np.exp(17.67 * Tc / (Tc + 243.5))  # Bolton 1980 equation 10

    es = es * units.pascal

    # Latent heat of condensation [J/kg]
    L = (2.501 - 0.00237 * Tc) * 1e6 # Bolton 1980 equation 2
    L = L * units.joule / units.kilogram

    # Saturation mixing ratio
    rs = gc_ratio * es / (p - es)

    # Density
    temp_virtual = temp*(1.0+rs/gc_ratio)/(1.0+rs)
    rho          = p/Rd/temp_virtual
    
    # Moist adiabatic lapse rate
    malr = (
        g/ cpd
        * (1 + rs)
        / (1 + cpv / cpd * rs)
        * (1 + L * rs / (Rd * temp))
        / (1 + L**2 * rs * (1 + rs / gc_ratio) / (Rv * temp**2 * (cpd + rs * cpv)))
    )  # kelvin/meter


    # Derivative of potential temperature with respect to pressure along a moist adiabat
    dtemp_dp_ma = malr / g / rho  # kelvin/pascal


    return dtemp_dp_ma.magnitude

def malr(arr):
    """
    Calculates the moist adiabatic lapse rate.

    """
    return xr.apply_ufunc(
        calc_malr_1d,
        arr,
        arr.plev,
        input_core_dims=[["plev"], ["plev"]],
        output_core_dims=[["plev"]],
    )  
    # units.kelvin / units.pascal

#%%
def s_entropy_1d(temp, p, relative_humidity=1.0):
    """
    Calculate saturation (moist) entropy s* = sd + Lvq*/T
    
    Parameters:
    temp (float): Temperature in Kelvin
    pressure (float): Pressure in Pa
    relative_humidity (float): Relative humidity (0-1), default=1.0 for saturation
    
    Returns:
    float: Saturation entropy in J/kg/K
    """
    # units
    temp = temp * units.kelvin
    p = p * units.pascal

    # Constants
    cpd = 1005.7 * units.joule / (units.kilogram * units.kelvin)  # specific heat dry air

    # Calculate potential temperature
    theta = mpcalc.potential_temperature(p, temp)

    # Calculate dry entropy component
    sd = cpd * (np.log(theta/units.kelvin)) 

    Lv = mpconstants.water_heat_vaporization
    # Calculate saturation vapor pressure (Bolton's formula)
    
    # Calculate mixing ratio at saturation

    # Constants
    Rd = 287.04 * units.joule / (units.kilogram * units.kelvin)  # gas constant for dry air
    Rv = 461.5 * units.joule / (units.kilogram * units.kelvin)  # gas constant for water vapor
    cpd = 1005.7 * units.joule / (units.kilogram * units.kelvin)  # specific heat dry air
    gc_ratio = Rd / Rv

    # Saturation vapor pressure [Pa]
    Tc = temp/units.kelvin - 273.15
    es = 611.20 * np.exp(17.67 * Tc / (Tc + 243.5))  # Bolton 1980 equation 10

    es = es * units.pascal

    # Saturation mixing ratio
    rs = gc_ratio * es / (p - es)

    # calculate saturation specific humidity
    qs = mpcalc.specific_humidity_from_mixing_ratio(rs)


    # Calculate moist component
    s_moist = Lv * qs / temp
    
    # Total saturation entropy
    s_star = sd + s_moist  # J/kg/K
    
    return s_star.magnitude

def calc_saturation_entropy(T):
    """
    Calculates the saturation entropy s* = sd + Lvq*/T

    """
    return xr.apply_ufunc(
        s_entropy_1d,
        T,
        T.plev,
    )

#%%
def calc_moisture_thermal_wind(ta):
    """
    Calculate the moisture thermal wind

    """
    # Calculate moist adiabatic lapse rate
    malr = malr(ta)
    # units
    malr = malr * units.kelvin / units.pascal
    
    # Calculate factor 1/fa
    factor = calc_factor(ta) # units second/meter

    
    # Calculate saturation entropy
    s_entropy = calc_saturation_entropy(ta) # units J/kg/K
    
    s_entropy_grad = s_entropy.differentiate("lon") # units J/kg/K/pascal
    s_entropy_grad = s_entropy_grad * units.joule / units.kilogram / units.kelvin / units.pascal

    # Calculate moisture thermal wind
    u_mt = -factor * malr * s_entropy_grad
           # second/meter * kelvin/pascal * meter/(kelvin * second**2)

    # aggregate all the plev levels
    u_mt = u_mt.integrate("plev") # second/meter
    
    return u_mt
# %%
ta = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zzz_tmp/ta_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc"
).ta
# %%
ta = ta.isel(time=slice(0, 4))
# %%
# apply_ufunc calc_malr to calculate moist adiabatic lapse rate
# along the vertical profile of temperature, p = ta.plev.values, for all lon,lat, and time
#%%
thermal_wind = calc_moisture_thermal_wind(ta)
# %%
temp = ta.isel(time=0, lon=0, lat=0).values
p = ta.plev.values
# %%
