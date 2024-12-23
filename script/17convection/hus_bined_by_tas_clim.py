# %%
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import cartopy.crs as ccrs
import cartopy
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as mcolors
import os
# %%
def read_data(var, decade):
    time_tag = f"{decade}0501-{decade+9}0930"
    data_path = (
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily_std/"
    )
    files = glob.glob(data_path + "r*i1p1f1/" + f"*{var}*{time_tag}.nc")

    data = xr.open_mfdataset(
        files, combine="nested", concat_dim="ens", chunks={"ens": 1}
    )
    data = data[var]

    # select -30 to 30 lat
    data = data.sel(lat=slice(-30, 30))
    # change longitude from 0-360 to -180-180
    data = data.assign_coords(lon=(data.lon + 180) % 360 - 180).sortby("lon")

    return data

def bin_hus_on_tas(lon_df):

    ts_diff_bins = np.arange(0, 16, 1)
    ts_diff_bins = np.append(ts_diff_bins, np.inf)  # Add an extra bin for >10

    hus_bined = (
        lon_df[["hus"]]
        .groupby(pd.cut(lon_df["tas"], bins=ts_diff_bins), observed=True)
        .mean()
    )
    # add one column called tas_diff, which is the middle value of the bin
    hus_bined["tas_diff"] = hus_bined.index.map(lambda x: x.mid if x.right != np.inf else 16) # 16 is the value for >15
    # make the tas_diff as the index
    hus_bined = hus_bined.set_index("tas_diff")
    return hus_bined


# %%
first_tas = read_data("tas", 1850)
first_hus = read_data("hus", 1850)
first_data = xr.Dataset({"tas": first_tas, "hus": first_hus})
first_df = first_data.to_dataframe()[["tas", "hus"]]

# %%

last_tas = read_data("tas", 2090)
last_hus = read_data("hus", 2090)
last_data = xr.Dataset({"tas": last_tas, "hus": last_hus})
last_df = last_data.to_dataframe()[["tas", "hus"]]


#%%

# %%
try:
    first_tas_95 = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_hur_variability/first_tas_95.csv")
except FileNotFoundError:
    first_tas_95 = first_df.groupby("lon").quantile(0.95).reset_index()
    first_tas_95.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_hur_variability/first_tas_95.csv", index=False)

try:
    last_tas_95 = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_hur_variability/last_tas_95.csv")
except FileNotFoundError:
    last_tas_95 = last_df.groupby("lon").quantile(0.95).reset_index()
    last_tas_95.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_hur_variability/last_tas_95.csv", index=False)
    

#%%
try:
    first_hus_bined = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_hur_variability/first_hus_bined.csv")
    last_hus_bined = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_hur_variability/last_hus_bined.csv")

except FileNotFoundError:
    first_hus_bined = first_df.groupby("lon").apply(bin_hus_on_tas).reset_index()
    last_hus_bined = last_df.groupby("lon").apply(bin_hus_on_tas).reset_index()
    first_hus_bined.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_hur_variability/first_hus_bined.csv", index=False)
    last_hus_bined.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_hur_variability/last_hus_bined.csv", index=False)

diff_hus_bined = last_hus_bined - first_hus_bined
# %%
# Reset index to convert MultiIndex to columns
first_hus_bined = first_hus_bined.reset_index()
last_hus_bined = last_hus_bined.reset_index()
diff_hus_bined = diff_hus_bined.reset_index()
# %%
first_hus_bined_plot = first_hus_bined.set_index(["tas_diff", "lon"]).to_xarray().hus
last_hus_bined_plot = last_hus_bined.set_index(["tas_diff", "lon"]).to_xarray().hus
diff_hus_bined_plot = diff_hus_bined.set_index(["tas_diff", "lon"]).to_xarray().hus

# %%
# change the 'tas_diff' to 'lat'
first_hus_bined_plot = first_hus_bined_plot.rename({"tas_diff": "lat"})
last_hus_bined_plot = last_hus_bined_plot.rename({"tas_diff": "lat"})
diff_hus_bined_plot = diff_hus_bined_plot.rename({"tas_diff": "lat"})
# %%
# value of 'lat' is multiplied by  3
first_hus_bined_plot["lat"] = first_hus_bined_plot["lat"] * 6
last_hus_bined_plot["lat"] = last_hus_bined_plot["lat"] * 6
diff_hus_bined_plot["lat"] = diff_hus_bined_plot["lat"] * 6
#%%
# change unit from 1 to g/kg
first_hus_bined_plot = first_hus_bined_plot * 1000
last_hus_bined_plot = last_hus_bined_plot * 1000
diff_hus_bined_plot = diff_hus_bined_plot * 1000
# %%
fig = plt.figure(figsize=(15, 10))

gs = fig.add_gridspec(4, 2, width_ratios=[50, 1], wspace=0.1)

axes = np.array(
    [
        [fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree(100)), fig.add_subplot(gs[0, 1])],  
        [fig.add_subplot(gs[1, 0], projection=ccrs.PlateCarree(100)), fig.add_subplot(gs[1, 1])],
        [fig.add_subplot(gs[2, 0], projection=ccrs.PlateCarree(100)), fig.add_subplot(gs[2, 1])],
        [fig.add_subplot(gs[3, 0], projection=ccrs.PlateCarree(100)), None],
    ]
)
seq_data_in_the_txt_file = np.loadtxt("/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_seq.txt")
div_data_in_the_txt_file = np.loadtxt("/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_div.txt")
#create the colormap
seq_prec_cm = mcolors.LinearSegmentedColormap.from_list('colormap', seq_data_in_the_txt_file)
div_prec_cm = mcolors.LinearSegmentedColormap.from_list('colormap', div_data_in_the_txt_file)

y_tick_labels = np.arange(0.5, 15, 1)
# add 11 at the end
y_tick_labels = np.append(y_tick_labels, '>15')

first_plot = first_hus_bined_plot.plot(
    ax=axes[0, 0],
    cmap=seq_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(0, 6, 0.5),
    extend="max",
    add_colorbar=False,
)
axes[0, 0].set_title("1850-1859")
axes[0, 0].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[0, 0].set_yticks(np.arange(0, 80, 5) + 2)
axes[0, 0].set_yticklabels(y_tick_labels)
axes[0, 0].set_ylabel("tas_diff")

axes[0,0].plot(first_tas_95.lon, first_tas_95.tas, color="black", linestyle="--", label="95% quantile")


fig.colorbar(first_plot, cax=axes[0, 1], orientation="vertical")
axes[0,1].set_ylabel("g/kg")


last_plot = last_hus_bined_plot.plot(
    ax=axes[1, 0],
    cmap=seq_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(0, 6, 0.5),
    extend="max",
    add_colorbar=False,
)
axes[1, 0].set_title("2090-2099")
axes[1, 0].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[1, 0].set_yticks(np.arange(0, 80, 5) + 2)
axes[1, 0].set_yticklabels(y_tick_labels)
axes[1, 0].set_ylabel("tas_diff")
axes[1,0].plot(last_tas_95.lon, last_tas_95.tas, color="black", linestyle="--", label="95% quantile")

fig.colorbar(last_plot, cax=axes[1, 1], orientation="vertical")
axes[1,1].set_ylabel("g/kg")

diff_plot = diff_hus_bined_plot.plot(
    ax=axes[2, 0],
    cmap=div_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(-2, 2.1, 0.2),
    extend="both",
    add_colorbar=False,
)
axes[2, 0].set_title("2090-2099 - 1850-1859")
axes[2, 0].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[2, 0].set_yticks(np.arange(0, 80, 5) + 2)
axes[2, 0].set_yticklabels(y_tick_labels)
axes[2, 0].set_ylabel("tas_diff")
fig.colorbar(diff_plot, cax=axes[2, 1], orientation="vertical")
axes[2,1].set_ylabel("g/kg")

axes[3, 0].coastlines()
# add ocean 
axes[3, 0].add_feature(cartopy.feature.OCEAN)
axes[3, 0].set_extent([-180, 180, -30, 30], crs=ccrs.PlateCarree())
axes[3, 0].set_yticks(np.arange(-30, 31, 10))
axes[3, 0].set_xlabel("lon")
axes[3, 0].set_ylabel("lat")
# add xticks and labels
axes[3, 0].set_xticks(np.arange(-180, 181, 60))

# Make the axes[3,0] smaller with a ratio compared to axes[0,0] and axes[1,0]
box = axes[3, 0].get_position()
axes[3, 0].set_position([axes[0,0].get_position().x0, box.y0, box.width * 0.78, box.height * 0.78])



plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/hus_bined_by_tas_clim.png")


# %%
