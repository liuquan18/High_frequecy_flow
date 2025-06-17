# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import seaborn.objects as so

from src.data_helper import read_composite
import importlib
import matplotlib
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
importlib.reload(read_composite)
from src.data_helper.read_variable import read_climatology

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var

# %%
levels_vq = np.arange(-3, 3.1, 0.5)
levels_uv = np.arange(-1.5, 1.6, 0.5)
levels_vt = np.arange(-3, 3.1, 0.5)
# %%
# read transient EP flux for positive and negative phase
# read data for first decade with region = western
_, _, _, pos_old = read_EP_flux(
    phase="pos",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
    keep_time = True
)
_, _, _, neg_old = read_EP_flux(
    phase="neg",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
    keep_time = True
)
pos_old = pos_old.sel(plev = 85000)
neg_old = neg_old.sel(plev = 85000)
# %%
pos_new =  read_comp_var(
    var = 'Fdiv_p_transient',
    phase = 'pos',
    decade = 1850,
    time_window='all',
    name = 'div2',
    method = 'no_stat',
    suffix = '',
    model_dir = 'MPI_GE_CMIP6_allplev',
)

neg_new = read_comp_var(
    var = 'Fdiv_p_transient',
    phase = 'neg',
    decade = 1850,
    time_window='all',
    name = 'div2',
    method = 'no_stat',
    suffix = '',
    model_dir = 'MPI_GE_CMIP6_allplev',
)
#%%
clima_new = read_climatology(
    var = 'Fdiv_p_transient',
    decade = 1850,
    name = 'div2',
    model_dir = 'MPI_GE_CMIP6_allplev',
)

#%%
_, _, _, clima_old = (
    read_EP_flux(
        phase="clima",
        decade=1850,
        eddy="transient",
        ano=False,
        lon_mean=False,
        region=None,
        keep_time = True
    )
)

# %%
# fldmean over [300, 360, 40, 80]
def to_dataframe(ds, var_name, phase, decade):

    ds = ds.sel(lat=slice(40, 80), lon=slice(280, 360))
    # create weights
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"
    ds = ds.weighted(weights)
    
    ds = ds.mean(dim=["lat", "lon"])

    df = ds.to_dataframe(var_name).reset_index()
    df['phase'] = phase
    df['decade'] = decade
    return df

# %%
pos_old_df = to_dataframe(pos_old, 'div', 'pos', 1850)
neg_old_df = to_dataframe(neg_old, 'div', 'neg', 1850)
pos_new_df = to_dataframe(pos_new, 'div', 'pos', 1850)
neg_new_df = to_dataframe(neg_new, 'div', 'neg', 1850)

# %%
clima_new_df = to_dataframe(
    clima_new,
    'div',
    'clima',
    1850
)
clima_old_df = to_dataframe(
    clima_old,
    'div',
    'clima',
    1850
)
# %%
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(
    data = pos_new_df,
    x = 'time',
    y = 'div',
    label='pos new',
    ax=ax,
    color = 'red'

)
sns.lineplot(
    data = pos_old_df,
    x = 'time',
    y = 'div',
    label='pos old',
    color = 'black',
    ax=ax

)

# neg dashed 
sns.lineplot(
    data = neg_new_df,
    x = 'time',
    y = 'div',
    label='neg new',
    ax=ax,
    linestyle='--',
    color = 'red'
)

sns.lineplot(
    data = neg_old_df,
    x = 'time',
    y = 'div',
    label='neg old',
    ax=ax,
    linestyle='--',
    color = 'black'
)

ax.axhline(clima_new_df[clima_new_df['plev'] == 85000]['div'].values[0], color='red', linestyle='dotted', label='clima 850hPa new')
ax.axhline(clima_old_df[clima_old_df['plev'] == 85000]['div'].values[0], color='black', linestyle='dotted', label='clima 850hPa old')

ax.set_xlim(-20, 20)
# %%
# %%
