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
logging.basicConfig(level=logging.WARNING)
# %%
import src.ConTrack.contrack as ct
#%%
import importlib
importlib.reload(ct)
#%%
# nodes and cores
try:
    node = int(sys.argv[1])
except ValueError:
    logging.warning("no node number provided, using default node 0")
    node = 0

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
def awb_event(period: str, ens : int, plev : int = 25000, persistence : int = 3):
    WB = ct.contrack()
    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/momentum_fluxes_daily_global/momentum_fluxes_MJJAS_ano_{period}_prime/"
    file = glob.glob(f"{base_dir}momentum_fluxes_day_*_r{ens}i1p1f1_gn_*.nc")[0]

    
    WB.read(file)
    # convert Convert timedelta64 to a Supported Resolution: Convert the timedelta64 object to seconds (s) first, and then to hours (h).

    WB.ds['time'] = WB.ds.indexes['time'].to_datetimeindex()
    WB.ds = WB.ds.sel(plev = plev).drop('plev')
    
    WB.set_up(force=True)

    WB.run_contrack(
        variable='ua',
        threshold=50,
        gorl = '>=',
        overlap=0.5,
        persistence=persistence,
        twosided=True,
    )

    # life cycle
    WB_df = WB.run_lifecycle(flag = 'flag', variable='ua')
    # outname
    outname = file.split('/')[-1]
    outname = outname.split('.')[0]
    outname = outname.replace('momentum_fluxes_day_', 'WB_')
    outname = outname + '.csv'
    outname = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/AWB_events/AWB_events_{period}/{outname}"
    WB_df.to_csv(outname, index=False)
# %%
periods = ["first10", "last10"]
period = periods[node]
#%%
members_all = list(range(1, 51))  # all members
members_single = np.array_split(members_all, size)[rank]  # members on this core

#%%
for ens in members_single:
    print(f"Period {period}: Rank {rank}, member {ens}/{members_single[-1]}")
    awb_event(period, ens)