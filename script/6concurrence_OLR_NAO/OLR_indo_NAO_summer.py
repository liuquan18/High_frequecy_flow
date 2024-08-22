# %%
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %%
import src.OLR_NAO.OLR_NAO_association as OLR_NAO

# %%
# read the OLR and NAO extremes
period = "first10"
member = 2
extreme_type = "pos"
dur_lim = 8


# %%
def read_extreme_mean(period, member, extreme_type="pos", lon_bins=slice(50, 110)):

    NAO_pos, OLR = OLR_NAO.read_extremes(
        period, member, extreme_type=extreme_type, limit_dur=True, lim_OLR=10
    )

    NAO_pos["sign_start_time"] = pd.to_datetime(NAO_pos["sign_start_time"])
    OLR["sign_start_time"] = pd.to_datetime(OLR["sign_start_time"])

    OLR_x = OLR.set_index(["sign_start_time", "lat", "lon"]).to_xarray()

    OLR_indo_x = OLR_x.sel(lon=lon_bins).mean(dim=["lat", "lon"])

    OLR_indo = OLR_indo_x.to_dataframe().reset_index()

    return OLR_indo, NAO_pos


# %%
def count_summer(period, lon_bins=slice(50, 110)):
    OLR_indos = []
    NAOs = []

    for member in range(1, 51):
        OLR_indo, NAO = read_extreme_mean(period, member, lon_bins=lon_bins)
        OLR_indo["member"] = member
        NAO["member"] = member

        OLR_indos.append(OLR_indo)
        NAOs.append(NAO)
    OLR_indos = pd.concat(OLR_indos)
    NAOs = pd.concat(NAOs)

    OLR_indo_summer = OLR_indos.groupby("member")[["extreme_duration"]].count()

    NAO_summer = NAOs.groupby("member")[["extreme_duration"]].count()

    #
    summer = pd.merge(
        OLR_indo_summer,
        NAO_summer,
        left_index=True,
        right_index=True,
        suffixes=("_OLR_indo", "_NAO"),
    )

    return summer


# %%

first_summer_indo = count_summer("first10")
last_summer_indo = count_summer("last10")


# %%
fig, ax = plt.subplots()
sns.scatterplot(
    data=first_summer_indo,
    x="extreme_duration_OLR_indo",
    y="extreme_duration_NAO",
    ax=ax,
)
sns.scatterplot(
    data=last_summer_indo,
    x="extreme_duration_OLR_indo",
    y="extreme_duration_NAO",
    ax=ax,
)
# plot scatter points of average along members
sns.scatterplot(
    data=first_summer_indo.mean().to_frame().T,
    x="extreme_duration_OLR_indo",
    y="extreme_duration_NAO",
    ax=ax,
    color="Blue",
    marker="X",
    s=100,
)
sns.scatterplot(
    data=last_summer_indo.mean().to_frame().T,
    x="extreme_duration_OLR_indo",
    y="extreme_duration_NAO",
    ax=ax,
    color="Red",
    marker="X",
    s=100,
)

plt.xlabel("OLR extremes occurance")
plt.ylabel("NAO extremes occurance")
# plt.ylim(0,15)
# plt.xlim(0,220)

plt.suptitle("Summer extremes")
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_extremes/OLR_indo_NAO_extreme_duration_scatter.png")
# %%

firrst_summer_pacific = count_summer("first10", lon_bins=slice(-180, -120))
last_summer_pacific = count_summer("last10", lon_bins=slice(-180, -120))
# %%
fig, ax = plt.subplots()
sns.scatterplot(
    data=firrst_summer_pacific,
    x="extreme_duration_OLR_indo",
    y="extreme_duration_NAO",
    ax=ax,
)
sns.scatterplot(
    data=last_summer_pacific,
    x="extreme_duration_OLR_indo",
    y="extreme_duration_NAO",
    ax=ax,
)
# plot scatter points of average along members
sns.scatterplot(
    data=firrst_summer_pacific.mean().to_frame().T,
    x="extreme_duration_OLR_indo",
    y="extreme_duration_NAO",
    ax=ax,
    color="Blue",
    marker="X",
    s=100,
)
sns.scatterplot(
    data=last_summer_pacific.mean().to_frame().T,
    x="extreme_duration_OLR_indo",
    y="extreme_duration_NAO",
    ax=ax,
    color="Red",
    marker="X",
    s=100,
)
plt.suptitle("Summer extremes in the Pacific")
plt.xlabel("OLR extremes occurance")
plt.ylabel("NAO extremes occurance")
# plt.ylim(0,15)
# plt.xlim(0,220)


# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_extremes/OLR_pacific_NAO_extreme_duration_scatter.png")
# %%
def NAO_after_OLR(OLR, NAO, lag=[-16, -6]):

    # -16 days lag of NAO time
    NAO["sign_start_time"] = pd.to_datetime(NAO["sign_start_time"])
    NAO["lag_start_time"] = NAO["sign_start_time"] + pd.DateOffset(days=lag[0])
    NAO["lag_end_time"] = NAO["sign_start_time"] + pd.DateOffset(days=lag[1])

    # for each row of NAO, find the rows in OLR whose sign_start_time is before the lag_time
    OLR_befores = []
    NAO_sels = []
    OLR["sign_start_time"] = pd.to_datetime(OLR["sign_start_time"])
    for i, row in NAO.iterrows():
        lag_start_time = row["lag_start_time"]
        lag_end_time = row["lag_end_time"]
        OLR_sel = OLR[
            (OLR["sign_start_time"] >= lag_start_time)
            & (OLR["sign_start_time"] <= lag_end_time)
            & (OLR["sign_start_time"].dt.year == lag_start_time.year)
        ]

        if OLR_sel.empty:
            continue
        NAO_sel = NAO.loc[i]
        OLR_befores.append(OLR_sel)
        NAO_sels.append(NAO_sel)

    if OLR_befores:
        OLR_before = pd.concat(OLR_befores)
        NAO_sels = pd.concat(NAO_sels)
        # drop duplicates
        OLR_before = OLR_before.drop_duplicates(subset=["sign_start_time"])

        return OLR_before.reset_index(drop=True), NAO_sels
    else:
        return pd.DataFrame(), pd.DataFrame()


# %%
# %%
def count_summer_select(period, lon_bins=slice(50, 110)):
    OLR_indos = []
    NAOs = []

    for member in range(1, 51):
        OLR_indo, NAO = read_extreme_mean(period, member, lon_bins=lon_bins)

        OLR_before, NAO_sel = NAO_after_OLR(OLR_indo, NAO)
        OLR_before["member"] = member
        NAO_sel["member"] = member

        if OLR_before.empty:
            continue

        OLR_indos.append(OLR_before)
        NAOs.append(NAO_sel)
    OLR_indos = pd.concat(OLR_indos)

    # drop duplicates
    NAOs = pd.concat(NAOs)
    NAOs = pd.DataFrame(NAOs)
    NAOs = NAOs.drop_duplicates(subset=["sign_start_time"])
    OLR_indos = OLR_indos.drop_duplicates(subset=["sign_start_time"])

    OLR_indo_summer = OLR_indos.groupby("member")[["extreme_duration"]].count()

    NAO_summer = NAOs.groupby("member")[["extreme_duration"]].count()

    #
    summer = pd.merge(
        OLR_indo_summer,
        NAO_summer,
        left_index=True,
        right_index=True,
        suffixes=("_OLR_indo", "_NAO"),
    )

    return summer


# %%
first_summer_indo_select = count_summer_select("first10")
# %%
last_summer_indo_select = count_summer_select("last10")
# %%
