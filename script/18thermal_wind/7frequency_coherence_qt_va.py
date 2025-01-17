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
def get_plot_data(Cxy, globe_mean = False, period = None):

    if period == 'first':
        Cxy = Cxy.sel(time = '1850')
    elif period == 'last':
        Cxy = Cxy.sel(time = '2090')
    
    else:
        logging.warning("No period specified, using all data")


    if globe_mean:
        Cxy = Cxy.mean(dim = ('lat', 'lon', 'time'))
    else:
        Cxy = Cxy.mean(dim = 'time')

    Cxy_mean = Cxy['coherence'].mean(dim = ('ens'))
    Cxy_95 = Cxy['coherence'].quantile(0.95, dim = ('ens'))
    Cxy_05 = Cxy['coherence'].quantile(0.05, dim = ('ens'))

    return Cxy_mean, Cxy_95, Cxy_05

#%%
hus_va_NAL_mean, hus_va_NAL_95, hus_va_NAL_05 = get_plot_data(hus_va_Cxy_NAL)
hus_va_NPO_mean, hus_va_NPO_95, hus_va_NPO_05 = get_plot_data(hus_va_Cxy_NPO)

vt_va_mean, vt_va_95, vt_va_05 = get_plot_data(vt_va_Cxy, globe_mean = True)
#%%
hus_va_NAL_mean_first, hus_va_NAL_95_first, hus_va_NAL_05_first = get_plot_data(hus_va_Cxy_NAL, period = 'first')
hus_va_NPO_mean_first, hus_va_NPO_95_first, hus_va_NPO_05_first = get_plot_data(hus_va_Cxy_NPO, period = 'first')

vt_va_mean_first, vt_va_95_first, vt_va_05_first = get_plot_data(vt_va_Cxy, globe_mean = True, period = 'first')
#%%
hus_va_NAL_mean_last, hus_va_NAL_95_last, hus_va_NAL_05_last = get_plot_data(hus_va_Cxy_NAL, period = 'last')
hus_va_NPO_mean_last, hus_va_NPO_95_last, hus_va_NPO_05_last = get_plot_data(hus_va_Cxy_NPO, period = 'last')

vt_va_mean_last, vt_va_95_last, vt_va_05_last = get_plot_data(vt_va_Cxy, globe_mean = True, period = 'last')

# %%
# plot all ensemble members
fig, axes = plt.subplots(1,3, figsize=(12,5))

plot_coherence(vt_va_Cxy['frequency'], vt_va_mean, vt_va_05, vt_va_95, axes[0])
axes[0].set_title('vt va')

plot_coherence(hus_va_Cxy_NPO['frequency'], hus_va_NPO_mean, hus_va_NPO_05, hus_va_NPO_95, axes[1])
axes[1].set_title('hus_std va NPO')

plot_coherence(hus_va_Cxy_NAL['frequency'], hus_va_NAL_mean, hus_va_NAL_05, hus_va_NAL_95, axes[2])
axes[2].set_title('hus_std va NAL')

axes[0].set_ylim(0.39, 0.48)
for ax in axes[1:]:
    ax.set_ylim(0.32, 0.41)

axes[0].set_title(r"$v_{t 20-60}$, $v_{a 20-60}$")
axes[1].set_title(r"$\Delta q_{NPO}$,  $v_{a 20-60}$ ")
axes[2].set_title(r"$\Delta q_{NAL}$, $v_{a 20-60}$")


# Add vertical lines at days = 2 and days = 12
axes[0].axvline(x=2, color='r', linestyle='--')
axes[0].axvline(x=6, color='r', linestyle='--')
axes[0].axvline(x=12, color='r', linestyle='--')

# Add double arrow lines and labels
axes[0].annotate(r'$v^{\prime}$', xy=(2, 0.40), xytext=(12, 0.399),
             arrowprops=dict(arrowstyle='<->', color='blue'), color='blue')
axes[0].annotate(r'$v^{\prime\prime}$', xy=(2, 0.41), xytext=(6, 0.409),
             arrowprops=dict(arrowstyle='<->', color='green'), color='green')

axes[0].set_xlim(0, 30)

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/vt_va_q_coherence.png", dpi = 300)
# %%
