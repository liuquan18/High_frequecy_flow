# %%
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
from xhistogram.xarray import histogram
import cartopy.crs as ccrs
import cartopy


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

    ts_diff_bins = np.arange(0, 11, 1)

    hus_bined = (
        lon_df[["hus"]]
        .groupby(pd.cut(lon_df["tas"], bins=ts_diff_bins), observed=True)
        .mean()
    )
    # add one column called tas_diff, which is the middle value of the bin
    hus_bined["tas_diff"] = hus_bined.index.map(lambda x: x.mid)
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

# %%
first_hus_bined = first_df.groupby("lon").apply(bin_hus_on_tas)

last_hus_bined = last_df.groupby("lon").apply(bin_hus_on_tas)

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
# %%
fig, axes = plt.subplots(
    4,
    1,
    figsize=(15, 10),
    subplot_kw={"projection": ccrs.PlateCarree(100)},
    sharex=True,
    sharey=False,
)

y_tick_labels = np.arange(0.5, 10, 1)

first_hus_bined_plot.plot(
    ax=axes[0],
    cmap="viridis",
    transform=ccrs.PlateCarree(),
    levels=np.arange(0, 30, 1),
    extend="max",
)
axes[0].set_title("1850-1859")
axes[0].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
# y-tick labels is divided by 6
axes[0].set_yticks(np.arange(0, 60, 6) + 3)
axes[0].set_yticklabels(y_tick_labels)
axes[0].set_ylabel("tas_diff")


last_hus_bined_plot.plot(
    ax=axes[1],
    cmap="viridis",
    transform=ccrs.PlateCarree(),
    levels=np.arange(0, 30, 1),
    extend="max",
)
axes[1].set_title("2090-2099")
axes[1].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[1].set_yticks(np.arange(0, 60, 6) + 3)
axes[1].set_yticklabels(y_tick_labels)
axes[1].set_ylabel("tas_diff")

diff_hus_bined_plot.plot(
    ax=axes[2],
    cmap="RdBu",
    transform=ccrs.PlateCarree(),
    levels=np.arange(-10, 11, 1),
    extend="max",
)
axes[2].set_title("2090-2099 - 1850-1859")
axes[2].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[2].set_yticks(np.arange(0, 60, 6) + 3)
axes[2].set_yticklabels(y_tick_labels)
axes[2].set_ylabel("tas_diff")


first_tas.isel(time=0, ens=0).plot(
    ax=axes[3], transform=ccrs.PlateCarree(), cmap="gray", add_colorbar=True
)

axes[3].coastlines()
axes[3].set_extent([-180, 180, -30, 30], crs=ccrs.PlateCarree())
# tick labels
axes[3].set_xticks(np.arange(-180, 180, 60))
axes[3].set_yticks(np.arange(-30, 30, 10))
axes[3].set_xlabel("lon")
axes[3].set_ylabel("lat")

plt.tight_layout()
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/quick_compare.png")

# chagne the ratio of each subplot

# %%
