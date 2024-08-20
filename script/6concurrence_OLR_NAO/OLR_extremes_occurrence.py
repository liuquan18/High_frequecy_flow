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
def duration_of_extreme(extreme):
    """
    Calculate the duration of the extreme events
    """
    extreme_sel = er.sel_event_above_duration(extreme, duration=8, by="extreme_duration")
    extreme_sel = extreme_sel[['sign_start_time','extreme_duration','lat','lon']]
    extreme_sel = extreme_sel.set_index(["sign_start_time", "lat","lon"])

    # to xarray
    ext_x = extreme_sel.to_xarray()

    # calculate the sum duration of the extreme events
    extreme_duration = ext_x.extreme_duration.sum(dim = 'sign_start_time')

    return extreme_duration
# %%

def extreme_duration_all_members(period, extreme_type):
    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_extremes_{extreme_type}/OLR_extremes_{extreme_type}_{period}/"
    extreme_durations = []
    for member in range(1,51):
        logging.info(f"member {member}")
        file = glob.glob(f"{base_dir}OLR_extremes*r{member}.csv")[0]

        extreme = pd.read_csv(file)
        extreme_duration = duration_of_extreme(extreme)    
        extreme_durations.append(extreme_duration)

    extreme_durations = xr.concat(extreme_durations, dim = 'member')
    extreme_mean_dur = extreme_durations.mean(dim = 'member')

    return extreme_mean_dur
#%%

first10_pos = extreme_duration_all_members('first10', 'pos')
first10_neg = extreme_duration_all_members('first10', 'neg')
last10_pos = extreme_duration_all_members('last10', 'pos')
last10_neg = extreme_duration_all_members('last10', 'neg')

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
