#%%
import xarray as xr
import pandas as pd
import numpy as np
import glob
# %%
period = 'first10'
ens = 1
# %%
# Load data
jet_loc = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_{period}/'
jet_file = glob.glob(f'{jet_loc}*r{ens}i1p1f1*.nc')[0]
# %%
jet = xr.open_dataset(jet_file).ua
# drop dim lon
jet = jet.isel(lon = 0)
# %%
# maximum westerly wind speed of the resulting profile is then identified and this is defined as the jet speed.
jet_speed = jet.max(dim = 'lat')

# %%
# The jet latitude is defined as the latitude at which this maximum is found.
jet_loc = jet.lat[jet.argmax(dim = 'lat')]
# %%
#Smooth seasonal cycles of the jet latitude and speed are defined by averaging over all years and then Fourier filtering, retaining only the mean and the two lowest frequencies. 
jet_loc_clim = jet_loc.groupby('time.month').mean(dim = 'time')
