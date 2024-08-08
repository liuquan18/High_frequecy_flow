# %%
import xarray as xr
import numpy as np
import pandas as pd
import os
import sys
import mpi4py.MPI as MPI
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import glob
# %%
from src.extremes.extreme_read import read_extremes_allens

# %%
first10_pos_events, first10_neg_events = read_extremes_allens("first10", 8)
last10_pos_events, last10_neg_events = read_extremes_allens("last10", 8)

#%%
extremes_all = {
    ("first10", "pos"): first10_pos_events,
    ("first10", "neg"): first10_neg_events,
    ("last10", "pos"): last10_pos_events,
    ("last10", "neg"): last10_neg_events,
}
# %%
first10_pos_ens2 = first10_pos_events[first10_pos_events["ens"] == 2]
# %%
OLR_ens2 = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_reconstructed/first10_OLR_reconstructed/rlut_day_MPI-ESM1-2-LR_historical_r2i1p1f1_gn_18500501-18590930_ano.nc"
)
OLR_ens2 = OLR_ens2.TP_OLR_reconstructed

# %%
def composite_times(events, lag_days = 6):
    event_start_times = events["start_time"]
    field_sel_times = event_start_times - pd.Timedelta(f"{lag_days}D")
    # if the field_sel_times contains value before May 1st, or After September 30th, remove it
    field_sel_times = field_sel_times[(field_sel_times.dt.month >= 5) & (field_sel_times.dt.month <= 9)]
    return field_sel_times.values

def composite_mean(field, times):
    field_sel = field.sel(time = times)
    return field_sel.mean(dim = "time")


def composite_OLR_events(period, extreme_type, lag_days = 6):
    OLR_events_lag_concur = []
    extremes = extremes_all[(period, extreme_type)]

    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_reconstructed/{period}_OLR_reconstructed/"
    for ens in range(1,51):

        # read OLR data
        file=f"{base_dir}rlut_day_MPI-ESM1-2-LR_*_r{ens}i1p1f1_gn_*_ano.nc"
        file = glob.glob(file)[0]
        OLR = xr.open_dataset(file).TP_OLR_reconstructed

        # read events of the ensemble
        extreme_single = extremes[extremes["ens"] == ens]
        if extreme_single.empty:
            continue

        # composite the OLR
        sel_times = composite_times(extreme_single, lag_days = lag_days)
        OLR_mean_single = composite_mean(OLR, sel_times)
        OLR_events_lag_concur.append(OLR_mean_single)

    OLR_events_lag_concur = xr.concat(OLR_events_lag_concur, dim = "events_id")

    OLR_event_composite = OLR_events_lag_concur.mean(dim = "events_id")
    return OLR_event_composite


def plot_composite(field, ax):
    p = field.plot(
        levels = np.arange(-10,11,1),
        transform=ccrs.PlateCarree(),
        add_colorbar = False,
        ax = ax
    )
    ax.coastlines()
    return p

# %%
# composite analysis with lag ranging from 15 days to 0
first_pos_OLR_lags = [composite_OLR_events("first10", "pos", lag_days = i) for i in range(15)]
first_neg_OLR_lags = [composite_OLR_events("first10", "neg", lag_days = i) for i in range(15)]
last_pos_OLR_lags = [composite_OLR_events("last10", "pos", lag_days = i) for i in range(15)]
last_neg_OLR_lags = [composite_OLR_events("last10", "neg", lag_days = i) for i in range(15)]

# %%
first_pos_OLR_lags = xr.concat(first_pos_OLR_lags, dim = "lag")
first_neg_OLR_lags = xr.concat(first_neg_OLR_lags, dim = "lag")
last_pos_OLR_lags = xr.concat(last_pos_OLR_lags, dim = "lag")
last_neg_OLR_lags = xr.concat(last_neg_OLR_lags, dim = "lag")

#%%
# coordinate for the lags
first_pos_OLR_lags["lag"] = np.arange(15)
first_neg_OLR_lags["lag"] = np.arange(15)
last_pos_OLR_lags["lag"] = np.arange(15)
last_neg_OLR_lags["lag"] = np.arange(15)

#%%
# plot composite with lags ranging from 10 days to 6 days as rows, different periods as columns
fig, axes = plt.subplots(5,2, figsize = (20,10),
        subplot_kw=dict(projection=ccrs.PlateCarree(
            central_longitude= 180
        ),facecolor='grey'))
lag_lables = ['-10 days', '-9 days', '-8 days', '-7 days', '-6 days']

# first columns
for i, ax in enumerate(axes[:,0]):
    plot_composite(first_pos_OLR_lags.sel(lag = 10 - i), ax)
    ax.set_title(lag_lables[i], loc = "left")

# second columns
for j, ax in enumerate(axes[:,1]):
    plot_composite(last_pos_OLR_lags.sel(lag = 10 - j), ax)
    ax.set_title(None)

# title for the first column as "First 10 years"
axes[0,0].set_title("First 10 years")
# title for the second column as "Last 10 years"
axes[0,1].set_title("Last 10 years")

# title at the middle between two column as [10, 9, 8, 7, 6]
# Add custom y-labels to the second column

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_composite_e2c/OLR_composite_pos.pdf")

# %%
# same for the negative events
fig, axes = plt.subplots(5,2, figsize = (20,10),
        subplot_kw=dict(projection=ccrs.PlateCarree(
            central_longitude= 180
        ),facecolor='grey'))

lag_lables = ['-10 days', '-9 days', '-8 days', '-7 days', '-6 days']
# first columns
for i, ax in enumerate(axes[:,0]):
    plot_composite(first_neg_OLR_lags.sel(lag = 10 - i), ax)
    ax.set_title(lag_lables[i], loc = "left")

# second columns
for j, ax in enumerate(axes[:,1]):
    plot_composite(last_neg_OLR_lags.sel(lag = 10 - j), ax)
    ax.set_title(None)

# title for the first column as "First 10 years"
axes[0,0].set_title("First 10 years")
# title for the second column as "Last 10 years"
axes[0,1].set_title("Last 10 years")

# title at the middle between two column as [10, 9, 8, 7, 6]
# Add custom y-labels to the second column
y_labels = ['10 days', '9 days', '8 days', '7 days', '6 days']
for idx, label in enumerate(y_labels):
    axes[idx, 1].text(-0.1, 0.5, label, va='center', ha='right', rotation=90,
                      transform=axes[idx, 1].transAxes, fontsize=12)

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_composite_e2c/OLR_composite_neg.pdf")

# %%
