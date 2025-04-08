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
F_phi_neg_first, F_p_neg_first, div1_neg_first, div2_neg_first = EP_flux(vptp_neg_first, upvp_neg_first, theta_first_ensmean)

#%%
div1 = div1_pos_first
div2 = div2_pos_first
Div = div1 + div2

div1_neg = div1_neg_first
div2_neg = div2_neg_first
Div_neg = div1_neg + div2_neg
# %%
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
lat = F_phi_pos_first.lat
plev = F_phi_pos_first.plev

# Positive case
Div.mean(dim='lon').plot.contourf(ax=axes[0, 0], levels=np.arange(-2, 2.1, 0.1), cmap='RdBu_r', add_colorbar=False)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=F_phi_pos_first.mean(dim='lon')[:, ::3],
    ep2=F_p_pos_first.mean(dim='lon')[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e15,
    xlim=[0, 90],
    fig=fig, ax=axes[0, 0],
)

# Negative case
Div_neg.mean(dim='lon').plot.contourf(ax=axes[0, 1], levels=np.arange(-2, 2.1, 0.1), cmap='RdBu_r', add_colorbar=False)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=F_phi_neg_first.mean(dim='lon')[:, ::3],
    ep2=F_p_neg_first.mean(dim='lon')[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e15,
    xlim=[0, 90],
    fig=fig, ax=axes[0, 1],
)

# Difference between positive and negative
Div_diff = Div - Div_neg
Div_diff.mean(dim='lon').plot.contourf(ax=axes[1, 0], levels=np.arange(-0.5, 0.6, 0.05), cmap='RdBu_r', add_colorbar=False)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=(F_phi_pos_first - F_phi_neg_first).mean(dim='lon')[:, ::3],
    ep2=(F_p_pos_first - F_p_neg_first).mean(dim='lon')[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=1e14,
    xlim=[0, 90],
    fig=fig, ax=axes[1, 0],
)
# %%
F_phi = F_phi_pos_first
F_p = F_p_pos_first

#%%
F = xr.Dataset({'F_phi': F_phi, 'F_p': F_p})
F = F.mean(dim = 'lon')
#%%

#%%
fig, ax = plt.subplots(figsize = (12, 8))

ax.quiver(
    F.lat,
    F.plev,
    F.F_phi,
    F.F_p,
)
ax.set_ylim(1000, 200)
# %%
