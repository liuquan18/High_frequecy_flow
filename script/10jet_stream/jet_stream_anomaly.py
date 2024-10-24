# %%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import logging

from src.jet_stream.jet_speed_and_location import jet_stream_anomaly

logging.basicConfig(level=logging.INFO)
#%%


# %%
def jet_stream_anomaly_period(period):

    jet_speed_ano = []
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

        speed_ano = jet_stream_anomaly(
            jet, jet_speed_clim, stat="speed"
        )
        speed_ano["ens"] = ens

        jet_speed_ano.append(speed_ano)
        jet_loc_ano.append(loc_ano)

    jet_speed_ano = xr.concat(jet_speed_ano, dim="ens")
    jet_loc_ano = xr.concat(jet_loc_ano, dim="ens")

    return jet_speed_ano, jet_loc_ano


# %%
############## jet location hist #####################
# climatology only use the first10 years

jet_speed_clim = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_speed_climatology_first10.nc"
).ua
jet_loc_clim = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_first10.nc"
).lat


jet_speed_first10_ano, jet_loc_first10_ano = jet_stream_anomaly_period("first10")

# %%
jet_speed_last10_ano, jet_loc_last10_ano = jet_stream_anomaly_period("last10")
