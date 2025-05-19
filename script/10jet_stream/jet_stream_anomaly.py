# %%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import logging

from src.dynamics.jet_speed_and_location import jet_stream_anomaly

logging.basicConfig(level=logging.INFO)


# %%
############## jet location hist #####################
# climatology only use the first10 years
def climatology(period, same_clim=True, eddy = True):
    """
    same_clim: if True, use the climatology of first10 for both first10 and last10
    eddy: if False, same plev of jet stream as the NAO are used rather than eddy-driven jet
    """

    
    base_dir = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/'

    if period == 'first10':
        if eddy:
            loc_path = base_dir + 'jet_loc_climatology_first10.nc'
        else:
            loc_path = base_dir + 'jet_loc_climatology_allplev_first10.nc'

    elif period == 'last10':
        if same_clim:
            if eddy:
                loc_path = base_dir + 'jet_loc_climatology_first10.nc'
            else:
                loc_path = base_dir + 'jet_loc_climatology_allplev_first10.nc'
        else: # use the last10 climatology
            if eddy:
                loc_path = base_dir + 'jet_loc_climatology_last10.nc'
            else:
                loc_path = base_dir + 'jet_loc_climatology_allplev_last10.nc'

    jet_loc_clim = xr.open_dataset(loc_path).lat

    try:
        jet_loc_clim = jet_loc_clim.sel(plev = 25000)
    except KeyError:
        pass

    return jet_loc_clim


def jet_stream_anomaly_period(period, jet_loc_clim):

    jet_loc_ano = []

    for ens in range(1, 51):
        # Load data
        jet_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_{period}/"
        jet_file = glob.glob(f"{jet_path}*r{ens}i1p1f1*.nc")[0]

        jet = xr.open_dataset(jet_file).ua
        # drop dim lon
        jet = jet.isel(lon=0)

        loc_ano = jet_stream_anomaly(
            jet, jet_loc_clim, stat="loc"
        )
        loc_ano["ens"] = ens

        jet_loc_ano.append(loc_ano)


    jet_loc_ano = xr.concat(jet_loc_ano, dim="ens")
    # name as lat
    jet_loc_ano.name = 'lat_ano'

    return jet_loc_ano

def save_path(eddy, same_clim):
    if eddy:
        if same_clim:
            first_to_path = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/loc_anomaly/jet_stream_anomaly_eddy_sameclima_first10.nc'
            last_to_path = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/loc_anomaly/jet_stream_anomaly_eddy_sameclima_last10.nc'
        else:
            first_to_path = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/loc_anomaly/jet_stream_anomaly_eddy_diffclima_first10.nc'
            last_to_path = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/loc_anomaly/jet_stream_anomaly_eddy_diffclima_last10.nc'
    else:
        if same_clim:
            first_to_path = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/loc_anomaly/jet_stream_anomaly_noneddy_sameclima_first10.nc'
            last_to_path = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/loc_anomaly/jet_stream_anomaly_noneddy_sameclima_last10.nc'
        else:
            first_to_path = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/loc_anomaly/jet_stream_anomaly_noneddy_diffclima_first10.nc'
            last_to_path = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/loc_anomaly/jet_stream_anomaly_noneddy_diffclima_last10.nc'

    return first_to_path, last_to_path


#%%
eddy = False
same_clim = False

#%%
first_jet_loc_clim = climatology("first10",same_clim = same_clim, eddy = eddy)
last_jet_loc_clim = climatology("last10",same_clim = same_clim, eddy = eddy)
jet_loc_first10_ano = jet_stream_anomaly_period("first10", first_jet_loc_clim)
jet_loc_last10_ano = jet_stream_anomaly_period("last10", last_jet_loc_clim)

first_save_path, last_save_path = save_path(eddy, same_clim)
#%%
jet_loc_first10_ano.to_netcdf(first_save_path)
jet_loc_last10_ano.to_netcdf(last_save_path)
# %%
