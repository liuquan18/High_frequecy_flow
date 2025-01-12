#%%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import logging
idx = pd.IndexSlice
logging.basicConfig(level=logging.INFO)
# %%
def var_before_NAO(var, decade, phase):
    file_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_NAO_{phase}/{var}_NAO_{phase}_{decade}.csv"
    data = pd.read_csv(file_path, index_col=[0, 1])
    return data

def read_data(var):
    first_NAO_pos = var_before_NAO(var, 1850, 'pos')
    first_NAO_neg = var_before_NAO(var, 1850, 'neg')

    last_NAO_pos = var_before_NAO(var, 2090, 'pos')
    last_NAO_neg = var_before_NAO(var, 2090, 'neg')

    return first_NAO_pos, first_NAO_neg, last_NAO_pos, last_NAO_neg
#%%
def event_mean(df, name = 'ratio'):
    df_weight = df['extreme_duration']

    all_columns = df.columns
    value_columns = all_columns.difference(['event_id', 'ens', 'lon', 'extreme_duration', 'extreme_start_time'])

    df_values = df[value_columns]


    df_values_weighted = df_values.multiply(df_weight, axis=0)
    df_values_weighted_mean = df_values_weighted.sum(axis=0) / df_weight.sum()


    df_values_weighted_mean = df_values_weighted_mean.to_frame(name=name)
    df_values_weighted_mean = df_values_weighted_mean.reset_index().rename(columns={'index': 'lag'})

    df_values_weighted_mean['lag'] = df_values_weighted_mean['lag'].astype(int)

    df_values_weighted_mean = df_values_weighted_mean.sort_values(by='lag')

    return df_values_weighted_mean

# %%
# basin mean util function
def zonal_mean(df):

    all_columns = df.columns
    value_columns = all_columns.difference(['event_id', 'ens', 'lon', 'extreme_duration'
                                            , 'extreme_start_time'])

    # mean over selected lons
    df_zonmean = df.groupby(['event_id','ens'])[value_columns].mean()

    # id info
    df_id = df.groupby(['event_id','ens'])[['extreme_duration', 'extreme_start_time']].first()

    # merge
    df_final = pd.merge(df_id, df_zonmean, on=['event_id','ens'], how='inner')

    df_final = df_final.reset_index().set_index('event_id')
    df_final.index.name = None

    return df_final


#%%
# hus_tas_ratio basin mean
def ratio_basin_mean(ratio):

    box_NAL = [-70, -35, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Atlantic
    box_NPO = [140, -145, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Pacific


    ratio = ratio.reset_index()
    ratio = ratio.rename(columns={'level_0': 'event_id'})

    # sel lon
    ratio_NAL = ratio.loc[(ratio['lon'] >= box_NAL[0]) & (ratio['lon'] <= box_NAL[1])]
    ratio_NAL_zonmean = zonal_mean(ratio_NAL)

    ratio_NPO = ratio.loc[(ratio['lon'] >= box_NPO[0]) & (ratio['lon'] <= 180) | (ratio['lon'] >= -180) & (ratio['lon'] <= box_NPO[1])]
    ratio_NPO_zonmean = zonal_mean(ratio_NPO)

    return ratio_NAL_zonmean, ratio_NPO_zonmean

#%%
def upvp_NA_mean(upvp):
    upvp = upvp.reset_index()
    upvp = upvp.rename(columns={'level_0': 'event_id'})

    upvp_NA = upvp.loc[(upvp['lon'] >= -100) & (upvp['lon'] <= -10)]
    upvp_NA_zonmean = zonal_mean(upvp_NA)

    upvp_NA_eventmean = event_mean(upvp_NA_zonmean, name = 'upvp')

    return upvp_NA_eventmean

#%%
def eke_lag_lon(first, last):

    first = first.reset_index()
    first = first.rename(columns={'level_0': 'event_id'})

    last = last.reset_index()
    last = last.rename(columns={'level_0': 'event_id'})


    first_eventmean = first.groupby('lon')[first.columns].apply(event_mean, name = 'eke')
    last_eventmean = last.groupby('lon')[last.columns].apply(event_mean, name = 'eke')

    # drop level 1, the same as 'lag'
    first_eventmean = first_eventmean.droplevel(1)
    last_eventmean = last_eventmean.droplevel(1)


    first_eventmean = first_eventmean.reset_index()
    last_eventmean  = last_eventmean.reset_index()

    eke_eventmean = first_eventmean.merge(last_eventmean, on=('lon', 'lag'), suffixes=('_first', '_last'))

    eke_eventmean['eke_diff'] = eke_eventmean['eke_last'] - eke_eventmean['eke_first']
    
    eke_eventmean = eke_eventmean.set_index(['lon', 'lag'])

    eke_eventmean_xr = eke_eventmean.to_xarray()

    return eke_eventmean_xr

#%%
def merge_ratio(first_NAL, first_NPO, last_NAL, last_NPO):

    # same phase

    first_NAL['region'] = 'NAL'
    first_NAL['period'] = 'first'

    first_NPO['region'] = 'NPO'
    first_NPO['period'] = 'first'

    last_NAL['region'] = 'NAL'
    last_NAL['period'] = 'last'

    last_NPO['region'] = 'NPO'
    last_NPO['period'] = 'last'

    ratio_df = pd.concat([first_NAL, first_NPO, last_NAL, last_NPO])

    return ratio_df


# %%
first_NAO_pos_eke, first_NAO_neg_eke, last_NAO_pos_eke, last_NAO_neg_eke = read_data('eke')
first_NAO_pos_upvp, first_NAO_neg_upvp, last_NAO_pos_upvp, last_NAO_neg_upvp = read_data('upvp')    
first_NAO_pos_ratio, first_NAO_neg_ratio, last_NAO_pos_ratio, last_NAO_neg_ratio = read_data('hus_tas_ratio')
# %%
# ratio
first_NAO_pos_ratio_NAL, first_NAO_pos_ratio_NPO = ratio_basin_mean(first_NAO_pos_ratio)
first_NAO_neg_ratio_NAL, first_NAO_neg_ratio_NPO = ratio_basin_mean(first_NAO_neg_ratio)

last_NAO_pos_ratio_NAL, last_NAO_pos_ratio_NPO = ratio_basin_mean(last_NAO_pos_ratio)
last_NAO_neg_ratio_NAL, last_NAO_neg_ratio_NPO = ratio_basin_mean(last_NAO_neg_ratio)

first_NAO_pos_ratio_NAL = event_mean(first_NAO_pos_ratio_NAL, 'ratio')
first_NAO_pos_ratio_NPO = event_mean(first_NAO_pos_ratio_NPO, 'ratio')

first_NAO_neg_ratio_NAL = event_mean(first_NAO_neg_ratio_NAL, 'ratio')
first_NAO_neg_ratio_NPO = event_mean(first_NAO_neg_ratio_NPO, 'ratio')

last_NAO_pos_ratio_NAL = event_mean(last_NAO_pos_ratio_NAL, 'ratio')
last_NAO_pos_ratio_NPO = event_mean(last_NAO_pos_ratio_NPO, 'ratio')

last_NAO_neg_ratio_NAL = event_mean(last_NAO_neg_ratio_NAL, 'ratio')
last_NAO_neg_ratio_NPO = event_mean(last_NAO_neg_ratio_NPO, 'ratio')

#%%
ratio_pos = merge_ratio(first_NAO_pos_ratio_NAL, first_NAO_pos_ratio_NPO, last_NAO_pos_ratio_NAL, last_NAO_pos_ratio_NPO)

ratio_neg = merge_ratio(first_NAO_neg_ratio_NAL, first_NAO_neg_ratio_NPO, last_NAO_neg_ratio_NAL, last_NAO_neg_ratio_NPO)
# %%
# eke
NAO_pos_eke_lag_lon = eke_lag_lon(first_NAO_pos_eke, last_NAO_pos_eke)
NAO_neg_eke_lag_lon = eke_lag_lon(first_NAO_neg_eke, last_NAO_neg_eke)

# %%
# upvp in NA mean
first_NAO_pos_upvp_NA = upvp_NA_mean(first_NAO_pos_upvp)
first_NAO_neg_upvp_NA = upvp_NA_mean(first_NAO_neg_upvp)

last_NAO_pos_upvp_NA = upvp_NA_mean(last_NAO_pos_upvp)
last_NAO_neg_upvp_NA = upvp_NA_mean(last_NAO_neg_upvp)
# %%
fig = plt.figure(figsize=(12, 8))

grid = plt.GridSpec(2,3, wspace=0.4, hspace=0.3, width_ratios=[1, 2, 1])

ratio_ax1 = fig.add_subplot(grid[0, 0])

sns.lineplot(data=ratio_pos.sort_values(by = 'ratio').sort_values(by = 'lag'), x='ratio', y='lag', hue='region', style='period', ax=ratio_ax1)
ratio_ax1.invert_yaxis()
# %%
def plot_line(data, ax, var = 'ratio'):
    data = data.sort_values(by = 'lag')
    sns.lineplot(data=data, x='ratio', y='lag', ax = ax)
    return ax
# %%
fig = plt.figure(figsize=(12, 8))

grid = plt.GridSpec(2,3, wspace=0.4, hspace=0.3, width_ratios=[1, 2, 1])

ratio_ax1 = fig.add_subplot(grid[0, 0])
plot_data = ratio_pos.set_index('ratio')
plot_line(plot_data[(plot_data['region'] == 'NAL') & (plot_data['period'] == 'first')], ratio_ax1)
# %%
