# %%
import xarray as xr
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# %%
first_NAO_pos_eke = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/eke_NAO_pos/eke_NAO_pos_1850.csv",
    index_col=[0, 1],
)


first_NAO_neg_eke = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/eke_NAO_neg/eke_NAO_neg_1850.csv",
    index_col=[0, 1],
)

# %%
last_NAO_pos_eke = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/eke_NAO_pos/eke_NAO_pos_2090.csv",
    index_col=[0, 1],
)

last_NAO_neg_eke = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/eke_NAO_neg/eke_NAO_neg_2090.csv",
    index_col=[0, 1],
)
#%%

def mean_across_event(eke):
    weight = eke['extreme_duration']
    eke = eke[[ '-20', '-19', '-18', '-17', '-16', '-15', '-14', '-13', '-12', '-11',
        '-10', '-9', '-8', '-7', '-6', '-5', '-4', '-3', '-2', '-1', '0', '1',
        '2', '3', '4', '5', '6', '7', '8', '9', '10']]

    eke = eke.dropna(how='all')

    # weight all rows with 'extreme_duration'
    eke = eke.multiply(weight, axis=0)
    # divide by the sum of 'extreme_duration' to get the weighted mean
    eke = eke.sum(axis=0) / weight.sum()
    eke = eke.to_frame(name='eke')
    return eke
#%%
def ratio_lag(eke):
    eke_mean = eke.groupby(level = 1).apply(mean_across_event)

    eke_mean = eke_mean.reset_index()
    
    eke_mean.columns = ['lon','lag','eke']
    eke_mean = eke_mean.pivot(index = 'lon', columns = 'lag', values = 'eke')
    return eke_mean


#%%
first_NAO_pos_eke = ratio_lag(first_NAO_pos_eke)
first_NAO_neg_eke = ratio_lag(first_NAO_neg_eke)

last_NAO_pos_eke = ratio_lag(last_NAO_pos_eke)
last_NAO_neg_eke = ratio_lag(last_NAO_neg_eke)

#%%
# sort the columns 
first_NAO_pos_eke = first_NAO_pos_eke[np.arange(-20,11,1).astype(str)]
first_NAO_neg_eke = first_NAO_neg_eke[np.arange(-20,11,1).astype(str)]

last_NAO_pos_eke = last_NAO_pos_eke[np.arange(-20,11,1).astype(str)]
last_NAO_neg_eke = last_NAO_neg_eke[np.arange(-20,11,1).astype(str)]

# %%
fig,axes = plt.subplots(2,2, figsize = (15,10), sharex = True, sharey = True)

sns.heatmap(first_NAO_pos_eke.T, ax = axes[0,0], cmap = 'coolwarm', center = 0, cbar_kws={'ticks': np.arange(30,60,5)})
sns.heatmap(first_NAO_neg_eke.T, ax = axes[0,1], cmap = 'coolwarm', center = 0)

sns.heatmap(last_NAO_pos_eke.T, ax = axes[1,0], cmap = 'coolwarm', center = 0)
sns.heatmap(last_NAO_neg_eke.T, ax = axes[1,1], cmap = 'coolwarm', center = 0)
# %%
