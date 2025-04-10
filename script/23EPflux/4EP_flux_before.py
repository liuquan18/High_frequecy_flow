# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

from src.EP_flux.EP_flux import (
    EP_flux,
    NPC_mean,
    NAL_mean,
    stat_stab,
    read_data_all,
    PlotEPfluxArrows,
)

import src.EP_flux.EP_flux as EP_flux_module
import importlib

importlib.reload(EP_flux_module)


# %%
equiv_theta = False
# %%
first_pos_upvp, first_pos_vptp, theta_first_ensmean = read_data_all(
    1850, "pos", ano=False, equiv_theta=equiv_theta
)
first_neg_upvp, first_neg_vptp, theta_first_ensmean = read_data_all(
    1850, "neg", ano=False, equiv_theta=equiv_theta
)
last_pos_upvp, last_pos_vptp, theta_last_ensmean = read_data_all(
    2090, "pos", ano=False, equiv_theta=equiv_theta
)
last_neg_upvp, last_neg_vptp, theta_last_ensmean = read_data_all(
    2090, "neg", ano=False, equiv_theta=equiv_theta
)

# %%
# dtheta / dp
stat_stab_pos_first = stat_stab(theta_first_ensmean)
stat_stab_neg_first = stat_stab(theta_first_ensmean)
stat_stab_pos_last = stat_stab(theta_last_ensmean)
stat_stab_neg_last = stat_stab(theta_last_ensmean)

# change from /ha to /hpa
stat_stab_pos_first = stat_stab_pos_first * 100
stat_stab_neg_first = stat_stab_neg_first * 100
stat_stab_pos_last = stat_stab_pos_last * 100
stat_stab_neg_last = stat_stab_neg_last * 100

# %%
# potential temperature
F_phi_pos_first, F_p_pos_first, div_pos_first = EP_flux(
    first_pos_vptp, first_pos_upvp, stat_stab_pos_first
)
F_phi_neg_first, F_p_neg_first, div_neg_first = EP_flux(
    first_neg_vptp, first_neg_upvp, stat_stab_neg_first
)
F_phi_pos_last, F_p_pos_last, div_pos_last = EP_flux(
    last_pos_vptp, last_pos_upvp, stat_stab_pos_last
)
F_phi_neg_last, F_p_neg_last, div_neg_last = EP_flux(
    last_neg_vptp, last_neg_upvp, stat_stab_neg_last
)

# %%
# NPC
F_phi_pos_first_NPC = NPC_mean(F_phi_pos_first)
F_p_pos_first_NPC = NPC_mean(F_p_pos_first)
F_phi_neg_first_NPC = NPC_mean(F_phi_neg_first)
F_p_neg_first_NPC = NPC_mean(F_p_neg_first)
F_phi_pos_last_NPC = NPC_mean(F_phi_pos_last)
F_p_pos_last_NPC = NPC_mean(F_p_pos_last)
F_phi_neg_last_NPC = NPC_mean(F_phi_neg_last)
F_p_neg_last_NPC = NPC_mean(F_p_neg_last)
# %%
div_pos_first_NPC = NPC_mean(div_pos_first)
div_neg_first_NPC = NPC_mean(div_neg_first)
div_pos_last_NPC = NPC_mean(div_pos_last)
div_neg_last_NPC = NPC_mean(div_neg_last)

# %%
# NAL
F_phi_pos_first_NAL = NAL_mean(F_phi_pos_first)
F_p_pos_first_NAL = NAL_mean(F_p_pos_first)
F_phi_neg_first_NAL = NAL_mean(F_phi_neg_first)
F_p_neg_first_NAL = NAL_mean(F_p_neg_first)
F_phi_pos_last_NAL = NAL_mean(F_phi_pos_last)
F_p_pos_last_NAL = NAL_mean(F_p_pos_last)
F_phi_neg_last_NAL = NAL_mean(F_phi_neg_last)
F_p_neg_last_NAL = NAL_mean(F_p_neg_last)
# %%
div_pos_first_NAL = NAL_mean(div_pos_first)
div_neg_first_NAL = NAL_mean(div_neg_first)
div_pos_last_NAL = NAL_mean(div_pos_last)
div_neg_last_NAL = NAL_mean(div_neg_last)

# %%
scale = 5e15
scale_div = 1e15
levels = np.arange(-5, 5.1, 0.5)
levels_div = np.arange(-0.8, 0.81, 0.1)

# %%
# plot NPC
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
lat = F_phi_pos_first.lat
plev = F_phi_pos_first.plev
# first row for first decade
div_pos_first_NPC.plot.contourf(
    ax=axes[0, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=F_phi_pos_first_NPC[:, ::3],
    ep2=F_p_pos_first_NPC[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 0],
)
div_neg_first_NPC.plot.contourf(
    ax=axes[0, 1], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=F_phi_neg_first_NPC[:, ::3],
    ep2=F_p_neg_first_NPC[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 1],
)

# third col for difference between positive and negative
div_diff_NPC = div_pos_first_NPC - div_neg_first_NPC
div_diff_NPC.plot.contourf(
    ax=axes[0, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=(F_phi_pos_first_NPC - F_phi_neg_first_NPC)[:, ::3],
    ep2=(F_p_pos_first_NPC - F_p_neg_first_NPC)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 2],
)

# second row for last decade
div_pos_last_NPC.plot.contourf(
    ax=axes[1, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=F_phi_pos_last_NPC[:, ::3],
    ep2=F_p_pos_last_NPC[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 0],
)
div_neg_last_NPC.plot.contourf(
    ax=axes[1, 1], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=F_phi_neg_last_NPC[:, ::3],
    ep2=F_p_neg_last_NPC[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 1],
)
# third col for difference between positive and negative
div_diff_NPC_last = div_pos_last_NPC - div_neg_last_NPC
div_diff_NPC_last.plot.contourf(
    ax=axes[1, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=(F_phi_pos_last_NPC - F_phi_neg_last_NPC)[:, ::3],
    ep2=(F_p_pos_last_NPC - F_p_neg_last_NPC)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 2],
)

# %%
# new plot for NAL
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
lat = F_phi_pos_first.lat
plev = F_phi_pos_first.plev
# first row for first decade
div_pos_first_NAL.plot.contourf(
    ax=axes[0, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=F_phi_pos_first_NAL[:, ::3],
    ep2=F_p_pos_first_NAL[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 0],
)
div_neg_first_NAL.plot.contourf(
    ax=axes[0, 1], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=F_phi_neg_first_NAL[:, ::3],
    ep2=F_p_neg_first_NAL[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 1],
)
# third col for difference between positive and negative
div_diff_NAL = div_pos_first_NAL - div_neg_first_NAL
div_diff_NAL.plot.contourf(
    ax=axes[0, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=(F_phi_pos_first_NAL - F_phi_neg_first_NAL)[:, ::3],
    ep2=(F_p_pos_first_NAL - F_p_neg_first_NAL)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 2],
)
# second row for last decade
div_pos_last_NAL.plot.contourf(
    ax=axes[1, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=F_phi_pos_last_NAL[:, ::3],
    ep2=F_p_pos_last_NAL[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 0],
)
div_neg_last_NAL.plot.contourf(
    ax=axes[1, 1], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=F_phi_neg_last_NAL[:, ::3],
    ep2=F_p_neg_last_NAL[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 1],
)
# third col for difference between positive and negative
div_diff_NAL_last = div_pos_last_NAL - div_neg_last_NAL
div_diff_NAL_last.plot.contourf(
    ax=axes[1, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=(F_phi_pos_last_NAL - F_phi_neg_last_NAL)[:, ::3],
    ep2=(F_p_pos_last_NAL - F_p_neg_last_NAL)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 2],
)
# %%

# new plot, only the difference, first row for first decade, second row for last decade
# first col for NPC, second col for NAL
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
# first row for first decade
div_diff_NPC.plot.contourf(
    ax=axes[0, 0], levels=levels_div, cmap="RdBu_r", add_colorbar=False, extend="both"
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=(F_phi_pos_first_NPC - F_phi_neg_first_NPC)[:, ::3],
    ep2=(F_p_pos_first_NPC - F_p_neg_first_NPC)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    ylim=[1000, 300],
    fig=fig,
    ax=axes[0, 0],
)
div_diff_NAL.plot.contourf(
    ax=axes[0, 1], levels=levels_div, cmap="RdBu_r", add_colorbar=False, extend="both"
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=(F_phi_pos_first_NAL - F_phi_neg_first_NAL)[:, ::3],
    ep2=(F_p_pos_first_NAL - F_p_neg_first_NAL)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    ylim=[1000, 300],
    fig=fig,
    ax=axes[0, 1],
)

# second row for last decade
div_diff_NPC_last.plot.contourf(
    ax=axes[1, 0], levels=levels_div, cmap="RdBu_r", add_colorbar=False, extend="both"
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=(F_phi_pos_last_NPC - F_phi_neg_last_NPC)[:, ::3],
    ep2=(F_p_pos_last_NPC - F_p_neg_last_NPC)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    ylim=[1000, 300],
    fig=fig,
    ax=axes[1, 0],
)

divergence = div_diff_NAL_last.plot.contourf(
    ax=axes[1, 1], levels=levels_div, cmap="RdBu_r", add_colorbar=False, extend="both"
)
PlotEPfluxArrows(
    x=lat[::3],
    y=plev,
    ep1=(F_phi_pos_last_NAL - F_phi_neg_last_NAL)[:, ::3],
    ep2=(F_p_pos_last_NAL - F_p_neg_last_NAL)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    ylim=[1000, 300],
    fig=fig,
    ax=axes[1, 1],
)

axes[0, 0].set_title("NPC first 10")
axes[0, 1].set_title("NAL first 10")

axes[1, 0].set_title("NPC last 10")
axes[1, 1].set_title("NAL last 10")

# no xlabel
axes[1, 0].set_xlabel("latitude")
axes[1, 1].set_xlabel("latitude")
axes[0, 0].set_xlabel("")
axes[0, 1].set_xlabel("")
axes[0, 0].set_ylabel("Pressure [hPa]")
axes[1, 0].set_ylabel("Pressure [hPa]")
axes[0, 1].set_ylabel("")
axes[1, 1].set_ylabel("")

# add new axis for colorbar at the bottom
cbar_ax = fig.add_axes([0.2, 0.1, 0.6, 0.02])
cbar = fig.colorbar(divergence, cax=cbar_ax, orientation="horizontal")
cbar.set_label(r"$ hPa / K^{-1}$")
plt.tight_layout(
    rect=[0, 0.15, 1, 1]
)  # Adjust the layout to leave space for the colorbar
# add a, b, c
for i, ax in enumerate(axes.flatten()):
    ax.text(
        0.02,
        1.02,
        f"{chr(97+i)}",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
    )
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/EP_flux.pdf",
    bbox_inches="tight",
    dpi=300,
)
# %%
