#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
#%%
Cxy_files = glob.glob("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_hus_coherence/r*i1p1f1/*.nc")

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
# %%
fig, ax1 = plt.subplots()
ax1.plot(1/f, Cxy_mean, label='mean', color='k')
ax1.set_xlabel('Period [days]')
ax1.set_ylabel('Coherence')

ax1.set_xticks(np.arange(0, 31, 6))

# fill between
ax1.fill_between(1/f, Cxy_5, Cxy_95, color='gray', alpha=0.5)

# Add vertical lines at days = 2 and days = 12
ax1.axvline(x=2, color='r', linestyle='--')
ax1.axvline(x=6, color='r', linestyle='--')
ax1.axvline(x=12, color='r', linestyle='--')

# Add double arrow lines and labels
ax1.annotate(r'$v^{\prime}$', xy=(2, 0.05), xytext=(12, 0.045),
             arrowprops=dict(arrowstyle='<->', color='blue'), color='blue')
ax1.annotate(r'$v^{\prime\prime}$', xy=(2, 0.1), xytext=(6, 0.096),
             arrowprops=dict(arrowstyle='<->', color='green'), color='green')

ax1.set_xlim(0, 30)


plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/vt_va_coherence.png", dpi = 300)

# %%
