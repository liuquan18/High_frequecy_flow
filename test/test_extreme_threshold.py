#%%
import pandas as pd
import src.extremes.extreme_threshold as et
import random
# %%
import importlib
importlib.reload(et)
# %%
df = pd.DataFrame({
    'time': pd.date_range(start='2010-01-01', end = '2020-12-31', freq='D'),
    'another': [random.randint(-10, 10) for _ in range(4018)]
})

#%%
# remove 29.02 if it's a leap year
df = df[~((df['time'].dt.month == 2) & (df['time'].dt.day == 29))]

#%%
df_window = et.construct_window(df, column_name='another', window=7)
# %%
df_threshold = et.threshold(df_window, column_name='another', type='pos')
# %%
df_threshold
# %%
df_residue = et.subtract_threshold(df, df_threshold, column_name='another')
# %%
