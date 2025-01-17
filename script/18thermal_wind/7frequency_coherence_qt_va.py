#%%
import xarray as xr
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import seaborn as sns

import os
import sys
import glob

import logging
logging.basicConfig(level=logging.INFO)

#%%
def read_Cxy(var1 = 'hus', var2 = 'va', region = 'NAL'):

    members = np.arange(1, 51)
    coherence = []

    for member in members:
        logging.info(f"Processing member {member}")
        base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var1}_{var2}_coherence/r{member}i1p1f1/"

        if region is not None:
            files = glob.glob(base_dir + f"*{region}*.nc")
        else:
            logging.warning("No region specified, reading all files")
            files = glob.glob(base_dir + "*.nc")

        cxy = xr.open_mfdataset(files, combine="by_coords")

        coherence.append(cxy)
    coherence = xr.concat(coherence, dim='ens')
    coherence['ens'] = members

    return coherence

#%%
hus_va_Cxy_NAL = read_Cxy('hus_std', 'va', 'NAL')
hus_va_Cxy_NPO = read_Cxy('hus_std', 'va', 'NPO')
#%%
vt_va_Cxy = read_Cxy('vt', 'va', None)
#%%
hus_va_Cxy_NAL.load()
hus_va_Cxy_NPO.load()
vt_va_Cxy.load()
#%%
def plot_coherence(f, Cxy_mean, Cxy_5, Cxy_95, ax):
    ax.plot(1/f, Cxy_mean, label='mean', color='k')
    ax.set_xlabel('Period [days]')
    ax.set_ylabel('Coherence')

    ax.set_xticks(np.arange(0, 31, 6))

    # fill between
    ax.fill_between(1/f, Cxy_5, Cxy_95, color='gray', alpha=0.5)


    ax.set_xlim(0, 30)

    return ax
#%%
hus_va_Cxy_NAL = hus_va_Cxy_NAL.mean(dim = 'time')
hus_va_Cxy_NPO = hus_va_Cxy_NPO.mean(dim = 'time')
vt_va_Cxy = vt_va_Cxy.mean(dim = ('lat','lon', 'time'))

# %%
hus_va_Cxy_NAL_mean = hus_va_Cxy_NAL['coherence'].mean(dim = ('ens'))
hus_va_Cxy_NAL_95 = hus_va_Cxy_NAL['coherence'].quantile(0.95, dim = ('ens'))
hus_va_Cxy_NAL_05 = hus_va_Cxy_NAL['coherence'].quantile(0.05, dim = ('ens'))

#%%
hus_va_Cxy_NPO_mean = hus_va_Cxy_NPO['coherence'].mean(dim = ('ens'))
hus_va_Cxy_NPO_95 = hus_va_Cxy_NPO['coherence'].quantile(0.95, dim = ('ens'))
hus_va_Cxy_NPO_05 = hus_va_Cxy_NPO['coherence'].quantile(0.05, dim = ('ens'))

#%%
vt_va_Cxy_mean = vt_va_Cxy['coherence'].mean(dim = ('ens'))
vt_va_Cxy_95 = vt_va_Cxy['coherence'].quantile(0.95, dim = ('ens'))
vt_va_Cxy_05 = vt_va_Cxy['coherence'].quantile(0.05, dim = ('ens'))
# %%
# plot all ensemble members
fig, axes = plt.subplots(1,3, figsize=(15,5))

plot_coherence(vt_va_Cxy['frequency'], vt_va_Cxy_mean, vt_va_Cxy_05, vt_va_Cxy_95, axes[0])
axes[0].set_title('vt va')

plot_coherence(hus_va_Cxy_NAL['frequency'], hus_va_Cxy_NAL_mean, hus_va_Cxy_NAL_05, hus_va_Cxy_NAL_95, axes[1])
axes[1].set_title('hus_std va NAL')

plot_coherence(hus_va_Cxy_NPO['frequency'], hus_va_Cxy_NPO_mean, hus_va_Cxy_NPO_05, hus_va_Cxy_NPO_95, axes[2])
axes[2].set_title('hus_std va NPO')

axes[0].set_ylim(0.39, 0.48)
for ax in axes[1:]:
    ax.set_ylim(0.32, 0.41)

# %%


# %%
