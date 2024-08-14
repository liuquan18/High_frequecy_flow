# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
import seaborn as sns

from src.extremes.extreme_read import sel_event_above_duration

from matplotlib.lines import Line2D
from scipy.signal import argrelmin


# %%
def read_data(period, ens, plev=25000):

    # OLR
    OLR_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/{period}_OLR_daily_ano/"
    OLR_file = glob.glob(OLR_dir + f"*r{ens}i1p1f1*.nc")[0]
    OLR = xr.open_dataset(OLR_file).rlut

    OLR_indo = OLR.sel(lon=slice(50, 100)).mean(dim=["lat", "lon"])
    OLR_natl = OLR.sel(lon=slice(-60, 0)).mean(dim=["lat", "lon"])

    # NAO
    NAO_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_{period}/"
    NAO_file = glob.glob(NAO_dir + f"*r{ens}.nc")[0]
    NAO = xr.open_dataset(NAO_file).pc.sel(plev=plev)

    # to dataframe
    OLR_indo = OLR_indo.to_dataframe().reset_index()[["time", "rlut"]].set_index("time")
    OLR_natl = OLR_natl.to_dataframe().reset_index()[["time", "rlut"]].set_index("time")
    NAO = NAO.to_dataframe().reset_index()[["time", "pc"]].set_index("time")

    return OLR_indo, OLR_natl, NAO


def read_extremes(
    period: str, ens: int, duration_lim=30, extreme_type="pos", plev=25000
):
    extreme_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{extreme_type}_extreme_events/{extreme_type}_extreme_events_{period}/"
    extreme_file = glob.glob(extreme_dir + f"*r{ens}.csv")[0]
    extreme = pd.read_csv(extreme_file)
    extreme = extreme[extreme["plev"] == plev]

    # select the extremes with durations longer than or equal to duration_lim
    extreme = sel_event_above_duration(
        extreme, duration=duration_lim, by="sign_duration"
    )

    if not extreme.empty:
        # select again with events at least 8 days in JJA
        extreme = sel_event_above_duration(extreme, duration=8, by="event_duration")

        # select the events where sign_start_time is after June 1st (at least 30 days after the OLR data starts)
        extreme = extreme[pd.to_datetime(extreme["sign_start_time"]).dt.month >= 6]

        # drop duplicates rows where the sign_start_time and sign_end_time are the same (two extreme events belong to a same sign event, with a break below the threshold)
        extreme = extreme.drop_duplicates(subset=("sign_start_time", "sign_end_time"))

        # give event_id to each event
        extreme["ens"] = ens
        extreme["csv_ind"] = extreme.index

    return extreme


# %%
def cross_corr(OLR, NAO, extremes, OLR_roll=3, lag_lim=40):
    """
    parameters:
    OLR: pd.DataFrame
        OLR data
    NAO: pd.DataFrame
        NAO data
    extremes: pd.DataFrame
        extreme events
    OLR_roll: int
        rolling window for OLR
    lag_lim: int
        minimum length of lags between


    """

    CCFs = []

    for i, extreme in extremes.iterrows():

        # [ens, csv_ind] as event_id
        event_id = str([extreme["ens"], extreme["csv_ind"]])
        start = extreme["sign_start_time"]
        end = extreme["sign_end_time"]
        extreme_NAO = NAO.loc[start:end]

        year = pd.to_datetime(start).year
        year_OLR = OLR.loc[str(year)]
        if OLR_roll is not None:
            year_OLR = year_OLR.rolling(OLR_roll).median()
        ccf = (
            year_OLR.loc[:end]
            .rolling(window=extreme_NAO.size, center=False)["rlut"]
            .apply(lambda x: np.corrcoef(x.values, extreme_NAO["pc"].values)[0, 1])
        )
        lags = (ccf.index - pd.to_datetime(end)).days - 1
        # create a series with lags as index, and ccf.values as data

        # length of lags should be above lag_lim
        if len(lags) < lag_lim:
            continue
        CCF = pd.DataFrame(data=np.nan, index=np.arange(-150, 0, 1), columns=[event_id])
        CCF.loc[lags, event_id] = ccf.values
        CCFs.append(CCF)
    CCFs = pd.concat(CCFs, axis=1)

    return CCFs


# %%
def ens_ccf(period, extreme_type="pos"):
    CCFs_indo = []
    CCFs_natl = []
    for ens in range(1, 51):
        OLR_indo, OLR_natl, NAO = read_data(period, ens, 25000)
        pos_extremes = read_extremes(period, ens, 30, extreme_type)
        if pos_extremes.empty:
            continue
        CCF_indo = cross_corr(OLR_indo, NAO, pos_extremes, OLR_roll=3)
        CCF_natl = cross_corr(OLR_natl, NAO, pos_extremes, OLR_roll=3)

        CCFs_indo.append(CCF_indo)
        CCFs_natl.append(CCF_natl)
    CCFs_indo = [CCF for CCF in CCFs_indo if CCF is not None]
    CCFs_natl = [CCF for CCF in CCFs_natl if CCF is not None]

    CCFs_indo = pd.concat(CCFs_indo, axis=1)
    CCFs_natl = pd.concat(CCFs_natl, axis=1)

    return CCFs_indo, CCFs_natl


def plot_ccf(CCFs_first10_pos_indo, ax):
    for column in CCFs_first10_pos_indo.columns:
        ax.plot(
            CCFs_first10_pos_indo.index,
            CCFs_first10_pos_indo[column],
            color="grey",
            alpha=0.3,
        )
    ax.plot(
        CCFs_first10_pos_indo.index,
        CCFs_first10_pos_indo.median(axis=1),
        color="black",
        linewidth=2,
        label="median",
    )

    ax_twin = ax.twinx()
    ax_twin.set_ylim(-0.2, 0.21)
    ax_twin.bar(
        CCFs_first10_pos_indo.index,
        ((CCFs_first10_pos_indo < -0.5).sum(axis=1))
        / len(CCFs_first10_pos_indo.columns)
        * -1,
        color="red",
        alpha=0.3,
        label="negative",
    )

    # hline at y = 0
    ax.hlines(y=0, xmin=-50, xmax=0, linestyles="--")
    ax.hlines(y=-0.5, xmin=-50, xmax=0, linestyles="--")

    ax.set_xlabel("Lags")
    ax.set_ylabel("Correlation")

    ax.set_xlim(-40, 0)
    ax.set_ylim(-0.85, 0.86)


########################## count of local minimum in lag (-16,-6] ##########################
def locmimum_index(ccf, roll_window=3):

    # smooth the ccf
    ccf = ccf.rolling(roll_window).mean()

    # identify the local minimum index
    loc_min = argrelmin(ccf.values)
    min_index = ccf.index[loc_min]

    # values on min_index must below -0.2, or drop
    min_index = min_index[ccf.loc[min_index] < -0.3]

    return min_index.values


# %%
# apply the function to each column
def locmimum_index_inbin(ccfs, bin=[-15, -6]):

    min_inds = ccfs.apply(lambda x: locmimum_index(x, roll_window=3), axis=0)

    # drop empty values
    min_inds = min_inds[min_inds.apply(len) > 0]

    # flat the column values
    min_inds = min_inds.explode()

    # count values in bin = [-16,-6]
    min_inds_bin = min_inds[(min_inds >= bin[0]) & (min_inds <= bin[1])]

    return min_inds_bin


def composite_mean_OLR(local_minind, period):
    OLRs = []
    for minind in local_minind.index:
        event_ens, event_csv_ind = eval(minind)  # [ens, csv_ind]
        event = read_extremes(period, event_ens, 30, "pos")
        event = event[event["csv_ind"] == event_csv_ind]
        event_start = event["sign_start_time"].values[0]

        # (-16,-6] days before the event_start
        OLR_start = pd.to_datetime(event_start) - pd.Timedelta(days=15)
        OLR_end = pd.to_datetime(event_start) - pd.Timedelta(days=5)

        # read OLR data
        OLR = xr.open_dataset(
            glob.glob(
                f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/{period}_OLR_daily_ano/*r{event_ens}i1p1f1*.nc"
            )[0]
        ).rlut
        OLR_before_event = OLR.sel(time=slice(OLR_start, OLR_end)).mean(dim="time")
        OLRs.append(OLR_before_event)

    OLRs = xr.concat(OLRs, dim="event")
    OLR_comp = OLRs.mean(dim="event")
    return OLR_comp
