#%%
import pandas as pd
import numpy as np
import xarray as xr
# %%
extremes = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/pos_extreme_events/pos_extreme_events_first10/troposphere_pos_extreme_events_1850_1859_r1.csv")
# %%
extremes
# %%
extremes = extremes[extremes['plev'] == 25000]
# %%
new_extremes = extremes
# %%
new_extremes = new_extremes.sort_values("event_start_time")
# %%
new_extremes.duplicated(subset = ['sign_start_time', 'sign_end_time'])

# %%
    new_extremes.loc[:, "event_start_time"] = pd.to_datetime(new_extremes["event_start_time"])
    new_extremes.loc[:, "end_time"] = pd.to_datetime(new_extremes["end_time"])
    new_extremes.loc[:, 'sign_start_time'] = pd.to_datetime(new_extremes['sign_start_time'])
    new_extremes.loc[:, 'sign_end_time'] = pd.to_datetime(new_extremes['sign_end_time'])
# %%
    # group by 'sign_start_time' and 'sign_end_time'
    new_extremes = new_extremes.groupby(["sign_start_time", "sign_end_time"])[new_extremes.columns].apply(
        lambda x: x.assign(
            start_time=x["event_start_time"].min(),
            end_time=x["end_time"].max(),
            duration=(x["end_time"].max() - x["event_start_time"].min()).days + 1,
        )
    )

    new_extremes = new_extremes.reset_index(drop=True)
    new_extremes = new_extremes.drop_duplicates(subset=["sign_start_time", "sign_end_time"], ignore_index=True)

# %%
