# %%
import xarray as xr
import numpy as np
import pandas as pd

import metpy.calc as mpcalc
from metpy.units import units
import metpy.constants as mpconstants

import sys
import os
import logging
import glob

logging.basicConfig(level=logging.INFO)
#%%
def thermal_wind(zg):
    zg = zg.metpy.assign_crs(
    grid_mapping_name='latitude_longitude',
    earth_radius=6371229.0
)
    zg = zg.metpy.quantify()
    u_g, v_g = mpcalc.geostrophic_wind(zg)
    v_g = v_g.sortby('plev', ascending=True)

    v_g = v_g.metpy.assign_crs(
    grid_mapping_name='latitude_longitude',
    earth_radius=6371229.0
)

    d_vg_dp = v_g.differentiate('plev')

    # thermal wind 
    v_t = d_vg_dp.integrate('plev')

    v_t = v_t.metpy.dequantify().drop_vars('metpy_crs')
    v_t.name = 'vt'

    return v_t

# %%
# nodes for different ensemble members
node = sys.argv[1]
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
member = node
data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily/r{member}i1p1f1/"
save_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vt_daily/r{member}i1p1f1/"

if rank == 0:
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    logging.info(f"Processing ensemble member {node}")

# %%
# %%
all_zg_files = glob.glob(data_path + "*.nc")
# %%
single_zg_files = np.array_split(all_zg_files, size)[rank]
# %%
for i, zg_file in enumerate(single_zg_files):
    logging.info(f"rank {rank} Processing {i+1}/{len(single_zg_files)}")
    ds = xr.open_dataset(zg_file, chunks ='auto')
    ds = ds['zg']
    v_t = thermal_wind(ds)
    to_file_name = save_path + zg_file.split('/')[-1]
    # replace 'zg' in to_file_name with 'vt'
    to_file_name = to_file_name.replace('zg', 'vt')
    v_t.to_netcdf(to_file_name)
    ds.close()
    v_t.close()