# %%
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.jet_stream.jet_speed_and_location import jet_stream_anomaly
import seaborn as sns
import logging
import glob
logging.basicConfig(level=logging.INFO)
# %%
############## read NAO ###################
# %%
first_eofs = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result_first_last2091-2100/first10_eofs.nc"
)
last_eofs = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result_first_last2091-2100/last10_eofs.nc"
)

# %%
first_pc = first_eofs.pc.sel(mode="NAO")
last_pc = last_eofs.pc.sel(mode="NAO")

# %%
# standardize
mean = first_pc.mean(dim=("time", "ens"))
std = first_pc.std(dim=("time", "ens"))

first_pc = (first_pc - mean) / std
last_pc = (last_pc - mean) / std
# %%
# find time and ens where the value of pc is above 1.5
first_pos = first_pc.where(first_pc > 1.5)
last_pos = last_pc.where(last_pc > 1.5)

# %%
first_neg = first_pc.where(first_pc < -1.5)
last_neg = last_pc.where(last_pc < -1.5)

# %%
################# jet location #####################
# %%
def jet_loc_anomaly(period, climatology, plev = 25000):

    try:
        climatology = climatology.sel(plev = plev)
    except KeyError:
        climatology = climatology
        logging.info("No plev dim in climatology")

    jet_locs = []

    for ens in range(1, 51):
        # Load data
        jet_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_{period}/"
        jet_file = glob.glob(f"{jet_path}*r{ens}i1p1f1*.nc")[0]

        jet = xr.open_dataset(jet_file).ua
        # drop dim lon
        jet = jet.isel(lon=0)

        loc_ano = jet_stream_anomaly(
            jet, climatology, stat="loc"
        )
        loc_ano["ens"] = ens

        jet_locs.append(loc_ano)

    jet_locs = xr.concat(jet_locs, dim="ens")

    return jet_locs

    
# %%
# select only the months in jet where the NAO_extreme is valid
def extreme_jet(NAO_extreme, jet, temporal_mean=False):
    selected_jet = []
    for ens in NAO_extreme.ens:
        NAO_extreme_ens = NAO_extreme.sel(ens=ens)
        jet_ens = jet.sel(ens=ens)

        # get avlid months for this ensemble member
        NAO_months = NAO_extreme_ens.time.dt.strftime("%Y-%m")
        valid_mask = ~np.isnan(NAO_extreme_ens)
        valid_months = NAO_months[valid_mask]

        # select only the valid months in daily jet
        daily_months = jet_ens.time.dt.strftime("%Y-%m")
        jet_mask = daily_months.isin(valid_months)

        selected_jet_ens = xr.where(jet_mask, jet_ens, np.nan)
        if temporal_mean:
            selected_jet_ens = selected_jet_ens.mean(dim="time")

        selected_jet.append(selected_jet_ens)

    selected_jet = xr.concat(selected_jet, dim="ens")

    return selected_jet


# %%
# config, climatology, and composite
allplev = True
temporal_mean = False

#%%
if allplev:
    first_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_allplev_first10.nc"
    last_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_allplev_last10.nc"
else:
    first_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_first10.nc"
    last_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_last10.nc"

jet_loc_clim_first = xr.open_dataset(first_path).lat
jet_loc_clim_last = xr.open_dataset(last_path).lat

#%%
#%%
jet_loc_first10_all = jet_loc_anomaly("first10", jet_loc_clim_first)
jet_loc_last10_all  = jet_loc_anomaly("last10", jet_loc_clim_first) # use the same climatology to show externally forced change
#%%
jet_loc_first10_ano = jet_loc_anomaly("first10", jet_loc_clim_first)
jet_loc_last10_ano = jet_loc_anomaly("last10", jet_loc_clim_last)


# %%
first_pos_jet = extreme_jet(first_pos, jet_loc_first10_ano, temporal_mean)
last_pos_jet = extreme_jet(last_pos, jet_loc_last10_ano, temporal_mean)

first_neg_jet = extreme_jet(first_neg, jet_loc_first10_ano, temporal_mean)
last_neg_jet = extreme_jet(last_neg, jet_loc_last10_ano, temporal_mean)

# %%
# # save data
# first_pos_jet.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/jet_stream_location/jet_loc_first10_pos.nc")
# last_pos_jet.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/jet_stream_location/jet_loc_last10_pos.nc")

# first_neg_jet.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/jet_stream_location/jet_loc_first10_neg.nc")
# last_neg_jet.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/jet_stream_location/jet_loc_last10_neg.nc")


# %%
fig = plt.figure(figsize=(20, 14))

gs = fig.add_gridspec(2, 3)


## histgram
hist_ax1 = fig.add_subplot(gs[1, 0])
# jet location anomaly
sns.histplot(
    jet_loc_first10_all.values.flatten(),
    label="first10",
    color="k",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=hist_ax1,
)
sns.histplot(
    jet_loc_last10_all.values.flatten(),
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=hist_ax1,
)

hist_ax1.set_title("Jet location anomaly all")


hist_ax2 = fig.add_subplot(gs[1, 1])
sns.histplot(
    first_pos_jet.values.flatten(),
    label="first10_pos",
    color="k",
    bins=np.arange(-20, 21, 2),
    stat="count",
    ax=hist_ax2,
)

sns.histplot(
    last_pos_jet.values.flatten(),
    label="last10_pos",
    color="r",
    bins=np.arange(-20, 21, 2),
    stat="count",
    alpha=0.5,
    ax=hist_ax2,
)
hist_ax2.set_title("Jet location anomaly positive NAO")


hist_ax3 = fig.add_subplot(gs[1, 2])
sns.histplot(
    first_neg_jet.values.flatten(),
    label="first10",
    color="k",
    bins=np.arange(-20, 21, 2),
    stat="count",
    ax=hist_ax3,
)

sns.histplot(
    last_neg_jet.values.flatten(),
    label="last10",
    color="r",
    bins=np.arange(-20, 21, 2),
    stat="count",
    alpha=0.5,
    ax=hist_ax3,
)
hist_ax3.set_title("Jet location anomaly negative NAO")
hist_ax3.legend()

# vertical line for hist axes
for ax in [hist_ax1, hist_ax2, hist_ax3]:
    ax.axvline(x=0, color="k", linestyle="--")

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/monthly/jet_location_month_nomean_250hpa.png")

# %%