#%%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import logging
logging.basicConfig(level = logging.INFO)
import seaborn as sns

import matplotlib.pyplot as plt
# %%
def _jet_stream_anomaly(ens, period, jet_speed_clim, jet_loc_clim):
    # Load data
    jet_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_{period}/'
    jet_file = glob.glob(f'{jet_path}*r{ens}i1p1f1*.nc')[0]
    
    jet = xr.open_dataset(jet_file).ua
    # drop dim lon
    jet = jet.isel(lon = 0)
    
    # maximum westerly wind speed of the resulting profile is then identified and this is defined as the jet speed.
    jet_speed = jet.max(dim = 'lat')
    jet_speed_ano = jet_speed.groupby('time.month') - jet_speed_clim
    
    # The jet latitude is defined as the latitude at which this maximum is found.
    jet_loc = jet.lat[jet.argmax(dim = 'lat')]
    
    jet_loc_ano = jet_loc.groupby('time.month') - jet_loc_clim

    if jet_loc_ano.min() < -50:
        logging.warning(f"Jet latitude anomaly is below -40 for ens {ens} in period {period}\n")

    return jet_speed_ano, jet_loc_ano

# %%
def jet_stream_anomaly(period):

    # climatology only use the first10 years
    jet_speed_clim  = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_speed_climatology_first10.nc").ua
    jet_loc_clim = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_first10.nc").lat

    jet_speed_ano = []
    jet_loc_ano = []

    for ens in range(1, 51):
        speed_ano, loc_ano = _jet_stream_anomaly(ens, period, jet_speed_clim, jet_loc_clim)
        speed_ano['ens'] = ens
        loc_ano['ens'] = ens

        jet_speed_ano.append(speed_ano)
        jet_loc_ano.append(loc_ano)

    jet_speed_ano = xr.concat(jet_speed_ano, dim = 'ens')
    jet_loc_ano = xr.concat(jet_loc_ano, dim = 'ens')

    return jet_speed_ano, jet_loc_ano
#%%

jet_speed_first10_ano, jet_loc_first10_ano = jet_stream_anomaly('first10')

#%%
jet_speed_last10_ano, jet_loc_last10_ano = jet_stream_anomaly('last10')
# %%
# jet location anomaly
sns.histplot(jet_loc_first10_ano.values.flatten(), label = 'first10', color = 'b', bins = np.arange(-30,31,2), stat = 'density')
sns.histplot(jet_loc_last10_ano.values.flatten(), label = 'last10', color = 'r', bins = np.arange(-30,31,2), stat = 'density', alpha = 0.5)
plt.legend()
# %%
sns.histplot(jet_speed_first10_ano.values.flatten(), label = 'first10', color = 'b', bins = np.arange(-5,5.2,0.5), stat = 'density')
sns.histplot(jet_speed_last10_ano.values.flatten(), label = 'last10', color = 'r', bins = np.arange(-5,5.2,0.5), stat = 'density', alpha = 0.5)
# %%
