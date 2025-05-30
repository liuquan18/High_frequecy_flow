# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line, lat2y, lon2x
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns
from src.data_helper.read_NAO_extremes import read_NAO_extremes
from src.data_helper.read_variable import read_prime_decmean, read_prime


# %%
def to_dataframe(ivke_region, region):
    ivke_region = ivke_region.to_dataframe().reset_index()
    ivke_region["decade"] = ivke_region["time"].dt.year // 10 * 10
    ivke_region = ivke_region[["hus", "decade"]].rename(
        columns={"hus": f"qq_{region}"}
    )
    return ivke_region


#%%
transient_ds = read_prime_decmean(var="vpetp_vpetp", NAL=True, plev=85000)

steady_ds = read_prime_decmean(var="vsets_vsets", NAL=True, plev=85000)

cov_ds = read_prime_decmean(var="vpetp_vsets", NAL=True, plev=85000)
#%%
transient = transient_ds['std']
steady = steady_ds['std']
cov = cov_ds['cov']
#%%
# difference from the first decade
transient = transient - transient.sel(year=1859)
steady = steady - steady.sel(year=1859)
cov = cov - cov.sel(year=1859)
#%%
transient = transient.to_dataframe().reset_index().rename(
    columns={"std": "transient_var", "year": "decade"}
)[['decade', 'transient_var']]


steady = steady.to_dataframe().reset_index().rename(
    columns={"std": "steady_var", "year": "decade"}
)[['decade', 'steady_var']]


cov = cov.to_dataframe().reset_index().rename(
    columns={"cov": "transient_steady_cov", "year": "decade"}
)[['decade', 'transient_steady_cov']]



qq_merge = pd.merge(transient, steady, on="decade").merge(cov, on="decade")

qq_merge["decade"] = qq_merge["decade"]-9

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

#%%
final_merge = pd.merge(qq_merge, NAO_merge, on="decade")


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
fig, axes = plt.subplots(1, 3, figsize=(12, 6))

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

sns.lineplot(
    data=final_merge,
    x="decade",
    y="transient_var",
    ax=axes[1],
    label="transient",
    color='k',
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="steady_var",
    ax=axes[1],
    label="steady",
    color='k',
    linestyle="--",
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="transient_steady_cov",
    ax=axes[2],
    label="transient-steady cov",
    color='k',
    linewidth=2,
)
axes[2].legend(loc='lower left')

axes[0].set_ylabel("extreme NAO days", fontsize=16)
axes[1].set_ylabel("variance of eddy heat flux", fontsize=16)
axes[2].set_ylabel("covariance of eddy heat flux", fontsize=16)

for ax in axes:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis='both', labelsize=16)
    ax.set_xlabel(ax.get_xlabel(), fontsize=16)
    # Set legend font size if legend exists
    leg = ax.get_legend()
    if leg is not None:
        for text in leg.get_texts():
            text.set_fontsize(16)

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
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/eddy_heat_flux_dec.pdf", dpi=300, bbox_inches="tight")
# %%
