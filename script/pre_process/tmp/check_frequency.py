#%%
import xarray as xr
# %%
high = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/tmp/timeseries.nc")
# %%
ts = high.sel(lat=0, lon=0,plev = 25000, method="nearest").ua
# %%
ts = ts.to_dataframe()
# %%
ts = ts[['ua']]
# %%
df = ts.reset_index()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

# Assuming your dataframe is called 'df' and has a 'time' column and a 'ua' column
# Convert 'time' to datetime if it's not already
df['time'] = pd.to_datetime(df['time'])

# Sort the dataframe by time to ensure it's in chronological order
df = df.sort_values('time')

# Calculate the sampling frequency (assuming daily data)
sampling_freq = 1  # 1 sample per day

# Perform the FFT
fft_result = fft(df['ua'].values)
n = len(fft_result)

# Calculate the frequencies
freqs = np.fft.fftfreq(n, d=1/sampling_freq)

# Calculate the periods (in days)
periods = 1 / freqs

# Calculate the power spectrum
power_spectrum = np.abs(fft_result)**2

# Create the plot
plt.figure(figsize=(12, 6))
plt.semilogx(periods[1:n//2], power_spectrum[1:n//2])  # Skip the first point (DC component)
plt.xlabel('Period (days)')
plt.ylabel('Power')
plt.title('Power Spectrum')
plt.grid(True)

# Set x-axis limits to show relevant period range (e.g., 2 to 365 days)
plt.xlim(2, 365)

# Add vertical lines for some common periods
common_periods = [2,5, 12, 90, 365]
for period in common_periods:
    plt.axvline(x=period, color='r', linestyle='--', alpha=0.5)
    plt.text(period, plt.ylim()[1], f'{period}d', rotation=90, va='top', ha='right')

plt.show()
# %%
