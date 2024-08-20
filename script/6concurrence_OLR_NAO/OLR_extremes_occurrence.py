#%%
import pandas as pd
import xarray as xr
import numpy as np
import cartopy.crs as ccrs

#%%
import src.extremes.extreme_read as er
# %%
extreme = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_extremes_pos/OLR_extremes_pos_first10/OLR_extremes_pos_1850_1859_r1.csv")
# %%
def duration_of_extreme(extreme):
    """
    Calculate the duration of the extreme events
    """
    extreme_sel = er.sel_event_above_duration(extreme, duration=8, by="extreme_duration")
    extreme_sel = extreme_sel[['sign_start_time','extreme_duration','lat','lon']]
    extreme_sel = extreme_sel.set_index(["sign_start_time", "lat","lon"])

    # to xarray
    ext_x = extreme_sel.to_xarray()

    # calculate the sum duration of the extreme events
    extreme_duration = ext_x.extreme_duration.sum(dim = 'sign_start_time')

    return extreme_duration
# %%









$%%
p = extreme_duration.plot(
    subplot_kws = dict(
        projection = ccrs.PlateCarree(central_longitude=180)
    ),
    transform = ccrs.PlateCarree(),
    levels = np.arange(20, 100, 10),
)

p.axes.coastlines()
# %%
