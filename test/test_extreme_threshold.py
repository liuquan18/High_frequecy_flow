#%%
import pandas as pd
import src.extremes.extreme_threshold as et

# %%
import importlib
importlib.reload(et)
# %%
df = pd.DataFrame({
    'time': pd.date_range(start='2023-01-01', periods=10, freq='D'),
    'another': range(10)
})

result = et.construct_window(df, column_name='another', window=7)
print(result)
# %%
