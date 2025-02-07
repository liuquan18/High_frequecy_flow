#%%
import xarray as xr
import numpy as np
import pandas as pd

import sys
from scipy.stats import linregress
import matplotlib.pyplot as plt 
import seaborn as sns
from glob import glob
# %%
def read_data(var, decade, basin, name = None):
    """
    var = 'vp', 'hus_daily_std', 'tas_daily_std'
    """
    if name is None:
        name = var

    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/basin_mean/{basin}/{var}/"

    files = glob(base_dir + f"r*i1p1f1/*_{decade}*.nc")

    data = xr.open_mfdataset(
        files, combine="nested", concat_dim="ens",
        chunks = { "time": -1, "lat": -1, "lon": -1}
    )
    
    data = data[name]
    data.load()
    if var == 'vp':
        data = data.sel(plev = [100000, 85000]).mean(dim = 'plev')

    if var == 'hus_daily_std':
        data = data * 1000 # convert to g/kg

    data = data.squeeze()

    try:
        data = data.drop_vars(('lat','lon'))
    except KeyError:
        pass

    df = data.to_dataframe()
    df = df.reset_index()
    return df
#%%
def construct_df(decade, basin):
    hus_df =  read_data('hus_daily_std', decade, basin, 'hus')
    tas_df = read_data('tas_daily_std', decade, basin, 'tas' )
    vp_df = read_data('vp', decade, basin, 'va')

    df_dec = hus_df.merge(tas_df, on = ['ens', 'time']).merge(vp_df, on = ['ens', 'time'])
    df_dec.columns = ['ens','time','hus_std', 'height', 'tas_std', 'vp']
    df_dec['year'] = df_dec['time'].dt.year
    return df_dec
#%%
dfs_NAL = []
for dec in range(1850, 2091,10):
    df_dec_NAL = construct_df(dec, 'NAL')
    dfs_NAL.append(df_dec_NAL)

dfs_NAL = pd.concat(dfs_NAL, axis = 0)

#%%
dfs_NPO = []

for dec in range(1850, 2091, 10):
    df_dec_NPO = construct_df(dec, 'NPO')
    dfs_NPO.append(df_dec_NPO)

dfs_NPO = pd.concat(dfs_NPO, axis = 0)

#%%
dfs_NAL = dfs_NAL.reset_index()
dfs_NPO = dfs_NPO.reset_index()
# %%
fig, ax = plt.subplots(2,1, figsize = (10, 10))
sns.scatterplot(dfs_NAL, ax = ax[0], x = 'hus_std', y = 'vp', hue = 'year', s = 1, palette=sns.color_palette("crest", as_cmap=True))
sns.scatterplot(dfs_NPO, ax = ax[1], x = 'hus_std', y = 'vp', hue = 'year', s = 1, palette=sns.color_palette("crest", as_cmap=True))
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/regression_2_vp/regression_basin_mean.png")
# %%
fig, ax = plt.subplots(2,1, figsize = (10, 10))
sns.scatterplot(dfs_NAL, ax = ax[0], x = 'tas_std', y = 'vp', hue = 'year', s = 1, palette=sns.color_palette("flare", as_cmap=True))
sns.scatterplot(dfs_NPO, ax = ax[1], x = 'tas_std', y = 'vp', hue = 'year', s = 1, palette=sns.color_palette("flare", as_cmap=True))
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/regression_2_vp/regression_basin_mean_tas.png")
# %%
