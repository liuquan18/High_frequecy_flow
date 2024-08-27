#%%
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import glob
import logging
import sys
logging.basicConfig(level=logging.WARNING)
import seaborn as sns

#%%
import src.extremes.extreme_read as er
import src.ConTrack.track_statistic as ts

#%%
import importlib
importlib.reload(ts)

# %%

first10_pos_AWBs = []
for ens in range(1,51):
    NAO, AWB = ts.read_NAO_WB('first10', ens, 25000, 'pos', 'AWB')
    first10_pos_AWB = ts.select_WB_before_NAO(NAO, AWB)
    first10_pos_AWBs.append(first10_pos_AWB)
first10_pos_AWBs = pd.concat(first10_pos_AWBs)



# %%
last10_pos_AWBs = []
for ens in range(1,51):
    NAO, AWB = ts.read_NAO_WB('last10', ens, 25000, 'pos', 'AWB')
    last10_pos_AWB = ts.select_WB_before_NAO(NAO, AWB)
    last10_pos_AWBs.append(last10_pos_AWB)

last10_pos_AWBs = pd.concat(last10_pos_AWBs)

# %%
first_start = first10_pos_AWBs.groupby('Flag').nth(0)
last_start = last10_pos_AWBs.groupby('Flag').nth(0)
# %%
sns.kdeplot(first_start, x= 'Longitude', y = 'lag_days', fill = True)
# %%
sns.kdeplot(last_start, x= 'Longitude', y = 'lag_days', fill = True)
# %%
# change the Longitude from 0-360 to -180-180
first_start['Longitude'] = np.where(first_start['Longitude'] > 180, first_start['Longitude'] - 360, first_start['Longitude'])
last_start['Longitude'] = np.where(last_start['Longitude'] > 180, last_start['Longitude'] - 360, last_start['Longitude'])

#%%
fig = plt.figure(figsize=(10, 10))
ax1 = fig.add_subplot(2, 1, 1 )

sns.kdeplot(first_start, x= 'Longitude', y = 'lag_days', fill = True, ax=ax1, color = 'k', levels = np.arange(0.1, 1.1, 0.1), common_norm = False)
sns.kdeplot(last_start, x= 'Longitude', y = 'lag_days', fill = False, ax=ax1, color = 'r', levels = np.arange(0.1, 1.1, 0.1), common_norm = False)

ax2 = fig.add_subplot(2,1,2)
sns.kdeplot(first_start, x= 'Intensity', y = 'lag_days', fill = True, levels = 10, color = 'k')
sns.kdeplot(last_start, x= 'Intensity', y = 'lag_days', fill = False, levels = 10, color = 'r')
# %%
first_data = first_start[['Longitude', 'lag_days', 'Intensity']].copy()
first_data['period'] = 'first'

last_data = last_start[['Longitude', 'lag_days','Intensity']].copy()
last_data['period'] = 'last'

data = pd.concat([first_data, last_data])
# %%
sns.scatterplot(data, x= 'Longitude', y = 'lag_days', hue = 'period')
# %%
sns.scatterplot(data, x= 'lag_days', y = 'Intensity', hue = 'period')

# %%
