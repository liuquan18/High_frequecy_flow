#%%
import xarray as xr
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

import os
import sys
# %%
member=sys.argv[1]

va_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_ano_lowlevel/r{member}i1p1f1/'
vt_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vt_daily_ano/r{member}i1p1f1/'

coherence_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vt_va_coherence/r{member}i1p1f1/'
if not os.path.exists(coherence_path):
    os.makedirs(coherence_path)

#%%
va= xr.open_mfdataset(f"{va_path}*.nc", combine='by_coords')
# %%
vt = xr.open_mfdataset(f"{vt_path}*.nc", combine='by_coords')
# %%
# lat mean
vt = vt.sel(lat = slice(20, 60)).mean('lat')
va = va.sel(lat = slice(20, 60)).mean('lat')
#%%
vt = vt['vt']
va = va['va']

# %%
f, Cxy = signal.coherence(vt, va, fs = 1, nperseg=153, detrend =False, noverlap = 0, axis = 0)

#%%
Cxy = xr.DataArray(Cxy, dims = ['frequency', 'lon'], coords = {'frequency': f, 'lon': vt.lon})

#%%

Cxy.name = 'coherence'

Cxy.to_netcdf(f"{coherence_path}coherence.nc")

# %%
# fig, ax1 = plt.subplots()

# ax1.plot(f, np.mean(Cxy, axis=1))
# ax1.set_xlabel('frequency [Hz]')
# ax1.set_ylabel('Coherence')

# # Create a secondary x-axis on top
# ax2 = ax1.twiny()
# ax2.set_xlim(ax1.get_xlim())
# ax2.set_xticks(ax1.get_xticks())
# ax2.set_xticklabels([f'{1/x:.1f}' if x != 0 else 'inf' for x in ax1.get_xticks()])
# ax2.set_xlabel('Period [days]')

# # Add vertical lines at days = 2 and days = 12
# days = [2, 12]
# for day in days:
#     freq = 1 / day
#     ax2.axvline(freq, color='r', linestyle='--')

# plt.show()


# %%
