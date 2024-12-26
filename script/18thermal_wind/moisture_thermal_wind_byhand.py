# %%
import xarray as xr
import numpy as np
import pandas as pd

import metpy.calc as mpcalc
from metpy.units import units
import metpy.constants as mpconstants

# %%
def calc_factor(arr):
    """
    calculate 1/fa

    """
    lat = arr.lat
    f = mpcalc.coriolis_parameter(lat * units.degree_north)
    a = mpconstants.earth_avg_radius

    return 1 / (f * a).metpy.dequantify()

#%%
def calc_malr_1d(temp):
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

def calc_malr(arr):
    """
    Calculates the moist adiabatic lapse rate.

    """
    return xr.apply_ufunc(
        calc_malr_1d,
        arr,
        input_core_dims=[["plev"]],
        output_core_dims=[["plev"]],
    )
#%%
def s_entropy_1d(T, p, relative_humidity=1.0):
    """
    Calculate saturation (moist) entropy s* = sd + Lvq*/T
    
    Parameters:
    T (float): Temperature in Kelvin
    p (float): Pressure in Pa
    relative_humidity (float): Relative humidity (0-1), default=1.0 for saturation
    
    Returns:
    float: Saturation entropy in J/kg/K
    """
    # Constants
    cp = 1004.0  # Specific heat at constant pressure (J/kg/K)
    Lv = 2.5e6   # Latent heat of vaporization (J/kg)
    Rd = 287.0   # Gas constant for dry air (J/kg/K)
    Rv = 461.5   # Gas constant for water vapor (J/kg/K)
    p0 = 100000  # Reference pressure (Pa)
    
    # Calculate saturation vapor pressure (Bolton's formula)
    es = 611.2 * np.exp(17.67 * (T - 273.15) / (T - 29.65))
    
    # Calculate mixing ratio at saturation
    qs = (0.622 * es * relative_humidity) / (p - es * relative_humidity)
    
    # Calculate potential temperature
    theta = T * (p0/p)**(Rd/cp)
    
    # Calculate dry entropy component
    sd = cp * np.log(theta)
    
    # Calculate moist component
    s_moist = Lv * qs / T
    
    # Total saturation entropy
    s_star = sd + s_moist
    
    return s_star

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
def d_s_entropy_d_lon(arr):
    """
    Calculate the gradient of saturation entropy s* = sd + Lvq*/T with respect to longitude

    """
    return arr.differentiate(coord="lon")


#%%
def calc_moisture_thermal_wind(ta):
    """
    Calculate the moisture thermal wind

    """
    # Calculate moist adiabatic lapse rate
    malr = calc_malr(ta)
    
    # Calculate factor 1/fa
    factor = calc_factor(ta)
    
    # Calculate saturation entropy
    s_entropy = calc_saturation_entropy(ta)
    
    # Calculate gradient of saturation entropy
    s_entropy_grad = d_s_entropy_d_lon(s_entropy)
    
    # Calculate moisture thermal wind
    u_mt = -factor * malr * s_entropy_grad

    # aggregate all the plev levels
    u_mt = u_mt.sum(dim="plev")
    
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
