#%%
import xarray as xr
import pandas as pd
import numpy as np
# %%
def _eddy_jet (ua):
    ua = ua.assign_coords(lon=(ua.lon + 180) % 360 - 180).sortby("lon") # -180 to 180
    ua = ua.sel(lat = slice(0, 90)) # NAO region, the same for composite mean
    # smooth over lat
    ua = ua.rolling(lat=5, center=True).mean()
    ua = ua.groupby("time.year").mean(dim="time") # annual mean
    return ua.sel(plev = slice(100000, 85000)).mean(dim = ('plev', 'lon')) # zonal mean eddy driven jet

def jet_latitude(ua):
    # average over lon if present, then find lat of max ua
    if "lon" in ua.dims:
        ua = ua.mean(dim="lon")
    jet_lat = ua.idxmax(dim="lat")
    jet_lat_df = jet_lat.to_dataframe("jet_lat").reset_index()
    return jet_lat_df

#%%
base_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_hat_monthly_ensmean"
ua_decades = xr.open_mfdataset(base_dir + "/*.nc", combine='by_coords', preprocess=_eddy_jet, parallel=True)
ua_decades.load()
#%%
# asign the decade coordinate, 1859 to 1850
decade=ua_decades['year'] // 10 * 10
ua_decades['year'] = decade
ua_decades = ua_decades.rename({'year': 'decade'})
#%%
ua_decades = ua_decades.ua
ua_jet_loc = ua_decades.idxmax(dim="lat")
#%%
#%%
