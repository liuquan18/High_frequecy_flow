# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

from src.EP_flux.EP_flux import EP_flux, PlotEPfluxArrows
from src.prime.prime_data import read_composite_MPI

import src.EP_flux.EP_flux as EP_flux_module
import importlib
importlib.reload(EP_flux_module)

# %%
def read_data_all(decade, phase, ano = False, before = '15_5', equiv_theta = False):
    """
    Read data for the specified decade and phase.
    Parameters:
    - decade: Decade to read data for (e.g., 1850, 2090).
    - phase: Phase to read data for (e.g., 'pos', 'neg').
    - ano: Boolean indicating whether to read anomaly data.
    - equiv_theta: Boolean indicating whether to read equivalent theta data.
    Returns:
    - upvp: u'v' data.
    - vptp: v't' data.
    - theta_ensmean: Ensemble mean of theta data.
    """
    upvp = read_composite_MPI("upvp", "ua", decade = decade, before = before, return_as=phase, ano=ano)
    if equiv_theta:
        vptp = read_composite_MPI("vpetp", "vpetp", decade = decade, before = before, return_as=phase, ano=ano)
        theta_ensmean = xr.open_dataset(
            "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/equiv_theta_monthly_ensmean/equiv_theta_monmean_ensmean_185005_185909.nc").etheta
    else:
        vptp = read_composite_MPI("vptp", "vptp", decade = decade, before = before, return_as=phase, ano=ano)
        theta_ensmean = xr.open_dataset(
            "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/theta_monthly_ensmean/theta_monmean_ensmean_185005_185909.nc").theta
    return upvp, vptp, theta_ensmean

def NPC_mean(arr):
    return arr.sel(lon = slice(120, 240)).mean(dim = 'lon')

def NAL_mean(arr):
    return arr.sel(lon = slice(270, 330)).mean(dim = 'lon')

# %%
equiv_theta = False
#%%
first_pos_upvp, first_pos_vptp, theta_first_ensmean = read_data_all(1850, 'pos', ano = False, equiv_theta=equiv_theta)
first_neg_upvp, first_neg_vptp, theta_first_ensmean = read_data_all(1850, 'neg', ano = False, equiv_theta=equiv_theta)
last_pos_upvp, last_pos_vptp, theta_last_ensmean = read_data_all(2090, 'pos', ano = False, equiv_theta=equiv_theta)
last_neg_upvp, last_neg_vptp, theta_last_ensmean = read_data_all(2090, 'neg', ano = False, equiv_theta=equiv_theta)

#%%
# potential temperature
F_phi_pos_first, F_p_pos_first, div_pos_first = EP_flux(first_pos_vptp, first_pos_upvp, theta_first_ensmean)
F_phi_neg_first, F_p_neg_first, div_neg_first = EP_flux(first_neg_vptp, first_neg_upvp, theta_first_ensmean)
F_phi_pos_last, F_p_pos_last, div_pos_last = EP_flux(last_pos_vptp, last_pos_upvp, theta_last_ensmean)
F_phi_neg_last, F_p_neg_last, div_neg_last = EP_flux(last_neg_vptp, last_neg_upvp, theta_last_ensmean)

#%%

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
