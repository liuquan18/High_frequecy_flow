#%%
import xarray as xr
import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt 
# %%
ex = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_MJJAS_first10/va_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_18500501-18590931.nc")
# %%
v = ex.va.sel(plev = 25000)
# %%
vmean = v.sel(lat = slice(35,70)).mean(dim = 'lat')
# %%
v_field = vmean
# %%
ds = ex
# %%
time = ds['time']
latitude = ds['lat']

# Define the range of wave numbers 
wave_numbers = np.arange(1, 16)

# %%
v_data =v_field.sel(time = '1850')
time = v_data.time
# %%
# Apply spectral analysis (e.g., using FFT)
frequencies, amplitudes = signal.welch(v_data, fs=1,  # Assuming daily data
                                        nperseg=len(time) // 3)  # Adjust segment length as needed

# %%
 # Loop through each wave number
for k in wave_numbers:

    # Apply spectral analysis (e.g., using FFT)
    frequencies, amplitudes = signal.welch(v_data, fs=1,  # Assuming daily data
                                            nperseg=len(time) // 4)  # Adjust segment length as needed

    # Find the dominant frequency and corresponding amplitude
    dominant_freq_index = np.argmax(amplitudes, axis = -1)
    dominant_frequency = frequencies[dominant_freq_index]
    Av = amplitudes[dominant_freq_index]

    break
# %%
