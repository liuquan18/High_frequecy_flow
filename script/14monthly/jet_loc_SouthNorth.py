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
def count_jet_loc(NAO_extreme, jet):
    jet_counts = []
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

        # count the jet that is north (south) of climatology

        jet_loc_count = selected_jet_ens.groupby('time.month').sum(dim='time')

        jet_counts.append(jet_loc_count)

    jet_counts = xr.concat(jet_counts, dim="ens")

    return jet_counts



#%%
same_clim = False  # if True, use the same climatology for first and last 10 years
eddy = False       # if True, use the eddy jet stream


#%%
# for plot the anomaly of all samples
jet_loc_first10_all = read_anomaly("first10", same_clim = True, eddy = eddy)
jet_loc_last10_all = read_anomaly("last10", same_clim = True, eddy = eddy)


jet_loc_first10_ano = read_anomaly("first10", same_clim = same_clim, eddy = eddy)
jet_loc_last10_ano = read_anomaly("last10", same_clim = same_clim, eddy = eddy)

# %%
# seperate the jet to north or south
first_jet_south = xr.where(jet_loc_first10_ano < 0, 1, 0)
last_jet_south = xr.where(jet_loc_last10_ano < 0, 1, 0)

first_jet_north = xr.where(jet_loc_first10_ano > 0, 1, 0)
last_jet_north = xr.where(jet_loc_last10_ano > 0, 1, 0)



# %%
first_pos_jet = count_jet_loc(first_pos, first_jet_north)
last_pos_jet = count_jet_loc(last_pos, last_jet_north)

first_neg_jet = count_jet_loc(first_neg, first_jet_south)
last_neg_jet = count_jet_loc(last_neg, last_jet_south)

#%%
first_pos_jet = first_pos_jet.where(first_pos_jet != 0, drop=True)
last_pos_jet = last_pos_jet.where(last_pos_jet != 0, drop=True)

first_neg_jet = first_neg_jet.where(first_neg_jet != 0, drop=True)
last_neg_jet = last_neg_jet.where(last_neg_jet != 0, drop=True)

#name
first_pos_jet.name = 'jet_loc'
last_pos_jet.name = 'jet_loc'
first_neg_jet.name = 'jet_loc'
last_neg_jet.name = 'jet_loc'


# %%
# save
first_pos_jet.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/physics/jet_loc_count/jet_loc_pos_north_first10.nc")
last_pos_jet.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/physics/jet_loc_count/jet_loc_pos_north_last10.nc")

first_neg_jet.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/physics/jet_loc_count/jet_loc_neg_south_first10.nc")
last_neg_jet.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/physics/jet_loc_count/jet_loc_neg_south_last10.nc")
# %%
