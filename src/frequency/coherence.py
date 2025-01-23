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