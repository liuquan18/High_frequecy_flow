#%%
import xarray as xr
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import seaborn as sns

import os
import sys
import glob
import matplotlib.colors as mcolors

import logging
logging.basicConfig(level=logging.INFO)

#%%
def read_Cxy(var1 = 'hus_std', var2 = 'va', region = 'NAL'):

    members = np.arange(1, 51)
    coherence = []

    for member in members:
        logging.info(f"Processing member {member}")
        base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var1}_{var2}_coherence/r{member}i1p1f1/"

        if region is not None:
            files = glob.glob(base_dir + f"*{region}*.nc")
        else:
            logging.warning("No region specified, reading all files except those with 'NAL' or 'NPO'")
            files = glob.glob(base_dir + "*.nc")
            files = [f for f in files if 'NAL' not in f and 'NPO' not in f]

        cxy = xr.open_mfdataset(files, combine="by_coords")

        coherence.append(cxy)
    coherence = xr.concat(coherence, dim='ens')
    coherence['ens'] = members

    return coherence

#%%
hus_vt_Cxy_NAL = read_Cxy('hus_std', 'vt', 'NAL')
hus_vt_Cxy_NPO = read_Cxy('hus_std', 'vt', 'NPO')
#%%
tas_vt_Cxy_NAL = read_Cxy('tas_std', 'vt', 'NAL')
tas_vt_Cxy_NPO = read_Cxy('tas_std', 'vt', 'NPO')
#%%
vt_va_Cxy_NAL = read_Cxy('vt', 'va', 'NAL')
vt_va_Cxy_NPO = read_Cxy('vt', 'va', 'NPO')
#%%
vt_va_Cxy = read_Cxy('vt', 'va', None)
#%%
hus_vt_Cxy_NAL.load()
hus_vt_Cxy_NPO.load()
#%%
tas_vt_Cxy_NAL.load()
tas_vt_Cxy_NPO.load()
#%%
vt_va_Cxy_NAL.load()
vt_va_Cxy_NPO.load()
#%%
vt_va_Cxy.load()

#%%
def plot_coherence(f, Cxy_mean, Cxy_5, Cxy_95, ax, color_line = 'k', color_shading = 'gray', label = None):
    ax.plot(1/f, Cxy_mean, label=label, color=color_line)
    ax.set_xlabel('Period [days]')
    ax.set_ylabel('Coherence')

    ax.set_xticks(np.arange(0, 31, 6))

    # fill between
    ax.fill_between(1/f, Cxy_5, Cxy_95, color=color_shading, alpha=0.5, label = r'5-95$\%$ ens spread')


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
hus_vt_NAL_mean, hus_vt_NAL_95, hus_vt_NAL_05 = get_plot_data(hus_vt_Cxy_NAL)
hus_vt_NPO_mean, hus_vt_NPO_95, hus_vt_NPO_05 = get_plot_data(hus_vt_Cxy_NPO)

vt_va_mean, vt_va_95, vt_va_05 = get_plot_data(vt_va_Cxy, globe_mean = False)
#%%
hus_vt_NAL_mean_first, hus_vt_NAL_95_first, hus_vt_NAL_05_first = get_plot_data(hus_vt_Cxy_NAL, period = 'first')
hus_vt_NPO_mean_first, hus_vt_NPO_95_first, hus_vt_NPO_05_first = get_plot_data(hus_vt_Cxy_NPO, period = 'first')

vt_va_mean_first, vt_va_95_first, vt_va_05_first = get_plot_data(vt_va_Cxy, globe_mean = False, period = 'first')
#%%
hus_vt_NAL_mean_last, hus_vt_NAL_95_last, hus_vt_NAL_05_last = get_plot_data(hus_vt_Cxy_NAL, period = 'last')
hus_vt_NPO_mean_last, hus_vt_NPO_95_last, hus_vt_NPO_05_last = get_plot_data(hus_vt_Cxy_NPO, period = 'last')

vt_va_mean_last, vt_va_95_last, vt_va_05_last = get_plot_data(vt_va_Cxy, globe_mean = False, period = 'last')
#%%
tas_vt_NAL_mean, tas_vt_NAL_95, tas_vt_NAL_05 = get_plot_data(tas_vt_Cxy_NAL)
tas_vt_NPO_mean, tas_vt_NPO_95, tas_vt_NPO_05 = get_plot_data(tas_vt_Cxy_NPO)

tas_vt_NAL_mean_first, tas_vt_NAL_95_first, tas_vt_NAL_05_first = get_plot_data(tas_vt_Cxy_NAL, period = 'first')
tas_vt_NPO_mean_first, tas_vt_NPO_95_first, tas_vt_NPO_05_first = get_plot_data(tas_vt_Cxy_NPO, period = 'first')

tas_vt_NAL_mean_last, tas_vt_NAL_95_last, tas_vt_NAL_05_last = get_plot_data(tas_vt_Cxy_NAL, period = 'last')
tas_vt_NPO_mean_last, tas_vt_NPO_95_last, tas_vt_NPO_05_last = get_plot_data(tas_vt_Cxy_NPO, period = 'last')

#%%
vt_va_NAL_mean, vt_va_NAL_95, vt_va_NAL_05 = get_plot_data(vt_va_Cxy_NAL)
vt_va_NPO_mean, vt_va_NPO_95, vt_va_NPO_05 = get_plot_data(vt_va_Cxy_NPO)

vt_va_NAL_mean_first, vt_va_NAL_95_first, vt_va_NAL_05_first = get_plot_data(vt_va_Cxy_NAL, period = 'first')
vt_va_NPO_mean_first, vt_va_NPO_95_first, vt_va_NPO_05_first = get_plot_data(vt_va_Cxy_NPO, period = 'first')

vt_va_NAL_mean_last, vt_va_NAL_95_last, vt_va_NAL_05_last = get_plot_data(vt_va_Cxy_NAL, period = 'last')
vt_va_NPO_mean_last, vt_va_NPO_95_last, vt_va_NPO_05_last = get_plot_data(vt_va_Cxy_NPO, period = 'last')

# %%
# plot all ensemble members
fig, axes = plt.subplots(1, 3, figsize=(12, 5))

# Plot vt_va_Cxy
axes[0] = plot_coherence(vt_va_Cxy['frequency'], vt_va_mean, vt_va_05, vt_va_95, axes[0], label='Global Mean')

# Plot vt_va_NAL and vt_va_NPO on the same axis
plot_coherence(vt_va_Cxy_NAL['frequency'], vt_va_NAL_mean, vt_va_NAL_05, vt_va_NAL_95, axes[0], color_line='orange', color_shading='orange', label='NAL')
plot_coherence(vt_va_Cxy_NPO['frequency'], vt_va_NPO_mean, vt_va_NPO_05, vt_va_NPO_95, axes[0], color_line='green', color_shading='green', label='NPO')

# Plot hus_std va NPO
plot_coherence(hus_vt_Cxy_NPO['frequency'], hus_vt_NPO_mean, hus_vt_NPO_05, hus_vt_NPO_95, axes[1])
axes[1].set_title('hus_std va NPO')

# Plot hus_std va NAL
plot_coherence(hus_vt_Cxy_NAL['frequency'], hus_vt_NAL_mean, hus_vt_NAL_05, hus_vt_NAL_95, axes[2])
axes[2].set_title('hus_std va NAL')

# axes[0].set_ylim(0.39, 0.48)
# for ax in axes[1:]:
#     ax.set_ylim(0.32, 0.41)

axes[0].set_title(r"$v_{t 20-60}$, $va_{20-60}$")
axes[1].set_title(r"$\Delta q_{NPO}$,  $va_{NPO}$ ")
axes[2].set_title(r"$\Delta q_{NAL}$, $va_{NAL}$")

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
axes[0].legend(frameon=False)

plt.tight_layout()
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/vt_va_q_coherence.png", dpi = 300)
# %%

# %%
temp_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/temp_seq.txt"
)
temp_cmap_seq = mcolors.ListedColormap(temp_cmap_seq, name="temp_div")


prec_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_seq.txt"
)
prec_cmap_seq = mcolors.ListedColormap(prec_cmap_seq, name="prec_div")

# %%
# plot all ensemble members
fig, axes = plt.subplots(1,3, figsize=(12,5))

axes[0] = plot_coherence(vt_va_Cxy['frequency'], vt_va_mean, vt_va_05, vt_va_95, axes[0])
axes[0].set_title('vt va')

# Plot hus_std va NPO and tas_std va NPO on the same axis
plot_coherence(tas_vt_Cxy_NPO['frequency'], tas_vt_NPO_mean, tas_vt_NPO_05, tas_vt_NPO_95, axes[1], color_line = temp_cmap_seq(0.7), color_shading = temp_cmap_seq(0.5), label = r"$\Delta T$ ~ $va$ ")
plot_coherence(hus_vt_Cxy_NPO['frequency'], hus_vt_NPO_mean, hus_vt_NPO_05, hus_vt_NPO_95, axes[1], color_line = prec_cmap_seq(0.9), color_shading = prec_cmap_seq(0.5), label = r"$\Delta q$ ~ $va$ ")

axes[1].set_title('hus_std and tas_std va NPO')

# Plot hus_std va NAL and tas_std va NAL on the same axis
plot_coherence(tas_vt_Cxy_NAL['frequency'], tas_vt_NAL_mean, tas_vt_NAL_05, tas_vt_NAL_95, axes[2], color_line = temp_cmap_seq(0.7), color_shading = temp_cmap_seq(0.5), label = r"$\Delta T$ ~ $va$ ")
plot_coherence(hus_vt_Cxy_NAL['frequency'], hus_vt_NAL_mean, hus_vt_NAL_05, hus_vt_NAL_95, axes[2], color_line = prec_cmap_seq(0.9), color_shading = prec_cmap_seq(0.5), label = r"$\Delta q$ ~ $va$ ")
axes[2].set_title('hus_std and tas_std va NAL')


axes[0].set_title(r"$v_{t 20-60}$, $va_{20-60}$")
axes[1].set_title("NPO spatial mean")
axes[2].set_title("NAL spatial mean")

# Add vertical lines at days = 2 and days = 12
axes[0].axvline(x=2, color='r', linestyle='--')
axes[0].axvline(x=6, color='r', linestyle='--')
axes[0].axvline(x=12, color='r', linestyle='--')

# Add double arrow lines and labels
axes[0].annotate(r'$v^{\prime}$', xy=(2, 0.40), xytext=(12, 0.399),
             arrowprops=dict(arrowstyle='<->', color='blue'), color='blue')
axes[0].annotate(r'$v^{\prime\prime}$', xy=(2, 0.41), xytext=(6, 0.409),
             arrowprops=dict(arrowstyle='<->', color='green'), color='green')

# axes[0].set_xlim(0, 30)
# axes[0].set_ylim(0.32, 0.49)
# axes[1].set_ylim(0.32, 0.49)
# axes[2].set_ylim(0.32, 0.49)


# Set colors for the legends
handles, labels = axes[1].get_legend_handles_labels()
axes[1].legend(handles, labels, frameon=False)

# handles, labels = axes[2].get_legend_handles_labels()
# axes[2].legend(handles, labels, frameon=False)

plt.tight_layout()
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/vt_q_t_va_coherence.png", dpi = 300)


# %%
