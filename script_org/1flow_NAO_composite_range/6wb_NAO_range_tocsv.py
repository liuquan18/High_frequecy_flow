# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import seaborn.objects as so

from src.data_helper import read_composite
from src.data_helper.read_variable import read_climatology
import importlib
import matplotlib
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
from src.plotting.util import lon360to180
importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var
# %%
awb_pos_first = read_comp_var(
    "wb_anticyclonic_allisen",
    "pos",
    1850,
    time_window = (-20, 20),
    name="smooth_pv",
    model_dir = 'MPI_GE_CMIP6_allplev',
    method = 'no_stat'
)

awb_neg_first = read_comp_var(
    "wb_anticyclonic_allisen",
    "neg",
    1850,
    time_window = (-20, 20),
    name="smooth_pv",
    model_dir = 'MPI_GE_CMIP6_allplev',
    method = 'no_stat'
)

awb_pos_last = read_comp_var(
    "wb_anticyclonic_allisen",
    "pos",
    2090,
    time_window = (-20, 20),
    name="smooth_pv",
    model_dir = 'MPI_GE_CMIP6_allplev',
    method = 'no_stat'
)
awb_neg_last = read_comp_var(
    "wb_anticyclonic_allisen",
    "neg",
    2090,
    time_window = (-20, 20),  
    name="smooth_pv",
    model_dir = 'MPI_GE_CMIP6_allplev',
    method = 'no_stat'
)

#%%
cwb_pos_first = read_comp_var(
    "wb_cyclonic_allisen",
    "pos",
    1850,
    time_window = (-20, 20),
    name="smooth_pv",
    model_dir = 'MPI_GE_CMIP6_allplev',
    method = 'no_stat'
)
cwb_neg_first = read_comp_var(
    "wb_cyclonic_allisen",
    "neg",
    1850,
    time_window = (-20, 20),
    name="smooth_pv",
    model_dir = 'MPI_GE_CMIP6_allplev',
    method = 'no_stat'
)
cwb_pos_last = read_comp_var(
    "wb_cyclonic_allisen",
    "pos",
    2090,
    time_window = (-20, 20),
    name="smooth_pv",
    model_dir = 'MPI_GE_CMIP6_allplev',
    method = 'no_stat'
)
cwb_neg_last = read_comp_var(
    "wb_cyclonic_allisen",
    "neg",
    2090,
    time_window = (-20, 20),
    name="smooth_pv",
    model_dir = 'MPI_GE_CMIP6_allplev',
    method = 'no_stat'
)



#%%
# fldmean over
def to_dataframe(ds, var_name, phase, decade, lat_slice = slice(40, 60), lon_slice = slice(-80, 0)):
    ds = lon360to180(ds)  # convert to 180W-180E
    ds = ds.sel(lat=lat_slice, lon=lon_slice)
    ds = ds.sum(dim = 'isen_level')
    
    # create weights
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"

    ds = ds.weighted(weights).mean(dim = ('lat', 'lon'))

    df = ds.to_dataframe(var_name).reset_index()
    df["phase"] = phase
    df["decade"] = decade
    return df
#%%
# awb [40, 60, -60, 30]
# cwb [50, 70, -120, -30]
awb_lat_slice = slice(40, 60)
awb_lon_slice = slice(-60, 30)
cwb_lat_slice = slice(50, 70)
cwb_lon_slice = slice(-120, -30)

#%%
awb_pos_first_df = to_dataframe(awb_pos_first,'smooth_pv', 'pos', '1850', lat_slice=awb_lat_slice, lon_slice=awb_lon_slice) 
awb_neg_first_df = to_dataframe(awb_neg_first,'smooth_pv', 'neg', '1850', lat_slice=awb_lat_slice, lon_slice=awb_lon_slice)
awb_pos_last_df = to_dataframe(awb_pos_last,'smooth_pv', 'pos', '2090', lat_slice=awb_lat_slice, lon_slice=awb_lon_slice)
awb_neg_last_df = to_dataframe(awb_neg_last,'smooth_pv', 'neg', '2090', lat_slice=awb_lat_slice, lon_slice=awb_lon_slice)

# save
awb_pos_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/awb_pos_first_smooth_pv_dy.csv", index=False)
awb_neg_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/awb_neg_first_smooth_pv_dy.csv", index=False)
awb_pos_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/awb_pos_last_smooth_pv_dy.csv", index=False)
awb_neg_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/awb_neg_last_smooth_pv_dy.csv", index=False)



#%%
cwb_pos_first_df = to_dataframe(cwb_pos_first,'smooth_pv', 'pos', '1850', lat_slice=cwb_lat_slice, lon_slice=cwb_lon_slice)
cwb_neg_first_df = to_dataframe(cwb_neg_first,'smooth_pv', 'neg', '1850', lat_slice=cwb_lat_slice, lon_slice=cwb_lon_slice)
cwb_pos_last_df = to_dataframe(cwb_pos_last,'smooth_pv', 'pos', '2090', lat_slice=cwb_lat_slice, lon_slice=cwb_lon_slice)
cwb_neg_last_df = to_dataframe(cwb_neg_last,'smooth_pv', 'neg', '2090', lat_slice=cwb_lat_slice, lon_slice=cwb_lon_slice)

cwb_pos_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/cwb_pos_first_smooth_pv_dy.csv", index=False)
cwb_neg_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/cwb_neg_first_smooth_pv_dy.csv", index=False)
cwb_pos_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/cwb_pos_last_smooth_pv_dy.csv", index=False)
cwb_neg_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/cwb_neg_last_smooth_pv_dy.csv", index=False)
# %%
