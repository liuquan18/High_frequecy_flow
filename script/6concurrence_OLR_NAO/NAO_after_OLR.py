# %%
import numpy as np
import pandas as pd
import xarray as xr
import logging
import matplotlib.pyplot as plt
import glob

# %%
import src.extremes.extreme_read as er

# %%
logging.basicConfig(level=logging.INFO)


# %%
# %%
def read_extremes(period, member, extreme_type="pos", dur_lim=8):
    """
    Read the NAO and OLR extremes
    """
    NAO_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{extreme_type}_extreme_events/{extreme_type}_extreme_events_first10/"
    OLR_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_extremes_pos/OLR_extremes_pos_{period}/"  # no extreme_type in the OLR_extremes

    # read NAO positive extremes
    NAO_file = glob.glob(
        f"{NAO_dir}troposphere_{extreme_type}_extreme_events*r{member}.csv"
    )[0]
    NAO_pos = pd.read_csv(NAO_file)
    NAO_pos = NAO_pos[NAO_pos["plev"] == 25000]

    # select extremes based on minimum duration
    NAO_pos = er.sel_event_above_duration(
        NAO_pos, duration=dur_lim, by="extreme_duration"
    )
    # select columns
    NAO_pos = NAO_pos[["sign_start_time", "extreme_duration"]]

    # read OLR extremes
    OLR_file = glob.glob(f"{OLR_dir}OLR_extremes*r{member}.csv")[0]
    OLR = pd.read_csv(OLR_file)
    # select extremes based on minimum duration but not limited in JJA
    OLR = OLR[OLR["extreme_duration"] >= dur_lim]
    # select columns
    OLR = OLR[["sign_start_time", "extreme_duration", "lat", "lon"]]

    return NAO_pos, OLR


# %%
def NAO_after_OLR(OLR, NAO, lag=-16):

    # -16 days lag of NAO time
    NAO["sign_start_time"] = pd.to_datetime(NAO["sign_start_time"])
    NAO["lag_time"] = NAO["sign_start_time"] + pd.DateOffset(days=lag)

    # for each row of NAO, find the rows in OLR whose sign_start_time is before the lag_time
    OLR_befores = []
    OLR["sign_start_time"] = pd.to_datetime(OLR["sign_start_time"])
    for i, row in NAO.iterrows():
        lag_time = row["lag_time"]
        OLR_sel = OLR[
            (OLR["sign_start_time"] < lag_time)
            & (OLR["sign_start_time"].dt.year == lag_time.year)
        ]
        OLR_befores.append(OLR_sel)

    OLR_before = pd.concat(OLR_befores)

    return OLR_before.reset_index(drop=True)


# %%
def NAO_after_OLR_all(period, dur_lim=8, extreme_type="pos", lag=-16):
    """
    select OLR extremes that are before the NAO extremes by lag days for all members
    """
    con_xs = []

    for member in range(1, 51):
        logging.info(f"member {member}")
        NAO_pos, OLR = read_extremes(
            period, member, extreme_type=extreme_type, dur_lim=dur_lim
        )
        concurrence = NAO_after_OLR(OLR, NAO_pos, lag=lag)
        if concurrence.empty:
            continue

        concurrence = concurrence[["sign_start_time", "extreme_duration", "lat", "lon"]]
        concurrence = concurrence.set_index(["sign_start_time", "lat", "lon"])
        con_x = concurrence.to_xarray()

        con_xs.append(con_x)
    con_xs = xr.concat(con_xs, dim="member")

    return con_xs


# %%
first10_pos = NAO_after_OLR_all("first10")

#%%
last10_pos = NAO_after_OLR_all("last10")
# %%
# 