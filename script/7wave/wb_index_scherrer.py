#%%
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import glob
import sys
import logging

logging.basicConfig(level=logging.WARNING)
# %%
import src.blocking.wave_breaking as wbi
#%%
import importlib
importlib.reload(wbi)

# %%
def calculate_wave_breaking_index(period, ens):
    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily_global/zg_MJJAS_ano_{period}/"
    file = glob.glob(f"{base_dir}zg_day_*_r{ens}i1p1f1_gn_*.nc")[0]

    to_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wavebreak_index/wb_{period}/"
    outfile= f"{to_dir}wb_index_{period}_r{ens}i1p1f1.nc"

    ds = xr.open_dataset(file)
    zg = ds.zg.sel(plev = 25000)

    wb = wbi.wave_breaking_index(zg)

    wb.to_netcdf(outfile)

# %%
# node for period, and rank for different ensemble members
try:
    node = int(sys.argv[1])

except ValueError:
    logging.warning("no node number provided, using default node 0")
    node = 0

periods = ["first10", "last10"]
period = periods[node]

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


members_all = list(range(1, 51))  # all members
members_single = np.array_split(members_all, size)[rank]  # members on this core

for i, ens in enumerate(members_single):
    print(f"node {node} for period {period}, rank {rank}, {i+1}/{len(members_single)}")
    calculate_wave_breaking_index(period, ens)