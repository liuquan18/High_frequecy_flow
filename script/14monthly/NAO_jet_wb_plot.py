#%%
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %%
def read_NAO_extremes():
    """both first10 and last10 are need to standardize"""
    first_eofs = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result_first_last2091-2100/first10_eofs.nc"
    )
    last_eofs = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result_first_last2091-2100/last10_eofs.nc"
    )
    # time to year-month
    first_eofs['time'] = first_eofs['time'].dt.strftime('%Y-%m')
    last_eofs['time'] = last_eofs['time'].dt.strftime('%Y-%m')

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
def read_jet(period, NAO_phase, jet_loc, eddy = False):
    """
    Parameters
    ----------
    period : str
        first10 or last10
    NAO_phase : str
        pos or neg
    jet_loc : str
        north or south
    """
    eddy_label = "_eddy" if eddy else ""
    base_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/physics/jet_loc_count/"
    jet_path = f"{base_dir}jet_loc{eddy_label}_{NAO_phase}_{jet_loc}_{period}.nc"

    jet = xr.open_dataset(jet_path).jet_loc

    # 0 to np.nan
    jet = xr.where(jet == 0, np.nan, jet)
    
    # time to year-month
    jet['time'] = jet['time'].dt.strftime('%Y-%m')

    return jet
# %%
def read_wb(period, NAO_phase, wb_type):
    """
    Parameters
    ----------
    period : str
        first10 or last10
    NAO_phase : str
        pos or neg
    wb_type : str
        AWB or CWB
    """
    base_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/physics/wave_break_count/"
    wb_path = f"{base_dir}wb_{NAO_phase}_{wb_type}_{period}.nc"

    wb = xr.open_dataset(wb_path).wb

    # 0 to np.nan
    wb = xr.where(wb == 0, np.nan, wb)

    # time to year-month
    wb['time'] = wb['time'].dt.strftime('%Y-%m')

    return wb
# %%
first_pos, last_pos, first_neg, last_neg = read_NAO_extremes()

# %%
first_pos_jet_north = read_jet("first10", "pos", "north")
last_pos_jet_north = read_jet("last10", "pos", "north")
first_neg_jet_north = read_jet("first10", "neg", "north")
last_neg_jet_north = read_jet("last10", "neg", "north")

first_pos_jet_south = read_jet("first10", "pos", "south")
last_pos_jet_south = read_jet("last10", "pos", "south")
first_neg_jet_south = read_jet("first10", "neg", "south")
last_neg_jet_south = read_jet("last10", "neg", "south")
# %%
first_pos_AWB = read_wb("first10", "pos", "AWB")
last_pos_AWB = read_wb("last10", "pos", "AWB")
first_neg_CWB = read_wb("first10", "neg", "CWB")
last_neg_CWB = read_wb("last10", "neg", "CWB")

first_pos_CWB = read_wb("first10", "pos", "CWB")
last_pos_CWB = read_wb("last10", "pos", "CWB")
first_neg_AWB = read_wb("first10", "neg", "AWB")
last_neg_AWB = read_wb("last10", "neg", "AWB")

# %%
# combine into one dataset
first_pos_NAO_expected = xr.merge(
    [first_pos, first_pos_jet_north, first_pos_AWB],
    compat = "minimal"
)

first_neg_NAO_expected = xr.merge(
    [first_neg, first_neg_jet_south, first_neg_CWB],
    compat = "minimal"
)
# %%
last_pos_NAO_expected = xr.merge(
    [last_pos, last_pos_jet_north, last_pos_AWB],
    compat = "minimal"
)

last_neg_NAO_expected = xr.merge(
    [last_neg, last_neg_jet_south, last_neg_CWB],
    compat = "minimal"
)
# %%
first_pos_NAO_unexpected = xr.merge(
    [first_pos, first_pos_jet_south, first_pos_CWB],
    compat = "minimal"
)

first_neg_NAO_unexpected = xr.merge(
    [first_neg, first_neg_jet_north, first_neg_AWB],
    compat = "minimal"
)

# %%
last_pos_NAO_unexpected = xr.merge(
    [last_pos, last_pos_jet_south, last_pos_CWB],
    compat = "minimal"
)

last_neg_NAO_unexpected = xr.merge(
    [last_neg, last_neg_jet_north, last_neg_AWB],
    compat = "minimal"
)
# %%
def to_dataframe(ds):
    df = ds.to_dataframe()[['pc', 'jet_loc', 'wb']]
    return df
# %%
def phy_diff(expected, unexpected):
    diff = expected - unexpected
    # keep 'pc' column no change
    diff['pc'] = expected['pc']
    return diff
# %%
first_pos_phy_diff = phy_diff(
    to_dataframe(first_pos_NAO_expected),
    to_dataframe(first_pos_NAO_unexpected)
)
# %%
last_pos_phy_diff = phy_diff(
    to_dataframe(last_pos_NAO_expected),
    to_dataframe(last_pos_NAO_unexpected)
)
# %%
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
sns.scatterplot(data=first_pos_phy_diff, x='jet_loc', y='wb',size = 'pc', ax=ax[0])
sns.scatterplot(data=last_pos_phy_diff, x='jet_loc', y='wb',size = 'pc', ax=ax[0])
# hline and vline at 0
ax[0].axhline(0, color='black', linewidth=0.5)
ax[0].axvline(0, color='black', linewidth=0.5)
# %%
# density plot
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
sns.kdeplot(data=first_pos_phy_diff, x='jet_loc', y='wb', ax=ax[1], fill=True)
sns.kdeplot(data=last_pos_phy_diff, x='jet_loc', y='wb', ax=ax[1], fill=False)
# %%