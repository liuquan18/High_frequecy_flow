# %%
import pytest
import src.composite.composite as composite
import pandas as pd

# %%
events = pd.DataFrame(
    {
        "start_time": [
            "1850-05-01 12:00:00",
            "1850-05-02 12:00:00",
            "1850-05-03 12:00:00",
            "1850-05-04 12:00:00",
            "1850-05-05 12:00:00",
        ],
        "end_time": [
            "1850-05-02 12:00:00",
            "1850-05-03 12:00:00",
            "1850-05-04 12:00:00",
            "1850-05-05 12:00:00",
            "1850-05-06 12:00:00",
        ],
        "plev": [25000, 25000, 25000, 25000, 25000],
    }
)
# %%
events[["start_time", "end_time"]] = events[["start_time", "end_time"]].apply(
    pd.to_datetime
)
# %%
date_range = composite.find_lead_lag_30days(events, base_plev=25000, cross_plev=1)
# %%
assert date_range is not None
# %%
