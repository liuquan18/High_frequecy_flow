#%%
import pandas as pd
# %%
def threshold(df):
    """
    extract the 1.5 standard deviation as the threshold
    """

    # make the dayofyear the same for both the normal year and leap year
    times = pd.to_datetime(df.time.values)

    # Identify leap years
    is_leap_year = times.is_leap_year

    # Adjust dayofyear for dates from March 1st onward in leap years
    adjusted_dayofyear = times.dayofyear - is_leap_year * ((times.month > 2).astype(int))

    # Now, incorporate this adjustment back into your xarray object
    df['adjusted_dayofyear'] = adjusted_dayofyear

    # groupby dayofyear 
    G = df.groupby('adjusted_dayofyear')
    # 1.5 standard deviation as the threshold, suppose the mean is already zero (anomaly data)
    pos_threshold = 1.5 * G['pc'].std()
    neg_threshold = -1.5 * G['pc'].std()
    pos_threshold = pos_threshold.reset_index()
    neg_threshold = neg_threshold.reset_index()
    pos_threshold.columns = ['dayofyear','threshold']
    neg_threshold.columns = ['dayofyear','threshold']

    return pos_threshold, neg_threshold
#%%
def construct_window(df, window = 7):
    """
    create a dataframe, with 3 days before and after the day as the window
    """
    # set time as index
    df = df.set_index('time')

    # create a window
    windows = [i for i in range(int(-(window -1)/2), int((window-1)/2 + 1))]
    df_window = pd.concat([df['pc'].shift(periods = i, freq = '1D').rename(i) for i in windows], axis=1).dropna(axis = 0, how = 'any')
    df_stack = df_window.stack().reset_index()
    df_stack.columns = ['time','window','pc']

    return df_stack

