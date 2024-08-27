#%%
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import glob
import logging
import sys
logging.basicConfig(level=logging.WARNING)

#%%
import src.extremes.extreme_read as er
import src.ConTrack.track_statistic as ts

#%%
import importlib
importlib.reload(ts)

# %%

first10_pos_AWBs = []
for ens in range(1,51):
    _, AWB = ts.read_NAO_WB('first10', ens, 25000, 'pos', 'AWB')
    first10_pos_AWBs.append(AWB)
first10_pos_AWBs = pd.concat(first10_pos_AWBs)



# %%
last10_pos_AWBs = []
for ens in range(1,51):
    NAO, AWB = ts.read_NAO_WB('last10', ens, 25000, 'pos', 'AWB')
    last10_pos_AWBs.append(AWB)

last10_pos_AWBs = pd.concat(last10_pos_AWBs)

# %%
fig, ax = plt.subplots(2, 1, figsize=(10,5), subplot_kw=dict(projection=ccrs.PlateCarree(-120)))
ts.plot_tracks(first10_pos_AWBs, ax[0])
ax[0].set_title('AWB events in the First 10 years ')

ts.plot_tracks(last10_pos_AWBs, ax[1])
ax[1].set_title('AWB events in the Last 10 years ')
ax[1].set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
ax[1].set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])
for ax in [ax[0], ax[1]]:
    ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])

plt.savefig('/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/AWB_all.png')
# %%
first10_pos_AWBs.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/WB_before_NAO/AWB_all_first10.csv", index=False)
last10_pos_AWBs.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/WB_before_NAO/AWB_all_last10.csv", index=False)
# %%
