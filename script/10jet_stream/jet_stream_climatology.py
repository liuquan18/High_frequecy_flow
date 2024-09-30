#%%
import xarray as xr
import pandas as pd
import numpy as np
import glob
# %%
from src.compute.slurm_cluster import init_dask_slurm_cluster
#%%
client, scluster = init_dask_slurm_cluster(walltime = "04:00:00", memory = "128GB")

#%%
client

#%%
def jet_stream_climatology(period):
    jet_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_{period}/'
    jets = xr.open_mfdataset(f'{jet_path}*.nc', combine = 'nested', concat_dim = 'ens')

    # drop lon dim
    jets = jets.isel(lon = 0).ua

    # load data into memory
    jets = jets.load()
    # maximum westerly wind speed of the resulting profile is then identified and this is defined as the jet speed.
    jet_speeds = jets.max(dim = 'lat')

    # seasonal cycle
    jet_speeds = jet_speeds.groupby('time.month').mean(dim = ('time', 'ens'))

    # save to file
    jet_speeds.to_netcdf(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_speed_climatology_{period}.nc")

    # The jet latitude is defined as the latitude at which this maximum is found.
    jet_locs = jets.lat[jets.argmax(dim = 'lat')]

    #Smooth seasonal cycles of the jet latitude and speed are defined by averaging over all years and then Fourier filtering, retaining only the mean and the two lowest frequencies.
    jet_locs_clim = jet_locs.groupby('time.month').mean(dim = ('time', 'ens'))

    # save to file
    jet_locs_clim.to_netcdf(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_{period}.nc")
# %%
jet_stream_climatology('first10')
jet_stream_climatology('last10')
# %%
