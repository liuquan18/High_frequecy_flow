#%%
import xarray as xr
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.ndimage import gaussian_filter
import os
import sys
import glob
import matplotlib.colors as mcolors

import logging
logging.basicConfig(level=logging.INFO)

#%%
def read_Cxy(var1 = 'hus', var2 = 'va', region = 'NAL', pixel_wise = True):

    if pixel_wise:
        base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/{var1}_{var2}_coherence_pixelwise/"
    else:
        base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/{var1}_{var2}_coherence/"

    if region is not None:
        files = glob.glob(base_dir + f"*{region}*.nc")
    else:
        logging.warning("No region specified, reading all files except those with 'NAL' or 'NPO'")
        files = glob.glob(base_dir + "*.nc")
        files = [f for f in files if 'NAL' not in f and 'NPO' not in f]

    # sort files
    files.sort()

    cxy = xr.open_mfdataset(files, combine="nested", concat_dim="time", parallel=True)

    cxy['time'] = np.arange(1979, 2025, 1)

    return cxy

#%%
hus_va_Cxy_NAL = read_Cxy('hus', 'va', 'NAL', pixel_wise = True)
hus_va_Cxy_NPO = read_Cxy('hus', 'va', 'NPO', pixel_wise = True)
#%%
tas_va_Cxy_NAL = read_Cxy('tas', 'va', 'NAL', pixel_wise=True)
tas_va_Cxy_NPO = read_Cxy('tas', 'va', 'NPO', pixel_wise=True)

#%%
# vt_va_Cxy = read_Cxy('vt', 'va', None)
#%%
hus_va_Cxy_NAL.load()
hus_va_Cxy_NPO.load()
#%%
tas_va_Cxy_NAL.load()
tas_va_Cxy_NPO.load()

#%%
# vt_va_Cxy.load()
# %%
temp_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/temp_seq.txt"
)
temp_cmap_seq = mcolors.ListedColormap(temp_cmap_seq, name="temp_div")


prec_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_seq.txt"
)
prec_cmap_seq = mcolors.ListedColormap(prec_cmap_seq, name="prec_div")

#%%
#%%
hus_va_NAL_mean = hus_va_Cxy_NAL.mean(dim = ('time', 'lat','lon'))
hus_va_NPO_mean = hus_va_Cxy_NPO.mean(dim = ('time', 'lat','lon'))

tas_va_NAL_mean = tas_va_Cxy_NAL.mean(dim = ('time', 'lat','lon'))
tas_va_NPO_mean = tas_va_Cxy_NPO.mean(dim = ('time', 'lat','lon'))
#%%
def smooth_period(cxy, period = 1.5):

    # smoothed_period = np.arange(0.1, 31, period)
    # smoothed_frequency = 1 / smoothed_period

    # cxy_smooth = cxy.interp(frequency = smoothed_frequency)

    # cxy_smooth = cxy.rolling(frequency = period, center = True).mean()
    cxy_smooth = gaussian_filter(cxy.coherence, sigma = period)

    return cxy_smooth

#%%
hus_va_NAL_mean_smooth = smooth_period(hus_va_NAL_mean)
hus_va_NPO_mean_smooth = smooth_period(hus_va_NPO_mean)

tas_va_NAL_mean_smooth = smooth_period(tas_va_NAL_mean)
tas_va_NPO_mean_smooth = smooth_period(tas_va_NPO_mean)



# %%
# plot all ensemble members
fig, axes = plt.subplots(1,2, figsize=(10,5))
f = hus_va_Cxy_NAL.frequency.values
axes[0].plot(1/f, hus_va_NPO_mean.coherence, label = r"$\Delta q$ ~ $va$", color = prec_cmap_seq(0.9), linewidth = 0.5)
axes[0].plot(1/f, tas_va_NPO_mean.coherence, label = r"$\Delta T$ ~ $va$", color = temp_cmap_seq(0.7), linewidth = 0.5)

axes[1].plot(1/f, hus_va_NAL_mean.coherence, label = r"$\Delta q$ ~ $va$", color = prec_cmap_seq(0.9), linewidth = 0.5)
axes[1].plot(1/f, tas_va_NAL_mean.coherence, label = r"$\Delta T$ ~ $va$", color = temp_cmap_seq(0.7), linewidth = 0.5)

# smooth
axes[0].plot(1/f, hus_va_NPO_mean_smooth, color = prec_cmap_seq(0.9), linewidth = 2, linestyle = '--')
axes[0].plot(1/f, tas_va_NPO_mean_smooth, color = temp_cmap_seq(0.7), linewidth = 2, linestyle = '--')

axes[1].plot(1/f, hus_va_NAL_mean_smooth, color = prec_cmap_seq(0.9), linewidth = 2, linestyle = '--')
axes[1].plot(1/f, tas_va_NAL_mean_smooth, color = temp_cmap_seq(0.7), linewidth = 2, linestyle = '--')

axes[0].set_title(r"$\Delta q_{NPO}$,  $va_{NPO}$ ")
axes[1].set_title(r"$\Delta q_{NAL}$, $va_{NAL}$")


# Add vertical lines at days = 2 and days = 12
axes[0].axvline(x=2, color='r', linestyle='--')
axes[0].axvline(x=12, color='r', linestyle='--')


axes[0].set_xlim(0, 30)
axes[1].set_xlim(0, 30)

axes[0].set_ylim(0.34, 0.40)
axes[1].set_ylim(0.34, 0.40)
axes[0].set_xticks(np.arange(0, 31, 6))
axes[1].set_xticks(np.arange(0, 31, 6))

axes[0].legend(frameon = False)


plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/coherence_ERA5.png", dpi = 300)

# %%
