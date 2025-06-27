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
def remap(ifile, var="ua", plev=None):
    cdo = Cdo()

    ofile = cdo.remapnn("r192x96", input=ifile, options="-f nc", returnXArray=var)
    if plev is not None:
        ofile = ofile.sel(plev=plev)

    return ofile

# %%
def wavebreaking(pv, mflux, mf_var="usvs"):
    pv = pv * 1e6
    pv = remap(pv, var = 'pv')
    mflux = remap(mflux, var = mf_var, plev = 25000)
    # contour_levels = [-2*1e-6, 2*1e-6]
    contour_levels = [-2, 2]
    
    smoothed = wb.calculate_smoothed_field(data=pv.sel(isentropic_level = 330),
                                        passes=5,
                                        weights=np.array([[0, 1, 0], [1, 2, 1], [0, 1, 0]]), # optional
                                        mode="wrap") # optional
    # smooth the mflux
    mflux = wb.calculate_smoothed_field(data=mflux,
                                        passes=5,
                                        weights=np.array([[0, 1, 0], [1, 2, 1], [0, 1, 0]]), # optional
                                        mode="wrap") # optional

    # make sure that the time of the smoothed data is the same as the mflux
    mflux['time'] = smoothed['time']


    contours = wb.calculate_contours(data=smoothed,
                                    contour_levels=contour_levels,
                                    periodic_add=120, # optional
                                    original_coordinates=False) # optional

    # calculate streamers
    streamers = wb.calculate_streamers(data=smoothed,
                                    contour_levels=contour_levels,
                                    contours=contours, #optional
                                    geo_dis=800, # optional
                                    cont_dis=1200, # optional
                                    intensity=mflux, # optional
                                    periodic_add=120) # optional


    # classify
    events = streamers
    # stratospheric and tropospheric (only for streamers and cutoffs)
    stratospheric = events[events.mean_var >= contour_levels[1]]
    tropospheric = events[events.mean_var < contour_levels[1]]


    # anticyclonic and cyclonic by intensity for the Northern Hemisphere
    anticyclonic = events[events.intensity >= 0]
    cyclonic = events[events.intensity < 0]



    # transform to xarray.DataArray
    stratospheric_array = wb.to_xarray(data=smoothed,
                            events=stratospheric)
    tropospheric_array = wb.to_xarray(data=smoothed,
                            events=tropospheric)
    anticyclonic_array = wb.to_xarray(data=smoothed,
                            events=anticyclonic)
    cyclonic_array = wb.to_xarray(data=smoothed,
                            events=cyclonic)

    return stratospheric_array, tropospheric_array, anticyclonic_array, cyclonic_array

# %%
node = sys.argv[1]
ens = int(node)
logging.info(f"Processing ensemble {ens}")
mf_var = "usvs"  # can change to transient flux

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
pv_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/pv_daily/r{ens}i1p1f1/"
mf_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/{mf_var}_daily/r{ens}i1p1f1/"  # change to transient flux

awb_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_anticyclonic_daily/r{ens}i1p1f1/"
cwb_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_cyclonic_daily/r{ens}i1p1f1/"


stratospheric_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_stratospheric_daily/r{ens}i1p1f1/"
tropospheric_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_tropospheric_daily/r{ens}i1p1f1/"


if rank == 0:
    if not os.path.exists(awb_path):
        os.makedirs(awb_path)

    if not os.path.exists(cwb_path):
        os.makedirs(cwb_path)

    if not os.path.exists(stratospheric_path):
        os.makedirs(stratospheric_path)
    if not os.path.exists(tropospheric_path):
        os.makedirs(tropospheric_path)
# %%
all_decades = np.arange(1850, 2100, 10)
single_decades = np.array_split(all_decades, size)[rank]

# %%
for i, dec in enumerate(single_decades):
    logging.info(f"rank {rank} Processing {i+1}/{len(single_decades)}")


    pv_file = glob.glob(pv_path + f"*{dec}*.nc")
    pv = xr.open_dataset(pv_file[0])
    pv = pv.pv

    mf_file = glob.glob(mf_path + f"*{dec}*.nc")
    mf = xr.open_dataset(mf_file[0])[mf_var]

    stratospheric_array, tropospheric_array, anticyclonic_array, cyclonic_array = wavebreaking(pv, mf, mf_var=mf_var)


    # save the data
    stratospheric_array.to_netcdf(stratospheric_path + f"wb_stratospheric_{ens}_{dec}.nc")
    tropospheric_array.to_netcdf(tropospheric_path + f"wb_tropospheric_{ens}_{dec}.nc")
    anticyclonic_array.to_netcdf(awb_path + f"wb_anticyclonic_{ens}_{dec}.nc")
    cyclonic_array.to_netcdf(cwb_path + f"wb_cyclonic_{ens}_{dec}.nc")
# %%
