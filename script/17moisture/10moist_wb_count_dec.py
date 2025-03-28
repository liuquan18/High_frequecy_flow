# %%
# %%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from src.moisture.longitudinal_contrast import read_NAO_extremes


# moisture
# %%
def read_ratio_data(decade):
    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/husDBtas_hussatDBtas_dec/moist_tas_ratio_{decade}.nc"
    data = xr.open_dataset(base_dir)
    return data


# %%
def sector(data):
    box_EAA = [
        -30,
        140,
        20,
        60,
    ]  # [lon_min, lon_max, lat_min, lat_max] Eurasia and Africa
    box_NAM = [-145, -70, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North America
    box_NAL = [-70, -30, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Atlantic
    box_NPC = [140, -145, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Pacific

    data_EAA = data.sel(lon=slice(box_EAA[0], box_EAA[1])).mean(dim=("lon", "lat"))
    data_NAM = data.sel(lon=slice(box_NAM[0], box_NAM[1])).mean(dim=("lon", "lat"))
    data_NAL = data.sel(lon=slice(box_NAL[0], box_NAL[1])).mean(dim=("lon", "lat"))
    data_NPC1 = data.sel(lon=slice(box_NPC[0], 180))
    data_NPC2 = data.sel(lon=slice(-180, box_NPC[1]))
    data_NPC = xr.concat([data_NPC1, data_NPC2], dim="lon").mean(dim=("lon", "lat"))
    return data_EAA, data_NAM, data_NAL, data_NPC


# %%
def read_hus_tas_ratio(read_ratio_data, sector):
    dfs = []

    for i in range(1850, 2100, 10):
        data = read_ratio_data(i)
        EAA, NAM, NAL, NPC = sector(data)

        dfs.append(
            {
                "decade": i,
                "hus": NAL.hus.values.item(),
                "hussat": NAL.hussat.values.item(),
                "region": "NAL",
            }
        )
        dfs.append(
            {
                "decade": i,
                "hus": NPC.hus.values.item(),
                "hussat": NPC.hussat.values.item(),
                "region": "NPC",
            }
        )

    df = pd.DataFrame(dfs)
    hus_NAL = df[df["region"] == "NAL"][["decade", "hus"]]
    hus_NPC = df[df["region"] == "NPC"][["decade", "hus"]]

    return hus_NAL, hus_NPC


hus_NAL, hus_NPC = read_hus_tas_ratio(read_ratio_data, sector)
# %%
moist_merge = pd.merge(hus_NAL, hus_NPC, on="decade", suffixes=("_NAL", "_NPC"))

# %%
# wave breaking
awb = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wave_breaking_stat/awb_th3_NAO_overlap70.csv",
    index_col=0,
)
# %%
cwb = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wave_breaking_stat/cwb_th3_NAO_overlap70.csv",
    index_col=0,
)
# %%
awb_count = awb.groupby(["dec"]).size().reset_index(name="count")
cwb_count = cwb.groupby(["dec"]).size().reset_index(name="count")
# %%
# rename 'dec' to 'decade' for merging
awb_count = awb_count.rename(columns={"dec": "decade"})
cwb_count = cwb_count.rename(columns={"dec": "decade"})

# %%
# count column divided by 50 (ensemble members)
awb_count["count"] = awb_count["count"] / 50
cwb_count["count"] = cwb_count["count"] / 50


# %%
# merge the dataframes awb_count, cwb_count, hus_NAL, hus_NPC on 'decade'
wb_merge = pd.merge(awb_count, cwb_count, on="decade", suffixes=("_awb", "_cwb"))


# %% NAO
def NAO_extremes(return_days=False, threshold=7):
    NAO_pos_counts = pd.DataFrame(columns=["decade", "count"])
    NAO_neg_counts = pd.DataFrame(columns=["decade", "count"])

    for i, dec in enumerate(range(1850, 2100, 10)):
        NAO_pos = read_NAO_extremes(dec, "positive")
        NAO_neg = read_NAO_extremes(dec, "negative")

        # filter only duration above 7 days
        NAO_pos = NAO_pos[NAO_pos["extreme_duration"] >= threshold]
        NAO_neg = NAO_neg[NAO_neg["extreme_duration"] >= threshold]

        if return_days:
            # NAO duration sum
            NAO_pos_count = NAO_pos["extreme_duration"].sum() / 50
            NAO_neg_count = NAO_neg["extreme_duration"].sum() / 50

        else:
            NAO_pos_count = NAO_pos.shape[0] / 50
            NAO_neg_count = NAO_neg.shape[0] / 50

        NAO_pos_counts.loc[i] = [dec, NAO_pos_count]
        NAO_neg_counts.loc[i] = [dec, NAO_neg_count]

    return NAO_pos_counts, NAO_neg_counts


# %%
NAO_pos_count, NAO_neg_count = NAO_extremes(False, 5)
NAO_pos_days, NAO_neg_days = NAO_extremes(True, 5)
# %%
NAO_pos_days = NAO_pos_days.rename(columns={"count": "days"})
NAO_neg_days = NAO_neg_days.rename(columns={"count": "days"})
# %%
NAO_count_merge = pd.merge(
    NAO_pos_count, NAO_neg_count, on="decade", suffixes=("_pos", "_neg")
)
NAO_days_merge = pd.merge(
    NAO_pos_days, NAO_neg_days, on="decade", suffixes=("_pos", "_neg")
)
NAO_merge = pd.merge(NAO_count_merge, NAO_days_merge, on="decade")
# %%
final_merge = pd.merge(
    pd.merge(wb_merge, moist_merge, on="decade"), NAO_merge, on="decade"
)
# %%
# plot
fig, ax = plt.subplots(1, 3, figsize=(10, 5))
sns.lineplot(
    data=final_merge,
    x="decade",
    y="count_awb",
    ax=ax[1],
    label="AWB",
    color="k",
    linewidth=2,
)
sns.lineplot(
    data=final_merge,
    x="decade",
    y="count_cwb",
    ax=ax[1],
    label="CWB",
    color="k",
    linestyle="--",
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="hus_NAL",
    ax=ax[0],
    label="NAL",
    color=sns.color_palette()[0],
    linewidth=2,
)
sns.lineplot(
    data=final_merge,
    x="decade",
    y="hus_NPC",
    ax=ax[0],
    label="NPC",
    color=sns.color_palette()[-1],
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="days_pos",
    ax=ax[2],
    label="NAO pos",
    color="k",
    linewidth=2,
)
sns.lineplot(
    data=final_merge,
    x="decade",
    y="days_neg",
    ax=ax[2],
    label="NAO neg",
    color="k",
    linestyle="--",
    linewidth=2,
)

ax[0].set_title("humidity 20-60N")
ax[1].set_title("wave breaking (NAL)")
ax[2].set_title("extreme NAO days")


ax[0].set_ylabel(r"$\Delta q / \Delta$ T ($g \cdot kg^{-1}K^{-1}$)")
ax[1].set_ylabel("wavebreaking count (per dec per ens)")
ax[2].set_ylabel("extreme NAO days (per dec per ens)")

ax[0].set_xticks(np.arange(1850, 2101, 50))
ax[1].set_xticks(np.arange(1850, 2101, 50))
ax[2].set_xticks(np.arange(1850, 2101, 50))


# ax[2].set_yticks(np.arange(35, 56,5))
# ax[2].set_ylim(32, 56)

# add a,b,c
ax[0].text(
    -0.1, 1.1, "a", transform=ax[0].transAxes, fontsize=16, fontweight="bold", va="top"
)
ax[1].text(
    -0.1, 1.1, "b", transform=ax[1].transAxes, fontsize=16, fontweight="bold", va="top"
)
ax[2].text(
    -0.1, 1.1, "c", transform=ax[2].transAxes, fontsize=16, fontweight="bold", va="top"
)

plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/hus_wb_NAO_count_dec.pdf",
    dpi=300,
)
# %%
