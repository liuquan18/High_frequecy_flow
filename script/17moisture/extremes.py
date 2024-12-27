#%%
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec
import glob
import logging
import sys
import os
logging.basicConfig(level=logging.WARNING)
# %%
import src.ConTrack.contrack as ct
#%%
import importlib
importlib.reload(ct)

# %%
def extract_extreme_1year(data, threshold, gorl = '>=', var = 'tas'):
    EE = ct.contrack()
    EE.ds = data

    EE.set_up(force=True)
    EE.run_contrack(
        variable=var,
        threshold=threshold, # quantile 0.99 of [0, 60] lat mean, 3.62 K for tas,  2 g/kg for hus, 12/-12 m/s for vt
        gorl = gorl,
        overlap=0.5,
        persistence=5,
        twosided=True,
    )

    return EE.flag
# %%
def extract_extremes(data, threshold, gorl = '>=', var = 'tas'):

    extremes = data.groupby('time.year').apply(extract_extreme_1year, threshold = threshold, gorl = gorl, var = var)
    return extremes


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
