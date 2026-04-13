#%%
import xarray as xr
import pandas as pd
import numpy as np
# %%
def _eddy_jet (ua):
    ua = ua.assign_coords(lon=(ua.lon + 180) % 360 - 180).sortby("lon") # -180 to 180
    ua = ua.sel(lon=slice(-90, 40),lat = slice(0, 90)) # NAO region, the same for composite mean
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
base_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_monthly_ensmean"
ua_decades = xr.open_mfdataset(base_dir + "/*.nc", combine='by_coords', preprocess=_eddy_jet)

#%%
# asign the decade coordinate, 1859 to 1850
ua_decades = ua_decades.assign_coords(decade=ua_decades['year'] // 10 * 10)
#%%
jet_lat_df = jet_latitude(ua_decades.ua)
#%%
jet_lat_df.plot(x = 'decade', y = 'jet_lat')
# %%
# save
jet_lat_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0flux_climatology/jet_latitude_alldecades.csv", index=False)