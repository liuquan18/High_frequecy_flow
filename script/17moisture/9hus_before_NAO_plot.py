# %%
import xarray as xr
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# %%
first_NAO_pos_NAL = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_pos_NAL/NAO_pos_NAL_1850.csv",
    index_col=0,
)
first_NAO_pos_NPO = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_pos_NPO/NAO_pos_NPO_1850.csv",
    index_col=0,
)

first_NAO_neg_NAL = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_neg_NAL/NAO_neg_NAL_1850.csv",
    index_col=0,
)
first_NAO_neg_NPO = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_neg_NPO/NAO_neg_NPO_1850.csv",
    index_col=0,
)

# %%
last_NAO_pos_NAL = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_pos_NAL/NAO_pos_NAL_2090.csv",
    index_col=0,
)
last_NAO_pos_NPO = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_pos_NPO/NAO_pos_NPO_2090.csv",
    index_col=0,
)

last_NAO_neg_NAL = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_neg_NAL/NAO_neg_NAL_2090.csv",
    index_col=0,
)
last_NAO_neg_NPO = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_neg_NPO/NAO_neg_NPO_2090.csv",
    index_col=0,
)


# %%
lag = range(-15, 0)
lag_columns = [str(i) for i in lag]

# %%
first_NAO_pos_NAL["lag_mean"] = first_NAO_pos_NAL[lag_columns].mean(axis=1)
first_NAO_pos_NPO["lag_mean"] = first_NAO_pos_NPO[lag_columns].mean(axis=1)

first_NAO_neg_NAL["lag_mean"] = first_NAO_neg_NAL[lag_columns].mean(axis=1)
first_NAO_neg_NPO["lag_mean"] = first_NAO_neg_NPO[lag_columns].mean(axis=1)

last_NAO_pos_NAL["lag_mean"] = last_NAO_pos_NAL[lag_columns].mean(axis=1)
last_NAO_pos_NPO["lag_mean"] = last_NAO_pos_NPO[lag_columns].mean(axis=1)

last_NAO_neg_NAL["lag_mean"] = last_NAO_neg_NAL[lag_columns].mean(axis=1)
last_NAO_neg_NPO["lag_mean"] = last_NAO_neg_NPO[lag_columns].mean(axis=1)


# %%
def select_columns_merge(NAO_NAL, NAO_NPO):
    NAO_NAL = NAO_NAL.reset_index()
    NAO_NPO = NAO_NPO.reset_index()

    NAO_df = NAO_NAL[["extreme_duration", "lag_mean"]].join(
        NAO_NPO[["lag_mean"]],
        lsuffix="_NAL",
        rsuffix="_NPO",
    )

    NAO_df = NAO_df[NAO_df["extreme_duration"] > 5]
    # dropna
    NAO_df = NAO_df.dropna(subset=["lag_mean_NAL", "lag_mean_NPO"])

    return NAO_df


# %%

first_NAO_pos = select_columns_merge(first_NAO_pos_NAL, first_NAO_pos_NPO)
first_NAO_neg = select_columns_merge(first_NAO_neg_NAL, first_NAO_neg_NPO)

last_NAO_pos = select_columns_merge(last_NAO_pos_NAL, last_NAO_pos_NPO)
last_NAO_neg = select_columns_merge(last_NAO_neg_NAL, last_NAO_neg_NPO)
# %%
first_NAO_pos["dec"] = 1850
first_NAO_neg["dec"] = 1850

last_NAO_pos["dec"] = 2090
last_NAO_neg["dec"] = 2090

# %%
NAO_pos = pd.concat([first_NAO_pos, last_NAO_pos])
NAO_neg = pd.concat([first_NAO_neg, last_NAO_neg])


# %%
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
sns.kdeplot(
    data=NAO_pos,
    x="lag_mean_NAL",
    y="lag_mean_NPO",
    hue="dec",
    ax=axes[0],
    common_norm=True,
    weights="extreme_duration",
    palette=['k','r'],
    alpha=0.7,
)


sns.kdeplot(
    data=NAO_neg,
    x="lag_mean_NAL",
    y="lag_mean_NPO",
    hue="dec",
    ax=axes[1],
    common_norm=True,
    fill=False,
    weights="extreme_duration",
    palette=['k','r'],
    alpha=0.7,
)
# plot the 1:1 line
for ax in axes:
    x = np.linspace(0, 1.2, 100)
    y = x
    ax.plot(x, y, "k", linestyle="dotted")
    ax.set_ylim(0.4, 1.2)
    ax.set_xlim(0.4, 1.2)

for ax in axes:
    ax.set_xlabel(r"North Atlantic $\Delta q / \Delta T$")
    ax.set_ylabel(r"North Pacific $\Delta q / \Delta T$")

axes[0].set_title("NAO positive")
axes[1].set_title("NAO negative")

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/NAO_lag_mean_moist.png")


# %%
NAO_pos['NPO_gt_NAL'] = np.where(NAO_pos['lag_mean_NPO'] > NAO_pos['lag_mean_NAL'], 1, -1)

#%%
NAO_neg['NPO_gt_NAL'] = np.where(NAO_neg['lag_mean_NPO'] > NAO_neg['lag_mean_NAL'], 1, -1)

#%%
# weight the 'NPO_gt_NAL' with 'extreme_duration'
NAO_pos['NPO_gt_NAL'] = NAO_pos['NPO_gt_NAL'] * NAO_pos['extreme_duration']
NAO_neg['NPO_gt_NAL'] = NAO_neg['NPO_gt_NAL'] * NAO_neg['extreme_duration']

#%%
NAO_pos_NPO_gt_NAL = NAO_pos[NAO_pos['NPO_gt_NAL'] >0]
NAO_pos_NPO_lt_NAL = NAO_pos[NAO_pos['NPO_gt_NAL'] <0]

NAO_neg_NPO_gt_NAL = NAO_neg[NAO_neg['NPO_gt_NAL'] >0]
NAO_neg_NPO_lt_NAL = NAO_neg[NAO_neg['NPO_gt_NAL'] <0]
#%%
NAO_pos_NPO_gt_NAL_num = NAO_pos_NPO_gt_NAL.groupby('dec')[['NPO_gt_NAL']].sum()
NAO_pos_NPO_lt_NAL_num = NAO_pos_NPO_lt_NAL.groupby('dec')[['NPO_gt_NAL']].sum()

NAO_neg_NPO_gt_NAL_num = NAO_neg_NPO_gt_NAL.groupby('dec')[['NPO_gt_NAL']].sum()
NAO_neg_NPO_lt_NAL_num = NAO_neg_NPO_lt_NAL.groupby('dec')[['NPO_gt_NAL']].sum()
#%%
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

sns.scatterplot(
    data=NAO_pos,
    x="lag_mean_NAL",
    y="lag_mean_NPO",
    hue="dec",
    size="extreme_duration",
    ax=axes[0],
    palette=['k', 'r'],
    alpha=0.7,
    legend=False,
    sizes = (20, 200),
)

sns.scatterplot(
    data=NAO_neg,
    x="lag_mean_NAL",
    y="lag_mean_NPO",
    hue="dec",
    size="extreme_duration",
    ax=axes[1],
    palette=['k', 'r'],
    alpha=0.7,
    legend=False,
    sizes = (20, 200),

)

# plot the 1:1 line
for ax in axes:
    x = np.linspace(0, 1.2, 100)
    y = x
    ax.plot(x, y, "k", linestyle="dotted")
    ax.set_ylim(0.4, 1.2)
    ax.set_xlim(0.4, 1.2)

for ax in axes:
    ax.set_xlabel(r"North Atlantic $\Delta q / \Delta T$")
    ax.set_ylabel(r"North Pacific $\Delta q / \Delta T$")

# add legend 'red' for 2090 and 'black' for 1850
axes[0].scatter([], [], c='r', label='2090-2099')
axes[0].scatter([], [], c='k', label='1850-1859')
axes[0].legend(loc = 'lower right')

axes[0].set_title("NAO positive")
axes[1].set_title("NAO negative")

# text annotation, black font for 1850 and red font for 2090, plot value of NAO_pos_NPO_gt_NAL_num and NAO_pos_NPO_lt_NAL_num, 
# respectively above slope line and below slope line

axes[0].text(1.0, 1.05, f"{NAO_pos_NPO_gt_NAL_num.loc[1850].values[0]:.0f}", fontsize=12, color='black', rotation=45)
axes[0].text(1.05, 1.02, f"{NAO_pos_NPO_lt_NAL_num.loc[1850].values[0]*-1:.0f}", fontsize=12, color='black', rotation=45)
axes[0].text(0.97, 1.08, f"{NAO_pos_NPO_gt_NAL_num.loc[2090].values[0]:.0f}", fontsize=12, color='red', rotation=45)
axes[0].text(1.08, 0.99, f"{NAO_pos_NPO_lt_NAL_num.loc[2090].values[0]*-1:.0f}", fontsize=12, color='red', rotation=45)

axes[1].text(1.0, 1.05, f"{NAO_neg_NPO_gt_NAL_num.loc[1850].values[0]:.0f}", fontsize=12, color='black', rotation=45)
axes[1].text(1.05, 1.02, f"{NAO_neg_NPO_lt_NAL_num.loc[1850].values[0]*-1:.0f}", fontsize=12, color='black', rotation=45)
axes[1].text(0.97, 1.08, f"{NAO_neg_NPO_gt_NAL_num.loc[2090].values[0]:.0f}", fontsize=12, color='red', rotation=45)
axes[1].text(1.08, 0.99, f"{NAO_neg_NPO_lt_NAL_num.loc[2090].values[0]*-1:.0f}", fontsize=12, color='red', rotation=45)

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/NAO_lag_mean_moist_scatter.png")
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/NAO_lag_mean_moist_scatter.pdf", dpi = 300, bbox_inches = 'tight')
# %%
