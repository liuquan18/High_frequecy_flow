# %%
import wavebreaking as wb
import numpy as np
import pandas as pd
import xarray as xr
import metpy.calc as mpcalc
import metpy.units as mpunits
import cartopy.crs as ccrs
from cdo import *  # python version
import os
import sys
import glob
import logging

logging.basicConfig(level=logging.INFO)



# %%
# %%
def remap(ifile, var="ua", plev=25000):
    cdo = Cdo()

    ofile = cdo.remapnn("r192x96", input=ifile, options="-f nc", returnXArray=var)

    ofile = ofile.sel(plev=plev)

    return ofile


# %%
def abs_vorticity(u, v):
    u = u * mpunits.units("m/s")
    v = v * mpunits.units("m/s")
    u = u.metpy.assign_crs(grid_mapping_name="latitude_longitude", earth_radius=6371229)
    v = v.metpy.assign_crs(grid_mapping_name="latitude_longitude", earth_radius=6371229)
    avor = mpcalc.absolute_vorticity(u, v)
    avor.name = "AV"

    # smooth data
    smoothed = wb.calculate_smoothed_field(data=avor, passes=5)

    return smoothed


# %%
def wavebreaking(avor, mflux):
    # calculate contours
    contours = wb.calculate_contours(
        data=avor,
        contour_levels=[9.4 * 1e-5],
        periodic_add=120,  # optional
        original_coordinates=False,
    )  # optional

    # calculate overturnings index
    overturnings = wb.calculate_overturnings(
        data=avor,
        contour_levels=[9.4 * 1e-5],
        contours=contours,  # optional
        range_group=5,  # optional
        min_exp=5,  # optional
        intensity=mflux,  # optional
        periodic_add=120,
    )  # optional

    # classify
    events = overturnings

    # positive (anticyclonic) as 2, negative (cyclonic) as 1
    events = events.assign(mean_var=(events.intensity > 0).astype(int) + 1)

    return events


# %%
def read_data(ens, period):
    base_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/"
    ufile = glob.glob(
        base_dir + f"ua_daily_global/ua_MJJAS_{period}/ua_day_*_r{ens}i1p1f1_gn_*.nc"
    )[0]
    vfile = glob.glob(
        base_dir + f"va_daily_global/va_MJJAS_{period}/va_day_*_r{ens}i1p1f1_gn_*.nc"
    )[0]
    mfluxfile = glob.glob(
        base_dir
        + f"E_N_daily_global/E_N_MJJAS_{period}_prime/E_N_day_*_r{ens}i1p1f1_gn_*.nc"
    )[0]

    u = remap(ufile, "ua")
    v = remap(vfile, "va")
    mflux = remap(mfluxfile, "ua")

    try:
        mflux["time"] = mflux.indexes["time"].to_datetimeindex()

    except AttributeError:
        pass
    return u, v, mflux


# %%
ens = 1
period = "first10"

#%%


u, v, mflux = read_data(ens, period)
avor = abs_vorticity(u, v)
events = wavebreaking(avor, mflux)

# anticyclonic and cyclonic by intensity for the Northern Hemisphere
anticyclonic = events[events.intensity >= 0]
cyclonic = events[events.intensity < 0]

anti_tracked = wb.track_events(
    events=anticyclonic,
    time_range=24,  # time range for temporal tracking in hours
    method="by_overlap",  # method for tracking ["by_overlap", "by_distance"], optional
    buffer=0,  # buffer in degrees for polygons overlapping, optional
    overlap=0.5,  # minimum overlap percentage, optinal
    distance=1000,
)  # distance in km for method "by_distance"

cyc_tracked = wb.track_events(
    events=cyclonic,
    time_range=24,  # time range for temporal tracking in hours
    method="by_overlap",  # method for tracking ["by_overlap", "by_distance"], optional
    buffer=0,  # buffer in degrees for polygons overlapping, optional
    overlap=0.5,  # minimum overlap percentage, optinal
    distance=1000,
)  # distance in km for method "by_distance"

# %%
anti_array = wb.to_xarray(data=avor, events=anti_tracked)
# %%
wb.plot_step(flag_data=anti_array,
             step=0, #index or date
             data=avor, # optional
             contour_level=[-9.4 * 1e-5, 9.4 * 1e-5], # optional
             levels = np.arange(-15 * 1e-5, 16 * 1e-5, 5 * 1e-5), # optional
             proj=ccrs.PlateCarree(180), # optional
             size=(12,8), # optional
             periodic=True, # optional
             labels=True,# optional
             cmap="Blues", # optional
             color_events="gold", # optional
             title="") # optional

# %%
wb.plot_clim(flag_data=anti_array,
             seasons=[6,7,8], # optional
             proj=ccrs.PlateCarree(), # optional
             size=(12,8), # optional
            #  smooth_passes=0, # optional
             periodic=True, # optional
             labels=True, # optional
            #  levels=np.arange(-15 * 1e-5, 16 * 1e-5, 5 * 1e-5), # optional
             cmap=None, # optional
             title="") # optional
# %%
wb.plot_tracks(data=avor,
               events=anti_tracked,
               proj=ccrs.PlateCarree(), # optional
               size=(12,8), # optional
               min_path=2, # optional
               plot_events=True, # optional
               labels=True, # optional
               title="") # optional
# %%
