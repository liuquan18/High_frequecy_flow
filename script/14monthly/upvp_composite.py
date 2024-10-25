#%%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt

# %%
def count_wb_NAO(NAO_extreme, wb):
    wb_counts = []
    for ens in NAO_extreme.ens:
        NAO_extreme_ens = NAO_extreme.sel(ens=ens)
        wb_ens = wb.sel(ens=ens)

        # get avlid months for this ensemble member
        NAO_months = NAO_extreme_ens.time.dt.strftime("%Y-%m")
        valid_mask = ~np.isnan(NAO_extreme_ens)
        valid_months = NAO_months[valid_mask]

        # select only the valid months in daily jet
        daily_months = wb_ens.time.dt.strftime("%Y-%m")
        month_mask = daily_months.isin(valid_months)
        selected_wb_ens = xr.where(month_mask, wb_ens, np.nan)

        # count the event
        wb_count_ens = selected_wb_ens.groupby('time.month').sum(dim='time')

        wb_counts.append(wb_count_ens)

    wb_counts = xr.concat(wb_counts, dim="ens")

    return wb_counts


#%%
def read_upvp(period, ens):
    base_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_{period}/'
    file=glob.glob(base_dir+f'*r{ens}i*.nc')[0]
    upvp = xr.open_dataset(file).ua.squeeze()
    upvp['time'] = upvp.indexes['time'].to_datetimeindex()
    return upvp
#%%
def read_NAO_extremes():
    """both first10 and last10 are need to standardize"""
    first_eofs = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result_first_last2091-2100/first10_eofs.nc"
    )
    last_eofs = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result_first_last2091-2100/last10_eofs.nc"
    )

    first_pc = first_eofs.pc.sel(mode="NAO")
    last_pc = last_eofs.pc.sel(mode="NAO")

    # standardize
    mean = first_pc.mean(dim=("time", "ens"))
    std = first_pc.std(dim=("time", "ens"))

    first_pc = (first_pc - mean) / std
    last_pc = (last_pc - mean) / std
    
    # find time and ens where the value of pc is above 1.5
    first_pos = first_pc.where(first_pc > 1.5)
    last_pos = last_pc.where(last_pc > 1.5)

    
    first_neg = first_pc.where(first_pc < -1.5)
    last_neg = last_pc.where(last_pc < -1.5)

    return first_pos, last_pos, first_neg, last_neg

# %%
def wave_break(period):
    upvps = []
    for ens in range(1, 51):
        upvp = read_upvp(period, ens)
        upvp['ens'] = ens
        upvps.append(upvp)
    upvps = xr.concat(upvps, dim='ens')

    AWB = xr.where(upvps > 1, 1, 0)
    CWB = xr.where(upvps < -1, 1, 0)

    return AWB, CWB
#%%
first_pos, last_pos, first_neg, last_neg = read_NAO_extremes()
first_AWB, first_CWB = wave_break("first10")
last_AWB, last_CWB = wave_break("last10")
# %%
first_pos_AWB = count_wb_NAO(first_pos, first_AWB)
last_pos_AWB = count_wb_NAO(last_pos, last_AWB)

first_neg_CWB = count_wb_NAO(first_neg, first_CWB)
last_neg_CWB = count_wb_NAO(last_neg, last_CWB)
# %%
# drop zero
first_pos_AWB = first_pos_AWB.where(first_pos_AWB != 0, drop=True)
last_pos_AWB = last_pos_AWB.where(last_pos_AWB != 0, drop=True)

first_neg_CWB = first_neg_CWB.where(first_neg_CWB != 0, drop=True)
last_neg_CWB = last_neg_CWB.where(last_neg_CWB != 0, drop=True)

# %%
# name
first_pos_AWB.name = "wb"
last_pos_AWB.name = "wb"

first_neg_CWB.name = "wb"
last_neg_CWB.name = "wb"
# %%
# save
first_pos_AWB.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/physics/wave_break_count/wb_first_pos_AWB.nc")
last_pos_AWB.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/physics/wave_break_count/wb_last_pos_AWB.nc")

first_neg_CWB.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/physics/wave_break_count/wb_first_neg_CWB.nc")
last_neg_CWB.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/physics/wave_break_count/wb_last_neg_CWB.nc")
# %%
