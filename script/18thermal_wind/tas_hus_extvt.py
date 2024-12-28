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


# %%
first_tas = read_data("tas", 1850, (0, 60), meridional_mean=False)
first_hus = read_data("hus", 1850, (0, 60), meridional_mean=False)
first_data = xr.Dataset({"tas": first_tas, "hus": first_hus})
first_df = first_data.to_dataframe()[["tas", "hus"]]

# %%

last_tas = read_data("tas", 2090, (0, 60), meridional_mean=False)
last_hus = read_data("hus", 2090, (0, 60), meridional_mean=False)
last_data = xr.Dataset({"tas": last_tas, "hus": last_hus})
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
# %%
plot_x = np.arange(0, 15, 0.1).reshape(-1, 1)
#%%
first_reg = regression(first_df)
first_y = first_reg.predict(plot_x)
# %%
last_hus_pred = regression(last_df)
last_y = last_hus_pred.predict(plot_x)

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

fig, ax = plt.subplots(1, 1, figsize=(10, 5))
ax.plot(plot_x, first_y, label='first10')
ax.plot(plot_x, last_y,  label='last10')

sns.scatterplot(data = df, x = 'tas', y = 'hus', hue = 'decade', ax = ax)

ax.set_xlim(3.5,4.8)
ax.set_ylim(0.0017, 0.0025)

ax.legend()
plt.show()
# %%
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
sns.scatterplot(data = df, x = 'tas', y = 'hus', hue = 'decade', size='vt_extreme_freq',sizes=(50,500), ax = ax)
ax.legend(ncol=2)
ax.set_xlabel('tas_diff (K)')
ax.set_ylabel('hus_diff (g/kg)')

# %%
