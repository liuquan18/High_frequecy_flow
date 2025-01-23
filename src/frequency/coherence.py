#%%
import xarray as xr
import numpy as np
from scipy import signal
import logging

def coherence_analy(da, pixel_wise = False):

    """pixel wise for same variable, e.g., vt and va, spatial average for different variables, e.g., vt and hus_std"""

    if pixel_wise:
        da1 = da[list(da.data_vars)[0]]
        da2 = da[list(da.data_vars)[1]]

        # calculate coherence every year, 153 long,segement lenth 76, 50% overlap
        f, Cxy = signal.coherence(da1, da2, fs = 1, nperseg=76, detrend =False, noverlap = 38, axis = 0)
        Cxy = xr.DataArray(Cxy, dims = ['frequency', 'lat', 'lon'], coords = {'frequency': f, 'lat': da1.lat, 'lon': da1.lon})

    else:
        try:
            da = da.mean(dim = ('lat', 'lon'))
        except ValueError:
            logging.warning("No lat lon dimension, skipping spatial average")
            pass

        da1 = da[list(da.data_vars)[0]]
        da2 = da[list(da.data_vars)[1]]

        # calculate coherence every year, 153 long,segement lenth 76, 50% overlap
        f, Cxy = signal.coherence(da1, da2, fs = 1, nperseg=76, detrend =False, noverlap = 38, axis = 0)

        Cxy = xr.DataArray(Cxy, dims = ['frequency'], coords = {'frequency': f})

    Cxy.name = 'coherence'

    return Cxy

def sector(data, split_basin = True):
    # change lon from 0-360 to -180-180
    data = data.assign_coords(lon=(data.lon + 180) % 360 - 180).sortby("lon")
    data = data.sel(lat = slice(20, 60))
    if split_basin:
            
        box_NAL = [-70, -35, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Atlantic
        box_NPO = [140, -145, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Pacific

        data_NAL = data.sel(lon=slice(box_NAL[0], box_NAL[1]))
        data_NPO1 = data.sel(lon=slice(box_NPO[0], 180))
        data_NPO2 = data.sel(lon=slice(-180, box_NPO[1]))
        data_NPO = xr.concat([data_NPO1, data_NPO2], dim="lon")

        return data_NAL, data_NPO

    else:
        data = data
        return data

