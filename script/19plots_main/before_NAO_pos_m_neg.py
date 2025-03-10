#%%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line
from src.plotting.util import lon2x

import matplotlib.colors as mcolors
import cartopy
import glob
#%%
import src.plotting.util as util
import src.moisture.longitudinal_contrast as lc

import importlib
importlib.reload(util)

#%%
def smooth(arr, lat_window = 3, lon_window = 9):

    arr = lc.rolling_lon_periodic(arr, lon_window, lat_window, stat = 'mean')
    return arr
#%%
def remove_zonalmean(arr):
    arr = arr - arr.mean(dim = 'lon')
    return arr
#%%
def postprocess(ds, do_smooth = False, remove_zonal = False):
    if do_smooth:
        ds = smooth(ds)
    if remove_zonal:
        ds = remove_zonalmean(ds)
    ds = erase_white_line(ds)
    return ds
#%%

def read_composite(var, name, decade):
    pos_file = glob.glob(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_pos_*_mean_{decade}.nc')
    neg_file = glob.glob(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_neg_*_mean_{decade}.nc')
    if len(pos_file) == 0 or len(neg_file) == 0:
        raise ValueError(f"no file found for {var} in {decade}")
    NAO_pos = xr.open_dataset(pos_file[0])
    NAO_neg = xr.open_dataset(neg_file[0])
    NAO_pos = NAO_pos[name]
    NAO_neg = NAO_neg[name]

    NAO_pos = NAO_pos.mean(dim = 'event').squeeze()
    NAO_neg = NAO_neg.mean(dim = 'event').squeeze()

    NAO_pos = postprocess(NAO_pos)
    NAO_neg = postprocess(NAO_neg)

    return NAO_pos.compute(), NAO_neg.compute()
#%%
uhat_composiste = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/"
uhat_pos_first10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_first10_pos.nc")
uhat_neg_first10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_first10_neg.nc")

uhat_pos_last10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_last10_pos.nc")
uhat_neg_last10 = xr.open_dataarray(f"{uhat_composiste}jetstream_MJJAS_last10_neg.nc")
#%%
uhat_NAO_first = uhat_pos_first10 - uhat_neg_first10
uhat_NAO_last = uhat_pos_last10 - uhat_neg_last10
#%%
uhat_NAO_first = postprocess(uhat_NAO_first)
uhat_NAO_last = postprocess(uhat_NAO_last)

# %%
eke_NAO_pos_first, eke_NAO_neg_first = read_composite('eke', 'eke', 1850)
eke_NAO_pos_last, eke_NAO_neg_last = read_composite('eke', 'eke', 2090)
# %%
upvp_NAO_pos_first, upvp_NAO_neg_first = read_composite('upvp', 'ua', 1850)
upvp_NAO_pos_last, upvp_NAO_neg_last = read_composite('upvp', 'ua', 2090)

# %%
eke_NAO_first = eke_NAO_pos_first - eke_NAO_neg_first
eke_NAO_last = eke_NAO_pos_last - eke_NAO_neg_last

upvp_NAO_first = upvp_NAO_pos_first - upvp_NAO_neg_first
upvp_NAO_last = upvp_NAO_pos_last - upvp_NAO_neg_last


#%%
# for plotting

# %%
temp_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/temp_seq.txt"
)
temp_cmap_seq = mcolors.ListedColormap(temp_cmap_seq, name="temp_div")

temp_cmap_div = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/temp_div.txt"
)
temp_cmap_div = mcolors.ListedColormap(temp_cmap_div, name="temp_div")

prec_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_seq.txt"
)
prec_cmap_seq = mcolors.ListedColormap(prec_cmap_seq, name="prec_div")

prec_cmap_div = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_div.txt"
)
prec_cmap_div = mcolors.ListedColormap(prec_cmap_div, name="prec_div")
#%%
eke_levels_div = np.arange(-2.5, 2.6, 0.5)
upvp_levels_div = np.arange(-25, 26, 5)
uhat_levels_div = np.arange(-12, 13, 2)



# %%
fig, axes = plt.subplots(3, 3, figsize=(10, 11), subplot_kw={'projection': ccrs.Orthographic(-20, 90)})
uhat_NAO_first.plot.contourf(ax=axes[0, 0], transform=ccrs.PlateCarree(), cmap=temp_cmap_div, levels=uhat_levels_div, extend='both', add_colorbar=False)
uhat_NAO_last.plot.contourf(ax=axes[1, 0], transform=ccrs.PlateCarree(), cmap=temp_cmap_div, levels=uhat_levels_div, extend='both', add_colorbar=False)
uhat_diff = (uhat_NAO_last - uhat_NAO_first).plot.contourf(ax=axes[2, 0], transform=ccrs.PlateCarree(), cmap=temp_cmap_div, levels=uhat_levels_div, extend='both', add_colorbar=False)
cbar_uhat = fig.colorbar(uhat_diff, ax=axes[:, 0], orientation='horizontal', shrink=0.6, pad=0.1)
cbar_uhat.set_label(r'$m/s$')


# second column for upvp
upvp_NAO_first.plot.contourf(ax=axes[0, 1], transform=ccrs.PlateCarree(), cmap=temp_cmap_div, levels=upvp_levels_div, extend='both', add_colorbar=False)
upvp_NAO_last.plot.contourf(ax=axes[1, 1], transform=ccrs.PlateCarree(), cmap=temp_cmap_div, levels=upvp_levels_div, extend='both', add_colorbar=False)
upvp_diff = (upvp_NAO_last - upvp_NAO_first).plot.contourf(ax=axes[2, 1], transform=ccrs.PlateCarree(), cmap=temp_cmap_div, levels=upvp_levels_div, extend='both', add_colorbar=False)
cbar_upvp = fig.colorbar(upvp_diff, ax=axes[:, 1], orientation='horizontal', shrink=0.6, pad=0.1)
cbar_upvp.set_label(r'$m^2/s^2$')

# third column for eke
eke_NAO_first.plot.contourf(ax=axes[0, 2], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=eke_levels_div, extend='both', add_colorbar=False)
eke_NAO_last.plot.contourf(ax=axes[1, 2], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=eke_levels_div, extend='both', add_colorbar=False)
eke_diff = (eke_NAO_last - eke_NAO_first).plot.contourf(ax=axes[2, 2], transform=ccrs.PlateCarree(), cmap='RdBu_r', levels=eke_levels_div, extend='both', add_colorbar=False)
cbar_eke = fig.colorbar(eke_diff, ax=axes[:, 2], orientation='horizontal', shrink=0.6, pad=0.1)
cbar_eke.set_label(r'$m^2/s^2$')

for ax in axes.flatten():
    ax.coastlines()
    # ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.axhline(20, color='k', lw=0.5, ls='dotted')
    ax.axhline(60, color='k', lw=0.5, ls='dotted')

# axes[2,2].axvline(x=lon2x(-145, axes[2,2]), ymin=0.22, ymax=0.65, color='k', lw=0.5, ls='dotted')
# axes[2,2].axvline(x=lon2x(140, axes[2,2]), ymin=0.22, ymax=0.65, color='k', lw=0.5, ls='dotted')
# axes[2,2].axvline(x=lon2x(-30, axes[2,2]), ymin=0.22, ymax=0.65, color='k', lw=0.5, ls='dotted')
# axes[2,2].axvline(x=lon2x(-70, axes[2,2]), ymin=0.22, ymax=0.65, color='k', lw=0.5, ls='dotted')

# latitude ticks
for i, ax in enumerate(axes.flatten()):
    # ax.set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())

    # if i % 3 == 0:
    #     ax.set_yticks([20, 60], crs=ccrs.PlateCarree())
    #     ax.set_ylabel("Latitude")
    #     ax.yaxis.set_major_formatter(cartopy.mpl.ticker.LatitudeFormatter())
    # else:
    #     ax.set_yticks([])
    
    # if i // 3 == 3:
    #     ax.set_xticklabels(['180°', '120°W', '60°W', '0°', '60°E', '120°E'])
    # else:
    #     ax.set_xticks([])

    ax.set_xlabel("")
    ax.set_ylabel("")

axes[0, 0].set_title(r"1850 $\bar{u}$")
axes[0, 1].set_title(r"1850 $u'v'$")
axes[0, 2].set_title(r"1850 EKE")
axes[1, 0].set_title(r"2090 $\bar{u}$")
axes[1, 1].set_title(r"2090 $u'v'$")
axes[1, 2].set_title(r"2090 EKE")
axes[2, 0].set_title(r"$\Delta \bar{u}$")
axes[2, 1].set_title(r"$\Delta u'v'$")
axes[2, 2].set_title(r"$\Delta$ EKE")



# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/eke_upvp_NAO_diff_maps.pdf", dpi = 300)
# %%
