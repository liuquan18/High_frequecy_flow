#%%
import xarray as xr
import numpy as np
import metpy.calc as mpcalc
from metpy.units import units
import metpy.constants as mpconstants

# %%
q_s = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_trop_daily/r1i1p1f1/hus_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc").hus
ta = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ta_daily/r1i1p1f1/ta_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc").ta
# %%
temp = ta.isel(time = 0, lon = 30, lat = 30)
p = ta.plev.values


#%%
q_s = q_s.isel(time = 0).isel(lon = 30, lat = 30)
ta = ta.isel(time = 0).isel(lon = 30, lat = 30)
# %%
Lv = mpconstants.water_heat_vaporization #joule/kilogram
# %%
q_s = q_s * units("kg/kg")
ta = ta * units("K")
# %%
object = Lv * q_s / (ta)  # joule/(kelvin kilogram)
# %%
object = object.metpy.dequantify()

#%%
# longitude gradient of object
object_grad = object.differentiate('lon')
# %%
#%%

# Constants
Rd = 287.04 * units.joule / (units.kilogram * units.kelvin)  # gas constant for dry air
Rv = 461.5 * units.joule / (units.kilogram * units.kelvin)  # gas constant for water vapor
cpd = 1005.7 * units.joule / (units.kilogram * units.kelvin)  # specific heat dry air
cpv = 1870 * units.joule / (units.kilogram * units.kelvin)  # specific heat water vapor
g = 9.80665 * units.meter / units.second**2  # gravitational acceleration
gc_ratio = Rd / Rv

# %%
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
    Tc = temp.metpy.magnitude - 273.15
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
    dtemp_dp_ma = malr / g / rho

# %%
