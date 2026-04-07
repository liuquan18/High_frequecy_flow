#%%
import xarray as xr
import pandas as pd
import numpy as np
# %%
ua_first = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_hat_monthly_ensmean/ua_hat_monmean_ensmean_185005_185909.nc")
ua_last = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_hat_monthly_ensmean/ua_hat_monmean_ensmean_209005_209909.nc")
# %%
eddy_ua_first = ua_first.sel(plev = slice(100000, 85000))
eddy_ua_last = ua_last.sel(plev = slice(100000, 85000))

# %%
eddy_ua_first = eddy_ua_first.ua.mean(dim = ('time', 'plev'))
eddy_ua_last = eddy_ua_last.ua.mean(dim = ('time', 'plev'))
#%%
# only northern hemisphere
eddy_ua_first = eddy_ua_first.sel(lat = slice(0, 90))
eddy_ua_last = eddy_ua_last.sel(lat = slice(0, 90))
# %%
def jet_location(ua):
    """Return the latitude of the maximum zonal mean zonal wind.

    Parameters
    ----------
    ua : xr.DataArray
        Zonal wind with at least a 'lat' dimension.

    Returns
    -------
    float or xr.DataArray
        Latitude of the jet stream maximum.
    """
    ua_zm = ua.mean(dim='lon') if 'lon' in ua.dims else ua
    return ua_zm.lat.isel(lat=ua_zm.argmax(dim='lat'))

# %%
jet_loc_first = jet_location(eddy_ua_first) # 47.56392575
jet_loc_last = jet_location(eddy_ua_last) # 49.4291537
# %%
