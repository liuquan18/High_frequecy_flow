#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import cmocean
import os
import matplotlib
from src.plotting.util import lon360to180

from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, FuncFormatter

from src.plotting.util import map_smooth
import src.plotting.util as util
import metpy.calc as mpcalc
from metpy.units import units
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec

# %%
data_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0composite_feedback"

def _load(name):
    return xr.open_dataarray(os.path.join(data_dir, f"{name}.nc"))

#%%
ua_pos_first = _load("ua_pos_1850")
ua_neg_first = _load("ua_neg_1850")
ua_pos_last  = _load("ua_pos_2090")
ua_neg_last  = _load("ua_neg_2090")

ua_pos_first = ua_pos_first.sel(lat = slice(0, 70))
ua_neg_first = ua_neg_first.sel(lat = slice(0, 70))
ua_pos_last  = ua_pos_last.sel(lat = slice(0, 70))
ua_neg_last  = ua_neg_last.sel(lat = slice(0, 70))

#%%
awb_pos_first = _load("wb_anticyclonic_pos_1850")
awb_neg_first = _load("wb_anticyclonic_neg_1850")
awb_pos_last  = _load("wb_anticyclonic_pos_2090")
awb_neg_last  = _load("wb_anticyclonic_neg_2090")


#%%
# baroclinic growth rate
baroc_pos_first = _load("eady_growth_rate_pos_1850")
baroc_neg_first = _load("eady_growth_rate_neg_1850")
baroc_pos_last  = _load("eady_growth_rate_pos_2090")
baroc_neg_last  = _load("eady_growth_rate_neg_2090")


#%%
zg_hat_pos_first = _load("zg_hat_pos_1850")
zg_hat_neg_first = _load("zg_hat_neg_1850")
zg_hat_pos_last  = _load("zg_hat_pos_2090")
zg_hat_neg_last  = _load("zg_hat_neg_2090")


#%%
# eddy driven jet
ua_pos_first = ua_pos_first.sel(plev=slice(92500, 70000)).mean(dim="plev")
ua_neg_first = ua_neg_first.sel(plev=slice(92500, 70000)).mean(dim="plev")
ua_pos_last  = ua_pos_last.sel(plev=slice(92500, 70000)).mean(dim="plev")
ua_neg_last  = ua_neg_last.sel(plev=slice(92500, 70000)).mean(dim="plev")
# select levels
zg_hat_pos_first = zg_hat_pos_first.sel(plev=50000)
zg_hat_neg_first = zg_hat_neg_first.sel(plev=50000)
zg_hat_pos_last  = zg_hat_pos_last.sel(plev=50000)
zg_hat_neg_last  = zg_hat_neg_last.sel(plev=50000)


#%%
# fldmean over
def to_dataframe(ds, var_name, phase, decade, lat_slice = slice(50, 70), ds_clim = None):
    ds = ds.sel(lat=lat_slice)    
    if ds_clim is not None:
        ds_clim = ds_clim.sel(lat=lat_slice)
        ds = ds - ds_clim # anomaly

    # create weights
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"

    ds = ds.weighted(weights).mean(dim = ('lat'))

    df = ds.to_dataframe(var_name).reset_index()
    df["phase"] = phase
    df["decade"] = decade
    return df
#%% calculate the jet location (lat of max ua)
def jet_latitude(ua, phase, decade):
    # average over lon if present, then find lat of max ua
    if "lon" in ua.dims:
        ua = ua.mean(dim="lon")
    jet_lat = ua.idxmax(dim="lat")
    jet_lat_df = jet_lat.to_dataframe("jet_lat").reset_index()
    jet_lat_df["phase"] = phase
    jet_lat_df["decade"] = decade
    return jet_lat_df

#%%
# awb_lat_slice = slice(40, 60)
# cwb_lat_slice = slice(50, 70)
awb_pos_first_df = to_dataframe(awb_pos_first, "awb", "pos", 1850, lat_slice = slice(40, 60))
awb_pos_last_df  = to_dataframe(awb_pos_last,  "awb", "pos", 2090, lat_slice = slice(40, 60))
awb_pos_df = pd.concat([awb_pos_first_df, awb_pos_last_df], ignore_index=True)

jet_lat_pos_first = jet_latitude(ua_pos_first, "pos", 1850)
jet_lat_pos_last  = jet_latitude(ua_pos_last,  "pos", 2090)
jet_lat_pos_df = pd.concat([jet_lat_pos_first, jet_lat_pos_last], ignore_index=True)

pos_df = awb_pos_df.merge(jet_lat_pos_df, on=['event', 'time', 'phase', 'decade'], how='inner')
#%%
baroc_neg_first_df = to_dataframe(baroc_neg_first, "baroclinicity", "neg", 1850,)
baroc_neg_last_df  = to_dataframe(baroc_neg_last,  "baroclinicity", "neg", 2090,)
baroc_neg_df = pd.concat([baroc_neg_first_df, baroc_neg_last_df], ignore_index=True)
baroc_neg_df['baroclinicity'] = baroc_neg_df['baroclinicity'] * 86400 # convert to day^-1   


zg_hat_neg_first_df = to_dataframe(zg_hat_neg_first, "GB_index", "neg", 1850, lat_slice= slice(60, 80))
zg_hat_neg_last_df  = to_dataframe(zg_hat_neg_last,  "GB_index", "neg", 2090, lat_slice= slice(60, 80))
zg_hat_neg_df = pd.concat([zg_hat_neg_first_df, zg_hat_neg_last_df], ignore_index=True)

# drop plev from zg_steady and baroc_neg
zg_hat_neg_df = zg_hat_neg_df.drop(columns=["plev"])
baroc_neg_df = baroc_neg_df.drop(columns=["plev"])

neg_df = baroc_neg_df.merge(zg_hat_neg_df, on=['event', 'time', 'phase', 'decade'], how='inner')

# %%
# ===== Density plots =====
COLOR_1850 = "#4C72B0"
COLOR_2090 = "#DD8452"

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# ----- Plot 1: pos_df, x=jet_lat, y=awb -----
sns.scatterplot(
    data = pos_df.groupby(['event', 'phase', 'decade'])[['jet_lat', 'awb']].mean().reset_index(),
    x = "jet_lat",
    y = "awb",
    alpha = 0.8,
    palette = [COLOR_1850, COLOR_2090],
    hue = "decade",
    ax = axes[0],
    sizes = 0.5,

)
axes[0].set_ylim(-0.01, 0.03)

# ----- Plot 2: neg_df, x=baroclinicity, y=cwb -----
sns.scatterplot(
    data = neg_df.groupby(['event', 'phase', 'decade'])[['baroclinicity', 'GB_index']].mean().reset_index(),
    y= "baroclinicity",
    x = "GB_index",
    alpha = 0.8,
    palette = [COLOR_1850, COLOR_2090],
    hue = "decade",
    ax = axes[1],
    sizes = 0.5,
)

# remove upper and right spines
for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

axes[0].set_xlabel("Jet Latitude (°N)")
axes[0].set_ylabel("AWB / day")
axes[1].set_xlabel("GB Index")
axes[1].set_ylabel("Baroclinicity / $day^{-1}$")
plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0after_defense/flux_composite_density.pdf")

# %%
