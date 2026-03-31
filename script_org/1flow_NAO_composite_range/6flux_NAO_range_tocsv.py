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
transient_pos_first = read_comp_var('transient_eddy_heat_dy', 'pos', 1850, time_window='all', method = 'no_stat', name = 'eddy_heat_dy', model_dir = 'MPI_GE_CMIP6_allplev')
transient_neg_first = read_comp_var('transient_eddy_heat_dy', 'neg', 1850, time_window='all', method = 'no_stat', name = 'eddy_heat_dy', model_dir = 'MPI_GE_CMIP6_allplev')
transient_pos_last = read_comp_var('transient_eddy_heat_dy', 'pos', 2090, time_window='all', method = 'no_stat', name = 'eddy_heat_dy', model_dir = 'MPI_GE_CMIP6_allplev')
transient_neg_last = read_comp_var('transient_eddy_heat_dy', 'neg', 2090, time_window='all', method = 'no_stat', name = 'eddy_heat_dy', model_dir = 'MPI_GE_CMIP6_allplev')
# %%
steady_pos_first = read_comp_var('steady_eddy_heat_dy', 'pos', 1850, time_window='all', method = 'no_stat', name = 'eddy_heat_dy', model_dir = 'MPI_GE_CMIP6_allplev')
steady_neg_first = read_comp_var('steady_eddy_heat_dy', 'neg', 1850, time_window='all', method = 'no_stat', name = 'eddy_heat_dy', model_dir = 'MPI_GE_CMIP6_allplev')
steady_pos_last = read_comp_var('steady_eddy_heat_dy', 'pos', 2090, time_window ='all', method = 'no_stat', name = 'eddy_heat_dy', model_dir = 'MPI_GE_CMIP6_allplev')
steady_neg_last = read_comp_var('steady_eddy_heat_dy', 'neg',       2090, time_window='all', method = 'no_stat', name = 'eddy_heat_dy', model_dir = 'MPI_GE_CMIP6_allplev')

#%%
transient_clima_first = read_climatology('transient_eddy_heat_dy', 1850, name = 'eddy_heat_dy', model_dir = 'MPI_GE_CMIP6_allplev')
transient_clima_last = read_climatology('transient_eddy_heat_dy', 2090, name = 'eddy_heat_dy', model_dir = 'MPI_GE_CMIP6_allplev')
steady_clima_first = read_climatology('steady_eddy_heat_dy', 1850, name = 'eddy_heat_dy', model_dir = 'MPI_GE_CMIP6_allplev')
steady_clima_last = read_climatology('steady_eddy_heat_dy', 2090, name = 'eddy_heat_dy', model_dir = 'MPI_GE_CMIP6_allplev')
#%%
# %%
def anomaly(ds, ds_clima):
    """
    Calculate the anomaly of a dataset with respect to a climatology.
    """
    # average over time and events
    ds = ds.sel(time = slice(-10, 5)).mean(dim=('time', 'event', 'lon'))
    ds_clima = ds_clima.mean(dim=('lon'))
    anomaly = ds - ds_clima
    return anomaly.compute()
#%%
transient_pos_first_anom = anomaly(transient_pos_first, transient_clima_first)
transient_neg_first_anom = anomaly(transient_neg_first, transient_clima_first)
transient_pos_last_anom = anomaly(transient_pos_last, transient_clima_last)
transient_neg_last_anom = anomaly(transient_neg_last, transient_clima_last)
#%%
steady_pos_first_anom = anomaly(steady_pos_first, steady_clima_first)
steady_neg_first_anom = anomaly(steady_neg_first, steady_clima_first)
steady_pos_last_anom = anomaly(steady_pos_last, steady_clima_last)
steady_neg_last_anom = anomaly(steady_neg_last, steady_clima_last)

#%%
sum_pos_first_anomaly = transient_pos_first_anom + steady_pos_first_anom
sum_neg_first_anomaly = transient_neg_first_anom + steady_neg_first_anom
sum_pos_last_anomaly = transient_pos_last_anom + steady_pos_last_anom
sum_neg_last_anomaly = transient_neg_last_anom + steady_neg_last_anom
#%%

## eke
#%%
eke_pos_first = read_comp_var(
    "eke",
    "pos",
    1850,
    time_window = 'all',
    name="eke",
    model_dir = 'MPI_GE_CMIP6_allplev',
    method = 'no_stat'
)

eke_neg_first = read_comp_var(
    "eke",
    "neg",
    1850,
    time_window = 'all',
    name="eke",
    model_dir = 'MPI_GE_CMIP6_allplev',
    method = 'no_stat'
)
eke_pos_last = read_comp_var(
    "eke",
    "pos",
    2090,
    time_window = 'all',
    name="eke",
    model_dir = 'MPI_GE_CMIP6_allplev',
    method = 'no_stat'
)
eke_neg_last = read_comp_var(
    "eke",
    "neg",
    2090,
    time_window = 'all',
    name="eke",
    model_dir = 'MPI_GE_CMIP6_allplev',
    method = 'no_stat'
)

## baroclinicity
# %%
baroc_pos_first = read_comp_var(
    "eady_growth_rate",
    "pos",
    1850,
    time_window=((-5, 5)),
    method="no_stat",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
baroc_neg_first = read_comp_var(
    "eady_growth_rate",
    "neg",
    1850,
    time_window=((-5, 5)),
    method="no_stat",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
baroc_pos_last = read_comp_var(
    "eady_growth_rate",
    "pos",
    2090,
    time_window=((-5, 5)),
    method="no_stat",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
baroc_neg_last = read_comp_var(
    "eady_growth_rate",
    "neg",
    2090,
    time_window=((-5, 5)),
    method="no_stat",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
#%%

eke_clima_first = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/eke_monthly_ensmean/eke_monmean_ensmean_185005_185909.nc")
eke_clima_last = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/eke_monthly_ensmean/eke_monmean_ensmean_209005_209909.nc")

eke_clima_first = eke_clima_first["eke"].mean(dim="time").sel(plev = 25000)
eke_clima_last = eke_clima_last["eke"].mean(dim="time").sel(plev = 25000)
#%%
baroc_clima_first = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/eady_growth_rate_monthly_ensmean/eady_growth_rate_monmean_ensmean_185005_185909.nc")
baroc_clima_last = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/eady_growth_rate_monthly_ensmean/eady_growth_rate_monmean_ensmean_209005_209909.nc")

baroc_clima_first = baroc_clima_first["eady_growth_rate"].mean(dim="time")
baroc_clima_last = baroc_clima_last["eady_growth_rate"].mean(dim="time")
#%%
# fldmean over
def to_dataframe(ds, ds_clima, var_name, phase, decade, plev = 85000, lat_slice = slice(50, 70), lon_slice = slice(-120, 0)):

    ds = lon360to180(ds)  # convert to 180W-180E
    ds_clima = lon360to180(ds_clima)
    
    # Remove duplicate coordinates if present
    ds = ds.drop_duplicates(dim='lon', keep='first')
    ds_clima = ds_clima.drop_duplicates(dim='lon', keep='first')
    
    ds = ds.sel(lat=lat_slice, lon=lon_slice)
    ds_clima = ds_clima.sel(lat=lat_slice, lon=lon_slice)

    if plev is not None:
        ds = ds.sel(plev = plev)
        ds_clima = ds_clima.sel(plev = plev)
    anomaly = ds - ds_clima

    # create weights
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"

    anomaly = anomaly.weighted(weights).mean(dim = ('lat', 'lon'))

    df = anomaly.to_dataframe(var_name).reset_index()
    df["phase"] = phase
    df["decade"] = decade
    return df
#%%
transient_pos_first_df = to_dataframe(transient_pos_first, transient_clima_first, "eddy_heat_dy", "pos", "1850")
transient_neg_first_df = to_dataframe(transient_neg_first, transient_clima_first, "eddy_heat_dy", "neg", "1850")
transient_pos_last_df = to_dataframe(transient_pos_last, transient_clima_last, "eddy_heat_dy", "pos", "2090")
transient_neg_last_df = to_dataframe(transient_neg_last, transient_clima_last, "eddy_heat_dy", "neg", "2090")

#%%
steady_pos_first_df = to_dataframe(steady_pos_first, steady_clima_first, "eddy_heat_dy", "pos", "1850")
steady_neg_first_df = to_dataframe(steady_neg_first, steady_clima_first, "eddy_heat_dy", "neg", "1850")
steady_pos_last_df = to_dataframe(steady_pos_last, steady_clima_last, "eddy_heat_dy", "pos", "2090")
steady_neg_last_df = to_dataframe(steady_neg_last, steady_clima_last, "eddy_heat_dy", "neg", "2090")

#%%
sum_pos_first_df = transient_pos_first_df.copy()
sum_pos_first_df["eddy_heat_dy"] = transient_pos_first_df["eddy_heat_dy"] + steady_pos_first_df["eddy_heat_dy"]

sum_neg_first_df = transient_neg_first_df.copy()
sum_neg_first_df["eddy_heat_dy"] = transient_neg_first_df["eddy_heat_dy"] + steady_neg_first_df["eddy_heat_dy"]

sum_pos_last_df = transient_pos_last_df.copy()
sum_pos_last_df["eddy_heat_dy"] = transient_pos_last_df["eddy_heat_dy"] + steady_pos_last_df["eddy_heat_dy"]
sum_neg_last_df = transient_neg_last_df.copy()
sum_neg_last_df["eddy_heat_dy"] = transient_neg_last_df["eddy_heat_dy"] + steady_neg_last_df["eddy_heat_dy"]

#%%
# save dataframes
transient_pos_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/transient_pos_first_vptp_dy.csv", index=False)
transient_neg_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/transient_neg_first_vptp_dy.csv", index=False)
transient_pos_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/transient_pos_last_vptp_dy.csv", index=False)
transient_neg_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/transient_neg_last_vptp_dy.csv", index=False)

steady_pos_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/steady_pos_first_vsts_dy.csv", index=False)
steady_neg_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/steady_neg_first_vsts_dy.csv", index=False)
steady_pos_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/steady_pos_last_vsts_dy.csv", index=False)
steady_neg_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/steady_neg_last_vsts_dy.csv", index=False)

sum_pos_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/sum_pos_first_vptp_dy.csv", index=False)
sum_neg_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/sum_neg_first_vptp_dy.csv", index=False)
sum_pos_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/sum_pos_last_vptp_dy.csv", index=False)
sum_neg_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/sum_neg_last_vptp_dy.csv", index=False)

#%%
eke_pos_first_df = to_dataframe(eke_pos_first, eke_clima_first, "eke", "pos", "1850", plev = None)
eke_neg_first_df = to_dataframe(eke_neg_first, eke_clima_first, "eke", "neg", "1850", plev = None)
eke_pos_last_df = to_dataframe(eke_pos_last, eke_clima_last, "eke", "pos", "2090", plev = None)
eke_neg_last_df = to_dataframe(eke_neg_last, eke_clima_last, "eke", "neg", "2090", plev = None)

#%%
baroc_pos_first_df = to_dataframe(baroc_pos_first, baroc_clima_first, "eady_growth_rate", "pos", "1850", plev = 85000)
baroc_neg_first_df = to_dataframe(baroc_neg_first, baroc_clima_first, "eady_growth_rate", "neg", "1850", plev = 85000)
baroc_pos_last_df = to_dataframe(baroc_pos_last, baroc_clima_last, "eady_growth_rate", "pos", "2090", plev = 85000)
baroc_neg_last_df = to_dataframe(baroc_neg_last, baroc_clima_last, "eady_growth_rate", "neg", "2090", plev = 85000)

#%%
# save
eke_pos_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/eke_pos_first.csv", index=False)
eke_neg_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/eke_neg_first.csv", index=False)
eke_pos_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/eke_pos_last.csv", index=False)
eke_neg_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/eke_neg_last.csv", index=False)
#%%
baroc_pos_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/baroc_pos_first.csv", index=False)
baroc_neg_first_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/baroc_neg_first.csv", index=False)
baroc_pos_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/baroc_pos_last.csv", index=False)
baroc_neg_last_df.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/baroc_neg_last.csv", index=False)

# %%
