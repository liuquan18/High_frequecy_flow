#%%
import pandas as pd
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import glob
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import logging
logging.basicConfig(level=logging.WARNING)
import matplotlib.colors as mcolors

#%%
import src.extremes.extreme_read as er
# %%
def extreme_stat(extreme,stat = 'duration',dur_min = 8):
    """
    Calculate the duration of the extreme events
    """
    extreme_sel = er.sel_event_above_duration(extreme, duration=dur_min, by="extreme_duration")
    extreme_sel = extreme_sel[['sign_start_time','extreme_duration','lat','lon']]
    extreme_sel = extreme_sel.set_index(["sign_start_time", "lat","lon"])

    # to xarray
    ext_x = extreme_sel.to_xarray()

    # calculate the sum duration of the extreme events
    if stat == 'duration':
        extreme_statistics = ext_x.extreme_duration.sum(dim = 'sign_start_time')
    elif stat == 'count':
        extreme_statistics = ext_x.extreme_duration.count(dim = 'sign_start_time')

    return extreme_statistics
# %%

def extreme_stat_all_members(period, extreme_type, stat = 'duration'):
    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_extremes_{extreme_type}/OLR_extremes_{extreme_type}_{period}/"
    extreme_statistics = []
    for member in range(1,51):
        logging.info(f"member {member}")
        file = glob.glob(f"{base_dir}OLR_extremes*r{member}.csv")[0]

        extreme = pd.read_csv(file)
        statistics = extreme_stat(extreme, stat)    
        extreme_statistics.append(statistics)

    extreme_statistics = xr.concat(extreme_statistics, dim = 'member')

    if stat == 'duration':
        # average duration
        extreme_stat_all = extreme_statistics.mean(dim = 'member')
    elif stat == 'count':
        # sum of the count
        extreme_stat_all = extreme_statistics.sum(dim = 'member')

    return extreme_stat_all
#%%

first10_pos = extreme_stat_all_members('first10', 'pos')
last10_pos = extreme_stat_all_members('last10', 'pos')

#%%

# Define the custom colormap
blues = plt.cm.Blues(np.linspace(0, 1, 256))
new_colors = np.vstack((
    np.array([1, 1, 1, 0]),  # Transparent color for values below 20
    blues[20:100],           # Blues colormap for values between 20 and 100
    blues[-1]                # Max color for values above 100
))

# Ensure the number of colors matches the number of bins
custom_cmap = mcolors.ListedColormap(new_colors)
boundaries = np.concatenate(([0], np.arange(20, 101), [101]))
norm = mcolors.BoundaryNorm(boundaries=boundaries, ncolors=custom_cmap.N, clip=True)

#%%
# Function to plot duration with custom colormap
def plot_duration(extreme_duration, ax, custom_cmap = 'Blues', levels=np.arange(5, 30, 5)):
    p = extreme_duration.plot(
        ax=ax,
        # cmap='Blues',
        transform=ccrs.PlateCarree(),
        levels=levels,
        extend='max',
    )
    p.axes.coastlines()
    return p

#%%
fig = plt.figure(figsize=(20, 5))
gs = gridspec.GridSpec(2, 1, wspace=0.1, hspace=0.1)
levels = np.arange(5, 40, 1)

ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree(central_longitude=180))
plot_duration(first10_pos, ax1, levels=levels)
ax1.set_title("First 10 years positive")

ax2 = fig.add_subplot(gs[1, 0], projection=ccrs.PlateCarree(central_longitude=180))
plot_duration(last10_pos, ax2, levels=levels)
ax2.set_title("Last 10 years positive")
plt.suptitle("Average summer duration of OLR extremes")
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_extremes/OLR_extremes_duration.png")
    
# %%

# count
first10_pos_count = extreme_stat_all_members('first10', 'pos', stat = 'count')
last10_pos_count = extreme_stat_all_members('last10', 'pos', stat = 'count')
# %%
