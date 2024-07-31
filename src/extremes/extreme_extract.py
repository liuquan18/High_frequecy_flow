#%%
import pandas as pd
from scipy import ndimage

#%%
def subtract_threshold(pc, threshold):
    # xarray exclude the data at 1st may to 3rd May, and the data during 28th Sep and 31st Sep
    # Create a mask for the dates to exclude
    mask_exclude = (
        ((pc['time.month'] == 5) & (pc['time.day'] >= 1) & (pc['time.day'] <= 3)) |
        ((pc['time.month'] == 9) & (pc['time.day'] >= 28) & (pc['time.day'] <= 30))
    )
    mask_keep = ~mask_exclude
    pc = pc.where(mask_keep, drop = True)


    df = pc.to_dataframe()

    G =  df.groupby(df.index.year)['pc']

    # subtract the threshold from original data
    residues = G.transform(lambda x: x - threshold['threshold'].values)
    return residues.reset_index()

# %%
def extract_pos_extremes(df):
    """
    extract exsecutively above zero events
    """
    # apply ndimage.median_filter to remove the single day anomaly data (with one day tolerance)
    df['pc'] = ndimage.median_filter(df['pc'], size=3)
    # A grouper that increaments every time a non-positive value is encountered
    Grouper_pos = df.groupby(df.time.dt.year)['pc'].transform(lambda x: x.lt(0).cumsum())

    # groupby the year and the grouper
    G = df[df['pc']>0].groupby([df.time.dt.year, Grouper_pos])

    # Get the statistics of the group
    Events = G.agg(
        start_time = pd.NamedAgg(column = 'time',aggfunc='min'),
        duration = pd.NamedAgg(column = 'time',aggfunc = 'size'),
        sum = pd.NamedAgg(column = 'pc',aggfunc = 'sum'),
        mean = pd.NamedAgg(column = 'pc',aggfunc = 'mean'),
        max = pd.NamedAgg(column = 'pc',aggfunc = 'max'),
        min = pd.NamedAgg(column = 'pc',aggfunc = 'min'),# add mean to make sure the data are all positive
        ).reset_index()    
    Events['end_time'] = Events['start_time'] + pd.to_timedelta(Events['duration']-1, unit='D')

    Events = Events[['start_time','end_time','duration','sum','mean','max', 'min']]
    return Events
# %%
def extract_neg_extremes(df):
    """
    extract exsecutively below zero events
    """
    # apply ndimage.median_filter to remove the single day anomaly data (with one day tolerance)
    df['pc'] = ndimage.median_filter(df['pc'], size=3)
    
    # A grouper that increaments every time a non-positive value is encountered
    Grouper_neg = df.groupby(df.time.dt.year)['pc'].transform(lambda x: x.gt(0).cumsum())

    # groupby the year and the grouper
    G = df[df['pc']<0].groupby([df.time.dt.year, Grouper_neg])

    # Get the statistics of the group
    Events = G.agg(
        start_time = pd.NamedAgg(column = 'time',aggfunc='min'),
        duration = pd.NamedAgg(column = 'time',aggfunc = 'size'),
        sum = pd.NamedAgg(column = 'pc',aggfunc = 'sum'),
        mean = pd.NamedAgg(column = 'pc',aggfunc = 'mean'),
        max = pd.NamedAgg(column = 'pc',aggfunc = 'max'),
        min = pd.NamedAgg(column = 'pc',aggfunc = 'min'),
        ).reset_index()
    Events['end_time'] = Events['start_time'] + pd.to_timedelta(Events['duration']-1, unit='D')

    Events = Events[['start_time','end_time','duration','sum','mean','max', 'min']]
    return Events