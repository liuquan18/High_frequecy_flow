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
def read_anomaly(period, same_clim = True, eddy = True):

    # anomaly
    ano_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/loc_anomaly/"
    clima_label = "sameclima" if same_clim else "diffclima"
    eddy_label = "eddy" if eddy else "noneddy"

    ano_path = f"{ano_dir}jet_stream_anomaly_{eddy_label}_{clima_label}_{period}.nc"



    loc_ano = xr.open_dataset(ano_path).lat_ano

    return loc_ano

    
# %%
# select only the months in jet where the NAO_extreme is valid
def extreme_jet(NAO_extreme, jet, temporal_mean=False,):
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
            selected_jet_ens = selected_jet_ens.groupby('time.month').sum(dim='time')

        selected_jet.append(selected_jet_ens)

    selected_jet = xr.concat(selected_jet, dim="ens")

    return selected_jet



#%%
same_clim = False
eddy = False
temporal_mean = True


#%%
# for plot the anomaly of all samples
jet_loc_first10_all = read_anomaly("first10", same_clim = True, eddy = eddy)
jet_loc_last10_all = read_anomaly("last10", same_clim = True, eddy = eddy)


jet_loc_first10_ano = read_anomaly("first10", same_clim = same_clim, eddy = eddy)
jet_loc_last10_ano = read_anomaly("last10", same_clim = same_clim, eddy = eddy)

# %%
# select the jet north or south
first_jet_south = xr.where(jet_loc_first10_ano < 0, 1, 0)
last_jet_south = xr.where(jet_loc_last10_ano < 0, 1, 0)

first_jet_north = xr.where(jet_loc_first10_ano > 0, 1, 0)
last_jet_north = xr.where(jet_loc_last10_ano > 0, 1, 0)



# %%
first_pos_jet = extreme_jet(first_pos, first_jet_north, temporal_mean)
last_pos_jet = extreme_jet(last_pos, last_jet_north, temporal_mean)

first_neg_jet = extreme_jet(first_neg, first_jet_south, temporal_mean)
last_neg_jet = extreme_jet(last_neg, last_jet_south, temporal_mean)

#%%
first_pos_jet = first_pos_jet.where(first_pos_jet != 0, drop=True)
last_pos_jet = last_pos_jet.where(last_pos_jet != 0, drop=True)

first_neg_jet = first_neg_jet.where(first_neg_jet != 0, drop=True)
last_neg_jet = last_neg_jet.where(last_neg_jet != 0, drop=True)
