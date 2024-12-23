# %%
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import cartopy.crs as ccrs
import cartopy
import matplotlib.colors as mcolors
from src.moisture.longitudinal_contrast import read_data
from src.moisture.plot_utils import draw_box
# %%

def bin_hus_on_tas(lon_df):

    ts_diff_bins = np.arange(0, 16, 0.5)
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
first_tas = read_data("tas", 1850, meridional_mean=True)
first_hus = read_data("hus", 1850, meridional_mean=True)
first_data = xr.Dataset({"tas": first_tas, "hus": first_hus})
first_df = first_data.to_dataframe()[["tas", "hus"]]

# %%

last_tas = read_data("tas", 2090, meridional_mean=True)
last_hus = read_data("hus", 2090, meridional_mean=True)
last_data = xr.Dataset({"tas": last_tas, "hus": last_hus})
last_df = last_data.to_dataframe()[["tas", "hus"]]



# %%
try:
    first_tas_95 = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_tas_95.csv")
except FileNotFoundError:
    first_tas_95 = first_df.groupby("lon").quantile(0.95).reset_index()
    first_tas_95.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_tas_95.csv", index=False)

try:
    last_tas_95 = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_tas_95.csv")
except FileNotFoundError:
    last_tas_95 = last_df.groupby("lon").quantile(0.95).reset_index()
    last_tas_95.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_tas_95.csv", index=False)
    

#%%
try:
    first_hus_bined = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_hus_bined.csv")
    last_hus_bined = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_hus_bined.csv")

except FileNotFoundError:
    first_hus_bined = first_df.groupby("lon").apply(bin_hus_on_tas)
    last_hus_bined = last_df.groupby("lon").apply(bin_hus_on_tas)
    first_hus_bined.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_hus_bined.csv", index=False)
    last_hus_bined.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_hus_bined.csv", index=False)

#%%
diff_hus_bined = last_hus_bined - first_hus_bined
first_hus_bined = first_hus_bined.reset_index()
last_hus_bined = last_hus_bined.reset_index()
diff_hus_bined = diff_hus_bined.reset_index()
# %%
def to_plot_data(df, var):
    # create fake 'lat' dimension to align with coastlines.
    df = df.reset_index()
    df = df.set_index(["tas_diff", "lon"]).to_xarray()[var]
    df = df.rename({"tas_diff": "lat"})
    df["lat"] = df["lat"] * 6
    df = df * 1000
    return df

#%%
first_hus_bined_plot = to_plot_data(first_hus_bined, "hus")
last_hus_bined_plot = to_plot_data(last_hus_bined, "hus")
diff_hus_bined_plot = to_plot_data(diff_hus_bined, "hus")


#%%
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
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/hus_bined_by_tas_clim.png")


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
    levels=np.arange(0, 3.1, 0.1),
    extend="max",
    add_colorbar=False,
)
axes[0, 0].set_title("1850-1859")
axes[0, 0].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[0, 0].set_yticks(np.arange(0, 80, 5) + 2.5)
axes[0, 0].set_yticklabels(y_tick_labels)
axes[0, 0].set_ylabel("tas_diff (K)")
axes[0,0].plot(first_tas_95.lon, first_tas_95.tas, color="black", linestyle="--", label="95% quantile")


fig.colorbar(first_plot, cax=axes[0, 1], orientation="vertical")
axes[0,1].set_ylabel("hus (g/kg)")


last_plot = last_hus_bined_plot.plot(
    ax=axes[1, 0],
    cmap=seq_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(0, 3.1, 0.1),
    extend="max",
    add_colorbar=False,
)
axes[1, 0].set_title("2090-2099")
axes[1, 0].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[1, 0].set_yticks(np.arange(0, 80, 5) + 2.5)
axes[1, 0].set_yticklabels(y_tick_labels, verticalalignment='center')
axes[1, 0].set_ylabel("tas_diff (K)")
axes[1,0].plot(last_tas_95.lon, last_tas_95.tas, color="black", linestyle="--", label="95% quantile")

fig.colorbar(last_plot, cax=axes[1, 1], orientation="vertical")
axes[1,1].set_ylabel("hus (g/kg)")

diff_plot = diff_hus_bined_plot.plot(
    ax=axes[2, 0],
    cmap=div_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(-1, 1.1, 0.1),
    extend="both",
    add_colorbar=False,
)
axes[2, 0].set_title("2090-2099 - 1850-1859")
axes[2, 0].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[2, 0].set_yticks(np.arange(0, 80, 5) + 2.5)
axes[2, 0].set_yticklabels(y_tick_labels)
axes[2, 0].set_ylabel("tas_diff (K)")
fig.colorbar(diff_plot, cax=axes[2, 1], orientation="vertical")
axes[2,1].set_ylabel("hus (g/kg)")

axes[3, 0].coastlines()
# add ocean 
axes[3, 0].add_feature(cartopy.feature.OCEAN)

# draw an example box
ex_base_point = (-60, 10)

draw_box(axes, ex_base_point)


axes[3, 0].set_extent([-180, 180, -30, 30], crs=ccrs.PlateCarree())
axes[3, 0].set_yticks(np.arange(-30, 31, 10))
axes[3, 0].set_xlabel("lon")
axes[3, 0].set_ylabel("lat")
# add xticks and labels
axes[3, 0].set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())
axes[3, 0].set_xticklabels(['180°', '120°W', '60°W', '0°', '60°E', '120°E'])

# Make the axes[3,0] smaller with a ratio compared to axes[0,0] and axes[1,0]
box = axes[3, 0].get_position()
# axes[3, 0].set_position([axes[0,0].get_position().x0, box.y0, axes[0,0].get_position().width, box.height * 1])
axes[3,0].set_aspect(0.8)
for ax in axes[:3,0]:
    ax.set_ylim(0, 35)

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/hus_bined_by_tas_clim_meridmean.png")
# %%
