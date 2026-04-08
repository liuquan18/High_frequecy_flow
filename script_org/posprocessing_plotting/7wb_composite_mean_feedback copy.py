# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import cmocean
import os


from src.data_helper import read_composite
from src.data_helper.read_variable import read_climatology
import importlib
import matplotlib
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

from src.plotting.util import map_smooth
import src.plotting.util as util

importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var


# %%
MODEL_DIR = "MPI_GE_CMIP6_allplev"


def _read_all(var_name, name=None, method="no_stat", chunks=None):
    """Read pos/neg x 1850/2090 composites.

    Returns a dict keyed by '{phase}_{decade}', e.g. 'pos_1850'.
    """
    kwargs = dict(time_window="all", model_dir=MODEL_DIR)
    if method is not None:
        kwargs["method"] = method
    if name is not None:
        kwargs["name"] = name
    if chunks is not None:
        kwargs["chunks"] = chunks
    return {
        f"{phase}_{decade}": read_comp_var(var_name, phase, decade, **kwargs).mean(dim = 'isen_level', skipna=True)
        for phase in ("pos", "neg")
        for decade in (1850, 2090)
    }


#%%
# Wave breaking (isen_level summed lazily to avoid OOM on large 5-D arrays)
awb = _read_all("wb_anticyclonic_allisen", name="smooth_pv", chunks=None)
#%%
cwb = _read_all("wb_cyclonic_allisen", name="smooth_pv", chunks=None)


#%%
def _zonal_mean(da, lon_min=-90, lon_max=40):
    """Zonal mean over [lon_min, lon_max], handling both 0-360 and -180-180 grids."""
    if da.lon.max() > 180:
        # Convert 0-360 to -180-180
        da = da.assign_coords(lon=(da.lon + 180) % 360 - 180).sortby("lon")
    return da.sel(lon=slice(lon_min, lon_max)).mean(dim="lon")

# %% Save all variables to 0composite_feedback

save_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0composite_feedback"
os.makedirs(save_dir, exist_ok=True)

awb_to_save = {
    "wb_anticyclonic_pos_1850":       awb["pos_1850"],
    "wb_anticyclonic_neg_1850":       awb["neg_1850"],
    "wb_anticyclonic_pos_2090":       awb["pos_2090"],
    "wb_anticyclonic_neg_2090":       awb["neg_2090"],
}
# awb_lon_slice = slice(-60, 30)
# cwb_lon_slice = slice(-120, -30)

# awb save
for fname, da in awb_to_save.items():
    path = os.path.join(save_dir, f"{fname}.nc")
    _zonal_mean(da, lon_min=-60, lon_max=30).to_netcdf(path)
    print(f"Saved {path}")

#%%
cwb_to_save = {
    "wb_cyclonic_pos_1850":          cwb["pos_1850"],
    "wb_cyclonic_neg_1850":          cwb["neg_1850"],
    "wb_cyclonic_pos_2090":          cwb["pos_2090"],
    "wb_cyclonic_neg_2090":          cwb["neg_2090"],
}

#%%
for fname, da in cwb_to_save.items():
    path = os.path.join(save_dir, f"{fname}.nc")
    _zonal_mean(da, lon_min=-120, lon_max=-30).to_netcdf(path)
    print(f"Saved {path}")
# %%

