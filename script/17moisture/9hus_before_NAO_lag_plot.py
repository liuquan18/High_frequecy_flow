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
#%%

def ratio_lag(ratio, region = 'NAL', period = '1850', phase = 'pos'):
    weight = ratio['extreme_duration']
    ratio = ratio[[ '-20', '-19', '-18', '-17', '-16', '-15', '-14', '-13', '-12', '-11',
        '-10', '-9', '-8', '-7', '-6', '-5', '-4', '-3', '-2', '-1', '0', '1',
        '2', '3', '4', '5', '6', '7', '8', '9', '10']]

    ratio = ratio.dropna(how='all')

    # weight all rows with 'extreme_duration'
    ratio = ratio.multiply(weight, axis=0)
    # divide by the sum of 'extreme_duration' to get the weighted mean
    ratio = ratio.sum(axis=0) / weight.sum()

    ratio = ratio.to_frame(name='ratio')
    ratio = ratio.reset_index()
    ratio['region'] = region
    ratio['period'] = period
    ratio['phase'] = phase

    return ratio

#%%
first_NAO_pos_NAL_lag = ratio_lag(first_NAO_pos_NAL, 'NAL', '1850', 'pos')
first_NAO_pos_NPO_lag = ratio_lag(first_NAO_pos_NPO, 'NPO', '1850', 'pos')

first_NAO_neg_NAL_lag = ratio_lag(first_NAO_neg_NAL, 'NAL', '1850', 'neg')
first_NAO_neg_NPO_lag = ratio_lag(first_NAO_neg_NPO, 'NPO', '1850', 'neg')

last_NAO_pos_NAL_lag = ratio_lag(last_NAO_pos_NAL, 'NAL', '2090', 'pos')
last_NAO_pos_NPO_lag = ratio_lag(last_NAO_pos_NPO, 'NPO', '2090', 'pos')

last_NAO_neg_NAL_lag = ratio_lag(last_NAO_neg_NAL, 'NAL', '2090', 'neg')
last_NAO_neg_NPO_lag = ratio_lag(last_NAO_neg_NPO, 'NPO', '2090', 'neg')
#%%
pos_df = pd.concat([first_NAO_pos_NAL_lag, first_NAO_pos_NPO_lag, last_NAO_pos_NAL_lag, last_NAO_pos_NPO_lag])
neg_df = pd.concat([first_NAO_neg_NAL_lag, first_NAO_neg_NPO_lag, last_NAO_neg_NAL_lag, last_NAO_neg_NPO_lag])
#%%
fig, axes = plt.subplots(1, 2, figsize=(8, 5))

sns.lineplot(data=pos_df, x='index', y='ratio', hue='period', style='region', ax=axes[0])
sns.lineplot(data=neg_df, x='index', y='ratio', hue='period', style='region', ax=axes[1])

# show x-ticks label every 2
for ax in axes:
    ax.set_xticks(ax.get_xticks()[::5])
    ax.set_ylim(0.53, 0.87)

    ax.set_xlabel('days relative to NAO onset (days)')

    ax.set_ylabel(r'$\Delta q / \Delta T $ ($g \cdot kg^{-1}K^{-1}$)')


axes[0].set_title('Positive NAO')
axes[1].set_title('Negative NAO')

plt.tight_layout()
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/hus_tas_ratio_NAO_lag.png")



# %%
