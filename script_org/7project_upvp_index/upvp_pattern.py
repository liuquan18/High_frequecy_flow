# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line, map_smooth, NA_box
from src.plotting.util import lon2x
from matplotlib.ticker import ScalarFormatter
import src.data_helper.read_variable as read_variable

from src.plotting.util import clip_map
import matplotlib.colors as mcolors
import cartopy
import glob
import matplotlib.ticker as mticker

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# %%
import src.plotting.util as util

import importlib

importlib.reload(read_variable)
importlib.reload(util)
# %%
from src.data_helper.read_variable import read_climatology
from src.data_helper.read_composite import read_comp_var
from matplotlib.patches import Rectangle

from src.data_helper import read_composite

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div

# %%%
# config
time_window = (-10, 5)
suffix = "_ano"
remove_zonmean = False

# %%
# read transient EP flux for positive and negative phase
# read data for first decade with region = western
_, _, Tdivphi_pos_first, Tdiv_p_pos_first = read_EP_flux(
    phase="pos",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
    time_window = (-10, 5)
)
_, _, Tdivphi_neg_first, Tdiv_p_neg_first = read_EP_flux(
    phase="neg",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
    time_window = (-10, 5)
)

# %%
# read climatological EP flux
_, _, Tdivphi_clima_first, Tdiv_p_clima_first = (
    read_EP_flux(
        phase="clima",
        decade=1850,
        eddy="transient",
        ano=False,
        lon_mean=False,
        region=None,
    )
)
# %%
Tdivphi_pos_first_ano = Tdivphi_pos_first - Tdivphi_clima_first
Tdivphi_neg_first_ano = Tdivphi_neg_first - Tdivphi_clima_first

# %%

pattern = (Tdivphi_pos_first_ano.mean(dim = 'event') - Tdivphi_neg_first_ano.mean(dim = 'event'))/2
# %%
pattern = pattern.sel(plev = 25000)
# %%
pattern.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/Fdiv_phi_pattern/Fdiv_phi_pattern_1850.nc")
# %%
