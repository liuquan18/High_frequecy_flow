# %%
import xarray as xr
import numpy as np
import pandas as pd
import os
import sys
import mpi4py.MPI as MPI
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
import logging
from mpl_toolkits.axes_grid1 import make_axes_locatable

logging.basicConfig(level=logging.warning)
import glob

# %%
from src.extremes.extreme_read import read_extremes_allens

# %%
first10_pos_events, first10_neg_events = read_extremes_allens("first10", 8)
last10_pos_events, last10_neg_events = read_extremes_allens("last10", 8)

# %%
extremes_all = {
    ("first10", "pos"): first10_pos_events,
    ("first10", "neg"): first10_neg_events,
    ("last10", "pos"): last10_pos_events,
    ("last10", "neg"): last10_neg_events,
}


# %%
def composite_times(events, lag_days=6):
    event_start_times = events["event_start_time"]
    field_sel_times = event_start_times - pd.Timedelta(f"{lag_days}D")
    # if the field_sel_times contains value before May 1st, or After September 30th, remove it
    field_sel_times = field_sel_times[
        (field_sel_times.dt.month >= 5) & (field_sel_times.dt.month <= 9)
    ]
    return field_sel_times.values


def composite_mean(field, times):
    field_sel = field.sel(time=times)
    return field_sel.mean(dim="time")


def composite_OLR_events(period, extreme_type, lag_days=6, bandfilter=False):
    OLR_events_lag_concur = []
    extremes = extremes_all[(period, extreme_type)]

    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_reconstructed/{period}_OLR_reconstructed/"
    if bandfilter:
        base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_reconstructed/{period}_OLR_reconstructed_bandfilter/"
    for ens in range(1, 51):
        # read OLR data
        file = f"{base_dir}rlut_day_MPI-ESM1-2-LR_*_r{ens}i1p1f1_gn_*_ano.nc"
        try:
            file = glob.glob(file)[0]
        except IndexError:
            logging.warning(f"Ensemble {ens} not found")

        OLR = xr.open_dataset(file).TP_OLR_reconstructed

        # read events of the ensemble
        extreme_single = extremes[extremes["ens"] == ens]
        if extreme_single.empty:
            continue

        # composite the OLR
        sel_times = composite_times(extreme_single, lag_days=lag_days)
        if sel_times.size == 0:
            continue
        OLR_mean_single = composite_mean(OLR, sel_times)
        OLR_events_lag_concur.append(OLR_mean_single)

    OLR_events_lag_concur = xr.concat(OLR_events_lag_concur, dim="events_id")

    OLR_event_composite = OLR_events_lag_concur.mean(dim="events_id")
    return OLR_event_composite


def plot_composite(field, ax, levels=np.arange(-10, 11, 1)):
    p = field.plot(
        levels=levels,
        transform=ccrs.PlateCarree(),
        add_colorbar=False,
        ax=ax,
        add_labels=False,
        extend="both",
    )
    ax.coastlines()
    return p


# %%
bandpass = False
# %%
# composite analysis with lag ranging from 15 days to 0
print("first10 positive")
first_pos_OLR_lags = [
    composite_OLR_events("first10", "pos", lag_days=i, bandfilter=bandpass)
    for i in range(60)
]
print("first10 negative")
first_neg_OLR_lags = [
    composite_OLR_events("first10", "neg", lag_days=i, bandfilter=bandpass)
    for i in range(60)
]

print("last10 positive")
last_pos_OLR_lags = [
    composite_OLR_events("last10", "pos", lag_days=i, bandfilter=bandpass)
    for i in range(60)
]

print("last10 negative")
last_neg_OLR_lags = [
    composite_OLR_events("last10", "neg", lag_days=i, bandfilter=bandpass)
    for i in range(60)
]

# %%
first_pos_OLR_lags = xr.concat(first_pos_OLR_lags, dim="lag")
first_neg_OLR_lags = xr.concat(first_neg_OLR_lags, dim="lag")
last_pos_OLR_lags = xr.concat(last_pos_OLR_lags, dim="lag")
last_neg_OLR_lags = xr.concat(last_neg_OLR_lags, dim="lag")

# %%
# coordinate for the lags
first_pos_OLR_lags["lag"] = np.arange(60)
first_neg_OLR_lags["lag"] = np.arange(60)
last_pos_OLR_lags["lag"] = np.arange(60)
last_neg_OLR_lags["lag"] = np.arange(60)

# %%

fig = plt.figure(figsize=(20, 10))
gs = gridspec.GridSpec(
    6, 2, height_ratios=[1, 1, 1, 1, 1, 0.3], hspace=0.3, wspace=0.01
)

lag_labels = ["-10 days", "-9 days", "-8 days", "-7 days", "-6 days"]
if not bandpass:
    levels = np.arange(-10, 11, 1)
else:
    levels = np.arange(-5, 6, 0.5)
# first columns
for i in range(5):
    ax = fig.add_subplot(gs[i, 0], projection=ccrs.PlateCarree(central_longitude=180))
    plot_composite(first_pos_OLR_lags.sel(lag=10 - i), ax, levels=levels)
    ax.set_title(lag_labels[i], loc="left")

# second columns
for j in range(5):
    ax = fig.add_subplot(gs[j, 1], projection=ccrs.PlateCarree(central_longitude=180))
    p = plot_composite(last_pos_OLR_lags.sel(lag=10 - j), ax, levels=levels)
    ax.set_title(None)


# add colorbar at the bottom
cax = fig.add_subplot(gs[5, :])
fig.colorbar(p, cax=cax, orientation="horizontal")
cax.set_title("OLR anomaly (W/m^2)")

plt.tight_layout()
figure_name = "/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_composite_e2c/OLR_composite_pos.png"
if bandpass:
    figure_name = figure_name.replace(".png", "_bandfilter.png")
plt.savefig(figure_name, dpi=300)


# %%
# same for negative events
fig = plt.figure(figsize=(20, 10))
gs = gridspec.GridSpec(
    6, 2, height_ratios=[1, 1, 1, 1, 1, 0.3], hspace=0.3, wspace=0.01
)

lag_labels = ["-10 days", "-9 days", "-8 days", "-7 days", "-6 days"]

# first columns
for i in range(5):
    ax = fig.add_subplot(gs[i, 0], projection=ccrs.PlateCarree(central_longitude=180))
    plot_composite(first_neg_OLR_lags.sel(lag=10 - i), ax, levels=levels)
    ax.set_title(lag_labels[i], loc="left")

# second columns
for j in range(5):
    ax = fig.add_subplot(gs[j, 1], projection=ccrs.PlateCarree(central_longitude=180))
    p = plot_composite(last_neg_OLR_lags.sel(lag=10 - j), ax, levels=levels)
    ax.set_title(None)


# add colorbar at the bottom
cax = fig.add_subplot(gs[5, :])
fig.colorbar(p, cax=cax, orientation="horizontal")
cax.set_title("OLR anomaly (W/m^2)")

plt.tight_layout()
figure_name = "/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_composite_e2c/OLR_composite_neg.png"
if bandpass:
    figure_name = figure_name.replace(".png", "_bandfilter.png")
plt.savefig(figure_name, dpi=300)
# %%
# profile lag-longitude plot
first_pos_OLR_lags_meridional = first_pos_OLR_lags.mean(dim="lat")

last_pos_OLR_lags_meridional = last_pos_OLR_lags.mean(dim="lat")

first_neg_OLR_lags_meridional = first_neg_OLR_lags.mean(dim="lat")
last_neg_OLR_lags_meridional = last_neg_OLR_lags.mean(dim="lat")
# %%
# use the
container1 = first_pos_OLR_lags.copy()
container2 = last_pos_OLR_lags.copy()

# %%
container1 = container1.isel(lag=0).drop_vars("lag")
container1["lat"] = np.arange(0, 32, 1)

container2 = container2.isel(lag=0).drop_vars("lag")
container2["lat"] = np.arange(32, 64, 1)

container = xr.concat([container1, container2], dim="lat")
container = container.sel(lat=slice(0, 59))

# %%
# create a container for the composite to align the x-axis
first_pos_OLR_lags_meridional_cont = container.copy(
    data=first_pos_OLR_lags_meridional.values
)
first_neg_OLR_lags_meridional_cont = container.copy(
    data=first_neg_OLR_lags_meridional.values
)
last_pos_OLR_lags_meridional_cont = container.copy(
    data=last_pos_OLR_lags_meridional.values
)
last_neg_OLR_lags_meridional_cont = container.copy(
    data=last_neg_OLR_lags_meridional.values
)


# %%
levels = np.arange(-3, 3.1, 0.3)
fig = plt.figure(figsize=(20, 10))
gs = gridspec.GridSpec(3, 2, height_ratios=[0.5, 1, 1], hspace=0.3, wspace=0.01)

# ax1 simple map with coastlines
ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree(central_longitude=180))
ax1.set_extent([0, 360, -30, 30], crs=ccrs.PlateCarree())
ax1.coastlines()
# brown land color, grey ocean color
# ax1.add_feature(
#     cfeature.NaturalEarthFeature(
#         "physical", "land", "110m", edgecolor="black", facecolor="Cornsilk"
#     )
# )
first_neg_OLR_lags.sel(lag=6).plot(
    ax=ax1,
    levels=levels * 3,
    add_colorbar=False,
    extend="both",
    add_labels=False,
    transform=ccrs.PlateCarree(),
)


# add longitude labels
ax1.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
ax1.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

ax1.set_yticks(range(-30, 31, 30), crs=ccrs.PlateCarree())
ax1.set_yticklabels([f"{lat}°" for lat in range(-30, 31, 30)])


ax2 = fig.add_subplot(gs[1, 0], projection=ccrs.PlateCarree(central_longitude=180))
first_pos_OLR_lags_meridional.plot.contourf(
    ax=ax2,
    levels=levels,
    add_colorbar=False,
    extend="both",
    add_labels=False,
    transform=ccrs.PlateCarree(),
)
ax2.set_title("first10")

ax3 = fig.add_subplot(gs[1, 1], projection=ccrs.PlateCarree(central_longitude=180))
last_pos_OLR_lags_meridional.plot.contourf(
    ax=ax3,
    levels=levels,
    add_colorbar=False,
    extend="both",
    add_labels=False,
    transform=ccrs.PlateCarree(),
)
ax3.set_title("last10")

ax4 = fig.add_subplot(gs[2, 0], projection=ccrs.PlateCarree(central_longitude=180))
first_neg_OLR_lags_meridional.plot.contourf(
    ax=ax4,
    levels=levels,
    add_colorbar=False,
    extend="both",
    add_labels=False,
    transform=ccrs.PlateCarree(),
)

ax5 = fig.add_subplot(gs[2, 1], projection=ccrs.PlateCarree(central_longitude=180))
last_neg_OLR_lags_meridional.plot.contourf(
    ax=ax5,
    levels=levels,
    add_colorbar=False,
    extend="both",
    add_labels=False,
    transform=ccrs.PlateCarree(),
)
for ax in [ax2, ax3, ax4, ax5]:

    ax.set_aspect("auto")
    ax.set_ylim(6, 30)

# set yticks and labels as [6..14],and times -1
for ax in [ax2, ax4]:
    ax.set_yticks(range(10, 30, 5), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"-{lat}" for lat in range(10, 30, 5)])

# add x-axis labels
for ax in [ax4, ax5]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

# make the cax width along y-axis 1/50 of the figure width
cax = fig.add_axes(
    [
        ax3.get_position().x0 + 0.01,
        ax3.get_position().y1 + 0.1,
        ax3.get_position().width,
        0.02,
    ]
)


fig.colorbar(ax2.collections[0], cax=cax, orientation="horizontal", aspect=50)
cax.set_title("OLR anomaly (W/m^2)")
fig.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_composite_e2c/OLR_composite_meridional.png",
    dpi=300,
)
# %%
