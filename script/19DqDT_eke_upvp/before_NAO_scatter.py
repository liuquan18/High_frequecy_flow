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
def lag_mean(df, name="ratio", lag = (-15,0)):

    all_columns = df.columns
    value_columns = np.arange(lag[0], lag[1]).astype(str)

    df[name + '_lag_mean'] = df[value_columns].mean(axis=1)
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
    eke['lat'] = eke['lat']*4 # fake lat to plot correctly the lon
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

#%%
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
#%%
first_NAO_pos_eke_zonalmean_lagmean = lag_mean(first_NAO_pos_eke_zonalmean, name='eke')
first_NAO_neg_eke_zonalmean_lagmean = lag_mean(first_NAO_neg_eke_zonalmean, name='eke')

last_NAO_pos_eke_zonalmean_lagmean = lag_mean(last_NAO_pos_eke_zonalmean, name='eke')
last_NAO_neg_eke_zonalmean_lagmean = lag_mean(last_NAO_neg_eke_zonalmean, name='eke')

# %%
# upvp in NA mean
first_NAO_pos_upvp_NA = upvp_NA_mean(first_NAO_pos_upvp)
first_NAO_neg_upvp_NA = upvp_NA_mean(first_NAO_neg_upvp)

last_NAO_pos_upvp_NA = upvp_NA_mean(last_NAO_pos_upvp)
last_NAO_neg_upvp_NA = upvp_NA_mean(last_NAO_neg_upvp)

# %%
first_NAO_pos_upvp_NA_lagmean = lag_mean(first_NAO_pos_upvp_NA, name='upvp')
first_NAO_neg_upvp_NA_lagmean = lag_mean(first_NAO_neg_upvp_NA, name='upvp')

last_NAO_pos_upvp_NA_lagmean = lag_mean(last_NAO_pos_upvp_NA, name='upvp')
last_NAO_neg_upvp_NA_lagmean = lag_mean(last_NAO_neg_upvp_NA, name='upvp')

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
fig = plt.figure(figsize=(12, 8))
