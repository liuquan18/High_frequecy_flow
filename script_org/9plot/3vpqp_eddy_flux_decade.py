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
from src.data_helper.read_variable import read_climatology_decmean
import glob

import logging
logging.basicConfig(level=logging.INFO)
# %%
transient_p = read_climatology_decmean(var = 'Fdiv_p_transient', NAL=True, plev=85000)

steady_p = read_climatology_decmean(var = 'Fdiv_p_steady', NAL=True, plev=85000)

#%%
# to decade
transient_p['year'] = transient_p['year'] - 9
steady_p['year'] = steady_p['year'] - 9
#%%
transient_p = transient_p.to_dataframe().reset_index().rename(
    columns = {'year': 'decade', 'div2': 'transient_div2'}
)[['decade', 'transient_div2']]
steady_p = steady_p.to_dataframe().reset_index().rename(
    columns = {'year': 'decade', 'div2': 'steady_div2'}
)[['decade', 'steady_div2']]


divp_merge = pd.merge(transient_p, steady_p, on="decade")

#%%
sum_p_var = read_climatology_decmean(var='Fdiv_p_sum_std', NAL=True, plev=None)
# change year to decade
sum_p_var['year'] = sum_p_var['year'] - 9
sum_p_var = sum_p_var.to_dataframe().reset_index().rename(
    columns={'year': 'decade'}
)[['decade', 'std']]
#%%
# from variance to std
sum_p_std = sum_p_var.copy()
sum_p_std['std'] = np.sqrt(sum_p_std['std'])
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
final_merge = pd.merge(divp_merge, NAO_merge, on="decade").merge(sum_p_std, on = 'decade')


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
    label="pos NAO",
    color="k",
    linewidth=2,
)
sns.lineplot(
    data=final_merge,
    x="decade",
    y="days_neg",
    ax=axes[0],
    label="neg NAO",
    color="k",
    linestyle="--",
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="transient_div2",
    ax=axes[1],
    label="transient",
    color='k',
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="steady_div2",
    ax=axes[1],
    label="stationary",
    color='k',
    linestyle="--",
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="std",
    ax=axes[2],
    label="std",
    color='k',
    linewidth=2,
)

axes[0].set_ylabel("extreme NAO days", fontsize=16)
axes[1].set_ylabel(r"$\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta_e'}}{\overline{\theta}_p} \right)$ [m $s^{-1}$ day ${-1}$]", fontsize=16)
axes[2].set_ylabel(r"$\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta_e'}}{\overline{\theta}_p} \right)$ [m $s^{-1}$ day ${-1}$]", fontsize=16)

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
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eddy_flux_dec.pdf", dpi=300, bbox_inches="tight", transparent=True)
# %%
fig, axes = plt.subplots(1, 2, figsize=(8, 6))

sns.lineplot(
    data=final_merge,
    x="decade",
    y="days_pos",
    ax=axes[0],
    label="pos NAO",
    color="k",
    linewidth=2,
)
sns.lineplot(
    data=final_merge,
    x="decade",
    y="days_neg",
    ax=axes[0],
    label="neg NAO",
    color="k",
    linestyle="--",
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="transient_div2",
    ax=axes[1],
    label="transient",
    color='k',
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="steady_div2",
    ax=axes[1],
    label="stationary",
    color='k',
    linestyle="--",
    linewidth=2,
)

axes[0].set_ylabel("extreme NAO days", fontsize=16)
axes[1].set_ylabel(r"$\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta'}}{\overline{\theta}_p} \right)$ [m $s^{-1}$ day $^{-1}$]", fontsize=16)

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



# add a, b
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
#save
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0main_text/eddy_flux_dec_first2.pdf", dpi=300, bbox_inches="tight", transparent=True)
# %%
