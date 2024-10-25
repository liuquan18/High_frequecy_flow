#%%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt

# %%
def month_extreme_composite(NAO_extreme, var, reduce = 'temporal_sum'):
    selected_var = []
    for ens in NAO_extreme.ens:
        NAO_extreme_ens = NAO_extreme.sel(ens=ens)
        var_ens = var.sel(ens=ens)

        # get avlid months for this ensemble member
        NAO_months = NAO_extreme_ens.time.dt.strftime("%Y-%m")
        valid_mask = ~np.isnan(NAO_extreme_ens)
        valid_months = NAO_months[valid_mask]

        # select only the valid months in daily jet
        daily_months = var_ens.time.dt.strftime("%Y-%m")
        jet_mask = daily_months.isin(valid_months)

        selected_var_ens = xr.where(jet_mask, var_ens, np.nan)
        if reduce == 'temporal_sum':
            selected_var_ens = selected_var_ens.groupby('time.month').sum(dim='time')
        elif reduce == 'none':
            selected_var_ens = selected_var_ens

        selected_var.append(selected_var_ens)

    selected_var = xr.concat(selected_var, dim="ens")

    return selected_var


#%%
def read_upvp(period, ens):
    base_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_{period}/'
    file=glob.glob(base_dir+f'*r{ens}i*.nc')[0]
    upvp = xr.open_dataset(file).ua.squeeze()
    upvp['time'] = upvp.indexes['time'].to_datetimeindex()
    return upvp
#%%
def read_NAO_extremes():
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
first_pos_AWB = month_extreme_composite(first_pos, first_AWB)
last_pos_AWB = month_extreme_composite(last_pos, last_AWB)
# %%
# drop zero
first_pos_AWB = first_pos_AWB.where(first_pos_AWB != 0, drop=True)
last_pos_AWB = last_pos_AWB.where(last_pos_AWB != 0, drop=True)
# %%
first_neg_CWB = month_extreme_composite(first_neg, first_CWB)
last_neg_CWB = month_extreme_composite(last_neg, last_CWB)

# drop zero
first_neg_CWB = first_neg_CWB.where(first_neg_CWB != 0, drop=True)
last_neg_CWB = last_neg_CWB.where(last_neg_CWB != 0, drop=True)
# %%
fig, ax = plt.subplots()
first_pos_AWB.plot.hist(bins = np.arange(2, 51,2), ax = ax)
last_pos_AWB.plot.hist(bins = np.arange(2, 51, 2), ax = ax, alpha = 0.5)
# %%
fig, ax = plt.subplots()
first_neg_CWB.plot.hist(bins = np.arange(0,30,2), ax = ax)
last_neg_CWB.plot.hist(bins = np.arange( 0,30,2), ax = ax, alpha = 0.5)
# %%
