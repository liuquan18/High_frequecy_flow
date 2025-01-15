#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
#%%
Cxy_files = glob.glob("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vt_va_coherence/r*i1p1f1/*.nc")

#%%
Cxy = xr.open_mfdataset(Cxy_files, combine='nested', concat_dim='member')
Cxy.load()
#%%
Cxy = Cxy['coherence']
Cxy = Cxy.mean(dim = 'lon')

#%%
Cxy_95 = Cxy.quantile(0.95, dim = 'member')
Cxy_5 = Cxy.quantile(0.05, dim = 'member')
#%%
Cxy_mean = Cxy.mean(dim = 'member')
#%%
f = Cxy['frequency']
#%%

fig, ax1 = plt.subplots()

ax1.plot(f, Cxy_mean, label = 'mean')
ax1.set_xlabel('frequency [Hz]')
ax1.set_ylabel('Coherence')

# fill between
ax1.fill_between(f, Cxy_5, Cxy_95, color = 'gray', alpha = 0.5)
ax1.set_xlim(0, 0.55)
# Create a secondary x-axis on top
ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(ax1.get_xticks())
ax2.set_xticklabels([f'{1/x:.1f}' if x != 0 else 'inf' for x in ax1.get_xticks()])
ax2.set_xlabel('Period [days]')

# Add vertical lines at days = 2 and days = 12
days = [2, 12]
for day in days:
    freq = 1 / day
    ax2.axvline(freq, color='r', linestyle='--')

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/vt_va_coherence.png", dpi = 300)

# %%
