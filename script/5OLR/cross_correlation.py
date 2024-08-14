# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd

from src.extremes.extreme_read import sel_event_above_duration


# %%
def read_data(period, ens, plev=25000, extreme_type="pos", duration_lim=30):

    # OLR
    OLR_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/{period}_OLR_daily_ano/"
    OLR_file = glob.glob(OLR_dir + f"*r{ens}i1p1f1*.nc")[0]
    OLR = xr.open_dataset(OLR_file).rlut

    OLR_indo = OLR.sel(lon=slice(50, 100)).mean(dim=["lat", "lon"])
    OLR_amaz = OLR.sel(lon=slice(-60,0)).mean(dim=["lat", "lon"])

    # NAO
    NAO_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_{period}/"
    NAO_file = glob.glob(NAO_dir + f"*r{ens}.nc")[0]
    NAO = xr.open_dataset(NAO_file).pc.sel(plev=plev)

    # to dataframe
    OLR_indo = OLR_indo.to_dataframe().reset_index()[["time", "rlut"]].set_index("time")
    OLR_amaz = OLR_amaz.to_dataframe().reset_index()[["time", "rlut"]].set_index("time")
    NAO = NAO.to_dataframe().reset_index()[["time", "pc"]].set_index("time")

    return OLR_indo, OLR_amaz, NAO

def read_extremes(period: str, ens:int, duration_lim: int=30, extreme_type="pos", plev=25000):
    extreme_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{extreme_type}_extreme_events/{extreme_type}_extreme_events_{period}/"
    extreme_file = glob.glob(extreme_dir + f"*r{ens}.csv")[0]
    extreme = pd.read_csv(extreme_file)
    extreme = extreme[extreme["plev"] == plev]

    # select the extremes with durations longer than or equal to start_duration
    extreme = sel_event_above_duration(
        extreme, duration=duration_lim, by="sign_duration"
    )

    # drop duplicates rows where the sign_start_time and sign_end_time are the same (two extreme events belong to a same sign event, with a break below the threshold)
    extreme = extreme.drop_duplicates(subset=('sign_start_time','sign_end_time'))
    return extreme


# %%
def cross_corr(OLR, NAO, extremes, OLR_roll=3, lag_lim=40):

    if not extremes.empty:
        CCFs = []
        CCF = pd.DataFrame(data=np.nan, index=np.arange(-150, 0, 1), columns=["corr"])

        for i, extreme in extremes.iterrows():
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

            CCF.loc[lags, "corr"] = ccf.values
            CCFs.append(CCF)
        CCFs = pd.concat(CCFs, axis=1, join="outer")

    else:
        CCFs = None

    return CCFs
#%%
def event_ccf(period, extreme_type = 'pos'):
    CCFs_indo = []
    CCFs_amaz = []
    for ens in range(1, 51):
        OLR_indo, OLR_amaz, NAO = read_data(period, ens, 25000, extreme_type)
        pos_extremes = read_extremes(period, ens, 30, extreme_type)
        CCF_indo = cross_corr(OLR_indo, NAO, pos_extremes, OLR_roll=3)
        CCF_amaz = cross_corr(OLR_amaz, NAO, pos_extremes, OLR_roll=3)
        CCFs_indo.append(CCF_indo)
        CCFs_amaz.append(CCF_amaz)
    CCFs_indo = [CCF for CCF in CCFs_indo if CCF is not None]
    CCFs_amaz = [CCF for CCF in CCFs_amaz if CCF is not None]

    CCFs_indo = pd.concat(CCFs_indo, axis=1)
    CCFs_amaz = pd.concat(CCFs_amaz, axis=1)

    CCFs_indo.columns = ["even_id" + str(i) for i in range(len(CCFs_indo.columns))]
    CCFs_amaz.columns = ["even_id" + str(i) for i in range(len(CCFs_amaz.columns))]

    return CCFs_indo, CCFs_amaz

# %%
# first 10 years
CCFs_first10_pos_indo, CCFs_first10_pos_amaz = event_ccf("first10", "pos")

# last 10 years
CCFs_last10_pos_indo, CCFs_last10_pos_amaz = event_ccf("last10", "pos")
#%%
def plot_ccf(CCFs_first10_pos_indo, ax):
    for column in CCFs_first10_pos_indo.columns:
        ax.plot(
        CCFs_first10_pos_indo.index, CCFs_first10_pos_indo[column], color="grey", alpha=0.3
    )
    ax.plot(
    CCFs_first10_pos_indo.index,
    CCFs_first10_pos_indo.median(axis=1),
    color="black",
    linewidth=2,
    label="median",
)

    ax_twin = ax.twinx()
    ax_twin.set_ylim(-0.2,0.21)
    ax_twin.bar(
    CCFs_first10_pos_indo.index,
    ((CCFs_first10_pos_indo < -0.5).sum(axis=1)) / len(CCFs_first10_pos_indo.columns) * -1,
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


# %%
fig, axes = plt.subplots(2, 2, figsize=(20, 10))


plot_ccf(CCFs_first10_pos_indo, axes[0, 0])
plot_ccf(CCFs_last10_pos_indo, axes[0, 1])
plot_ccf(CCFs_first10_pos_amaz, axes[1, 0])
plot_ccf(CCFs_last10_pos_amaz, axes[1, 1])

axes[0, 0].set_title("First 10 years Indo-Pacific")
axes[0, 1].set_title("Last 10 years Indo-Pacific")

axes[1, 0].set_title("First 10 years Amazon")
axes[1, 1].set_title("Last 10 years Amazon")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_composite_e2c/Indo_amazon_OLR_NAO_pos_ccf.png"
)


# %%
