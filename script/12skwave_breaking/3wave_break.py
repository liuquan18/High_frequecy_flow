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
def remap(ifile, var="ua", plev=25000):
    cdo = Cdo()

    ofile = cdo.remapnn("r192x96", input=ifile, options="-f nc", returnXArray=var)

    ofile = ofile.sel(plev=plev)

    return ofile

# %%
def wavebreaking(avor, mflux):

    # calculate overturnings index
    overturnings = wb.calculate_overturnings(
        data=avor,
        contour_levels=[4 * 1e-5], # 90th percentile of [20, 60]
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
def event_classify(events):
    # anticyclonic and cyclonic by intensity for the Northern Hemisphere
    anticyclonic = events[events.intensity > 0]
    cyclonic = events[events.intensity < 0]

    anti_tracked = wb.track_events(
        events=anticyclonic,
        time_range=24,  # time range for temporal tracking in hours
        method="by_overlap",  # method for tracking ["by_overlap", "by_distance"], optional
        buffer=1.9,  # buffer in degrees for polygons overlapping, spatial resolution is 1.875 
        overlap=0.3,  # minimum overlap percentage, optinal
    )  # distance in km for method "by_distance"

    cyc_tracked = wb.track_events(
        events=cyclonic,
        time_range=24,  # time range for temporal tracking in hours
        method="by_overlap",  # method for tracking ["by_overlap", "by_distance"], optional
        buffer=1.9,  # buffer in degrees for polygons overlapping, optional
        overlap=0.3,  # minimum overlap percentage, optinal
    )  


    # to array
    # anti_array = wb.to_xarray(data=avor, events=anti_tracked)
    # cyc_array = wb.to_xarray(data=avor, events=cyc_tracked)

    return anti_tracked, cyc_tracked
# %%
node = sys.argv[1]
ens = int(node)
logging.info(f"Processing ensemble {ens}")
# %%
#%%
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # [0,1,2,3,4,5,6,7,8,9]
    size = comm.Get_size()  # 10
except:
    logging.warning("::: Warning: Proceeding without mpi4py! :::")
    rank = 0
    size = 1
# %%
av_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/av_daily_ano/r{ens}i1p1f1/"
mf_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/upvp_daily_ano/r{ens}i1p1f1/"

awb_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/WB_awb_daily/r{ens}i1p1f1/"
cwb_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/WB_cwb_daily/r{ens}i1p1f1/"

if rank == 0:
    if not os.path.exists(awb_path):
        os.makedirs(awb_path)

    if not os.path.exists(cwb_path):
        os.makedirs(cwb_path)
# %%
all_decades = np.arange(1850, 2100, 10)
single_decades = np.array_split(all_decades, size)[rank]
# %%
for i, dec in enumerate(single_decades):
    logging.info(f"rank {rank} Processing {i+1}/{len(single_decades)}")


    av_file = glob.glob(av_path + f"av_day_MPI-ESM1-2-LR_r{ens}i1p1f1_gn_{dec}*.nc")
    av = xr.open_dataset(av_file[0])
    av = av.AV

    mf_file = glob.glob(mf_path + f"upvp_day_MPI-ESM1-2-LR_r{ens}i1p1f1_gn_{dec}*.nc")
    # remap mf, while av is remaped during its calculation
    mf = remap(mf_file[0], var = 'ua')

    events = wavebreaking(av, mf)

    anti_tracked, cyc_tracked = event_classify(events)

    anti_tracked.to_csv(
        awb_path + f"AWB_r{ens}_{dec}0502-{dec+9}0930.csv", index=False
    )

    cyc_tracked.to_csv(
        cwb_path + f"CWB_r{ens}_{dec}0502-{dec+9}0930.csv", index=False
    )

# %%
