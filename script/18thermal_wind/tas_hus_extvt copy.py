#%%
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import cartopy.crs as ccrs
import cartopy
import matplotlib.colors as mcolors
from src.moisture.longitudinal_contrast import read_data
from sklearn.linear_model import LinearRegression
import seaborn as sns
import random

# %%
first_tas = read_data("tas", 1850, (0, 60), meridional_mean=False)
first_hus = read_data("hus", 1850, (0, 60), meridional_mean=False)
first_data = xr.Dataset({"tas": first_tas, "hus": first_hus*1000})
first_df = first_data.to_dataframe()[["tas", "hus"]]

# %%

last_tas = read_data("tas", 2090, (0, 60), meridional_mean=False)
last_hus = read_data("hus", 2090, (0, 60), meridional_mean=False)
last_data = xr.Dataset({"tas": last_tas, "hus": last_hus*1000})
last_df = last_data.to_dataframe()[["tas", "hus"]]


# %%
# regression column 'hus' on 'tas'

def regression(df):
    X = df['tas'].values.reshape(-1, 1)
    y = df['hus'].values.reshape(-1, 1)
    reg = LinearRegression().fit(X, y)
    return reg

def read_dec_stat(var = 'vt_extremes_freq_decade'):
    data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}/"
    data = xr.open_mfdataset(data_path + "*.nc", combine = 'nested', concat_dim = 'decade')
    data['decade'] = np.arange(1850, 2100, 10)
    data = data.mean(dim = ('lat', 'lon'))

    return data

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

#%%
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
plot_tas_std = np.arange(0, 15, 0.1).reshape(-1, 1)
#%%
first_reg = regression(first_df)
first_y = first_reg.predict(plot_tas_std)

#%%
last_hus_pred = regression(last_df)
last_y = last_hus_pred.predict(plot_tas_std)
#%%

vt_extremes_freq_decade = read_dec_stat('vt_extremes_freq_decade')

tas_decade = read_dec_stat('tas_daily_std_dec')

hus_decade = read_dec_stat('hus_daily_std_dec')


#%%
vt_df = vt_extremes_freq_decade.to_dataframe()
vt_df.columns = ['vt_extreme_freq']

tas_df = tas_decade.to_dataframe()
tas_df = tas_df[['tas']]

hus_df = hus_decade.to_dataframe()
hus_df = hus_df[['hus']]
hus_df = hus_df*1000
#%%

# concat all dataframes
df = pd.concat([vt_df, tas_df, hus_df], axis = 1)
#%%
df = df.reset_index()

# %%
# tangent line
# Calculate tangent lines at T=250K and T=290K
T_tangent = np.array([290.4, 295.6])
dqs_dT_tangent = calculate_dqs_dT(T_tangent)*1000

# %%
delta_tas = plot_tas_std
# %%
dqs_first = dqs_dT_tangent[0]*delta_tas
# %%
dqs_last = dqs_dT_tangent[1]*delta_tas
# %%


fig, ax = plt.subplots(1, 1, figsize=(10, 5))
ax.plot(plot_tas_std, first_y, label='first10')
ax.plot(plot_tas_std, last_y,  label='last10')

ax.plot(plot_tas_std, dqs_first, label='dqs_first', linestyle='--', color = 'C0')
ax.plot(plot_tas_std, dqs_last, label='dqs_last', linestyle='--', color = 'C1')

sns.scatterplot(data = df, x = 'tas', y = 'hus', hue = 'decade', size='vt_extreme_freq',sizes=(50,500), ax = ax)

ax.set_xlim(3.7,4.5)

ax.set_ylim(1.5, 2.5)
ax.legend(ncol = 2)
plt.show()
# %%
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
# sns.scatterplot(data = df, x = 'tas', y = 'hus', hue = 'decade', size='vt_extreme_freq',sizes=(50,500), ax = ax)

ax.plot(plot_tas_std, first_y, label='first10')
ax.plot(plot_tas_std, last_y,  label='last10')


ax.plot(plot_tas_std, dqs_first, label='CC tagent_line at 290.4K', linestyle='--', color = 'C0')
ax.plot(plot_tas_std, dqs_last, label='CC tagent_line at 295.6K', linestyle='--', color = 'C1')

# ax.set_xlim(3.7,4.5)
# ax.set_ylim(1.5, 5)

ax.legend(ncol=2)

ax.set_xlabel('tas_diff (K)')
ax.set_ylabel('hus_diff (g/kg)')
# %%
Tas_first_mean = 290.4
Tas_last_mean = 295.6
#%%
first_CC_hus_std = get_CC_hus_std(Tas_first_mean, plot_tas_std)
last_CC_hus_std = get_CC_hus_std(Tas_last_mean, plot_tas_std)

# %%
first_CC_reg = regression(pd.DataFrame({'tas': plot_tas_std.ravel(), 'hus': first_CC_hus_std}))
first_CC_hus_std_pred = first_CC_reg.predict(plot_tas_std)*1000

#%%
last_CC_reg = regression(pd.DataFrame({'tas': plot_tas_std.ravel(), 'hus': last_CC_hus_std}))
last_CC_hus_std_pred = last_CC_reg.predict(plot_tas_std)*1000
# %%
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
ax.plot(plot_tas_std, first_y, label='first10')
ax.plot(plot_tas_std, last_y,  label='last10')

ax.plot(plot_tas_std, first_CC_hus_std_pred, label='dqs_first', linestyle='--', color = 'C0')
ax.plot(plot_tas_std, last_CC_hus_std_pred, label='dqs_last', linestyle='--', color = 'C1')

# sns.scatterplot(data = df, x = 'tas', y = 'hus', hue = 'decade', size='vt_extreme_freq',sizes=(50,500), ax = ax)

# ax.set_xlim(3.7,4.5)

# ax.set_ylim(1.5, 2.5)
ax.legend(ncol = 2)
plt.show()
# %%
