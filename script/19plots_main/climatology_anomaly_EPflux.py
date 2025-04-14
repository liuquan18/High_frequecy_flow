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

import importlib

importlib.reload(util)
# %%
from src.prime.prime_data import read_composite_MPI  # noqa: E402
from src.prime.prime_data import read_MPI_GE_uhat
from src.EP_flux.EP_flux import (
    NPC_mean,
    PlotEPfluxArrows,
    NAL_mean,
)
#%%
# %%
def read_EP_flux(decade, phase, ano=True, isentrope=True, region="NPC", smooth = True):
    if isentrope:
        EP_flux_dir = (
            "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0EP_flux_isen/"
        )
    else:
        EP_flux_dir = (
            "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0EP_flux/"
        )

    if ano:
        F_phi = xr.open_dataarray(f"{EP_flux_dir}F_phi_{phase}_{decade}_ano{ano}.nc")
        F_p = xr.open_dataarray(f"{EP_flux_dir}F_p_{phase}_{decade}_ano{ano}.nc")
        div = xr.open_dataarray(f"{EP_flux_dir}div_{phase}_{decade}_ano{ano}.nc")
    else:
        F_phi = xr.open_dataarray(f"{EP_flux_dir}F_phi_{decade}_ensmean.nc")
        F_p = xr.open_dataarray(f"{EP_flux_dir}F_p_{decade}_ensmean.nc")
        div = xr.open_dataarray(f"{EP_flux_dir}div_{decade}_ensmean.nc")

    if region == "NPC":
        F_phi = NPC_mean(F_phi)
        F_p = NPC_mean(F_p)
        div = NPC_mean(div)

    elif region == "NAL":
        F_phi = NAL_mean(F_phi)
        F_p = NAL_mean(F_p)
        div = NAL_mean(div)
    if smooth:
        div = div.rolling(theta=3).mean()

    return F_phi, F_p, div

#%%
# read anoamly data

F_phi_pos_first_NPC, F_p_pos_first_NPC, div_pos_first_NPC = read_EP_flux(
    phase="pos", decade=1850, region="NPC"
)
F_phi_neg_first_NPC, F_p_neg_first_NPC, div_neg_first_NPC = read_EP_flux(
    phase="neg", decade=1850, region="NPC"
)
F_phi_pos_last_NPC, F_p_pos_last_NPC, div_pos_last_NPC = read_EP_flux(
    phase="pos", decade=2090, region="NPC"
)
F_phi_neg_last_NPC, F_p_neg_last_NPC, div_neg_last_NPC = read_EP_flux(
    phase="neg", decade=2090, region="NPC"
)

# %%
# Read data for NAL
F_phi_pos_first_NAL, F_p_pos_first_NAL, div_pos_first_NAL = read_EP_flux(
    phase="pos", decade=1850, region="NAL"
)
F_phi_neg_first_NAL, F_p_neg_first_NAL, div_neg_first_NAL = read_EP_flux(
    phase="neg", decade=1850, region="NAL"
)
F_phi_pos_last_NAL, F_p_pos_last_NAL, div_pos_last_NAL = read_EP_flux(
    phase="pos", decade=2090, region="NAL"
)
F_phi_neg_last_NAL, F_p_neg_last_NAL, div_neg_last_NAL = read_EP_flux(
    phase="neg", decade=2090, region="NAL"
)


# %%
# read ensemble mean data
F_phi_first_NPC, F_p_first_NPC, div_first_NPC = read_EP_flux(
    decade=1850, phase = None, region="NPC", ano=False, isentrope=True
)

F_phi_last_NPC, F_p_last_NPC, div_last_NPC = read_EP_flux(
    decade=2090, phase = None, region="NPC", ano=False, isentrope=True
)
#%%
F_phi_first_NAL, F_p_first_NAL, div_first_NAL = read_EP_flux(
    decade=1850, phase = None, region="NAL", ano=False, isentrope=True
)   
F_phi_last_NAL, F_p_last_NAL, div_last_NAL = read_EP_flux(
    decade=2090, phase = None, region="NAL", ano=False, isentrope=True
)

# %%

# %%
scale = 2e15
scale_div = 5e15
levels = np.arange(-5, 5.1, 0.5)
levels_div = np.arange(-0.5, 0.51, 0.05)

# %%
# plot NPC
# plot NPC
fig, axes = plt.subplots(2, 3, figsize=(12, 8))

# first row first ten years,
# first column ensemble mean
div_first_NPC.plot.contourf(
    ax=axes[0, 0],
    cmap="RdBu_r",
    levels=levels_div,
    add_colorbar=False,
    extend="both",
)

ensmean_arrow = PlotEPfluxArrows(
    x = F_phi_first_NPC.lat[::3],
    y = F_phi_first_NPC.theta[::3],
    ep1 = F_phi_first_NPC[::3, ::3],
    ep2 = F_p_first_NPC[::3, ::3],
    xscale='linear',
    yscale='linear',
    scale=scale,
    xlim = [0, 85],
    fig=fig,
    ax=axes[0, 0],
    draw_key = True,
    key_loc = (0.15, 0.05)
)

# second column for positive anomaly
div_pos_first_NPC.plot.contourf(
    ax=axes[0, 1],
    cmap="RdBu_r",
    levels=levels_div,
    add_colorbar=False,
    extend="both",
)
ano_arrow = PlotEPfluxArrows(
    x = F_phi_pos_first_NPC.lat[::3],
    y = F_phi_pos_first_NPC.theta[::3],
    ep1 = F_phi_pos_first_NPC[::3, ::3],
    ep2 = F_p_pos_first_NPC[::3, ::3],
    xscale='linear',
    yscale='linear',
    scale=scale_div,
    xlim = [0, 85],
    fig=fig,
    ax=axes[0, 1],
    draw_key = True,
    key_loc = (0.15, 0.05)
)

# third column for negative anomaly
div_neg_first_NPC.plot.contourf(
    ax=axes[0, 2],
    cmap="RdBu_r",
    levels=levels_div,
    add_colorbar=False,
    extend="both",
)
PlotEPfluxArrows(
    x = F_phi_neg_first_NPC.lat[::3],
    y = F_phi_neg_first_NPC.theta[::3],
    ep1 = F_phi_neg_first_NPC[::3, ::3],
    ep2 = F_p_neg_first_NPC[::3, ::3],
    xscale='linear',
    yscale='linear',
    scale=scale_div,
    xlim = [0, 85],
    fig=fig,
    ax=axes[0, 2],
    draw_key = True,
    key_loc = (0.15, 0.05)
)

# second row for last 10 years
# first column ensemble mean
div_last_NPC.plot.contourf(
    ax=axes[1, 0],
    cmap="RdBu_r",
    levels=levels_div,
    add_colorbar=False,
    extend="both",
)

PlotEPfluxArrows(
    x = F_phi_last_NPC.lat[::3],
    y = F_phi_last_NPC.theta[::3],
    ep1 = F_phi_last_NPC[::3, ::3],
    ep2 = F_p_last_NPC[::3, ::3],
    xscale='linear',
    yscale='linear',
    scale=scale,
    xlim = [0, 85],
    fig=fig,
    ax=axes[1, 0],
    draw_key = True,
    key_loc = (0.15, 0.05)
)

# second column for positive anomaly
div_pos_last_NPC.plot.contourf(
    ax=axes[1, 1],
    cmap="RdBu_r",
    levels=levels_div,
    add_colorbar=False,
    extend="both",
)
PlotEPfluxArrows(
    x = F_phi_pos_last_NPC.lat[::3],
    y = F_phi_pos_last_NPC.theta[::3],
    ep1 = F_phi_pos_last_NPC[::3, ::3],
    ep2 = F_p_pos_last_NPC[::3, ::3],
    xscale='linear',
    yscale='linear',
    scale=scale_div,
    xlim = [0, 85],
    fig=fig,
    ax=axes[1, 1],
    draw_key = True,
    key_loc = (0.15, 0.05)
)

# third column for negative anomaly
div_map = div_neg_last_NPC.plot.contourf(
    ax=axes[1, 2],
    cmap="RdBu_r",
    levels=levels_div,
    add_colorbar=False,
    extend="both",
)
PlotEPfluxArrows(
    x = F_phi_neg_last_NPC.lat[::3],
    y = F_phi_neg_last_NPC.theta[::3],
    ep1 = F_phi_neg_last_NPC[::3, ::3],
    ep2 = F_p_neg_last_NPC[::3, ::3],
    xscale='linear',
    yscale='linear',
    scale=scale_div,
    xlim = [0, 85],
    fig=fig,
    ax=axes[1, 2],
    draw_key = True,
    key_loc = (0.15, 0.05)
)
for ax in axes.flatten():
    ax.set_ylim(285, 345)
    ax.set_xlim(0, 85)
    ax.set_xlabel("lat / °N")
    ax.set_ylabel("")

# plot quiver key for axes [0,0]


axes[0, 0].set_ylabel(r"$\theta_e / K$")
axes[1, 0].set_ylabel(r"$\theta_e / K$")

# add colorbar
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = fig.colorbar(
    div_map,
    cax=cbar_ax,
    orientation="vertical",
)

plt.tight_layout(rect=[0, 0, 0.9, 1])  # Leave space on the right for the colorbar

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/EP_flux_clim_ano_NPC.png", dpi=300)
# %%
# plot NAL
fig, axes = plt.subplots(2, 3, figsize=(12, 8))

# first row first ten years,
# first column ensemble mean
div_first_NAL.plot.contourf(
    ax=axes[0, 0],
    cmap="RdBu_r",
    levels=levels_div,
    add_colorbar=False,
    extend="both",
)

ensmean_arrow = PlotEPfluxArrows(
    x = F_phi_first_NAL.lat[::3],
    y = F_phi_first_NAL.theta[::3],
    ep1 = F_phi_first_NAL[::3, ::3],
    ep2 = F_p_first_NAL[::3, ::3],
    xscale='linear',
    yscale='linear',
    scale=scale,
    xlim = [0, 85],
    fig=fig,
    ax=axes[0, 0],
    draw_key = True,
    key_loc = (0.15, 0.05)
)

# second column for positive anomaly
div_pos_first_NAL.plot.contourf(
    ax=axes[0, 1],
    cmap="RdBu_r",
    levels=levels_div,
    add_colorbar=False,
    extend="both",
)
ano_arrow = PlotEPfluxArrows(
    x = F_phi_pos_first_NAL.lat[::3],
    y = F_phi_pos_first_NAL.theta[::3],
    ep1 = F_phi_pos_first_NAL[::3, ::3],
    ep2 = F_p_pos_first_NAL[::3, ::3],
    xscale='linear',
    yscale='linear',
    scale=scale_div,
    xlim = [0, 85],
    fig=fig,
    ax=axes[0, 1],
    draw_key = True,
    key_loc = (0.15, 0.05)
)

# third column for negative anomaly
div_neg_first_NAL.plot.contourf(
    ax=axes[0, 2],
    cmap="RdBu_r",
    levels=levels_div,
    add_colorbar=False,
    extend="both",
)
PlotEPfluxArrows(
    x = F_phi_neg_first_NAL.lat[::3],
    y = F_phi_neg_first_NAL.theta[::3],
    ep1 = F_phi_neg_first_NAL[::3, ::3],
    ep2 = F_p_neg_first_NAL[::3, ::3],
    xscale='linear',
    yscale='linear',
    scale=scale_div,
    xlim = [0, 85],
    fig=fig,
    ax=axes[0, 2],
    draw_key = True,
    key_loc = (0.15, 0.05)
)

# second row for last 10 years
# first column ensemble mean
div_last_NAL.plot.contourf(
    ax=axes[1, 0],
    cmap="RdBu_r",
    levels=levels_div,
    add_colorbar=False,
    extend="both",
)

PlotEPfluxArrows(
    x = F_phi_last_NAL.lat[::3],
    y = F_phi_last_NAL.theta[::3],
    ep1 = F_phi_last_NAL[::3, ::3],
    ep2 = F_p_last_NAL[::3, ::3],
    xscale='linear',
    yscale='linear',
    scale=scale,
    xlim = [0, 85],
    fig=fig,
    ax=axes[1, 0],
    draw_key = True,
    key_loc = (0.15, 0.05)
)

# second column for positive anomaly
div_pos_last_NAL.plot.contourf(
    ax=axes[1, 1],
    cmap="RdBu_r",
    levels=levels_div,
    add_colorbar=False,
    extend="both",
)
PlotEPfluxArrows(
    x = F_phi_pos_last_NAL.lat[::3],
    y = F_phi_pos_last_NAL.theta[::3],
    ep1 = F_phi_pos_last_NAL[::3, ::3],
    ep2 = F_p_pos_last_NAL[::3, ::3],
    xscale='linear',
    yscale='linear',
    scale=scale_div,
    xlim = [0, 85],
    fig=fig,
    ax=axes[1, 1],
    draw_key = True,
    key_loc = (0.15, 0.05)
)

# third column for negative anomaly
div_map = div_neg_last_NAL.plot.contourf(
    ax=axes[1, 2],
    cmap="RdBu_r",
    levels=levels_div,
    add_colorbar=False,
    extend="both",
)
PlotEPfluxArrows(
    x = F_phi_neg_last_NAL.lat[::3],
    y = F_phi_neg_last_NAL.theta[::3],
    ep1 = F_phi_neg_last_NAL[::3, ::3],
    ep2 = F_p_neg_last_NAL[::3, ::3],
    xscale='linear',
    yscale='linear',
    scale=scale_div,
    xlim = [0, 85],
    fig=fig,
    ax=axes[1, 2],
    draw_key = True,
    key_loc = (0.15, 0.05)
)
for ax in axes.flatten():
    ax.set_ylim(285, 345)
    ax.set_xlim(0, 85)
    ax.set_xlabel("lat / °N")
    ax.set_ylabel("")

axes[0, 0].set_ylabel(r"$\theta_e / K$")
axes[1, 0].set_ylabel(r"$\theta_e / K$")

# add colorbar
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = fig.colorbar(
    div_map,
    cax=cbar_ax,
    orientation="vertical",
)

plt.tight_layout(rect=[0, 0, 0.9, 1])  # Leave space on the right for the colorbar

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/EP_flux_clim_ano_NAL.png", dpi=300)
# %%
