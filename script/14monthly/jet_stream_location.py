#%%
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.jet_stream.jet_speed_and_location import jet_stream_anomaly, jet_event
import seaborn as sns
# %%
first_eofs = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result_first_last2091-2100/first10_eofs.nc")
last_eofs = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result_first_last2091-2100/last10_eofs.nc")

#%%
first_pc = first_eofs.pc.sel(mode='NAO')
last_pc = last_eofs.pc.sel(mode='NAO')

#%%
# standardize
mean = first_pc.mean(dim = ('time','ens'))
std = first_pc.std(dim = ('time', 'ens'))

first_pc = (first_pc - mean) / std
last_pc = (last_pc - mean) / std
# %%
# find time and ens where the value of pc is above 1.5
first_pos = first_pc.where(first_pc > 1.5)
last_pos = last_pc.where(last_pc > 1.5)

#%%
first_neg = first_pc.where(first_pc < -1.5)
last_neg = last_pc.where(last_pc < -1.5)
# %%
############## jet location hist #####################
_, jet_loc_first10_ano = jet_stream_anomaly("first10")

_, jet_loc_last10_ano = jet_stream_anomaly("last10")
#%%
jet_loc_last10_ano = jet_loc_last10_ano - jet_loc_last10_ano.mean(dim = ('time', 'ens'))
# %%
# %%
# select only the months in jet where the NAO_extreme is valid
def extreme_jet(NAO_extreme, jet, temporal_mean = True):
    selected_jet = []
    for ens in NAO_extreme.ens:
        NAO_extreme_ens = NAO_extreme.sel(ens = ens)
        jet_ens = jet.sel(ens = ens)

    # get avlid months for this ensemble member
        NAO_months = NAO_extreme_ens.time.dt.strftime('%Y-%m')
        valid_mask = ~np.isnan(NAO_extreme_ens)
        valid_months = NAO_months[valid_mask]


    # select only the valid months in daily jet
        daily_months = jet_ens.time.dt.strftime('%Y-%m')
        jet_mask = daily_months.isin(valid_months)

        selected_jet_ens = xr.where(jet_mask, jet_ens, np.nan)
        if temporal_mean:
            selected_jet_ens = selected_jet_ens.mean(dim = 'time')
    
        selected_jet.append(selected_jet_ens)

    selected_jet = xr.concat(selected_jet, dim = 'ens')

    return selected_jet
    


# %%
first_pos_jet = extreme_jet(first_pos, jet_loc_first10_ano)
last_pos_jet = extreme_jet(last_pos, jet_loc_last10_ano)

first_neg_jet = extreme_jet(first_neg, jet_loc_first10_ano)
last_neg_jet = extreme_jet(last_neg, jet_loc_last10_ano)

#%%
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
    jet_loc_first10_ano.values.flatten(),
    label="first10",
    color="k",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=hist_ax1,
)
sns.histplot(
    jet_loc_last10_ano.values.flatten(),
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
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=hist_ax2,
)

sns.histplot(
    last_pos_jet.values.flatten(),
    label="last10_pos",
    color="r",
    bins=np.arange(-30, 31, 2),
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
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax=hist_ax3,
)

sns.histplot(
    last_neg_jet.values.flatten(),
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax=hist_ax3,
)
hist_ax3.set_title("Jet location anomaly negative NAO")
hist_ax3.legend()

# vertical line for hist axes
for ax in [hist_ax1, hist_ax2, hist_ax3]:
    ax.axvline(x=0, color="k", linestyle="--")

# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/monthly/jet_location_month_mean.png")

# %%
