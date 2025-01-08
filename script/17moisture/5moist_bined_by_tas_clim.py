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


def bin_hus_on_tas(lon_df, var="hus"):

    ts_diff_bins = np.arange(0, 16, 0.5)
    ts_diff_bins = np.append(ts_diff_bins, np.inf)  # Add an extra bin for >10

    hus_bined = (
        lon_df[[var]]
        .groupby(pd.cut(lon_df["tas"], bins=ts_diff_bins), observed=True)
        .mean()
    )
    # add one column called tas_diff, which is the middle value of the bin
    hus_bined["tas_diff"] = hus_bined.index.map(
        lambda x: x.mid if x.right != np.inf else 16
    )  # 16 is the value for >15
    # make the tas_diff as the index
    hus_bined = hus_bined.set_index("tas_diff")
    return hus_bined


# %%
first_tas = read_data("tas", 1850, (20, 60), True)
first_hus = read_data("hus", 1850, (20, 60), True)
first_hussat = read_data("hussat", 1850, (20, 60), True)
first_data = xr.Dataset(
    {"tas": first_tas, "hus": first_hus * 1000, "hussat": first_hussat * 1000}
)

# %%

last_tas = read_data("tas", 2090, (20, 60), True)
last_hus = read_data("hus", 2090, (20, 60), True)
last_hussat = read_data("hussat", 2090, (20, 60), True)
last_data = xr.Dataset(
    {"tas": last_tas, "hus": last_hus * 1000, "hussat": last_hussat * 1000}
)

# %%
first_df = first_data.to_dataframe()
last_df = last_data.to_dataframe()

# %%
first_df = first_df.drop(columns=["height"])
last_df = last_df.drop(columns=["height"])

# %%
first_hus_bined = first_df.groupby("lon").apply(bin_hus_on_tas, var="hus")
last_hus_bined = last_df.groupby("lon").apply(bin_hus_on_tas, var="hus")
# %%
first_hussat_bined = first_df.groupby("lon").apply(bin_hus_on_tas, var="hussat")
last_hussat_bined = last_df.groupby("lon").apply(bin_hus_on_tas, var="hussat")

# %%
diff_hus_bined = last_hus_bined - first_hus_bined
first_hus_bined = first_hus_bined.reset_index()
last_hus_bined = last_hus_bined.reset_index()
diff_hus_bined = diff_hus_bined.reset_index()
# %%
# same for hussat
diff_hussat_bined = last_hussat_bined - first_hussat_bined
first_hussat_bined = first_hussat_bined.reset_index()
last_hussat_bined = last_hussat_bined.reset_index()
diff_hussat_bined = diff_hussat_bined.reset_index()


# %%
def to_plot_data(df, var):
    # create fake 'lat' dimension to align with coastlines.
    df = df.reset_index()
    df = df.set_index(["tas_diff", "lon"]).to_xarray()[var]
    df = df.rename({"tas_diff": "lat"})
    df["lat"] = df["lat"] * 6
    return df


# %%
first_hus_bined_plot = to_plot_data(first_hus_bined, "hus")
last_hus_bined_plot = to_plot_data(last_hus_bined, "hus")
diff_hus_bined_plot = to_plot_data(diff_hus_bined, "hus")
# %%
first_hussat_bined_plot = to_plot_data(first_hussat_bined, "hussat")
last_hussat_bined_plot = to_plot_data(last_hussat_bined, "hussat")
diff_hussat_bined_plot = to_plot_data(diff_hussat_bined, "hussat")
# %%
first_tas.load()
last_tas.load()
# %%
first_tas_05 = first_tas.groupby("lon").quantile(0.05, dim=("ens", "time"))
last_tas_05 = last_tas.groupby("lon").quantile(0.05, dim=("ens", "time"))
# %%
# save the 95th percentile of tas for plotting
# first_tas_05.to_netcdf(
#     "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_tas_95.nc"
# )
# last_tas_05.to_netcdf(
#     "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_tas_95.nc"
# )
# %%
# first_tas_05 = xr.open_dataset(
#     "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_tas_95.nc"
# )
# last_tas_05 = xr.open_dataset(
#     "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_tas_95.nc"
# )

# %%
first_tas_95_plot = first_tas_05 * 6
last_tas_95_plot = last_tas_05 * 6
# %%
fig, axes = plt.subplots(
    3, 2, figsize=(11, 5), subplot_kw={"projection": ccrs.PlateCarree(100)}
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

y_tick_labels = np.arange(0, 14, 2)
# add 11 at the end
y_tick_labels = np.append(y_tick_labels, ">15")

# plot hussat
first_hussat_bined_plot.plot(
    ax=axes[0, 0],
    cmap=seq_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(0, 2.6, 0.1) * 2,
    extend="max",
    cbar_kwargs={"shrink": 1.0, "label": r"$\Delta q^*$"},
)
axes[0, 0].set_title("1850-1859")
axes[0, 0].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[0, 0].set_yticks(np.arange(0, 80, 10))
axes[0, 0].set_yticklabels(y_tick_labels)
axes[0, 0].set_ylabel("tas_diff (K)")

last_hussat_bined_plot.plot(
    ax=axes[1, 0],
    cmap=seq_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(0, 2.6, 0.1) * 2,
    extend="max",
    cbar_kwargs={"shrink": 1.0, "label": r"$\Delta q^*$"},
)
axes[1, 0].set_title("2090-2099")
axes[1, 0].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[1, 0].set_yticks(np.arange(0, 80, 10))
axes[1, 0].set_yticklabels(y_tick_labels, verticalalignment="center")
axes[1, 0].set_ylabel("tas_diff (K)")

diff_hussat_bined_plot.plot(
    ax=axes[2, 0],
    cmap=div_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(-1, 1.1, 0.1) * 2,
    extend="both",
    cbar_kwargs={"shrink": 1.0, "label": r"$\Delta q^*$"},
)
axes[2, 0].set_title("2090-2099 - 1850-1859")
axes[2, 0].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[2, 0].set_yticks(np.arange(0, 80, 10))
axes[2, 0].set_yticklabels(y_tick_labels)

first_plot = first_hus_bined_plot.plot(
    ax=axes[0, 1],
    cmap=seq_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(0, 2.6, 0.1),
    extend="max",
    cbar_kwargs={"shrink": 1.0, "label": r"$\Delta q$"},
)
first_tas_95_plot.plot(
    color="black",
    label="tas_diff 5th perc",
    linestyle="--",
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
)
axes[0, 1].set_title("1850-1859")
axes[0, 1].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[0, 1].set_yticks(np.arange(0, 80, 10))
axes[0, 1].set_yticklabels(y_tick_labels)

last_plot = last_hus_bined_plot.plot(
    ax=axes[1, 1],
    cmap=seq_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(0, 2.6, 0.1),
    extend="max",
    cbar_kwargs={"shrink": 1.0, "label": r"$\Delta q$"},
)
last_tas_95_plot.plot(
    color="black", linestyle="--", ax=axes[1, 0], transform=ccrs.PlateCarree()
)
axes[1, 1].set_title("2090-2099")
axes[1, 1].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[1, 1].set_yticks(np.arange(0, 80, 10))
axes[1, 1].set_yticklabels(y_tick_labels, verticalalignment="center")

diff_plot = diff_hus_bined_plot.plot(
    ax=axes[2, 1],
    cmap=div_prec_cm,
    transform=ccrs.PlateCarree(),
    levels=np.arange(-1, 1.1, 0.1),
    extend="both",
    cbar_kwargs={"shrink": 1.0, "label": r"$\Delta q$"},
)
axes[2, 1].set_title("2090-2099 - 1850-1859")
axes[2, 1].set_extent([-180, 180, 0, 60], crs=ccrs.PlateCarree())
axes[2, 1].set_yticks(np.arange(0, 80, 10))
axes[2, 1].set_yticklabels(y_tick_labels)

for ax in axes.flatten():
    ax.set_ylim(0, 50)
    ax.set_aspect(1.8)
    ax.set_ylabel(r"$\Delta T$ (K)")

axes[2, 0].set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())
axes[2, 0].set_xticklabels(["180W", "120W", "60W", "0", "60E", "120E"])

axes[2, 1].set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())
axes[2, 1].set_xticklabels(["180W", "120W", "60W", "0", "60E", "120E"])

# add a, b, c, d, e, f
for i, ax in enumerate(axes.flatten()):
    ax.text(
        -0.2,
        1.0,
        chr(97 + i),
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
    )

plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/hus_bined_by_tas_clim_meridmean_0-60.pdf",
    dpi=300,
)
# %%
