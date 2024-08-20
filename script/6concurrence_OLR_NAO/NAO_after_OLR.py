# %%
import numpy as np
import pandas as pd
import xarray as xr
import logging
import matplotlib.pyplot as plt
import glob

#%%
import src.extremes.extreme_read as er
# %%
logging.basicConfig(level=logging.WARNING)
# %%
# read the NAO extremes
period = 'first10'
extreme_type = 'pos'
#%%
NAO_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{extreme_type}_extreme_events/{extreme_type}_extreme_events_first10/"
OLR_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_extremes_pos/OLR_extremes_pos_{period}/" # no extreme_type in the OLR_extremes
# %%
# read the NAO extremes
member = 1
dur_lim = 8
# %%
# read NAO positive extremes
NAO_file = glob.glob(f"{NAO_dir}troposphere_{extreme_type}_extreme_events*r{member}.csv")[0]
NAO_pos = pd.read_csv(NAO_file)
NAO_pos = NAO_pos[NAO_pos['plev'] == 25000]

# select extremes based on minimum duration
NAO_pos = er.sel_event_above_duration(NAO_pos, duration=dur_lim, by="extreme_duration")
# select columns
NAO_pos = NAO_pos[['sign_start_time', 'extreme_duration']]
# %%
# read OLR extremes
OLR_file = glob.glob(f"{OLR_dir}OLR_extremes*r{member}.csv")[0]
OLR = pd.read_csv(OLR_file)
# select extremes based on minimum duration
OLR = er.sel_event_above_duration(OLR, duration=dur_lim, by="extreme_duration")
# select columns
OLR = OLR[['sign_start_time', 'extreme_duration', 'spatial','lat', 'lon']]

# %%
G = OLR.groupby('spatial')
# %%
def NAO_before_OLR(NAO, OLR):