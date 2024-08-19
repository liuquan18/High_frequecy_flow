# %%
import pandas as pd
import xarray as xr
import numpy as np
from mpi4py import MPI
import sys
import logging

logging.basicConfig(level=logging.WARNING)

import eventextreme.extreme_threshold as et

# %%


# remove when the package et is updated
def threshold(
    df: pd.DataFrame,
    column_name: str = "pc",
    threshold: int = 1.5,
    extreme_type: str = "pos",
) -> pd.DataFrame:
    """
    Calculate the threshold for the anomaly data across multiple years.

    Parameters:
    df (pd.DataFrame): Input dataframe with columns ['time', column_name].
    column_name (str): The name of the column to be used in the threshold calculation.
    threshold (float): The threshold value. Default is 1.5 standard deviation.
    type (str): The type of threshold. Default is 'pos'.


    """

    # make the dayofyear the same for both the normal year and leap year
    times = pd.to_datetime(df.time.values)

    # Identify leap years
    is_leap_year = times.is_leap_year

    # Adjust dayofyear for dates from March 1st onward in leap years
    adjusted_dayofyear = times.dayofyear - is_leap_year * (
        (times.month > 2).astype(int)
    )

    # Now, incorporate this adjustment back into your xarray object
    df["adjusted_dayofyear"] = adjusted_dayofyear

    # groupby dayofyear
    G = df.groupby("adjusted_dayofyear")
    # 1.5 standard deviation as the threshold, suppose the mean is already zero (anomaly data)

    if extreme_type == "pos":
        # the standard deviation of the data is calculated from all possible columns
        threshold = 1.5 * G[column_name].std()
    elif extreme_type == "neg":
        threshold = -1.5 * G[column_name].std()
    threshold = pd.DataFrame(threshold)
    threshold = threshold.reset_index()
    threshold.columns = ["dayofyear", "threshold"]

    return threshold


# %%

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print(f"Rank {rank} out of {size} on node {MPI.Get_processor_name()}")

# %%
file_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/first10_OLR_daily_ano/"

# %%
# members_all = list(range(1, 51))  # all members
members_all = [6, 7, 8, 9, 10, 16, 17, 18, 19, 20, 26, 27, 28, 29, 30, 36, 37, 38, 39, 40, 46, 47, 48, 49, 50]
members_single = np.array_split(members_all, size)[rank]  # members on this core


# %%
def get_threshold(arr):
    df = arr.to_dataframe().reset_index()
    df_window = et.construct_window(df, window=7, column_name="rlut")

    pos_thr_dayofyear = threshold(df_window, column_name="rlut", extreme_type="pos")

    pos_thr_dayofyear = pos_thr_dayofyear.set_index("dayofyear")
    pos_thr_dayofyear.columns = ["pos_thr"]

    neg_thr_dayofyear = threshold(df_window, column_name="rlut", extreme_type="neg")
    neg_thr_dayofyear = neg_thr_dayofyear.set_index("dayofyear")
    neg_thr_dayofyear.columns = ["neg_thr"]

    thr_dayofyear = pd.concat([pos_thr_dayofyear, neg_thr_dayofyear], axis=1)

    return thr_dayofyear.to_xarray()


# %%

for i, member in enumerate(members_single):

    print(f"Rank {rank} processing member {member}")
    olr = xr.open_dataset(
        f"{file_path}rlut_day_MPI-ESM1-2-LR_historical_r{member}i1p1f1_gn_18500501-18590930_ano.nc",
        chunks="auto",
    )

    olr = olr.rlut

    olr_spatial = olr.stack(spatial=("lat", "lon"))

    thr_dayofyear = olr_spatial.groupby("spatial", squeeze=True).apply(get_threshold)
    thr_dayofyear = thr_dayofyear.unstack()

    thr_dayofyear.to_netcdf(
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_threshold/rlut_threshold_first10_r{member}.nc"
    )

# %%
