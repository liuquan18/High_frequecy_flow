#%%
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
def abs_vorticity(u, v):
    u = u * mpunits.units("m/s")
    v = v * mpunits.units("m/s")
    u = u.metpy.assign_crs(grid_mapping_name="latitude_longitude", earth_radius=6371229)
    v = v.metpy.assign_crs(grid_mapping_name="latitude_longitude", earth_radius=6371229)
    avor = mpcalc.absolute_vorticity(u, v)
    avor.name = "AV"

    # smooth data
    smoothed = avor.rolling(time = 3, center = True).median()
    return smoothed

# %%
# nodes for different ensemble members
node = sys.argv[1]
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
#%%
member = int(node)
#%%
u_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily/r{member}i1p1f1/'
v_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily/r{member}i1p1f1/'

avor_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/avor_daily/r{member}i1p1f1/'

if rank == 0:
    if not os.path.exists(avor_path):
        os.makedirs(avor_path)

    logging.error(f"Processing ensemble member {node}")

# %%
all_decades = np.arange(1850, 2100, 10)
single_decades = np.array_split(all_decades, size)[rank]
# %%
for i, dec in enumerate(single_decades):
    logging.info(f"rank {rank} Processing {i+1}/{len(single_decades)}")

    u_files = glob.glob(u_path + f"ua_day_*_{dec}*.nc")
    v_files = glob.glob(v_path + f"va_day_*_{dec}*.nc")

    u = remap(u_files[0], var='ua')
    v = remap(v_files[0], var='va')

    avor = abs_vorticity(u, v)
    avor = avor.drop_vars('metpy_crs')

    filename = u_files[0].split('/')[-1]
    filename = filename.replace('ua', 'av')

    avor.to_netcdf(avor_path + filename)

# %%
