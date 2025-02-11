#%%
import xarray as xr
import numpy as np
import glob 
import os
import sys
import logging
import metpy.constants as mpconstants

logging.basicConfig(level=logging.INFO)

# %%
import src.moisture.moist_thermal_wind as mtw
#%%
import importlib
importlib.reload(mtw)
# %%
member = sys.argv[1]
#%%
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
T_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ta_daily/r{member}i1p1f1/"
sd_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/sd_daily_std/r{member}i1p1f1/"
malr_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/malr_daily/r{member}i1p1f1/"
hus_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/hus_daily_std/r{member}i1p1f1/"
#%%
mtw_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/mtw_daily/r{member}i1p1f1/"
if rank == 0:
    if not os.path.exists(mtw_path):
        os.makedirs(mtw_path)
    logging.info(f"This node is processing {member}")
# %%
decs = np.arange(1850, 2099, 10)
decs_single = np.array_split(decs, size)[rank]
# %%
for i, dec in enumerate(decs_single):
    logging.info(f"rank {rank} Processing {i+1}/{len(decs_single)}")

    T_file = glob.glob(T_path + f"*{dec}*.nc")[0]
    sd_file = glob.glob(sd_path + f"*{dec}*.nc")[0]
    malr_file = glob.glob(malr_path + f"*{dec}*.nc")[0]
    hus_file = glob.glob(hus_path + f"*{dec}*.nc")[0]

    T = xr.open_dataset(T_file).ta
    sd_std = xr.open_dataset(sd_file).sd
    malr = xr.open_dataset(malr_file).malr
    hus_std = xr.open_dataset(hus_file).hus

    # factor
    factor = mtw.factor(T)

    # Lv/T
    Lv_T = mtw.Lv_T(T)

    # equation
    vtm_plev = factor * malr * sd_std + factor * malr * Lv_T * hus_std
    vtm = vtm_plev.integrate("plev")

    vtm.name = 'vtm'

    outfile_basename = T_file.split('/')[-1].replace('ta', 'vtm')
    vtm.to_netcdf(mtw_path + outfile_basename)
    T.close()
    sd_std.close()
    malr.close()
    hus_std.close()
    vtm.close()
# %%
