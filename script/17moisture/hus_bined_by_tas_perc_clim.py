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
import geopandas as gpd

# %%


def bin_hus_on_tas(lon_df):
    # Calculate the percentiles
    percentiles = np.arange(0, 105, 5)
    tas_percent_labeliles = np.percentile(lon_df["tas"], percentiles)

    hus_bined = (
        lon_df[["hus"]]
        .groupby(pd.cut(lon_df["tas"], bins=tas_percent_labeliles, include_lowest=True), observed=True)
        .mean()
    )
    # add one column called tas_percent_label, which is the percentile value (0, 5, 10, ..., 100)
    hus_bined["tas_percent"] = percentiles[:-1] + 2.5  # middle of each bin
    # make the tas_percent_label as the index
    hus_bined = hus_bined.set_index("tas_percent_label")
    # add one column called tas_percent_label_label, which is the percentile value (0, 5, 10, ..., 100)
    hus_bined["tas_percent"] = percentiles[:-1]
    # make the tas_percent_label_label as the index
    hus_bined = hus_bined.set_index("tas_percent")
    return hus_bined

# %%
first_tas = read_data("tas", 1850, (0, 60), meridional_mean=False)
first_hus = read_data("hus", 1850, (0, 60), meridional_mean=False)
first_data = xr.Dataset({"tas": first_tas, "hus": first_hus})
first_df = first_data.to_dataframe()[["tas", "hus"]]

# %%

last_tas = read_data("tas", 2090, (0, 60), meridional_mean=False)
last_hus = read_data("hus", 2090, (0, 60), meridional_mean=False)
last_data = xr.Dataset({"tas": last_tas, "hus": last_hus})
last_df = last_data.to_dataframe()[["tas", "hus"]]


# %%
first_hus_bined = first_df.groupby("lon").apply(bin_hus_on_tas)
last_hus_bined = last_df.groupby("lon").apply(bin_hus_on_tas)

# %%
diff_hus_bined = last_hus_bined - first_hus_bined
first_hus_bined = first_hus_bined.reset_index()
last_hus_bined = last_hus_bined.reset_index()
diff_hus_bined = diff_hus_bined.reset_index()


#%%
# %%
def to_plot_data(df, var):
    # create fake 'lat' dimension to align with coastlines.
    df = df.reset_index()
    df = df.set_index(["tas_percent", "lon"]).to_xarray()[var]
    df = df.rename({"tas_percent": "lat"})
    df["lat"] = df["lat"]/2
    df = df * 1000
    return df
# %%
first_hus_bined_plot = to_plot_data(first_hus_bined, "hus")
last_hus_bined_plot = to_plot_data(last_hus_bined, "hus")
diff_hus_bined_plot = to_plot_data(diff_hus_bined, "hus")
#%%

# # %%
# first_tas.load()
# last_tas.load()
# # %%
# first_tas_05 = first_tas.groupby("lon").quantile(0.05, dim=("ens", "time"))
# last_tas_05 = last_tas.groupby("lon").quantile(0.05, dim=("ens", "time"))
# %%
# save the 95th percentile of tas for plotting
# first_tas_05.to_netcdf(
#     "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_tas_95.nc"
# )
# last_tas_05.to_netcdf(
#     "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_tas_95.nc"
# )
# # %%
# first_tas_95_plot = first_tas_05 * 6
# last_tas_95_plot = last_tas_05 * 6
# %%
fig = plt.figure(figsize=(10, 8))

gs = fig.add_gridspec(4, 2, width_ratios=[50, 1], wspace=0.1)

axes = np.array(
    [
        [
            fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree(100)),
            fig.add_subplot(gs[0, 1]),
        ],
        [
            fig.add_subplot(gs[1, 0], projection=ccrs.PlateCarree(100)),
            fig.add_subplot(gs[1, 1]),
        ],
        [
            fig.add_subplot(gs[2, 0], projection=ccrs.PlateCarree(100)),
            fig.add_subplot(gs[2, 1]),
        ],
    ]
)
seq_data_in_the_txt_file = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_seq.txt"
)
div_data_in_the_txt_file = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_div.txt"
)
# create the colormap
seq_prec_cm = mcolors.LinearSegmentedColormap.from_list(
    "colormap", seq_data_in_the_txt_file
)
div_prec_cm = mcolors.LinearSegmentedColormap.from_list(
    "colormap", div_data_in_the_txt_file
)



first_plot = first_hus_bined_plot.plot(
    ax=axes[0, 0],
    cmap=seq_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(0, 4.1, 0.2),
    extend="max",
    add_colorbar=False,
)


axes[0, 0].set_title("1850-1859")
axes[0, 0].set_extent([-180, 180, 0, 50], crs=ccrs.PlateCarree())


axes[0, 0].set_ylabel("tas_percent  (%)")


fig.colorbar(first_plot, cax=axes[0, 1])
axes[0, 1].set_ylabel("hus (g/kg)")


last_plot = last_hus_bined_plot.plot(
    ax=axes[1, 0],
    cmap=seq_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(0, 4.1, 0.2),
    extend="max",
    add_colorbar=False,
)

axes[1, 0].set_title("2090-2099")
axes[1, 0].set_extent([-180, 180, 0, 50], crs=ccrs.PlateCarree())

axes[1, 0].set_ylabel("tas_percent (%)")


fig.colorbar(last_plot, cax=axes[1, 1])
axes[1, 1].set_ylabel("hus (g/kg)")

diff_plot = diff_hus_bined_plot.plot(
    ax=axes[2, 0],
    cmap=div_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(-1.5, 1.55, 0.1),
    extend="both",
    add_colorbar=False,
)
axes[2, 0].set_title("2090-2099 - 1850-1859")

axes[2, 0].set_ylabel("tas_percent (%)")
fig.colorbar(diff_plot, cax=axes[2, 1],)
axes[2, 1].set_ylabel("hus (g/kg)")

for ax in axes[:3, 0]:
    # ax.set_ylim(0, 100)
    ax.set_aspect(1.5)
    ax.set_yticks(np.arange(0, 51, 10))
    ax.set_yticklabels(np.arange(0, 110, 20))

axes[2, 0].set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())
axes[2, 0].set_xticklabels(["180W", "120W", "60W", "0", "60E", "120E"])



plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/hus_bined_by_tasPerc_clim_nomeridmean_0-60.png")
# %%
