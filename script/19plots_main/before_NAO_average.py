# %%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import logging
import cartopy.crs as ccrs
import matplotlib.colors as mcolors
import cartopy.feature as cfeature

idx = pd.IndexSlice
logging.basicConfig(level=logging.INFO)


# %%
def var_before_NAO(var, decade, phase):
    file_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_NAO_{phase}/{var}_NAO_{phase}_{decade}.csv"
    data = pd.read_csv(file_path, index_col=[0, 1])
    return data


def read_data(var):
    first_NAO_pos = var_before_NAO(var, 1850, "pos")
    first_NAO_neg = var_before_NAO(var, 1850, "neg")

    last_NAO_pos = var_before_NAO(var, 2090, "pos")
    last_NAO_neg = var_before_NAO(var, 2090, "neg")

    return first_NAO_pos, first_NAO_neg, last_NAO_pos, last_NAO_neg


# %%
def event_mean(df, name="ratio"):
    df_weight = df["extreme_duration"]

    all_columns = df.columns
    value_columns = all_columns.difference(
        ["event_id", "ens", "lon", "extreme_duration", "extreme_start_time"]
    )

    df_values = df[value_columns]

    df_values_weighted = df_values.multiply(df_weight, axis=0)
    df_values_weighted_mean = df_values_weighted.sum(axis=0) / df_weight.sum()

    df_values_weighted_mean = df_values_weighted_mean.to_frame(name=name)
    df_values_weighted_mean = df_values_weighted_mean.reset_index().rename(
        columns={"index": "lag"}
    )

    df_values_weighted_mean["lag"] = df_values_weighted_mean["lag"].astype(int)

    df_values_weighted_mean = df_values_weighted_mean.sort_values(by="lag")

    return df_values_weighted_mean


# %%
# basin mean util function
def zonal_mean(df):

    all_columns = df.columns
    value_columns = all_columns.difference(
        ["event_id", "ens", "lon", "extreme_duration", "extreme_start_time"]
    )

    # mean over selected lons
    df_zonmean = df.groupby(["event_id", "ens"])[value_columns].mean()

    # id info
    df_id = df.groupby(["event_id", "ens"])[
        ["extreme_duration", "extreme_start_time"]
    ].first()

    # merge
    df_final = pd.merge(df_id, df_zonmean, on=["event_id", "ens"], how="inner")

    df_final = df_final.reset_index().set_index("event_id")
    df_final.index.name = None

    return df_final


# %%
# hus_tas_ratio basin mean
def ratio_basin_mean(ratio):

    box_NAL = [-70, -30, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Atlantic
    box_NPC = [140, -145, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Pacific

    ratio = ratio.reset_index()
    ratio = ratio.rename(columns={"level_0": "event_id"})

    # sel lon
    ratio_NAL = ratio.loc[(ratio["lon"] >= box_NAL[0]) & (ratio["lon"] <= box_NAL[1])]
    ratio_NAL_zonmean = zonal_mean(ratio_NAL)

    ratio_NPC = ratio.loc[
        (ratio["lon"] >= box_NPC[0]) & (ratio["lon"] <= 180)
        | (ratio["lon"] >= -180) & (ratio["lon"] <= box_NPC[1])
    ]
    ratio_NPC_zonmean = zonal_mean(ratio_NPC)

    return ratio_NAL_zonmean, ratio_NPC_zonmean


# %%
def upvp_NA_mean(upvp):
    upvp = upvp.reset_index()
    upvp = upvp.rename(columns={"level_0": "event_id"})

    upvp_NA = upvp.loc[(upvp["lon"] >= -100) & (upvp["lon"] <= -10)]
    upvp_NA_zonmean = zonal_mean(upvp_NA)

    upvp_NA_eventmean = event_mean(upvp_NA_zonmean, name="upvp")

    return upvp_NA_eventmean


# %%
def eke_lag_lon(first, last):

    first = first.reset_index()
    first = first.rename(columns={"level_0": "event_id"})

    last = last.reset_index()
    last = last.rename(columns={"level_0": "event_id"})

    first_eventmean = first.groupby("lon")[first.columns].apply(event_mean, name="eke")
    last_eventmean = last.groupby("lon")[last.columns].apply(event_mean, name="eke")

    # drop level 1, the same as 'lag'
    first_eventmean = first_eventmean.droplevel(1)
    last_eventmean = last_eventmean.droplevel(1)

    first_eventmean = first_eventmean.reset_index()
    last_eventmean = last_eventmean.reset_index()

    eke_eventmean = first_eventmean.merge(
        last_eventmean, on=("lon", "lag"), suffixes=("_first", "_last")
    )

    eke_eventmean["eke_diff"] = eke_eventmean["eke_last"] - eke_eventmean["eke_first"]

    eke_eventmean = eke_eventmean.set_index(["lon", "lag"])

    eke_eventmean_xr = eke_eventmean.to_xarray()

    return eke_eventmean_xr


# %%
def remove_zonalmean(eke):
    zonal_mean = eke.mean(dim="lon")
    eke = eke - zonal_mean
    return eke


# %%
def to_plot_data(eke):
    eke = eke.rename({"lag": "lat"})  # fake lat to plot correctly the lon
    eke["lat"] = eke["lat"] * 4  # fake lat to plot correctly the lon
    # Solve the problem on 180 longitude by extending the data
    eke = eke.reindex(lon=np.append(eke.lon.values, 180), method="nearest")
    lon_values = eke.lon.values
    lon_values[-1] = 180
    eke["lon"] = lon_values

    return eke


# %%
def rolling(eke, lon_win=25, lat_win=3):
    extended_eke = xr.concat([eke, eke], dim="lon")
    eke_rolling = extended_eke.rolling(lon=lon_win, lat=lat_win).mean()

    original_lonsize = eke.lon.size
    eke_rolling = eke_rolling.isel(lon=slice(original_lonsize, 2 * original_lonsize))
    return eke_rolling.sortby("lon")


# %%
first_NAO_pos_eke, first_NAO_neg_eke, last_NAO_pos_eke, last_NAO_neg_eke = read_data(
    "eke"
)
first_NAO_pos_upvp, first_NAO_neg_upvp, last_NAO_pos_upvp, last_NAO_neg_upvp = (
    read_data("upvp")
)
first_NAO_pos_ratio, first_NAO_neg_ratio, last_NAO_pos_ratio, last_NAO_neg_ratio = (
    read_data("hus_tas_ratio")
)
# %%
# ratio
first_NAO_pos_ratio_NAL, first_NAO_pos_ratio_NPC = ratio_basin_mean(first_NAO_pos_ratio)
first_NAO_neg_ratio_NAL, first_NAO_neg_ratio_NPC = ratio_basin_mean(first_NAO_neg_ratio)

last_NAO_pos_ratio_NAL, last_NAO_pos_ratio_NPC = ratio_basin_mean(last_NAO_pos_ratio)
last_NAO_neg_ratio_NAL, last_NAO_neg_ratio_NPC = ratio_basin_mean(last_NAO_neg_ratio)

first_NAO_pos_ratio_NAL = event_mean(first_NAO_pos_ratio_NAL, "ratio")
first_NAO_pos_ratio_NPC = event_mean(first_NAO_pos_ratio_NPC, "ratio")

first_NAO_neg_ratio_NAL = event_mean(first_NAO_neg_ratio_NAL, "ratio")
first_NAO_neg_ratio_NPC = event_mean(first_NAO_neg_ratio_NPC, "ratio")

last_NAO_pos_ratio_NAL = event_mean(last_NAO_pos_ratio_NAL, "ratio")
last_NAO_pos_ratio_NPC = event_mean(last_NAO_pos_ratio_NPC, "ratio")

last_NAO_neg_ratio_NAL = event_mean(last_NAO_neg_ratio_NAL, "ratio")
last_NAO_neg_ratio_NPC = event_mean(last_NAO_neg_ratio_NPC, "ratio")


# %%
# eke
NAO_pos_eke_lag_lon = eke_lag_lon(first_NAO_pos_eke, last_NAO_pos_eke)
NAO_neg_eke_lag_lon = eke_lag_lon(first_NAO_neg_eke, last_NAO_neg_eke)
# %%
NAO_pos_eke_lag_lon = remove_zonalmean(NAO_pos_eke_lag_lon)
NAO_neg_eke_lag_lon = remove_zonalmean(NAO_neg_eke_lag_lon)
# %%
# for plotting
NAO_pos_eke_lat_lon = to_plot_data(NAO_pos_eke_lag_lon)
NAO_neg_eke_lat_lon = to_plot_data(NAO_neg_eke_lag_lon)

# %%
# upvp in NA mean
first_NAO_pos_upvp_NA = upvp_NA_mean(first_NAO_pos_upvp)
first_NAO_neg_upvp_NA = upvp_NA_mean(first_NAO_neg_upvp)

last_NAO_pos_upvp_NA = upvp_NA_mean(last_NAO_pos_upvp)
last_NAO_neg_upvp_NA = upvp_NA_mean(last_NAO_neg_upvp)

# %%
# %%
eke_cmap = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/misc_div.txt"
)
eke_cmap = mcolors.ListedColormap(eke_cmap, name="temp_div")


def lon2x(longitude, ax):
    """
    Convert longitude to corresponding x-coordinates.
    """
    x_coord = ax.projection.transform_point(longitude, 0, ccrs.PlateCarree())[0]

    return x_coord


# %%


# %%


eke_smooth = True

if eke_smooth:
    NAO_pos_eke_lat_lon = rolling(NAO_pos_eke_lat_lon)
    NAO_neg_eke_lat_lon = rolling(NAO_neg_eke_lat_lon)
# %%

eke_levels = np.arange(-0.6, 0.65, 0.1)

# %%
fig = plt.figure(figsize=(10, 12))

grid = plt.GridSpec(6, 4, height_ratios=[1, 0.2, 1, 1, 1, 0.3], hspace=0)

grid.update(hspace=0.3)
# ratio positive
ratio_ax2 = fig.add_subplot(grid[0, 1])
ratio_ax1 = fig.add_subplot(grid[0, 3])

upvp_ax2 = fig.add_subplot(grid[0, 0])
upvp_ax1 = fig.add_subplot(grid[0, 2])

legend_ax = fig.add_subplot(grid[1, :])

# second row
eke_first_ax2 = fig.add_subplot(grid[2, :2], projection=ccrs.PlateCarree(-90))
eke_first_ax1 = fig.add_subplot(grid[2, 2:], projection=ccrs.PlateCarree(-90))

# third row
eke_last_ax2 = fig.add_subplot(grid[3, :2], projection=ccrs.PlateCarree(-90))
eke_last_ax1 = fig.add_subplot(grid[3, 2:], projection=ccrs.PlateCarree(-90))

# forth row
eke_diff_ax2 = fig.add_subplot(grid[4, :2], projection=ccrs.PlateCarree(-90))
eke_diff_ax1 = fig.add_subplot(grid[4, 2:], projection=ccrs.PlateCarree(-90))

# fifth row
eke_coast_ax = fig.add_subplot(grid[5, :2], projection=ccrs.PlateCarree(-90))

cbar_ax = fig.add_subplot(grid[5, 2:])


ratio_ax1.plot(
    first_NAO_pos_ratio_NAL["ratio"],
    first_NAO_pos_ratio_NAL["lag"],
    label="first_NAL",
    color=sns.color_palette("Paired")[0],
    linewidth=2,
)
ratio_ax1.plot(
    last_NAO_pos_ratio_NAL["ratio"],
    last_NAO_pos_ratio_NAL["lag"],
    label="last_NAL",
    color=sns.color_palette("Paired")[1],
    linewidth=2,
)

ratio_ax1.plot(
    first_NAO_pos_ratio_NPC["ratio"],
    first_NAO_pos_ratio_NPC["lag"],
    label="first_NPC",
    color=sns.color_palette("Paired")[0],
    linestyle="--",
    linewidth=2,
)

ratio_ax1.plot(
    last_NAO_pos_ratio_NPC["ratio"],
    last_NAO_pos_ratio_NPC["lag"],
    label="last_NPC",
    color=sns.color_palette("Paired")[1],
    linestyle="--",
    linewidth=2,
)

# upvp positive
upvp_ax1.plot(
    first_NAO_pos_upvp_NA["upvp"],
    first_NAO_pos_upvp_NA["lag"],
    label="first",
    color=sns.color_palette("Paired")[2],
    linewidth=2,
)

upvp_ax1.plot(
    last_NAO_pos_upvp_NA["upvp"],
    last_NAO_pos_upvp_NA["lag"],
    label="last",
    color=sns.color_palette("Paired")[3],
    linewidth=2,
)


# eke first positive

NAO_pos_eke_lat_lon["eke_first"].T.plot.contourf(
    x="lon",
    y="lat",
    ax=eke_first_ax1,
    transform=ccrs.PlateCarree(),
    cmap=eke_cmap,
    levels=eke_levels,
    add_colorbar=False,
)
# eke_first_ax1.set_aspect(2)
eke_first_ax1.set_yticks(np.arange(-20, 10, 5) * 4)
eke_first_ax1.set_yticklabels("")
eke_first_ax1.set_ylabel("")

# eke last positive
NAO_pos_eke_lat_lon["eke_last"].T.plot.contourf(
    x="lon",
    y="lat",
    ax=eke_last_ax1,
    transform=ccrs.PlateCarree(),
    cmap=eke_cmap,
    add_colorbar=False,
    levels=eke_levels,
)

# eke_last_ax1.set_aspect(2)
eke_last_ax1.set_yticks(np.arange(-20, 10, 5) * 4)
eke_last_ax1.set_yticklabels("")
eke_last_ax1.set_ylabel("")

# eke diff positive

NAO_pos_eke_lat_lon["eke_diff"].T.plot.contourf(
    x="lon",
    y="lat",
    ax=eke_diff_ax1,
    transform=ccrs.PlateCarree(),
    cmap=eke_cmap,
    add_colorbar=False,
    levels=eke_levels,
)
# eke_diff_ax1.set_aspect(2)
eke_diff_ax1.set_yticks(np.arange(-20, 10, 5) * 4)
eke_diff_ax1.set_yticklabels("")
eke_diff_ax1.set_ylabel("")


# ratio negative

ratio_ax2.plot(
    first_NAO_neg_ratio_NAL["ratio"],
    first_NAO_neg_ratio_NAL["lag"],
    label="first_NAL",
    color=sns.color_palette("Paired")[0],
    linewidth=2,
)
ratio_ax2.plot(
    last_NAO_neg_ratio_NAL["ratio"],
    last_NAO_neg_ratio_NAL["lag"],
    label="last_NAL",
    color=sns.color_palette("Paired")[1],
    linewidth=2,
)

ratio_ax2.plot(
    first_NAO_neg_ratio_NPC["ratio"],
    first_NAO_neg_ratio_NPC["lag"],
    label="first_NPC",
    color=sns.color_palette("Paired")[0],
    linestyle="--",
    linewidth=2,
)

ratio_ax2.plot(
    last_NAO_neg_ratio_NPC["ratio"],
    last_NAO_neg_ratio_NPC["lag"],
    label="last_NPC",
    color=sns.color_palette("Paired")[1],
    linestyle="--",
    linewidth=2,
)

# upvp negative
upvp_ax2.plot(
    first_NAO_neg_upvp_NA["upvp"],
    first_NAO_neg_upvp_NA["lag"],
    label="first",
    color=sns.color_palette("Paired")[2],
    linewidth=2,
)

upvp_ax2.plot(
    last_NAO_neg_upvp_NA["upvp"],
    last_NAO_neg_upvp_NA["lag"],
    label="last",
    color=sns.color_palette("Paired")[3],
    linewidth=2,
)

# eke first negative

NAO_neg_eke_lat_lon["eke_first"].T.plot.contourf(
    x="lon",
    y="lat",
    ax=eke_first_ax2,
    transform=ccrs.PlateCarree(),
    cmap=eke_cmap,
    add_colorbar=False,
    levels=eke_levels,
)
# eke_first_ax2.set_aspect(2)
eke_first_ax2.set_yticks(np.arange(-20, 10, 5) * 4)
eke_first_ax2.set_yticklabels("")
eke_first_ax2.set_ylabel("")

# eke last negative
NAO_neg_eke_lat_lon["eke_last"].T.plot.contourf(
    x="lon",
    y="lat",
    ax=eke_last_ax2,
    transform=ccrs.PlateCarree(),
    cmap=eke_cmap,
    add_colorbar=False,
    levels=eke_levels,
)

# eke_last_ax2.set_aspect(2)
eke_last_ax2.set_yticks(np.arange(-20, 10, 5) * 4)
eke_last_ax2.set_yticklabels("")
eke_last_ax2.set_ylabel("")

# eke diff negative

NAO_neg_eke_lat_lon["eke_diff"].T.plot.contourf(
    x="lon",
    y="lat",
    ax=eke_diff_ax2,
    transform=ccrs.PlateCarree(),
    cmap=eke_cmap,
    add_colorbar=False,
    levels=eke_levels,
)
# eke_diff_ax2.set_aspect(2)
eke_diff_ax2.set_yticks(np.arange(-20, 10, 5) * 4)
eke_diff_ax2.set_yticklabels("")
eke_diff_ax2.set_ylabel("")


upvp_ax1.set_xlim(-2, 15.2)
upvp_ax2.set_xlim(-15.2, 2)


for ax in [
    ratio_ax1,
    ratio_ax2,
    upvp_ax1,
    upvp_ax2,
    eke_diff_ax1,
    eke_diff_ax2,
    eke_first_ax1,
    eke_first_ax2,
    eke_last_ax1,
    eke_last_ax2,
]:
    ax.axhline(0, color="black", linewidth=2, linestyle="dotted")

ratio_ax1.set_xlabel(r"$\Delta q / \Delta T$ (g $\cdot$ kg$^{-1}$ $\cdot$ K$^{-1}$)")
upvp_ax1.set_xlabel(r"$u^{'}v^{'}$ (m$^2$ $\cdot$ s$^{-2}$)")


ratio_ax2.set_xlabel(r"$\Delta q / \Delta T$ (g $\cdot$ kg$^{-1}$ $\cdot$ K$^{-1}$)")
upvp_ax2.set_xlabel(r"$u^{'}v^{'}$ (m$^2$ $\cdot$ s$^{-2}$)")

ratio_ax1.set_yticks(np.arange(-20, 11, 5))

for ax in [ratio_ax2, ratio_ax1, upvp_ax1, upvp_ax2]:
    ax.set_yticks(np.arange(-20, 11, 5))
    ax.set_yticklabels("")

for ax in [
    ratio_ax1,
    ratio_ax2,
    upvp_ax1,
    upvp_ax2,
]:

    # remove the top and right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

for ax in [eke_diff_ax1, eke_diff_ax2]:
    ax.set_ylabel("")

for ax in [eke_first_ax2, eke_last_ax2, eke_diff_ax2]:
    ax.set_ylabel("Lag (days)")
    ax.set_yticks(np.arange(-20, 11, 5) * 4)
    ax.set_yticklabels(np.arange(-20, 11, 5))

upvp_ax2.set_yticklabels(np.arange(-20, 11, 5))
upvp_ax2.set_ylabel("Lag (days)")


for ax in [
    eke_first_ax1,
    eke_first_ax2,
    eke_last_ax1,
    eke_last_ax2,
]:
    ax.set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels("")
    ax.set_xlabel("")

for ax in [eke_diff_ax1, eke_diff_ax2]:
    ax.set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels(["180W", "120W", "60W", "0", "60E", "120E"])
    ax.set_xlabel("")

eke_first_ax1.set_title("1850-1859 pos")
eke_last_ax1.set_title("2090-2099 pos")

eke_first_ax2.set_title("1850-1859 neg")
eke_last_ax2.set_title("2090-2099 neg")

eke_diff_ax1.set_title("2090-2099 - 1850-1859 pos")
eke_diff_ax2.set_title("2090-2099 - 1850-1859 neg")

row2 = [eke_first_ax1, eke_first_ax2]
row3 = [eke_last_ax1, eke_last_ax2]
row4 = [eke_diff_ax1, eke_diff_ax2]

# Adjust positions
for ax in row2:
    pos = ax.get_position()
    ax.set_position(
        [pos.x0, pos.y0 - 0.04, pos.width, pos.height]
    )  # Move second row down slightly

for ax in row3:
    pos = ax.get_position()
    ax.set_position(
        [pos.x0, pos.y0 - 0.02, pos.width, pos.height]
    )  # Move third row down less

for ax in row4:
    pos = ax.get_position()
    ax.set_position(
        [pos.x0, pos.y0, pos.width, pos.height]
    )  # Move fourth row down less


# add custom legend for ratio_ax1
handles_ratio, labels = ratio_ax1.get_legend_handles_labels()

labels = [
    r"$\Delta q / \Delta T$ _first_NAL",
    r"$\Delta q / \Delta T$_last_NAL",
    r"$\Delta q / \Delta T$ _first_NPC",
    r"$\Delta q / \Delta T$ _last_NPC",
]
# add legend of upvp to legend_ax
handles_upvp, labels_upvp = upvp_ax1.get_legend_handles_labels()
labels_upvp = ["$u^{'}v^{'}$ _first", "$u^{'}v^{'}$ _last"]

handles_together = handles_ratio + handles_upvp
labels_together = labels + labels_upvp

legend_ax.legend(handles_together, labels_together, loc="center", frameon=False, ncol=4)
legend_ax.axis("off")
legend_pos = legend_ax.get_position()
legend_ax.set_position(
    [legend_pos.x0, legend_pos.y0 - 0.04, legend_pos.width, legend_pos.height]
)

# add colorbar of eke
cbar = plt.colorbar(
    mappable=eke_diff_ax1.collections[0],
    cax=cbar_ax,
    orientation="horizontal",
    aspect=30,
    label=r"EKE (m$^2$ s$^{-2}$)",
)
cbar_ax.set_aspect(0.05)

# eke region
eke_coast_ax.coastlines()
eke_coast_ax.set_extent([-180, 180, 20, 60], crs=ccrs.PlateCarree())
# add ocean feature
eke_coast_ax.add_feature(
    cfeature.NaturalEarthFeature(
        "physical", "ocean", "50m", edgecolor="face", facecolor="lightblue"
    )
)
# set the position of the ax
pos1 = eke_diff_ax2.get_position()
eke_coast_ax.set_position([pos1.x0, pos1.y0 - 0.36, pos1.width, pos1.width * 1.5])


# vline at lon = [-70, -30] and [140, -145]
eke_coast_ax.axvline(
    lon2x(-70, eke_coast_ax), color="black", linewidth=1.5, linestyle="dotted"
)
eke_coast_ax.axvline(
    lon2x(-30, eke_coast_ax), color="black", linewidth=1.5, linestyle="dotted"
)
eke_coast_ax.axvline(
    lon2x(140, eke_coast_ax), color="black", linewidth=1.5, linestyle="dotted"
)
eke_coast_ax.axvline(
    lon2x(-145, eke_coast_ax), color="black", linewidth=1.5, linestyle="dotted"
)


# add tilted line for eke eke_first_ax1 from  120E to 60E
eke_first_ax1.plot(
    [lon2x(180, eke_first_ax1), lon2x(60, eke_first_ax1)],
    [-15.5 * 4, -5.5 * 4],
    color="black",
    linestyle=(0, (5, 10)),
    linewidth=1.2,
)

eke_last_ax1.plot(
    [lon2x(120, eke_first_ax1), lon2x(60, eke_first_ax1)],
    [-15.5 * 4, -5.5 * 4],
    color="black",
    linestyle=(0, (5, 10)),
    linewidth=1.2,
)

# add text 'NPC' between 140 and -145, NAL between -70 and -30
eke_coast_ax.text(lon2x(-65.0, eke_coast_ax), 30, "NAL", fontsize=12)
eke_coast_ax.text(lon2x(145.0, eke_coast_ax), 30, "NPC", fontsize=12)
# add a,b,c,d
upvp_ax2.text(
    -0.1, 1.05, "a", transform=upvp_ax2.transAxes, fontsize=12, fontweight="bold"
)
ratio_ax2.text(
    -0.1, 1.05, "b", transform=ratio_ax2.transAxes, fontsize=12, fontweight="bold"
)
upvp_ax1.text(
    -0.1, 1.05, "c", transform=upvp_ax1.transAxes, fontsize=12, fontweight="bold"
)
ratio_ax1.text(
    -0.1, 1.05, "d", transform=ratio_ax1.transAxes, fontsize=12, fontweight="bold"
)

eke_first_ax2.text(
    0.0, 1.05, "e", transform=eke_first_ax2.transAxes, fontsize=12, fontweight="bold"
)
eke_first_ax1.text(
    0.0, 1.05, "f", transform=eke_first_ax1.transAxes, fontsize=12, fontweight="bold"
)
eke_last_ax2.text(
    0.0, 1.05, "g", transform=eke_last_ax2.transAxes, fontsize=12, fontweight="bold"
)
eke_last_ax1.text(
    0.0, 1.05, "h", transform=eke_last_ax1.transAxes, fontsize=12, fontweight="bold"
)
eke_diff_ax2.text(
    0.0, 1.05, "i", transform=eke_diff_ax2.transAxes, fontsize=12, fontweight="bold"
)
eke_diff_ax1.text(
    0.0, 1.05, "j", transform=eke_diff_ax1.transAxes, fontsize=12, fontweight="bold"
)


plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/ratio_eke_together_2060N_500hPa_smooth.pdf",
    dpi=300,
)

# %%
fig = plt.figure(figsize=(10, 12))

grid = plt.GridSpec(6, 4, height_ratios=[1, 0.2, 1, 1, 1, 0.3], hspace=0)

grid.update(hspace=0.3)

# second row
eke_first_ax2 = fig.add_subplot(grid[2, :2], projection=ccrs.PlateCarree(-90))
eke_first_ax1 = fig.add_subplot(grid[2, 2:], projection=ccrs.PlateCarree(-90))

# third row
eke_last_ax2 = fig.add_subplot(grid[3, :2], projection=ccrs.PlateCarree(-90))
eke_last_ax1 = fig.add_subplot(grid[3, 2:], projection=ccrs.PlateCarree(-90))

# forth row
eke_diff_ax2 = fig.add_subplot(grid[4, :2], projection=ccrs.PlateCarree(-90))
eke_diff_ax1 = fig.add_subplot(grid[4, 2:], projection=ccrs.PlateCarree(-90))

# fifth row
eke_coast_ax = fig.add_subplot(grid[5, :2], projection=ccrs.PlateCarree(-90))

cbar_ax = fig.add_subplot(grid[5, 2:])

# eke first positive
NAO_pos_eke_lat_lon["eke_first"].T.plot.contourf(
    x="lon",
    y="lat",
    ax=eke_first_ax1,
    transform=ccrs.PlateCarree(),
    cmap=eke_cmap,
    levels=eke_levels,
    add_colorbar=False,
)
eke_first_ax1.set_yticks(np.arange(-20, 10, 5) * 4)
eke_first_ax1.set_yticklabels("")
eke_first_ax1.set_ylabel("")

# eke last positive
NAO_pos_eke_lat_lon["eke_last"].T.plot.contourf(
    x="lon",
    y="lat",
    ax=eke_last_ax1,
    transform=ccrs.PlateCarree(),
    cmap=eke_cmap,
    add_colorbar=False,
    levels=eke_levels,
)
eke_last_ax1.set_yticks(np.arange(-20, 10, 5) * 4)
eke_last_ax1.set_yticklabels("")
eke_last_ax1.set_ylabel("")

# eke diff positive
NAO_pos_eke_lat_lon["eke_diff"].T.plot.contourf(
    x="lon",
    y="lat",
    ax=eke_diff_ax1,
    transform=ccrs.PlateCarree(),
    cmap=eke_cmap,
    add_colorbar=False,
    levels=eke_levels,
)
eke_diff_ax1.set_yticks(np.arange(-20, 10, 5) * 4)
eke_diff_ax1.set_yticklabels("")
eke_diff_ax1.set_ylabel("")

# eke first negative
NAO_neg_eke_lat_lon["eke_first"].T.plot.contourf(
    x="lon",
    y="lat",
    ax=eke_first_ax2,
    transform=ccrs.PlateCarree(),
    cmap=eke_cmap,
    add_colorbar=False,
    levels=eke_levels,
)
eke_first_ax2.set_yticks(np.arange(-20, 10, 5) * 4)
eke_first_ax2.set_yticklabels("")
eke_first_ax2.set_ylabel("")

# eke last negative
NAO_neg_eke_lat_lon["eke_last"].T.plot.contourf(
    x="lon",
    y="lat",
    ax=eke_last_ax2,
    transform=ccrs.PlateCarree(),
    cmap=eke_cmap,
    add_colorbar=False,
    levels=eke_levels,
)
eke_last_ax2.set_yticks(np.arange(-20, 10, 5) * 4)
eke_last_ax2.set_yticklabels("")
eke_last_ax2.set_ylabel("")

# eke diff negative
NAO_neg_eke_lat_lon["eke_diff"].T.plot.contourf(
    x="lon",
    y="lat",
    ax=eke_diff_ax2,
    transform=ccrs.PlateCarree(),
    cmap=eke_cmap,
    add_colorbar=False,
    levels=eke_levels,
)
eke_diff_ax2.set_yticks(np.arange(-20, 10, 5) * 4)
eke_diff_ax2.set_yticklabels("")
eke_diff_ax2.set_ylabel("")

for ax in [
    eke_diff_ax1,
    eke_diff_ax2,
    eke_first_ax1,
    eke_first_ax2,
    eke_last_ax1,
    eke_last_ax2,
]:
    ax.axhline(0, color="black", linewidth=2, linestyle="dotted")

for ax in [eke_diff_ax1, eke_diff_ax2]:
    ax.set_ylabel("")

for ax in [eke_first_ax2, eke_last_ax2, eke_diff_ax2]:
    ax.set_ylabel("Lag (days)")
    ax.set_yticks(np.arange(-20, 11, 5) * 4)
    ax.set_yticklabels(np.arange(-20, 11, 5))

for ax in [
    eke_first_ax1,
    eke_first_ax2,
    eke_last_ax1,
    eke_last_ax2,
]:
    ax.set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels("")
    ax.set_xlabel("")

for ax in [eke_diff_ax1, eke_diff_ax2]:
    ax.set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels(["180W", "120W", "60W", "0", "60E", "120E"])
    ax.set_xlabel("")

eke_first_ax1.set_title("1850-1859 pos")
eke_last_ax1.set_title("2090-2099 pos")

eke_first_ax2.set_title("1850-1859 neg")
eke_last_ax2.set_title("2090-2099 neg")

eke_diff_ax1.set_title("2090-2099 - 1850-1859 pos")
eke_diff_ax2.set_title("2090-2099 - 1850-1859 neg")

row2 = [eke_first_ax1, eke_first_ax2]
row3 = [eke_last_ax1, eke_last_ax2]
row4 = [eke_diff_ax1, eke_diff_ax2]

# Adjust positions
for ax in row2:
    pos = ax.get_position()
    ax.set_position(
        [pos.x0, pos.y0 - 0.04, pos.width, pos.height]
    )  # Move second row down slightly

for ax in row3:
    pos = ax.get_position()
    ax.set_position(
        [pos.x0, pos.y0 - 0.02, pos.width, pos.height]
    )  # Move third row down less

for ax in row4:
    pos = ax.get_position()
    ax.set_position(
        [pos.x0, pos.y0, pos.width, pos.height]
    )  # Move fourth row down less

# add colorbar of eke
cbar = plt.colorbar(
    mappable=eke_diff_ax1.collections[0],
    cax=cbar_ax,
    orientation="horizontal",
    aspect=30,
    label=r"EKE (m$^2$ s$^{-2}$)",
)
cbar_ax.set_aspect(0.05)

# eke region
eke_coast_ax.coastlines()
eke_coast_ax.set_extent([-180, 180, 20, 60], crs=ccrs.PlateCarree())
# add ocean feature
eke_coast_ax.add_feature(
    cfeature.NaturalEarthFeature(
        "physical", "ocean", "50m", edgecolor="face", facecolor="lightblue"
    )
)
# set the position of the ax
pos1 = eke_diff_ax2.get_position()
eke_coast_ax.set_position([pos1.x0, pos1.y0 - 0.36, pos1.width, pos1.width * 1.5])

# vline at lon = [-70, -30] and [140, -145]
eke_coast_ax.axvline(
    lon2x(-70, eke_coast_ax), color="black", linewidth=1.5, linestyle="dotted"
)
eke_coast_ax.axvline(
    lon2x(-30, eke_coast_ax), color="black", linewidth=1.5, linestyle="dotted"
)
eke_coast_ax.axvline(
    lon2x(140, eke_coast_ax), color="black", linewidth=1.5, linestyle="dotted"
)
eke_coast_ax.axvline(
    lon2x(-145, eke_coast_ax), color="black", linewidth=1.5, linestyle="dotted"
)

# add tilted line for eke eke_first_ax1 from  120E to 60E
eke_first_ax1.plot(
    [lon2x(180, eke_first_ax1), lon2x(60, eke_first_ax1)],
    [-15.5 * 4, -5.5 * 4],
    color="black",
    linestyle=(0, (5, 10)),
    linewidth=1.2,
)

eke_last_ax1.plot(
    [lon2x(120, eke_first_ax1), lon2x(60, eke_first_ax1)],
    [-15.5 * 4, -5.5 * 4],
    color="black",
    linestyle=(0, (5, 10)),
    linewidth=1.2,
)

# add text 'NPC' between 140 and -145, NAL between -70 and -30
eke_coast_ax.text(lon2x(-65.0, eke_coast_ax), 30, "NAL", fontsize=12)
eke_coast_ax.text(lon2x(145.0, eke_coast_ax), 30, "NPC", fontsize=12)

# add a,b,c,d
eke_first_ax2.text(
    0.0, 1.05, "a", transform=eke_first_ax2.transAxes, fontsize=12, fontweight="bold"
)
eke_first_ax1.text(
    0.0, 1.05, "b", transform=eke_first_ax1.transAxes, fontsize=12, fontweight="bold"
)
eke_last_ax2.text(
    0.0, 1.05, "c", transform=eke_last_ax2.transAxes, fontsize=12, fontweight="bold"
)
eke_last_ax1.text(
    0.0, 1.05, "d", transform=eke_last_ax1.transAxes, fontsize=12, fontweight="bold"
)
eke_diff_ax2.text(
    0.0, 1.05, "e", transform=eke_diff_ax2.transAxes, fontsize=12, fontweight="bold"
)
eke_diff_ax1.text(
    0.0, 1.05, "f", transform=eke_diff_ax1.transAxes, fontsize=12, fontweight="bold"
)

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/eke_2060N_500hPa_smooth.pdf",
    dpi=300,
)

# %%
