# %%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import logging
import cartopy.crs as ccrs
import matplotlib.colors as mcolors
import cartopy.feature as cfeature

idx = pd.IndexSlice
logging.basicConfig(level=logging.INFO)


# %%
def var_before_NAO(var, decade, phase):
    file_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_NAO_{phase}/{var}_NAO_{phase}_{decade}.csv"
    data = pd.read_csv(file_path, index_col=[0, 1])
    return data


def read_data(var):
    first_NAO_pos = var_before_NAO(var, 1850, "pos")
    first_NAO_neg = var_before_NAO(var, 1850, "neg")

    last_NAO_pos = var_before_NAO(var, 2090, "pos")
    last_NAO_neg = var_before_NAO(var, 2090, "neg")

    return first_NAO_pos, first_NAO_neg, last_NAO_pos, last_NAO_neg


# %%
def lag_mean(df, name="ratio", lag=(-15, -5)):

    value_columns = np.arange(lag[0], lag[1]).astype(str)

    df[name + "_lag_mean"] = df[value_columns].mean(axis=1)
    return df


# %%
# basin mean util function
def zonal_mean(df):

    all_columns = df.columns
    value_columns = all_columns.difference(
        ["event_id", "ens", "lon", "extreme_duration", "extreme_start_time"]
    )

    # mean over selected lons
    df_zonmean = df.groupby(["event_id", "ens"])[value_columns].mean()

    # id info
    df_id = df.groupby(["event_id", "ens"])[
        ["extreme_duration", "extreme_start_time"]
    ].first()

    # merge
    df_final = pd.merge(df_id, df_zonmean, on=["event_id", "ens"], how="inner")

    df_final = df_final.reset_index().set_index("event_id")
    df_final.index.name = None

    return df_final


# %%
# hus_tas_ratio basin mean
def ratio_basin_mean(ratio):

    box_NAL = [-70, -35, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Atlantic
    box_NPO = [140, -145, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Pacific

    ratio = ratio.reset_index()
    ratio = ratio.rename(columns={"level_0": "event_id"})

    # sel lon
    ratio_NAL = ratio.loc[(ratio["lon"] >= box_NAL[0]) & (ratio["lon"] <= box_NAL[1])]
    ratio_NAL_zonmean = zonal_mean(ratio_NAL)

    ratio_NPO = ratio.loc[
        (ratio["lon"] >= box_NPO[0]) & (ratio["lon"] <= 180)
        | (ratio["lon"] >= -180) & (ratio["lon"] <= box_NPO[1])
    ]
    ratio_NPO_zonmean = zonal_mean(ratio_NPO)

    return ratio_NAL_zonmean, ratio_NPO_zonmean


# %%
def upvp_NA_mean(upvp):
    upvp = upvp.reset_index()
    upvp = upvp.rename(columns={"level_0": "event_id"})

    upvp_NA = upvp.loc[(upvp["lon"] >= -100) & (upvp["lon"] <= -10)]
    upvp_NA_zonmean = zonal_mean(upvp_NA)

    return upvp_NA_zonmean


def eke_2060_mean(eke):
    eke = eke.reset_index()
    eke = eke.rename(columns={"level_0": "event_id"})

    eke_2060_zonmean = zonal_mean(eke)

    return eke_2060_zonmean


# %%
def to_plot_data(eke):
    eke = eke.rename({"lag": "lat"})  # fake lat to plot correctly the lon
    eke["lat"] = eke["lat"] * 4  # fake lat to plot correctly the lon
    # Solve the problem on 180 longitude by extending the data
    eke = eke.reindex(lon=np.append(eke.lon.values, 180), method="nearest")
    lon_values = eke.lon.values
    lon_values[-1] = 180
    eke["lon"] = lon_values

    return eke


# %%
first_NAO_pos_eke, first_NAO_neg_eke, last_NAO_pos_eke, last_NAO_neg_eke = read_data(
    "eke"
)
first_NAO_pos_upvp, first_NAO_neg_upvp, last_NAO_pos_upvp, last_NAO_neg_upvp = (
    read_data("upvp")
)
first_NAO_pos_ratio, first_NAO_neg_ratio, last_NAO_pos_ratio, last_NAO_neg_ratio = (
    read_data("hus_tas_ratio")
)
# %%
# ratio
first_NAO_pos_ratio_NAL, first_NAO_pos_ratio_NPO = ratio_basin_mean(first_NAO_pos_ratio)
first_NAO_neg_ratio_NAL, first_NAO_neg_ratio_NPO = ratio_basin_mean(first_NAO_neg_ratio)

last_NAO_pos_ratio_NAL, last_NAO_pos_ratio_NPO = ratio_basin_mean(last_NAO_pos_ratio)
last_NAO_neg_ratio_NAL, last_NAO_neg_ratio_NPO = ratio_basin_mean(last_NAO_neg_ratio)

# %%
first_NAO_pos_ratio_NAL_lagmean = lag_mean(first_NAO_pos_ratio_NAL)
first_NAO_pos_ratio_NPO_lagmean = lag_mean(first_NAO_pos_ratio_NPO)

first_NAO_neg_ratio_NAL_lagmean = lag_mean(first_NAO_neg_ratio_NAL)
first_NAO_neg_ratio_NPO_lagmean = lag_mean(first_NAO_neg_ratio_NPO)

last_NAO_pos_ratio_NAL_lagmean = lag_mean(last_NAO_pos_ratio_NAL)
last_NAO_pos_ratio_NPO_lagmean = lag_mean(last_NAO_pos_ratio_NPO)

last_NAO_neg_ratio_NAL_lagmean = lag_mean(last_NAO_neg_ratio_NAL)
last_NAO_neg_ratio_NPO_lagmean = lag_mean(last_NAO_neg_ratio_NPO)

# %%
# eke
first_NAO_pos_eke_zonalmean = eke_2060_mean(first_NAO_pos_eke)
first_NAO_neg_eke_zonalmean = eke_2060_mean(first_NAO_neg_eke)

last_NAO_pos_eke_zonalmean = eke_2060_mean(last_NAO_pos_eke)
last_NAO_neg_eke_zonalmean = eke_2060_mean(last_NAO_neg_eke)
# %%
first_NAO_pos_eke_zonalmean_lagmean = lag_mean(first_NAO_pos_eke_zonalmean, name="eke")
first_NAO_neg_eke_zonalmean_lagmean = lag_mean(first_NAO_neg_eke_zonalmean, name="eke")

last_NAO_pos_eke_zonalmean_lagmean = lag_mean(last_NAO_pos_eke_zonalmean, name="eke")
last_NAO_neg_eke_zonalmean_lagmean = lag_mean(last_NAO_neg_eke_zonalmean, name="eke")

# %%
# upvp in NA mean
first_NAO_pos_upvp_NA = upvp_NA_mean(first_NAO_pos_upvp)
first_NAO_neg_upvp_NA = upvp_NA_mean(first_NAO_neg_upvp)

last_NAO_pos_upvp_NA = upvp_NA_mean(last_NAO_pos_upvp)
last_NAO_neg_upvp_NA = upvp_NA_mean(last_NAO_neg_upvp)

# %%
first_NAO_pos_upvp_NA_lagmean = lag_mean(first_NAO_pos_upvp_NA, name="upvp")
first_NAO_neg_upvp_NA_lagmean = lag_mean(first_NAO_neg_upvp_NA, name="upvp")

last_NAO_pos_upvp_NA_lagmean = lag_mean(last_NAO_pos_upvp_NA, name="upvp")
last_NAO_neg_upvp_NA_lagmean = lag_mean(last_NAO_neg_upvp_NA, name="upvp")

# %%
eke_cmap = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/misc_div.txt"
)
eke_cmap = mcolors.ListedColormap(eke_cmap, name="temp_div")


def lon2x(longitude, ax):
    """
    Convert longitude to corresponding x-coordinates.
    """
    x_coord = ax.projection.transform_point(longitude, 0, ccrs.PlateCarree())[0]

    return x_coord


# %%
def merge_ratio_eke_upvp(ratio, eke, upvp, period, phase, region):
    df = ratio[
        ["ens", "extreme_duration", "extreme_start_time", "ratio_lag_mean"]
    ].copy()
    df["eke_lag_mean"] = eke["eke_lag_mean"]
    df["upvp_lag_mean"] = upvp["upvp_lag_mean"]
    df["period"] = period
    df["region"] = region
    df["phase"] = phase
    # drop nan
    df = df.dropna(subset = ['ratio_lag_mean', 'eke_lag_mean', 'upvp_lag_mean'], how = 'any')
    return df


# %%
first_NAO_pos_NPO = merge_ratio_eke_upvp(
    first_NAO_pos_ratio_NPO_lagmean,
    first_NAO_pos_eke_zonalmean_lagmean,
    first_NAO_pos_upvp_NA_lagmean,
    "first",
    "pos",
    "NPO",
)
first_NAO_neg_NPO = merge_ratio_eke_upvp(
    first_NAO_neg_ratio_NPO_lagmean,
    first_NAO_neg_eke_zonalmean_lagmean,
    first_NAO_neg_upvp_NA_lagmean,
    "first",
    "neg",
    "NPO",
)

last_NAO_pos_NPO = merge_ratio_eke_upvp(
    last_NAO_pos_ratio_NPO_lagmean,
    last_NAO_pos_eke_zonalmean_lagmean,
    last_NAO_pos_upvp_NA_lagmean,
    "last",
    "pos",
    "NPO",
)
last_NAO_neg_NPO = merge_ratio_eke_upvp(
    last_NAO_neg_ratio_NPO_lagmean,
    last_NAO_neg_eke_zonalmean_lagmean,
    last_NAO_neg_upvp_NA_lagmean,
    "last",
    "neg",
    "NPO",
)

first_NAO_pos_NAL = merge_ratio_eke_upvp(
    first_NAO_pos_ratio_NAL_lagmean,
    first_NAO_pos_eke_zonalmean_lagmean,
    first_NAO_pos_upvp_NA_lagmean,
    "first",
    "pos",
    "NAL",
)
first_NAO_neg_NAL = merge_ratio_eke_upvp(
    first_NAO_neg_ratio_NAL_lagmean,
    first_NAO_neg_eke_zonalmean_lagmean,
    first_NAO_neg_upvp_NA_lagmean,
    "first",
    "neg",
    "NAL",
)

last_NAO_pos_NAL = merge_ratio_eke_upvp(
    last_NAO_pos_ratio_NAL_lagmean,
    last_NAO_pos_eke_zonalmean_lagmean,
    last_NAO_pos_upvp_NA_lagmean,
    "last",
    "pos",
    "NAL",
)
last_NAO_neg_NAL = merge_ratio_eke_upvp(
    last_NAO_neg_ratio_NAL_lagmean,
    last_NAO_neg_eke_zonalmean_lagmean,
    last_NAO_neg_upvp_NA_lagmean,
    "last",
    "neg",
    "NAL",
)

# %%
df_NPO_pos = pd.concat([first_NAO_pos_NPO, last_NAO_pos_NPO])
df_NPO_neg = pd.concat([first_NAO_neg_NPO, last_NAO_neg_NPO])

df_NAL_pos = pd.concat([first_NAO_pos_NAL, last_NAO_pos_NAL])
df_NAL_neg = pd.concat([first_NAO_neg_NAL, last_NAO_neg_NAL])

# %%
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
sns.scatterplot(
    data=df_NPO_pos,
    x="upvp_lag_mean",
    y="eke_lag_mean",
    hue="ratio_lag_mean",
    style="period",
    sizes = (5, 200),
    ax=axes[0,0],
)

sns.scatterplot(
    data=df_NPO[df_NPO['phase'] == 'neg'],
    x="upvp_lag_mean",
    y="eke_lag_mean",
    hue="period",
    size="ratio_lag_mean",
    sizes = (5, 200),
    ax=axes[0,1],
)

# axes[0,0].set_xlim(-40, 40)
# axes[0,1].set_xlim(-40, 40)
# %%
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
sns.scatterplot(
    data=df_NPO_pos,
    x="ratio_lag_mean",
    y="eke_lag_mean",
    hue="period",
    size = 'extreme_duration',
    sizes = (5, 300),
    ax=axes[0,0],
    legend=False,
    alpha=0.7,
)

sns.scatterplot(
    data=df_NPO_neg,
    x="ratio_lag_mean",
    y="eke_lag_mean",
    hue="period",
    size = 'extreme_duration',
    sizes = (5, 300),
    ax=axes[0,1],
    legend=False,
    alpha=0.7,
)

axes[0,0].set_ylim(-25, 45)
axes[0,1].set_ylim(-25, 45)


sns.scatterplot(
    data=df_NAL_pos,
    x="ratio_lag_mean",
    y="eke_lag_mean",
    hue="period",
    size = 'extreme_duration',
    sizes = (5, 300),
    ax=axes[1,0],
    legend=False,
    alpha=0.7,
)

sns.scatterplot(
    data=df_NAL_neg,
    x="ratio_lag_mean",
    y="eke_lag_mean",
    hue="period",
    size = 'extreme_duration',
    sizes = (5, 300),
    ax=axes[1,1],
    legend=False,
    alpha=0.7,
)

axes[1,0].set_ylim(-25, 45)
axes[1,1].set_ylim(-25, 45)


# %%
