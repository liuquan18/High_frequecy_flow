
# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from xarray.groupers import UniqueGrouper
import logging

logging.basicConfig(level=logging.INFO)
# %%
# define a function called band,for each base point,
# return the sector that is within 180 longtitude to the east of the base pont and within 10 latitude
def band_stat(base_point, v_data, stat = 'var', **kwargs):

    lat_base, lon_base = (
        base_point.lat.values.ravel()[0],
        base_point.lon.values.ravel()[0],
    )
    lon_min = lon_base
    lon_max = lon_base + 180
    lat_min = lat_base - 5
    lat_max = lat_base + 5

    if lon_max > 360:
        lon_max -= 360
        sector1 = v_data.sel(lon=slice(lon_min, 360), lat=slice(lat_min, lat_max))
        sector2 = v_data.sel(lon=slice(0, lon_max), lat=slice(lat_min, lat_max))
        sector = xr.concat([sector1, sector2], dim="lon")
    else:
        sector = v_data.sel(lon=slice(lon_min, lon_max), lat=slice(lat_min, lat_max))

    # if stat = 'var', look for mean from kwargs
    if stat == 'var':
        try:
            mean = kwargs['mean']
            logging.info("using mean provided to calculate 'var'")
        except KeyError:
            logging.warning("no valid mean provided, calculate 'mean' from current data")
            mean = v_data.mean(dim = ['lat', 'lon'])
        mean_base = mean.sel(lat=lat_base, lon=lon_base, method='nearest')
        return ((sector - mean_base) ** 2).mean(dim=["lat", "lon"])
    
    elif stat == 'mean':
        logging.info("calculating mean")
        return sector.mean(dim = ['lat', 'lon', 'time'])
#%%
def band_mean(v_data):
    v_data_cut = v_data.sel(lat=slice(5, 85))   
    mean_band = v_data_cut.groupby(
        lat=UniqueGrouper(), lon=UniqueGrouper() # time should be averaged
    ).apply(band_stat, v_data=v_data, stat = 'mean')

    # de weight data with cos(lat)
    mean_band = mean_band / np.cos(np.deg2rad(mean_band.lat))
    return mean_band
#%%
def band_variance(v_data, **kwargs):
    v_data_cut = v_data.sel(lat=slice(5, 85))
    variance_band = v_data_cut.groupby(
        lat=UniqueGrouper(), lon=UniqueGrouper(), time = UniqueGrouper() # time should be retained
    ).apply(band_stat, v_data=v_data, stat = 'var', **kwargs)
    # deweight data with cos(lat)
    variance_band = variance_band / np.cos(np.deg2rad(variance_band.lat))

    return variance_band