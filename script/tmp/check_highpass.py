#%%
import xarray as xr
from scipy.signal import butter, filtfilt
# %%
data = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/tmp/pass_ex.nc")
# %%
data = data.va.squeeze()
#%%
cdo_result = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/tmp/high_pass_cdo.nc").va.squeeze()
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

#%%

# Load your data (replace with your actual data loading)
# Assuming a CSV with columns: 'date' and 'va'

df = data.to_dataframe()[['va']]
#%%
# Handle date range edge case (September has only 30 days)
df = df.loc['1850-05-01':'1850-09-30']

# Check for missing values
if df['va'].isnull().any():
    df['va'] = df['va'].interpolate()  # Linear interpolation for missing values

# Filter parameters
sampling_freq = 1  # Daily data (1 sample/day)
cutoff_period = 12  # Days
nyquist_freq = 0.5 * sampling_freq
cutoff_freq = 1 / cutoff_period  # Convert period to frequency

# Create high-pass Butterworth filter
order = 4  # Filter order
b, a = butter(order, cutoff_freq/nyquist_freq, btype='high', analog=False)

# Apply zero-phase filter using filtfilt
va_hp = filtfilt(b, a, df['va'])

# Create results DataFrame
result = pd.DataFrame({
    'Original': df['va'],
    'Highpassed': va_hp
}, index=df.index)

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(result['Original'], label='Original', alpha=0.7)
plt.plot(result['Highpassed'], label='Highpassed (12-day cutoff)', color='orange')
cdo_result.plot(label='CDO Highpassed', color='red')

plt.title('Meridional Wind Component (va) - Highpass Filtered')
plt.ylabel('Wind Speed')
plt.xlabel('Date')
plt.legend()
plt.grid(True)
plt.show()

# %%
