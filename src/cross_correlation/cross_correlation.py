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
    CCFs_amaz = []
    for ens in range(1, 51):
        OLR_indo, OLR_amaz, NAO = read_data(period, ens, 25000)
        pos_extremes = read_extremes(period, ens, 30, extreme_type)
        if pos_extremes.empty:
            continue
        CCF_indo = cross_corr(OLR_indo, NAO, pos_extremes, OLR_roll=3)
        CCF_amaz = cross_corr(OLR_amaz, NAO, pos_extremes, OLR_roll=3)

        CCFs_indo.append(CCF_indo)
        CCFs_amaz.append(CCF_amaz)
    CCFs_indo = [CCF for CCF in CCFs_indo if CCF is not None]
    CCFs_amaz = [CCF for CCF in CCFs_amaz if CCF is not None]

    CCFs_indo = pd.concat(CCFs_indo, axis=1)
    CCFs_amaz = pd.concat(CCFs_amaz, axis=1)

    return CCFs_indo, CCFs_amaz


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
    min_index = min_index[ccf.loc[min_index] < -0.2]

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
