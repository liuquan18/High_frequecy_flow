# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line
from src.plotting.util import lon2x
from matplotlib.ticker import ScalarFormatter
from src.prime.prime_data import vert_integrate

import matplotlib.colors as mcolors
import cartopy
import glob

# %%
import src.plotting.util as util
import src.moisture.longitudinal_contrast as lc
from src.EP_flux.EP_flux import EP_flux, PlotEPfluxArrows

import src.EP_flux.EP_flux as EP_flux_module
import importlib
importlib.reload(EP_flux_module)

# %%
from src.prime.prime_data import read_composite_MPI

# %%
# u'v' -15, 5 days before
upvp_pos_first = read_composite_MPI("upvp", "ua", 1850, '15_5', 'pos', False)
upvp_pos_last = read_composite_MPI("upvp", "ua", 2090, '15_5', 'pos', False)

# neg
upvp_neg_first = read_composite_MPI("upvp", "ua", 1850, '15_5', 'neg', False)
upvp_neg_last = read_composite_MPI("upvp", "ua", 2090, '15_5', 'neg', False)
#%%
# v't' -15 - 5 days before
vptp_pos_first = read_composite_MPI("vptp", "vptp", 1850, '15_5', 'pos', False)
vptp_pos_last = read_composite_MPI("vptp", "vptp", 2090, '15_5', 'pos', False)

vptp_neg_first = read_composite_MPI("vptp", "vptp", 1850, '15_5', 'neg', False)
vptp_neg_last = read_composite_MPI("vptp", "vptp", 2090, '15_5', 'neg', False)
# %%
# ensmean
# etheta_first_ensmean = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/equiv_theta_monthly_ensmean/equiv_theta_monmean_ensmean_185005_185909.nc")
# etheta_last_ensmean = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/equiv_theta_monthly_ensmean/equiv_theta_monmean_ensmean_209005_209909.nc")

# etheta_first_ensmean = etheta_first_ensmean.etheta
# etheta_last_ensmean = etheta_last_ensmean.etheta

#%%
theta_first_ensmean = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/theta_monthly_ensmean/theta_monmean_ensmean_185005_185909.nc")
theta_last_ensmean = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/theta_monthly_ensmean/theta_monmean_ensmean_209005_209909.nc")
theta_first_ensmean = theta_first_ensmean.theta
theta_last_ensmean = theta_last_ensmean.theta
# %%
F_phi_pos_first, F_p_pos_first, div1_pos_first, div2_pos_first = EP_flux(vptp_pos_first, upvp_pos_first, theta_first_ensmean)

#%%
F_phi_pos_first['plev'] = F_phi_pos_first['plev'] / 100
F_p_pos_first['plev'] = F_p_pos_first['plev'] / 100
div1_pos_first['plev'] = div1_pos_first['plev'] / 100
div2_pos_first['plev'] = div2_pos_first['plev'] / 100
# %%
fig, axes = plt.subplots(2,2, figsize = (12, 8))
lat = F_phi_pos_first.lat
plev = F_phi_pos_first.plev
PlotEPfluxArrows(x = lat, y = plev,
                 ep1=F_phi_pos_first.mean(dim = 'lon'),
                    ep2=F_p_pos_first.mean(dim = 'lon'),
                    fig=fig, ax=axes[0,0],)
# %%
