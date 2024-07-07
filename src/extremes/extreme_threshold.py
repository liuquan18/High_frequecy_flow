#%%
import xarray as xr
import pandas as pd
import datetime
# %%
def threshold(pc, N = 7):
    df = pc.to_dataframe()
    df_window = pd.concat([df['pc'].shift(periods = i, freq = '1D').rename(i) for i in [-3,-2,-1,0,1,2,3]], axis=1).dropna(axis = 0, how = 'any')
    df_stack = df_window.stack().reset_index()
    df_stack.columns = ['time','window','pc']
    # groupby dayofyear 
    G = df_stack.groupby(df_stack.time.dt.dayofyear)
    # 1.5 standard deviation as the threshold, suppose the mean is already zero (anomaly data)
    pos_threshold = 1.5 * G['pc'].std()
    neg_threshold = -1.5 * G['pc'].std()
    pos_threshold = pos_threshold.reset_index()
    neg_threshold = neg_threshold.reset_index()
    pos_threshold.columns = ['dayofyear','threshold']
    neg_threshold.columns = ['dayofyear','threshold']
    

    return pos_threshold, neg_threshold

