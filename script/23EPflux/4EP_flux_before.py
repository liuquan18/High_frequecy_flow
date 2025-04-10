# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

from src.EP_flux.EP_flux import EP_flux, PlotEPfluxArrows, stat_stab
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
        
    # check if the 'plev' coordinate is in Pa and convert to hPa
    if 'plev' in vptp.coords and vptp['plev'].max() > 1000:
        vptp = vptp.assign_coords(plev=vptp['plev'] / 100)
    if 'plev' in upvp.coords and upvp['plev'].max() > 1000:
        upvp = upvp.assign_coords(plev=upvp['plev'] / 100)
    if 'plev' in theta_ensmean.coords and theta_ensmean['plev'].max() > 1000:
        theta_ensmean = theta_ensmean.assign_coords(plev=theta_ensmean['plev'] / 100)
        
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
# dtheta / dp
stat_stab_pos_first = stat_stab(theta_first_ensmean)
stat_stab_neg_first = stat_stab(theta_first_ensmean)
stat_stab_pos_last = stat_stab(theta_last_ensmean)
stat_stab_neg_last = stat_stab(theta_last_ensmean)


#%%
# potential temperature
F_phi_pos_first, F_p_pos_first, div_pos_first = EP_flux(first_pos_vptp, first_pos_upvp, stat_stab_pos_first)
F_phi_neg_first, F_p_neg_first, div_neg_first = EP_flux(first_neg_vptp, first_neg_upvp, stat_stab_neg_first)
F_phi_pos_last, F_p_pos_last, div_pos_last = EP_flux(last_pos_vptp, last_pos_upvp, stat_stab_pos_last)
F_phi_neg_last, F_p_neg_last, div_neg_last = EP_flux(last_neg_vptp, last_neg_upvp, stat_stab_neg_last)

#%%
# NPC
F_phi_pos_first_NPC = NPC_mean(F_phi_pos_first)
F_p_pos_first_NPC = NPC_mean(F_p_pos_first)
F_phi_neg_first_NPC = NPC_mean(F_phi_neg_first)
F_p_neg_first_NPC = NPC_mean(F_p_neg_first)
F_phi_pos_last_NPC = NPC_mean(F_phi_pos_last)
F_p_pos_last_NPC = NPC_mean(F_p_pos_last)
F_phi_neg_last_NPC = NPC_mean(F_phi_neg_last)
F_p_neg_last_NPC = NPC_mean(F_p_neg_last)
#%%
div_pos_first_NPC = NPC_mean(div_pos_first)
div_neg_first_NPC = NPC_mean(div_neg_first)
div_pos_last_NPC = NPC_mean(div_pos_last)
div_neg_last_NPC = NPC_mean(div_neg_last)

#%%
# NAL
F_phi_pos_first_NAL = NAL_mean(F_phi_pos_first)
F_p_pos_first_NAL = NAL_mean(F_p_pos_first)
F_phi_neg_first_NAL = NAL_mean(F_phi_neg_first)
F_p_neg_first_NAL = NAL_mean(F_p_neg_first)
F_phi_pos_last_NAL = NAL_mean(F_phi_pos_last)
F_p_pos_last_NAL = NAL_mean(F_p_pos_last)
F_phi_neg_last_NAL = NAL_mean(F_phi_neg_last)
F_p_neg_last_NAL = NAL_mean(F_p_neg_last)
#%%
div_pos_first_NAL = NAL_mean(div_pos_first)
div_neg_first_NAL = NAL_mean(div_neg_first)
div_pos_last_NAL = NAL_mean(div_pos_last)
div_neg_last_NAL = NAL_mean(div_neg_last)
# %%
# plot NPC
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
lat = F_phi_pos_first.lat
plev = F_phi_pos_first.plev
# first row for first decade
div_pos_first_NPC.plot.contourf(
    ax=axes[0, 0], levels=np.arange(-2, 2.1, 0.1), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=F_phi_pos_first_NPC[:, ::3],
    ep2=F_p_pos_first_NPC[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e15,
    xlim=[0, 90],
    fig=fig, ax=axes[0, 0],
)
div_neg_first_NPC.plot.contourf(
    ax=axes[0, 1], levels=np.arange(-2, 2.1, 0.1), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=F_phi_neg_first_NPC[:, ::3],
    ep2=F_p_neg_first_NPC[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e15,
    xlim=[0, 90],
    fig=fig, ax=axes[0, 1],
)

# third col for difference between positive and negative
div_diff_NPC = div_pos_first_NPC - div_neg_first_NPC
div_diff_NPC.plot.contourf(
    ax=axes[0, 2], levels=np.arange(-0.5, 0.6, 0.05), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=(F_phi_pos_first_NPC - F_phi_neg_first_NPC)[:, ::3],
    ep2=(F_p_pos_first_NPC - F_p_neg_first_NPC)[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e14,
    xlim=[0, 90],
    fig=fig, ax=axes[0, 2],
)

# second row for last decade
div_pos_last_NPC.plot.contourf(
    ax=axes[1, 0], levels=np.arange(-2, 2.1, 0.1), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=F_phi_pos_last_NPC[:, ::3],
    ep2=F_p_pos_last_NPC[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e15,
    xlim=[0, 90],
    fig=fig, ax=axes[1, 0],
)
div_neg_last_NPC.plot.contourf(
    ax=axes[1, 1], levels=np.arange(-2, 2.1, 0.1), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=F_phi_neg_last_NPC[:, ::3],
    ep2=F_p_neg_last_NPC[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e15,
    xlim=[0, 90],
    fig=fig, ax=axes[1, 1],
)
# third col for difference between positive and negative
div_diff_NPC_last = div_pos_last_NPC - div_neg_last_NPC
div_diff_NPC_last.plot.contourf(
    ax=axes[1, 2], levels=np.arange(-0.5, 0.6, 0.05), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=(F_phi_pos_last_NPC - F_phi_neg_last_NPC)[:, ::3],
    ep2=(F_p_pos_last_NPC - F_p_neg_last_NPC)[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e14,
    xlim=[0, 90],
    fig=fig, ax=axes[1, 2],
)

#%%
# new plot for NAL
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
lat = F_phi_pos_first.lat
plev = F_phi_pos_first.plev
# first row for first decade
div_pos_first_NAL.plot.contourf(
    ax=axes[0, 0], levels=np.arange(-2, 2.1, 0.1), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=F_phi_pos_first_NAL[:, ::3],
    ep2=F_p_pos_first_NAL[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e15,
    xlim=[0, 90],
    fig=fig, ax=axes[0, 0],
)
div_neg_first_NAL.plot.contourf(
    ax=axes[0, 1], levels=np.arange(-2, 2.1, 0.1), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=F_phi_neg_first_NAL[:, ::3],
    ep2=F_p_neg_first_NAL[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e15,
    xlim=[0, 90],
    fig=fig, ax=axes[0, 1],
)
# third col for difference between positive and negative
div_diff_NAL = div_pos_first_NAL - div_neg_first_NAL
div_diff_NAL.plot.contourf(
    ax=axes[0, 2], levels=np.arange(-0.5, 0.6, 0.05), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=(F_phi_pos_first_NAL - F_phi_neg_first_NAL)[:, ::3],
    ep2=(F_p_pos_first_NAL - F_p_neg_first_NAL)[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e14,
    xlim=[0, 90],
    fig=fig, ax=axes[0, 2],
)
# second row for last decade
div_pos_last_NAL.plot.contourf(
    ax=axes[1, 0], levels=np.arange(-2, 2.1, 0.1), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=F_phi_pos_last_NAL[:, ::3],
    ep2=F_p_pos_last_NAL[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e15,
    xlim=[0, 90],
    fig=fig, ax=axes[1, 0],
)
div_neg_last_NAL.plot.contourf(
    ax=axes[1, 1], levels=np.arange(-2, 2.1, 0.1), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=F_phi_neg_last_NAL[:, ::3],
    ep2=F_p_neg_last_NAL[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e15,
    xlim=[0, 90],
    fig=fig, ax=axes[1, 1],
)
# third col for difference between positive and negative
div_diff_NAL_last = div_pos_last_NAL - div_neg_last_NAL
div_diff_NAL_last.plot.contourf(
    ax=axes[1, 2], levels=np.arange(-0.5, 0.6, 0.05), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=(F_phi_pos_last_NAL - F_phi_neg_last_NAL)[:, ::3],
    ep2=(F_p_pos_last_NAL - F_p_neg_last_NAL)[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e14,
    xlim=[0, 90],
    fig=fig, ax=axes[1, 2],
)
# %%

# new plot, only the difference, first row for first decade, second row for last decade
# first col for NPC, second col for NAL
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
# first row for first decade
div_diff_NPC.plot.contourf(
    ax=axes[0, 0], levels=np.arange(-0.5, 0.6, 0.05), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=(F_phi_pos_first_NPC - F_phi_neg_first_NPC)[:, ::3],
    ep2=(F_p_pos_first_NPC - F_p_neg_first_NPC)[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e14,
    xlim=[0, 90],ylim = [1000, 500],
    fig=fig, ax=axes[0, 0],
)
div_diff_NAL.plot.contourf(
    ax=axes[0, 1], levels=np.arange(-0.5, 0.6, 0.05), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=(F_phi_pos_first_NAL - F_phi_neg_first_NAL)[:, ::3],
    ep2=(F_p_pos_first_NAL - F_p_neg_first_NAL)[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e14,
    xlim=[0, 90],ylim = [1000, 500],
    fig=fig, ax=axes[0, 1],
)

# second row for last decade
div_diff_NPC_last.plot.contourf(
    ax=axes[1, 0], levels=np.arange(-0.5, 0.6, 0.05), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=(F_phi_pos_last_NPC - F_phi_neg_last_NPC)[:, ::3],
    ep2=(F_p_pos_last_NPC - F_p_neg_last_NPC)[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e14,
    xlim=[0, 90],ylim = [1000, 500],
    fig=fig, ax=axes[1, 0],
)

div_diff_NAL_last.plot.contourf(
    ax=axes[1, 1], levels=np.arange(-0.5, 0.6, 0.05), cmap='RdBu_r', add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3], y=plev,
    ep1=(F_phi_pos_last_NAL - F_phi_neg_last_NAL)[:, ::3],
    ep2=(F_p_pos_last_NAL - F_p_neg_last_NAL)[:, ::3],
    xscale='linear',
    yscale='linear',
    scale=5e14,
    xlim=[0, 90],ylim = [1000, 500],
    fig=fig, ax=axes[1, 1],
)
plt.tight_layout()
# %%
