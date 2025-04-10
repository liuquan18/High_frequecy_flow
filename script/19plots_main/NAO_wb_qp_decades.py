# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line, lat2y, lon2x
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns
from src.moisture.longitudinal_contrast import read_NAO_extremes


# %%
def to_dataframe(ivke_region, region):
    ivke_region = ivke_region.to_dataframe().reset_index()
    ivke_region["decade"] = ivke_region["time"].dt.year // 10 * 10
    ivke_region = ivke_region[["hus", "decade"]].rename(
        columns={"hus": f"qq_{region}"}
    )
    return ivke_region
#%%

qq = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/qpqp_monthly_ensmean/*.nc")
# %%
qq =qq.hus*1e6 # kg/kg to g/kg
# %%
qq = qq.sel(plev = 85000)
#%%
qq = qq.rolling(time = 10).mean()
# %%
qq.compute()
# %%
qq_NPC = qq.sel(lon = slice(120, 240), lat = slice(30, 50)).mean(dim = ['lon', 'lat'])
qq_NAL = qq.sel(lon = slice(270, 330), lat = slice(30, 50)).mean(dim = ['lon', 'lat'])
# %%
qq_NPC = to_dataframe(qq_NPC, "NPC")
qq_NAL = to_dataframe(qq_NAL, "NAL")
# %%
qq_merge = pd.merge(qq_NPC, qq_NAL, on="decade")
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
NAO_merge["decade"] = NAO_merge["decade"].astype(int)
# %%
final_merge = pd.merge(qq_merge, wb_merge, on="decade").merge(NAO_merge, on="decade")


# %%
prec_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_seq.txt"
)
prec_cmap_seq = mcolors.ListedColormap(prec_cmap_seq, name="prec_div")

prec_cmap_div = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_div.txt"
)
prec_cmap_div = mcolors.ListedColormap(prec_cmap_div, name="prec_div")
# %%
fig, axes = plt.subplots(1,3, figsize=(12, 6))


sns.lineplot(
    data=final_merge,
    x="decade",
    y="qq_NPC",
    ax=axes[2],
    label=r"$q'^2$ NPC",
    color="k",
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="qq_NAL",
    ax=axes[2],
    label=r"$q'^2$ NAL",
    color="k",
    linewidth=2,
    linestyle="--",
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="count_awb",
    ax=axes[1],
    label="AWB",
    color="k",
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="count_cwb",
    ax=axes[1],
    label="CWB",
    color="k",
    linestyle="--",
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="days_pos",
    ax=axes[0],
    label="NAO pos",
    color="k",
    linewidth=2,
)
sns.lineplot(
    data=final_merge,
    x="decade",
    y="days_neg",
    ax=axes[0],
    label="NAO neg",
    color="k",
    linestyle="--",
    linewidth=2,
)


axes[2].set_ylabel(r"$q'^2 \: / \: g^2 kg^{-2}$")
axes[1].set_ylabel("wave breaking")
axes[0].set_ylabel("extreme NAO days")

for ax in axes:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# add a, b, c
for i, ax in enumerate(axes.flat):
    ax.text(
        -0.1,
        1.05,
        f"{chr(97+i)}",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
    )
plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/transients_response.pdf", dpi=300, bbox_inches="tight")
# %%
