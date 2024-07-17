#%%
import xarray as xr
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# %%


def sel_event_above_duration (df, duration = 5):

    """
    select the extreme events, which durates 5 days or more in June to August
    """

    # Convert start_time and end_time to datetime if they aren't already
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    # Apply the function to each row
    df['days_in_JJA'] = df.apply(lambda row: days_in_june_to_aug(row['start_time'], row['end_time']), axis=1)

    # Filter rows where there are at least 5 days in June to August
    result = df[df['days_in_JJA'] >= duration]
    return result

def sel_event_duration (df, duration = 5):

    """
    select the extreme events, which durates 5 days or more in June to August
    """

    # Convert start_time and end_time to datetime if they aren't already
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    # Apply the function to each row
    df['days_in_JJA'] = df.apply(lambda row: days_in_june_to_aug(row['start_time'], row['end_time']), axis=1)

    # Filter rows where there are at least 5 days in June to August
    result = df[df['days_in_JJA'] == duration]
    return result


def days_in_june_to_aug(start, end):
    # Check if the event spans multiple years
    if start.year != end.year:
        return 0
    
    june1 = pd.Timestamp(start.year, 6, 1)
    sep1 = pd.Timestamp(start.year, 9, 1)
    
    overlap_start = max(start, june1)
    overlap_end = min(end, sep1)
    
    if overlap_start < overlap_end:
        return (overlap_end - overlap_start).days + 1
    return 0


# %%
def sel_pc_duration(events, pc):

    if len(events) == 0:
        sel_pcs = None
    else:
        sel_pcs = []
        for i in range(len(events)):
            sel_pc = pc.sel(time = slice(events.start_time.iloc[i], events.end_time.iloc[i]))
            sel_pc = sel_pc.assign_coords(duration_index=("time", np.arange(1, sel_pc.sizes['time'] + 1)))
            sel_pc_df = sel_pc.to_dataframe().reset_index()[['duration_index','pc']]
            sel_pc_df['duration'] = events.duration.iloc[i]
            sel_pc_df = sel_pc_df.set_index(['duration', 'duration_index'])
            sel_pcs.append(sel_pc_df)

        sel_pcs = pd.concat(sel_pcs, axis = 1).sort_index()
    return sel_pcs

# %%
def read_extremes(period, start_duration = 5, plev =  50000):
    pos_extreme_path = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/pos_extreme_events/'
    neg_extreme_path = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/neg_extreme_events/'

    tags = {'first10': '1850_1859', 'last10': '2091_2100'}
    tag = tags[period]

    pos_extremes = []
    neg_extremes = []


    for i in range(50):
        pos_extreme = pd.read_csv(f'{pos_extreme_path}pos_extreme_events_{period}/troposphere_pos_extreme_events_{tag}_r{i+1}.csv')
        neg_extreme = pd.read_csv(f'{neg_extreme_path}neg_extreme_events_{period}/troposphere_neg_extreme_events_{tag}_r{i+1}.csv')

        # select plev and delete the 'plev' column
        pos_extreme = pos_extreme[pos_extreme["plev"] == plev][
            ["start_time", "end_time", "duration", "mean", "sum", "max", "min"]
        ]

        neg_extreme = neg_extreme[neg_extreme["plev"] == plev][
            ["start_time", "end_time", "duration", "mean", "sum", "max", "min"]
        ]

        pos_extreme = sel_event_above_duration(pos_extreme, duration=start_duration)
        neg_extreme = sel_event_above_duration(neg_extreme, duration=start_duration)


        pos_extremes.append(pos_extreme)
        neg_extremes.append(neg_extreme)

    pos_extremes = pd.concat(pos_extremes, axis=0)
    neg_extremes = pd.concat(neg_extremes, axis=0)
    return pos_extremes, neg_extremes
