# %%
import xarray as xr
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import statsmodels.api as sm
import glob
import seaborn as sns
import pandas as pd
import glob

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

    extreme_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{extreme_type}_extreme_events/{extreme_type}_extreme_events_{period}/"
    extreme_file = glob.glob(extreme_dir + f"*r{ens}.csv")[0]
    extreme = pd.read_csv(extreme_file)
    extreme = extreme[extreme["plev"] == plev]

    # select the extremes with durations longer than or equal to start_duration
    extreme = sel_event_above_duration(
        extreme, duration=duration_lim, by="sign_duration"
    )

    # to dataframe
    OLR_indo = OLR_indo.to_dataframe().reset_index()[["time", "rlut"]].set_index("time")
    OLR_amaz = OLR_amaz.to_dataframe().reset_index()[["time", "rlut"]].set_index("time")
    NAO = NAO.to_dataframe().reset_index()[["time", "pc"]].set_index("time")

    return OLR_indo, OLR_amaz, NAO, extreme


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


# %%
# first 10 years
CCFs_first10_pos = [
    cross_corr(*read_data("first10", i, 25000, "pos")) for i in range(1, 51)
]

# Filter out None elements before concatenation
CCFs_first10_pos = [CCF for CCF in CCFs_first10_pos if CCF is not None]

# Concatenate the filtered list
CCFs_first10_pos = pd.concat(CCFs_first10_pos, axis=1)

# columns name as 'even_id', and values range from o to len(columns)
CCFs_first10_pos.columns = [
    "even_id" + str(i) for i in range(len(CCFs_first10_pos.columns))
]


# %%
# last 10 years
CCFs_last10_pos = [
    cross_corr(*read_data("last10", i, 25000, "pos")) for i in range(1, 51)
]

# filter out None elements before concatenation
CCFs_last10_pos = [CCF for CCF in CCFs_last10_pos if CCF is not None]

# Concatenate the filtered list
CCFs_last10_pos = pd.concat(CCFs_last10_pos, axis=1)

# columns name as 'even_id', and values range from o to len(columns)
CCFs_last10_pos.columns = [
    "even_id" + str(i) for i in range(len(CCFs_last10_pos.columns))
]


# %%
fig, axes = plt.subplots(1, 2, figsize=(20, 10))
for column in CCFs_first10_pos.columns:
    if column != "median":
        axes[0].plot(
            CCFs_first10_pos.index, CCFs_first10_pos[column], color="grey", alpha=0.3
        )
axes[0].plot(
    CCFs_first10_pos.index,
    CCFs_first10_pos.median(axis=1),
    color="black",
    linewidth=2,
    label="median",
)

# count how many columns are below 0 and plot as bar * -1 use a twin y axis
axes_twin_0 = axes[0].twinx()
axes_twin_0.set_ylim(-0.6, 0.61)
axes[0].set_ylim(-0.85, 0.86)
axes_twin_0.bar(
    CCFs_first10_pos.index,
    ((CCFs_first10_pos < 0).sum(axis=1)) / len(CCFs_first10_pos.columns) * -1,
    color="red",
    alpha=0.3,
    label="negative",
)

# hline at y = 0
axes[0].hlines(y=0, xmin=-50, xmax=0, linestyles="--")
axes_twin_0.hlines(y=-0.5, xmin=-50, xmax=0, linestyles="--")

axes[0].set_xlabel("Lags")
axes[0].set_ylabel("Correlation")

axes[0].set_title("First 10 years")
axes[0].set_xlim(-40, 0)

for column in CCFs_last10_pos.columns:
    axes[1].plot(
        CCFs_last10_pos.index, CCFs_last10_pos[column], color="grey", alpha=0.3
    )
axes[1].plot(
    CCFs_last10_pos.index,
    CCFs_last10_pos.median(axis=1),
    color="black",
    linewidth=2,
    label="median",
)

# count how many columns are below 0 and plot as bar * -1
axes[1].set_ylim(-0.85, 0.86)
axes_twin_1 = axes[1].twinx()
axes_twin_1.set_ylim(-0.6, 0.61)

axes_twin_1.bar(
    CCFs_last10_pos.index,
    ((CCFs_last10_pos < 0).sum(axis=1)) / len(CCFs_last10_pos.columns) * -1,
    color="red",
    alpha=0.3,
    label="negative",
)

# hline at y = 0
axes[1].hlines(y=0, xmin=-50, xmax=0, linestyles="--")
axes[1].set_xlabel("Lags")

axes_twin_1.hlines(y=-0.5, xmin=-50, xmax=0, linestyles="--")

axes[1].set_title("Last 10 years")
axes[1].set_xlim(-40, 0)
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_composite_e2c/Indo_pacific_OLR_NAO_pos_ccf.png"
)

# %%
