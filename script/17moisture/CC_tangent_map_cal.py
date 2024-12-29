#%%
import numpy as np
import matplotlib.pyplot as plt

from src.moisture.longitudinal_contrast import read_data
#%%
def calculate_saturation_specific_humidity(T):
    """
    Calculate saturation specific humidity using Clausius-Clapeyron relation
    
    Parameters:
    T (float or array): Temperature in Kelvin
    
    Returns:
    float or array: Saturation specific humidity (kg/kg)
    """
    # Constants
    Rv = 461.5  # Gas constant for water vapor (J/(kg·K))
    Rd = 287.0  # Gas constant for dry air (J/(kg·K))
    L = 2.5e6   # Latent heat of vaporization (J/kg)
    es0 = 611.0 # Reference saturation vapor pressure at T0 (Pa)
    T0 = 273.15 # Reference temperature (K)
    P0 = 101325 # Standard atmospheric pressure (Pa)
    
    # Calculate saturation vapor pressure using Clausius-Clapeyron equation
    es = es0 * np.exp((L/Rv) * (1/T0 - 1/T))
    
    # Calculate saturation specific humidity
    qs = (Rd/Rv) * es / (P0 - (1 - Rd/Rv) * es)
    
    return qs

def calculate_dqs_dT(T):
    """
    Calculate the derivative of saturation specific humidity with respect to temperature
    
    Parameters:
    T (float or array): Temperature in Kelvin
    
    Returns:
    float or array: Derivative of saturation specific humidity (kg/(kg·K))
    """
    # Constants
    Rv = 461.5
    Rd = 287.0
    L = 2.5e6
    es0 = 611.0
    T0 = 273.15
    P0 = 101325
    
    # Calculate es and its derivative
    es = es0 * np.exp((L/Rv) * (1/T0 - 1/T))
    des_dT = es * L/(Rv * T**2)
    
    # Calculate derivative of qs
    dqs_dT = (Rd/Rv) * des_dT * P0 / (P0 - (1 - Rd/Rv) * es)**2
    
    return dqs_dT
# %%
first_tas = read_data('tas', 1850, (-90, 90), meridional_mean=False, suffix='')
# %%
first_tas_mean = first_tas.mean(dim = ('time', 'ens'))
# %%
last_tas = read_data('tas', 2090, (-90, 90), meridional_mean=False, suffix='')
last_tas_mean = last_tas.mean(dim = ('time', 'ens'))
# %%
# apply calculate_dqs_dT to each grid point
first_tas_dqs_dT = calculate_dqs_dT(first_tas_mean)
# %%
first_tas_dqs_dT.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_tas_dqs_dT.nc")
# %%
last_tas_dqs_dT = calculate_dqs_dT(last_tas_mean)
# %%
last_tas_dqs_dT.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_tas_dqs_dT.nc")
# %%
