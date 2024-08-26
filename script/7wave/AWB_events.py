#%%
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec
import glob
# %%
import src.ConTrack.contrack as ct
#%%
import importlib
importlib.reload(ct)
# %%
def awb_event(period: str, ens : int, plev : int = 25000):
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
        persistence=3,
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
    WB_df.to_csv(outname)
# %%
