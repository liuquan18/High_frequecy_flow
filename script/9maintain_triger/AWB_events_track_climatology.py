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
    2, 1, figsize=(10, 10), subplot_kw=dict(projection=ccrs.PlateCarree(-120))
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
    pac_dur = wb.groupby(["Flag", "ens"])[wb.columns].filter(
        lambda x: (x.iloc[0]["Longitude"] > 130)
        & (x.iloc[0]["Longitude"] < 230)
        & (x.iloc[0]["Latitude"] > 35)
        & (x.iloc[0]["Latitude"] < 65)
    )
    return pac_dur


def sel_atlantic(wb):
    atl_dur = wb.groupby(["Flag", "ens"])[wb.columns].filter(
        lambda x: ((x.iloc[0]["Longitude"] > 290) | (x.iloc[0]["Longitude"] < 20))
        & (x.iloc[0]["Latitude"] > 35)
        & (x.iloc[0]["Latitude"] < 65)
    )
    return atl_dur


# %%
def wb_duration(wb):
    dur = wb.groupby(["Flag", "ens"])[wb.columns].size()
    return dur


# %%
def delta_lon(wb):
    wb = wb.groupby(["Flag", "ens"])[["Longitude"]].apply(
        lambda x: x[x["Longitude"] == x["Longitude"].max()].values.reshape(-1)[0]
        - x[x["Longitude"] == x["Longitude"].min()].values.reshape(-1)[0]
    )
    return wb

def delta_lat(wb):
    wb = wb.groupby(["Flag", "ens"])[["Latitude"]].apply(
        lambda x: x[x["Latitude"] == x["Latitude"].max()].values.reshape(-1)[0]
        - x[x["Latitude"] == x["Latitude"].min()].values.reshape(-1)[0]
    )
    return wb

# %%

first10_WBs_pacific = sel_pacific(first10_WBs)
last10_WBs_pacific = sel_pacific(last10_WBs)

first10_WBs_atlantic = sel_atlantic(first10_WBs)
last10_WBs_atlantic = sel_atlantic(last10_WBs)

# %%
# use the function to calculate the duration of each WB
first10_WBs_pacific_dur = wb_duration(first10_WBs_pacific)
last10_WBs_pacific_dur = wb_duration(last10_WBs_pacific)

first10_WBs_atlantic_dur = wb_duration(first10_WBs_atlantic)
last10_WBs_atlantic_dur = wb_duration(last10_WBs_atlantic)

# %%
fig, ax = plt.subplots(1, 2, figsize=(10, 7))
bins = np.arange(5, 20, 2)
sns.histplot(first10_WBs_pacific_dur, ax=ax[0], bins=bins, kde=False)
sns.histplot(last10_WBs_pacific_dur, ax=ax[0], bins=bins, kde=False, alpha=0.5)

# add legend
ax[0].legend(["First 10 years", "Last 10 years"])

ax[0].set_title("Pacific WBs")
sns.histplot(first10_WBs_atlantic_dur, ax=ax[1], bins=bins, kde=False)
sns.histplot(last10_WBs_atlantic_dur, ax=ax[1], bins=bins, kde=False, alpha=0.5)
ax[1].set_title("Atlantic WBs")
ax[0].set_xlabel("Duration (days)")
ax[1].set_xlabel("Duration (days)")


plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/Scherrer_wave_break_climatology_duration.png"
)

# %%
# calculate the elongation of the WBs
first10_WBs_pacific_elong = delta_lon(first10_WBs_pacific)
last10_WBs_pacific_elong = delta_lon(last10_WBs_pacific)

first10_WBs_atlantic_elong = delta_lon(first10_WBs_atlantic)
last10_WBs_atlantic_elong = delta_lon(last10_WBs_atlantic)
# %%
fig, ax = plt.subplots(1, 2, figsize=(10, 7))
bins = np.arange(0, 51, 2)
sns.histplot(first10_WBs_pacific_elong, ax=ax[0], bins=bins, kde=False)
sns.histplot(last10_WBs_pacific_elong, ax=ax[0], bins=bins, kde=False, alpha=0.5)

# add legend
ax[0].legend(["First 10 years", "Last 10 years"])

ax[0].set_title("Pacific WBs")
sns.histplot(first10_WBs_atlantic_elong, ax=ax[1], bins=bins, kde=False)
sns.histplot(last10_WBs_atlantic_elong, ax=ax[1], bins=bins, kde=False, alpha=0.5)
ax[1].set_title("Atlantic WBs")
ax[0].set_xlabel("delta lon (°)")
ax[1].set_xlabel("delta lon (°)")
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/Scherrer_wave_break_climatology_delta_lon.png"
)

#%%
# delta latitude
first10_WBs_pacific_lat = delta_lat(first10_WBs_pacific)
last10_WBs_pacific_lat = delta_lat(last10_WBs_pacific)

first10_WBs_atlantic_lat = delta_lat(first10_WBs_atlantic)
last10_WBs_atlantic_lat = delta_lat(last10_WBs_atlantic)
#%%
fig, ax = plt.subplots(1, 2, figsize=(10, 7))
bins = np.arange(0, 30, 2)
sns.histplot(first10_WBs_pacific_lat, ax=ax[0], bins=bins, kde=False)
sns.histplot(last10_WBs_pacific_lat, ax=ax[0], bins=bins, kde=False, alpha=0.5)

# add legend
ax[0].legend(["First 10 years", "Last 10 years"])

ax[0].set_title("Pacific WBs")
sns.histplot(first10_WBs_atlantic_lat, ax=ax[1], bins=bins, kde=False)
sns.histplot(last10_WBs_atlantic_lat, ax=ax[1], bins=bins, kde=False, alpha=0.5)
ax[1].set_title("Atlantic WBs")
ax[0].set_xlabel("delta lat (°)")
ax[1].set_xlabel("delta lat (°)")
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/Scherrer_wave_break_climatology_delta_lat.png"
)



# %%
## read NAO positive and negative events
first10_pos, first10_neg = er.read_extremes_allens("first10", 8)
last10_pos, last10_neg = er.read_extremes_allens("last10", 8)

# %%
first10_pos = first10_pos[first10_pos["plev"] == 25000]
last10_pos = last10_pos[last10_pos["plev"] == 25000]

# %%
def WB_NAO_concurrence(NAO, WB):
    WB_before_NAO = []
    WB_during_NAO = []

    for ens in range(1, 51):
        nao = NAO[NAO["ens"] == ens]

        wb = WB[WB["ens"] == ens]

        wb_before_nao = ts.select_WB_before_NAO(nao, wb)
        wb_during_nao = ts.select_WB_during_NAO(nao, wb)

        if not wb_before_nao.empty:
            wb_before_nao["ens"] = ens
            WB_before_NAO.append(wb_before_nao)

        if not wb_during_nao.empty:
            wb_during_nao["ens"] = ens
            WB_during_NAO.append(wb_during_nao)
    try:
        WB_before_NAO = pd.concat(WB_before_NAO)
    except ValueError:
        WB_before_NAO = pd.DataFrame()
        logging.warning("No WB before NAO+")
    
    try:
        WB_during_NAO = pd.concat(WB_during_NAO)
    except ValueError:
        WB_during_NAO = pd.DataFrame()
        logging.warning("No WB during NAO")

    return WB_before_NAO, WB_during_NAO

# %%
first_NAO = first10_pos # AWB corresponds to NAO positive
last_NAO = last10_pos
#%%
first_pacific_AWB_before_NAO, first_pacific_AWB_during_NAO = WB_NAO_concurrence(first_NAO, first10_WBs_pacific)

#%%
last_pacific_AWB_before_NAO, last_pacific_AWB_during_NAO = WB_NAO_concurrence(last_NAO, last10_WBs_pacific)
#%%
first_atlantic_AWB_before_NAO, first_atlantic_AWB_during_NAO = WB_NAO_concurrence(first_NAO, first10_WBs_atlantic)

#%%
last_atlantic_AWB_before_NAO, last_atlantic_AWB_during_NAO = WB_NAO_concurrence(last_NAO, last10_WBs_atlantic)
# %%
# duration for before pacific
first_pacific_AWB_before_NAO_dur = wb_duration(first_pacific_AWB_before_NAO)
last_pacific_AWB_before_NAO_dur = wb_duration(last_pacific_AWB_before_NAO)

# duration for during pacific
first_pacific_AWB_during_NAO_dur = wb_duration(first_pacific_AWB_during_NAO)
last_pacific_AWB_during_NAO_dur = wb_duration(last_pacific_AWB_during_NAO)

# duration for before atlantic
first_atlantic_AWB_before_NAO_dur = wb_duration(first_atlantic_AWB_before_NAO)
last_atlantic_AWB_before_NAO_dur = wb_duration(last_atlantic_AWB_before_NAO)

# duration for during atlantic
first_atlantic_AWB_during_NAO_dur = wb_duration(first_atlantic_AWB_during_NAO)
last_atlantic_AWB_during_NAO_dur = wb_duration(last_atlantic_AWB_during_NAO)
# %%
fig, ax = plt.subplots(2, 2, figsize=(10, 10))
bins = np.arange(5, 20, 1)

# before NAO
sns.histplot(first_pacific_AWB_before_NAO_dur, ax=ax[0, 0], bins=bins, kde=False)
sns.histplot(last_pacific_AWB_before_NAO_dur, ax=ax[0, 0], bins=bins, kde=False, alpha=0.5)

# add legend
ax[0, 0].legend(["First 10 years", "Last 10 years"])
ax[0, 0].set_title("Pacific WBs before NAO+")

sns.histplot(first_atlantic_AWB_before_NAO_dur, ax=ax[0, 1], bins=bins, kde=False)
sns.histplot(last_atlantic_AWB_before_NAO_dur, ax=ax[0, 1], bins=bins, kde=False, alpha=0.5)
ax[0, 1].set_title("Atlantic WBs before NAO+")

# during NAO
sns.histplot(first_pacific_AWB_during_NAO_dur, ax=ax[1, 0], bins=bins, kde=False)
sns.histplot(last_pacific_AWB_during_NAO_dur, ax=ax[1, 0], bins=bins, kde=False, alpha=0.5)

sns.histplot(first_atlantic_AWB_during_NAO_dur, ax=ax[1, 1], bins=bins, kde=False)
sns.histplot(last_atlantic_AWB_during_NAO_dur, ax=ax[1, 1], bins=bins, kde=False, alpha=0.5)

ax[1, 0].set_title("Pacific WBs during NAO")
ax[1, 1].set_title("Atlantic WBs during NAO")

ax[1, 0].set_xlabel("Duration (days)")
ax[1,1].set_xlabel("Duration (days)")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/Scherrer_wave_break_climatology_beforeduring_NAO+_duration.png"
)
# %%
# elongation for before pacific
first_pacific_AWB_before_NAO_elong = delta_lon(first_pacific_AWB_before_NAO)
last_pacific_AWB_before_NAO_elong = delta_lon(last_pacific_AWB_before_NAO)

# elongation for during pacific
first_pacific_AWB_during_NAO_elong = delta_lon(first_pacific_AWB_during_NAO)
last_pacific_AWB_during_NAO_elong = delta_lon(last_pacific_AWB_during_NAO)

# elongation for before atlantic
first_atlantic_AWB_before_NAO_elong = delta_lon(first_atlantic_AWB_before_NAO)
last_atlantic_AWB_before_NAO_elong = delta_lon(last_atlantic_AWB_before_NAO)

# elongation for during atlantic
first_atlantic_AWB_during_NAO_elong = delta_lon(first_atlantic_AWB_during_NAO)
last_atlantic_AWB_during_NAO_elong = delta_lon(last_atlantic_AWB_during_NAO)
# %%
fig, ax = plt.subplots(2, 2, figsize=(10, 10))
bins = np.arange(0, 51, 2)

# before NAO
sns.histplot(first_pacific_AWB_before_NAO_elong, ax=ax[0, 0], bins=bins, kde=False)
sns.histplot(last_pacific_AWB_before_NAO_elong, ax=ax[0, 0], bins=bins, kde=False, alpha=0.5)


sns.histplot(first_atlantic_AWB_before_NAO_elong, ax=ax[0, 1], bins=bins, kde=False)
sns.histplot(last_atlantic_AWB_before_NAO_elong, ax=ax[0, 1], bins=bins, kde=False, alpha=0.5)

# add legend
ax[0, 0].legend(["First 10 years", "Last 10 years"])
ax[0, 0].set_title("Pacific WBs before NAO+")
ax[0, 1].set_title("Atlantic WBs before NAO+")

# during NAO
sns.histplot(first_pacific_AWB_during_NAO_elong, ax=ax[1, 0], bins=bins, kde=False)
sns.histplot(last_pacific_AWB_during_NAO_elong, ax=ax[1, 0], bins=bins, kde=False, alpha=0.5)

sns.histplot(first_atlantic_AWB_during_NAO_elong, ax=ax[1, 1], bins=bins, kde=False)
sns.histplot(last_atlantic_AWB_during_NAO_elong, ax=ax[1, 1], bins=bins, kde=False, alpha=0.5)

ax[1, 0].set_title("Pacific WBs during NAO")
ax[1, 1].set_title("Atlantic WBs during NAO")

ax[1, 0].set_xlabel("delta lon (°)")
ax[1,1].set_xlabel("delta lon (°)")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/Scherrer_wave_break_climatology_beforeduring_NAO+_delta_lon.png"
)
# %%

# delta latitude
# elongation for before pacific
first_pacific_AWB_before_NAO_lat = delta_lat(first_pacific_AWB_before_NAO)
last_pacific_AWB_before_NAO_lat = delta_lat(last_pacific_AWB_before_NAO)

# elongation for during pacific
first_pacific_AWB_during_NAO_lat = delta_lat(first_pacific_AWB_during_NAO)
last_pacific_AWB_during_NAO_lat = delta_lat(last_pacific_AWB_during_NAO)

# elongation for before atlantic
first_atlantic_AWB_before_NAO_lat = delta_lat(first_atlantic_AWB_before_NAO)
last_atlantic_AWB_before_NAO_lat = delta_lat(last_atlantic_AWB_before_NAO)

# elongation for during atlantic
first_atlantic_AWB_during_NAO_lat = delta_lat(first_atlantic_AWB_during_NAO)
last_atlantic_AWB_during_NAO_lat = delta_lat(last_atlantic_AWB_during_NAO)
# %%
fig, ax = plt.subplots(2, 2, figsize=(10, 10))
bins = np.arange(0, 30, 2)

# before NAO
sns.histplot(first_pacific_AWB_before_NAO_lat, ax=ax[0, 0], bins=bins, kde=False)
sns.histplot(last_pacific_AWB_before_NAO_lat, ax=ax[0, 0], bins=bins, kde=False, alpha=0.5)

sns.histplot(first_atlantic_AWB_before_NAO_lat, ax=ax[0, 1], bins=bins, kde=False)
sns.histplot(last_atlantic_AWB_before_NAO_lat, ax=ax[0, 1], bins=bins, kde=False, alpha=0.5)

# add legend
ax[0, 0].legend(["First 10 years", "Last 10 years"])
ax[0, 0].set_title("Pacific WBs before NAO+")
ax[0, 1].set_title("Atlantic WBs before NAO+")

# during NAO
sns.histplot(first_pacific_AWB_during_NAO_lat, ax=ax[1, 0], bins=bins, kde=False)
sns.histplot(last_pacific_AWB_during_NAO_lat, ax=ax[1, 0], bins=bins, kde=False, alpha=0.5)


sns.histplot(first_atlantic_AWB_during_NAO_lat, ax=ax[1, 1], bins=bins, kde=False)
sns.histplot(last_atlantic_AWB_during_NAO_lat, ax=ax[1, 1], bins=bins, kde=False, alpha=0.5)

ax[1, 0].set_title("Pacific WBs during NAO")
ax[1, 1].set_title("Atlantic WBs during NAO")

ax[1, 0].set_xlabel("delta lat (°)")
ax[1,1].set_xlabel("delta lat (°)")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/Scherrer_wave_break_climatology_beforeduring_NAO+_delta_lat.png"
)
# %%
