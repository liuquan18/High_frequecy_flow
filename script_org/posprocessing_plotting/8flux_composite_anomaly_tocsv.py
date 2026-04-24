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
awb_pos_first = _load("wb_anticyclonic_pos_1850")
awb_neg_first = _load("wb_anticyclonic_neg_1850")
awb_pos_last  = _load("wb_anticyclonic_pos_2090")
awb_neg_last  = _load("wb_anticyclonic_neg_2090")

#%%
cwb_pos_first = _load("wb_cyclonic_pos_1850")
cwb_neg_first = _load("wb_cyclonic_neg_1850")
cwb_pos_last  = _load("wb_cyclonic_pos_2090")
cwb_neg_last  = _load("wb_cyclonic_neg_2090")

#%%

# Convergence of eddy momentum flux
Fdiv_transient_pos_first = _load("Fdiv_phi_transient_pos_1850")
Fdiv_transient_neg_first = _load("Fdiv_phi_transient_neg_1850")
Fdiv_transient_pos_last  = _load("Fdiv_phi_transient_pos_2090")
Fdiv_transient_neg_last  = _load("Fdiv_phi_transient_neg_2090")

#%%
Fdiv_steady_pos_first = _load("Fdiv_phi_steady_pos_1850")
Fdiv_steady_neg_first = _load("Fdiv_phi_steady_neg_1850")
Fdiv_steady_pos_last  = _load("Fdiv_phi_steady_pos_2090")
Fdiv_steady_neg_last  = _load("Fdiv_phi_steady_neg_2090")

#%%
# eke
eke_pos_first = _load("eke_pos_1850")
eke_neg_first = _load("eke_neg_1850")
eke_pos_last  = _load("eke_pos_2090")
eke_neg_last  = _load("eke_neg_2090")
#%%
eke_high_pos_first = _load("eke_high_pos_1850")
eke_high_neg_first = _load("eke_high_neg_1850")
eke_high_pos_last  = _load("eke_high_pos_2090")
eke_high_neg_last  = _load("eke_high_neg_2090")
#%%
# baroclinic growth rate
baroc_pos_first = _load("eady_growth_rate_pos_1850")
baroc_neg_first = _load("eady_growth_rate_neg_1850")
baroc_pos_last  = _load("eady_growth_rate_pos_2090")
baroc_neg_last  = _load("eady_growth_rate_neg_2090")

#%%
# eddy thermal feedback transient
transient_eddy_heat_d2y2_pos_first = _load("transient_eddy_heat_d2y2_pos_1850")
transient_eddy_heat_d2y2_neg_first = _load("transient_eddy_heat_d2y2_neg_1850")
transient_eddy_heat_d2y2_pos_last  = _load("transient_eddy_heat_d2y2_pos_2090")
transient_eddy_heat_d2y2_neg_last  = _load("transient_eddy_heat_d2y2_neg_2090")

#%%
# eddy thermal feedback steady
steady_eddy_heat_d2y2_pos_first = _load("steady_eddy_heat_d2y2_pos_1850")
steady_eddy_heat_d2y2_neg_first = _load("steady_eddy_heat_d2y2_neg_1850")
steady_eddy_heat_d2y2_pos_last  = _load("steady_eddy_heat_d2y2_pos_2090")
steady_eddy_heat_d2y2_neg_last  = _load("steady_eddy_heat_d2y2_neg_2090")

#%%
# select levels

transient_eddy_heat_d2y2_pos_first = transient_eddy_heat_d2y2_pos_first.sel(plev=85000)
transient_eddy_heat_d2y2_neg_first = transient_eddy_heat_d2y2_neg_first.sel(plev=85000)
transient_eddy_heat_d2y2_pos_last  = transient_eddy_heat_d2y2_pos_last.sel(plev=85000)
transient_eddy_heat_d2y2_neg_last  = transient_eddy_heat_d2y2_neg_last.sel(plev=85000)

steady_eddy_heat_d2y2_pos_first = steady_eddy_heat_d2y2_pos_first.sel(plev=85000)
steady_eddy_heat_d2y2_neg_first = steady_eddy_heat_d2y2_neg_first.sel(plev=85000)
steady_eddy_heat_d2y2_pos_last  = steady_eddy_heat_d2y2_pos_last.sel(plev=85000)
steady_eddy_heat_d2y2_neg_last  = steady_eddy_heat_d2y2_neg_last.sel(plev=85000)


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

#%%#%%
Fdiv_transient_pos_first_df = to_dataframe(Fdiv_transient_pos_first, "Fdiv_transient", "pos", 1850, )
Fdiv_transient_neg_first_df = to_dataframe(Fdiv_transient_neg_first, "Fdiv_transient", "neg", 1850, )
Fdiv_transient_pos_last_df  = to_dataframe(Fdiv_transient_pos_last,  "Fdiv_transient", "pos", 2090, )
Fdiv_transient_neg_last_df  = to_dataframe(Fdiv_transient_neg_last,  "Fdiv_transient", "neg", 2090, )

Fdiv_steady_pos_first_df = to_dataframe(Fdiv_steady_pos_first, "Fdiv_steady", "pos", 1850, )
Fdiv_steady_neg_first_df = to_dataframe(Fdiv_steady_neg_first, "Fdiv_steady", "neg", 1850, )
Fdiv_steady_pos_last_df  = to_dataframe(Fdiv_steady_pos_last,  "Fdiv_steady", "pos", 2090, )
Fdiv_steady_neg_last_df  = to_dataframe(Fdiv_steady_neg_last,  "Fdiv_steady", "neg", 2090, )

#%%
eke_pos_first_df = to_dataframe(eke_pos_first, "eke", "pos", 1850, lat_slice=slice(40, 70))
eke_neg_first_df = to_dataframe(eke_neg_first, "eke", "neg", 1850, lat_slice=slice(40, 70))
eke_pos_last_df  = to_dataframe(eke_pos_last,  "eke", "pos", 2090, lat_slice=slice(40, 70))
eke_neg_last_df  = to_dataframe(eke_neg_last,  "eke", "neg", 2090, lat_slice=slice(40, 70))

eke_high_pos_first_df = to_dataframe(eke_high_pos_first, "eke_high", "pos", 1850, lat_slice=slice(50, 70))
eke_high_neg_first_df = to_dataframe(eke_high_neg_first, "eke_high", "neg", 1850, lat_slice=slice(50, 70))
eke_high_pos_last_df  = to_dataframe(eke_high_pos_last,  "eke_high", "pos", 2090, lat_slice=slice(50, 70))
eke_high_neg_last_df  = to_dataframe(eke_high_neg_last,  "eke_high", "neg", 2090, lat_slice=slice(50, 70))

baroc_pos_first_df = to_dataframe(baroc_pos_first, "baroclinicity", "pos", 1850, )
baroc_neg_first_df = to_dataframe(baroc_neg_first, "baroclinicity", "neg", 1850, )
baroc_pos_last_df  = to_dataframe(baroc_pos_last,  "baroclinicity", "pos", 2090, )
baroc_neg_last_df  = to_dataframe(baroc_neg_last,  "baroclinicity", "neg", 2090, )

#%%
transient_eddy_heat_d2y2_pos_first_df = to_dataframe(transient_eddy_heat_d2y2_pos_first, "transient_eddy_heat_d2y2", "pos", 1850, )
transient_eddy_heat_d2y2_neg_first_df = to_dataframe(transient_eddy_heat_d2y2_neg_first, "transient_eddy_heat_d2y2", "neg", 1850, )
transient_eddy_heat_d2y2_pos_last_df  = to_dataframe(transient_eddy_heat_d2y2_pos_last,  "transient_eddy_heat_d2y2", "pos", 2090, )
transient_eddy_heat_d2y2_neg_last_df  = to_dataframe(transient_eddy_heat_d2y2_neg_last,  "transient_eddy_heat_d2y2", "neg", 2090, )

steady_eddy_heat_d2y2_pos_first_df = to_dataframe(steady_eddy_heat_d2y2_pos_first, "steady_eddy_heat_d2y2", "pos", 1850, )
steady_eddy_heat_d2y2_neg_first_df = to_dataframe(steady_eddy_heat_d2y2_neg_first, "steady_eddy_heat_d2y2", "neg", 1850, )   
steady_eddy_heat_d2y2_pos_last_df  = to_dataframe(steady_eddy_heat_d2y2_pos_last,  "steady_eddy_heat_d2y2", "pos", 2090, )
steady_eddy_heat_d2y2_neg_last_df  = to_dataframe(steady_eddy_heat_d2y2_neg_last,  "steady_eddy_heat_d2y2", "neg", 2090, )
#%%
# save the above dataframes for plotting
save_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pd/non_anomaly"
os.makedirs(save_dir, exist_ok=True)
_to_save = {
    # "Fdiv_transient_pos_first_df": Fdiv_transient_pos_first_df,
    # "Fdiv_transient_neg_first_df": Fdiv_transient_neg_first_df,
    # "Fdiv_transient_pos_last_df":  Fdiv_transient_pos_last_df,
    # "Fdiv_transient_neg_last_df":  Fdiv_transient_neg_last_df,
    # "Fdiv_steady_pos_first_df": Fdiv_steady_pos_first_df,
    # "Fdiv_steady_neg_first_df": Fdiv_steady_neg_first_df,
    # "Fdiv_steady_pos_last_df":  Fdiv_steady_pos_last_df,
    # "Fdiv_steady_neg_last_df":  Fdiv_steady_neg_last_df,
    # "eke_pos_first_df": eke_pos_first_df,
    # "eke_neg_first_df": eke_neg_first_df,
    # "eke_pos_last_df":  eke_pos_last_df,
    # "eke_neg_last_df":  eke_neg_last_df,
    "eke_high_pos_first_df": eke_high_pos_first_df,
    "eke_high_neg_first_df": eke_high_neg_first_df,
    "eke_high_pos_last_df":  eke_high_pos_last_df,
    "eke_high_neg_last_df":  eke_high_neg_last_df,
    # "baroc_pos_first_df": baroc_pos_first_df,
    # "baroc_neg_first_df": baroc_neg_first_df,
    # "baroc_pos_last_df":  baroc_pos_last_df,
    # "baroc_neg_last_df":  baroc_neg_last_df,
    # "transient_eddy_heat_d2y2_pos_first_df": transient_eddy_heat_d2y2_pos_first_df,
    # "transient_eddy_heat_d2y2_neg_first_df": transient_eddy_heat_d2y2_neg_first_df,
    # "transient_eddy_heat_d2y2_pos_last_df": transient_eddy_heat_d2y2_pos_last_df,
    # "transient_eddy_heat_d2y2_neg_last_df": transient_eddy_heat_d2y2_neg_last_df,
    # "steady_eddy_heat_d2y2_pos_first_df": steady_eddy_heat_d2y2_pos_first_df,
    # "steady_eddy_heat_d2y2_neg_first_df": steady_eddy_heat_d2y2_neg_first_df,
    # "steady_eddy_heat_d2y2_pos_last_df": steady_eddy_heat_d2y2_pos_last_df,
    # "steady_eddy_heat_d2y2_neg_last_df": steady_eddy_heat_d2y2_neg_last_df,
}
for name, df in _to_save.items():
    df.to_csv(os.path.join(save_dir, f"{name}.csv"), index=False)

# %%
