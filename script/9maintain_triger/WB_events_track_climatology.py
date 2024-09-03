# %%
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import glob
import logging
import sys

logging.basicConfig(level=logging.WARNING)
import seaborn as sns

# %%
import src.ConTrack.track_statistic as ts
import src.extremes.extreme_read as er

# %%
import importlib

importlib.reload(ts)


# %%
def read_WB_events(period="first10", break_type="AWB"):
    WB_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wavebreak_events/{break_type}_events_{period}/"

    WBs = []
    for ens in range(1, 51):
        WB = pd.read_csv(glob.glob(f"{WB_path}wb_events_*r{ens}i1p1f1.csv")[0])
        WB["ens"] = ens
        WBs.append(WB)

    WBs = pd.concat(WBs)

    # time to datetime
    WBs["Date"] = pd.to_datetime(WBs["Date"], format="%Y%m%d_%H")
    return WBs


# %%
first10_WBs = read_WB_events("first10")
# %%
last10_WBs = read_WB_events("last10")
# %%
fig, ax = plt.subplots(
    1, 2, figsize=(10, 5), subplot_kw=dict(projection=ccrs.PlateCarree(-120))
)
for ens in first10_WBs["ens"].unique():
    ts.plot_tracks(first10_WBs[first10_WBs["ens"] == ens], ax[0])

ax[0].set_title("WB events in the First 10 years ")

for ens in last10_WBs["ens"].unique():
    ts.plot_tracks(last10_WBs[last10_WBs["ens"] == ens], ax[1])

ax[1].set_title("WB events in the Last 10 years ")

# draw box
# pacific  [130,230, 35, 65]
# atlantic  [290, 20, 35, 65]
ax[0].plot(
    [130, 130, 230, 230, 130],
    [35, 65, 65, 35, 35],
    transform=ccrs.PlateCarree(),
    color="red",
)

ax[0].plot(
    [290, 290, 360, 360, 290],
    [35, 65, 65, 35, 35],
    transform=ccrs.PlateCarree(),
    color="red",
)
ax[0].plot(
    [0, 0, 20, 20, 0],
    [35, 65, 65, 35, 35],
    transform=ccrs.PlateCarree(),
    color="red",
)

for ax in [ax[0], ax[1]]:
    ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])
    ax.set_xticks(range(0, 360, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(0, 360, 60)])
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/Scherrer_wave_break_climatology_track.png"
)
# %%
# pacific WBs [130,230, 35, 65]
# atlantic WBs [290, 20, 35, 65]


def sel_pacific(wb):
    pac_dur = wb.groupby("Flag")[wb.columns].filter(
        lambda x: (x.iloc[0]["Longitude"] > 130)
        & (x.iloc[0]["Longitude"] < 230)
        & (x.iloc[0]["Latitude"] > 35)
        & (x.iloc[0]["Latitude"] < 65)
    )
    return pac_dur.drop(columns='Unnamed: 0')


def sel_atlantic(wb):
    atl_dur = wb.groupby("Flag")[wb.columns].filter(
        lambda x: ((x.iloc[0]["Longitude"] > 290) | (x.iloc[0]["Longitude"] < 20))
        & (x.iloc[0]["Latitude"] > 35)
        & (x.iloc[0]["Latitude"] < 65)
    )
    return atl_dur.drop(columns='Unnamed: 0')

#%%
def wb_duration(wb):
    dur = wb.groupby("Flag").size()
    return dur
# %%

first10_WBs_pacific = sel_pacific(first10_WBs)
last10_WBs_pacific = sel_pacific(last10_WBs)

first10_WBs_atlantic = sel_atlantic(first10_WBs)
last10_WBs_atlantic = sel_atlantic(last10_WBs)


# %%
first10_WBs_pacific_dur = first10_WBs_pacific.groupby("Flag").size()
last10_WBs_pacific_dur = last10_WBs_pacific.groupby("Flag").size()

first10_WBs_atlantic_dur = first10_WBs_atlantic.groupby("Flag").size()
last10_WBs_atlantic_dur = last10_WBs_atlantic.groupby("Flag").size()
# %%
fig, ax = plt.subplots(1, 2, figsize=(10, 7))
bins = np.arange(5, 20, 2)
sns.histplot(first10_WBs_pacific_dur, ax=ax[0], bins=bins, kde=False)
sns.histplot(last10_WBs_pacific_dur, ax=ax[0], bins=bins, kde=False, alpha=0.5)

ax[0].set_title("Pacific WBs")
sns.histplot(first10_WBs_atlantic_dur, ax=ax[1], bins=bins, kde=False)
sns.histplot(last10_WBs_atlantic_dur, ax=ax[1], bins=bins, kde=False, alpha=0.5)
ax[1].set_title("Atlantic WBs")
ax[0].set_xlabel("Duration (days)")
ax[1].set_xlabel("Duration (days)")


# plt.savefig(
#     "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/Scherrer_wave_break_climatology_duration.png"
# )
# %%
## read NAO positive and negative events
first10_pos, first10_neg = er.read_extremes_allens("first10", 8)
last10_pos, last10_neg = er.read_extremes_allens("last10", 8)

#%%
first10_pos = first10_pos[first10_pos['plev'] == 25000]
last10_pos = last10_pos[last10_pos['plev'] == 25000]
# %%
# pos only
nao = first10_pos
wb = first10_WBs

#%%
WB_before_NAO = []
WB_after_NAO = []

for ens in range(1,51):
    nao = nao[nao['ens'] == ens]

    wb = wb[wb['ens'] == ens]

    wb_before_nao = ts.select_WB_before_NAO(nao, wb)
    wb_after_nao = ts.select_WB_after_NAO(nao, wb)

    if not wb_before_nao.empty:
        wb_before_nao['ens'] = ens
        WB_before_NAO.append(wb_before_nao)

    if not wb_after_nao.empty:
        wb_after_nao['ens'] = ens
        WB_after_NAO.append(wb_after_nao)

#%%
WB_before_NAO = pd.concat(WB_before_NAO)
WB_after_NAO = pd.concat(WB_after_NAO)

# %%
