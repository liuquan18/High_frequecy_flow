import xarray as xr
import pandas as pd
import numpy as np
import glob
import logging

logging.basicConfig(level=logging.INFO)
#%%
def sel_var(uhat, events):
    try:
        uhat["time"] = uhat.indexes["time"].to_datetimeindex()
    except AttributeError:
        pass

    uhat_extreme = []
    for i, event in events.iterrows():
        uhat_extreme.append(
            uhat.sel(time=slice(event["extreme_start_time"], event["extreme_end_time"]))
        )

    uhat_extreme = xr.concat(uhat_extreme, dim="time")

    # average over time
    uhat_extreme = uhat_extreme.mean(dim="time")

    return uhat_extreme
