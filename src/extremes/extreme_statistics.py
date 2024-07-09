#%%
import xarray as xr
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# %%


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
    result = df[df['days_in_JJA'] >= duration]
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

        sel_pcs = pd.concat(sel_pcs, axis = 0).sort_index()
    return sel_pcs

# %%
