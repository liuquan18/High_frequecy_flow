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

# === mpi4py ===
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # [0,1,2,3,4,5,6,7,8,9]
    npro = comm.Get_size()  # 10
except:
    print("::: Warning: Proceeding without mpi4py! :::")
    rank = 0
    npro = 1


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
def process(ens, period):
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


    anti_array = wb.to_xarray(data=avor, events=anti_tracked)
    cyc_array = wb.to_xarray(data=avor, events=cyc_tracked)

    to_dir = (
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/skader_wb_events/"
    )

    # avor.to_netcdf(to_dir + f"AV/AV_{period}/AV_{period}_r{ens}.nc")
    # anti_tracked.to_csv(
    #     to_dir + f"AWB/AWB_{period}/AWB_{period}_r{ens}.csv", index=False
    # )
    # cyc_tracked.to_csv(
    #     to_dir + f"CWB/CWB_{period}/CWB_{period}_r{ens}.csv", index=False
    # )

    # save arrays
    anti_array.to_netcdf(to_dir + f"AWB_array/AWB_array_{period}/AWB_{period}_r{ens}.nc")
    cyc_array.to_netcdf(to_dir + f"CWB_array/CWB_array_{period}/CWB_{period}_r{ens}.nc")


# %%
# period from keyboard
period = sys.argv[1]  # 'first10' or 'last10'
all_ens = np.arange(1, 51)
# %%
ens_single = np.array_split(all_ens, npro)[rank]
for i, ens in enumerate(ens_single):
    logging.info(f"Period {period} ens {ens} rank {rank}: {i+1}/{len(ens_single)}")
    process(ens, period)
