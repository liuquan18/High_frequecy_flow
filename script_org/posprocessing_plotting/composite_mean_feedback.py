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


# Jet stream
#%%
ua_pos_first = read_comp_var(
    "ua",
    "pos",
    1850,
    time_window=(0, 20),
    method="no_stat",
    name="ua",
    model_dir="MPI_GE_CMIP6_allplev",
)
ua_neg_first = read_comp_var(
    "ua",
    "neg",
    1850,
    time_window=(0, 20),
    method="no_stat",
    name="ua",
    model_dir="MPI_GE_CMIP6_allplev",
)

ua_pos_last = read_comp_var(
    "ua",
    "pos",
    2090,
    time_window=(0, 20),
    method="no_stat",
    name="ua",
    model_dir="MPI_GE_CMIP6_allplev",
)
ua_neg_last = read_comp_var(
    "ua",
    "neg",
    2090,
    time_window=(0, 20),
    method="no_stat",
    name="ua",
    model_dir="MPI_GE_CMIP6_allplev",
)

## convergence of eddy momentum flux
#%%
momentum_pos_first = read_comp_var(
    "Fdiv_phi_transient",
    "pos",
    1850,
    time_window=(0, 20),
    method="no_stat",
    name = 'div',
    model_dir="MPI_GE_CMIP6_allplev",
)
momentum_neg_first = read_comp_var(
    "Fdiv_phi_transient",
    "neg",
    1850,
    time_window=(0, 20),
    method="no_stat",
    name = 'div',
    model_dir="MPI_GE_CMIP6_allplev",
)

momentum_pos_last = read_comp_var(
    "Fdiv_phi_transient",
    "pos",
    2090,
    time_window=(0, 20),
    method="no_stat",
    name = 'div',
    model_dir="MPI_GE_CMIP6_allplev",
)
momentum_neg_last = read_comp_var(
    "Fdiv_phi_transient",
    "neg",
    2090,
    time_window=(0, 20),
    method="no_stat",
    name="div",
    model_dir="MPI_GE_CMIP6_allplev",
)


## baroclinicity
# %%
baroc_pos_first = read_comp_var(
    "eady_growth_rate",
    "pos",
    1850,
    time_window=(0, 20),
    method="no_stat",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
baroc_neg_first = read_comp_var(
    "eady_growth_rate",
    "neg",
    1850,
    time_window=(0, 20),
    method="no_stat",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
baroc_pos_last = read_comp_var(
    "eady_growth_rate",
    "pos",
    2090,
    time_window=(0, 20),
    method="no_stat",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
baroc_neg_last = read_comp_var(
    "eady_growth_rate",
    "neg",
    2090,
    time_window=(0, 20),
    method="no_stat",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)


## steady eddies/ blocking
# %%
steady_pos_first = read_comp_var(
    "zg_steady",
    "pos",
    1850,
    time_window=(0, 20),
    name="zg",
    model_dir = 'MPI_GE_CMIP6_allplev'
)

steady_neg_first = read_comp_var(
    "zg_steady",
    "neg",
    1850,
    time_window=(0, 20),
    name="zg",
    model_dir = 'MPI_GE_CMIP6_allplev'
)

steady_pos_last = read_comp_var(
    "zg_steady",
    "pos",
    2090,
    time_window=(0, 20),
    name="zg",
    model_dir = 'MPI_GE_CMIP6_allplev'
)

steady_neg_last = read_comp_var(
    "zg_steady",
    "neg",
    2090,
    time_window=(0, 20),
    name="zg",
    model_dir = 'MPI_GE_CMIP6_allplev'
)
# %%
vsts_pos_first = read_comp_var(
    "vsets",
    "pos",
    1850,
    time_window=(0, 20),
    method="no_stat",
    name="vsets",
    model_dir="MPI_GE_CMIP6_allplev",
)
vsts_neg_first = read_comp_var(
    "vsets",
    "neg",
    1850,
    time_window=(0, 20),
    method="no_stat",
    name="vsets",
    model_dir="MPI_GE_CMIP6_allplev",
)
vsts_pos_last = read_comp_var(
    "vsets",
    "pos",
    2090,
    time_window=(0, 20),
    method="no_stat",
    name="vsets",
    model_dir="MPI_GE_CMIP6_allplev",
)
vsts_neg_last = read_comp_var(
    "vsets",
    "neg",
    2090,
    time_window=(0, 20),
    method="no_stat",
    name="vsets",
    model_dir="MPI_GE_CMIP6_allplev",
)

#%%

vstsdy_pos_first = read_comp_var(
    "steady_eddy_heat_dy",
    "pos",
    1850,
    time_window="all",
    method="no_stat",
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)
vstsdy_neg_first = read_comp_var(
    "steady_eddy_heat_dy",
    "neg",
    1850,
    time_window="all",
    method="no_stat",
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)
vstsdy_pos_last = read_comp_var(
    "steady_eddy_heat_dy",
    "pos",
    2090,
    time_window="all",
    method="no_stat",
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)
vstsdy_neg_last = read_comp_var(
    "steady_eddy_heat_dy",
    "neg",
    2090,
    time_window="all",
    method="no_stat",
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)

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

_to_save = {
    "ua_pos_1850":               ua_pos_first,
    "ua_neg_1850":               ua_neg_first,
    "ua_pos_2090":               ua_pos_last,
    "ua_neg_2090":               ua_neg_last,
    "Fdiv_phi_transient_pos_1850": momentum_pos_first,
    "Fdiv_phi_transient_neg_1850": momentum_neg_first,
    "Fdiv_phi_transient_pos_2090": momentum_pos_last,
    "Fdiv_phi_transient_neg_2090": momentum_neg_last,
    "eady_growth_rate_pos_1850": baroc_pos_first,
    "eady_growth_rate_neg_1850": baroc_neg_first,
    "eady_growth_rate_pos_2090": baroc_pos_last,
    "eady_growth_rate_neg_2090": baroc_neg_last,
    "zg_steady_pos_1850":        steady_pos_first,
    "zg_steady_neg_1850":        steady_neg_first,
    "zg_steady_pos_2090":        steady_pos_last,
    "zg_steady_neg_2090":        steady_neg_last,
    "vsets_pos_1850":            vsts_pos_first,
    "vsets_neg_1850":            vsts_neg_first,
    "vsets_pos_2090":            vsts_pos_last,
    "vsets_neg_2090":            vsts_neg_last,
    "steady_eddy_heat_dy_pos_1850": vstsdy_pos_first,
    "steady_eddy_heat_dy_neg_1850": vstsdy_neg_first,
    "steady_eddy_heat_dy_pos_2090": vstsdy_pos_last,
    "steady_eddy_heat_dy_neg_2090": vstsdy_neg_last,
}

for fname, da in _to_save.items():
    path = os.path.join(save_dir, f"{fname}.nc")
    _zonal_mean(da).to_netcdf(path)
    print(f"Saved {path}")

# %%

