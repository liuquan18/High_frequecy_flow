# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


from src.EP_flux.EP_flux import (
    NPC_mean,
    PlotEPfluxArrows,
    NAL_mean,
)


# %%
def read_EP_flux(phase, decade, ano=False, isentrope=True, region="NPC", smooth=True):
    if isentrope:
        EP_flux_dir = (
            "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0EP_flux_isen/"
        )
    else:
        EP_flux_dir = (
            "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0EP_flux/"
        )

    F_phi = xr.open_dataarray(f"{EP_flux_dir}F_phi_{phase}_{decade}_ano{ano}.nc")
    F_p = xr.open_dataarray(f"{EP_flux_dir}F_p_{phase}_{decade}_ano{ano}.nc")
    div = xr.open_dataarray(f"{EP_flux_dir}div_{phase}_{decade}_ano{ano}.nc")

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


# %%
# Read data for NPC
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
scale = 5e17
scale_div = 5e16
levels = np.arange(-10, 10.1, 1)
levels_div = np.arange(-5, 5.1, 1)

# %%
# plot NPC
# plot NPC
fig, axes = plt.subplots(2, 3, figsize=(12, 8))

# first row for first decade
div_pos_first_NPC.plot.contourf(
    ax=axes[0, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=F_phi_pos_first_NPC.lat[::3],
    y=F_phi_pos_first_NPC.theta[::3],
    ep1=F_phi_pos_first_NPC[::3, ::3],
    ep2=F_p_pos_first_NPC[::3, ::3],
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
    x=F_phi_neg_first_NPC.lat[::3],
    y=F_phi_neg_first_NPC.theta[::3],
    ep1=F_phi_neg_first_NPC[::3, ::3],
    ep2=F_p_neg_first_NPC[::3, ::3],
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
    x=F_phi_pos_first_NPC.lat[::3],
    y=F_phi_pos_first_NPC.theta[::3],
    ep1=(F_phi_pos_first_NPC - F_phi_neg_first_NPC)[::3, ::3],
    ep2=(F_p_pos_first_NPC - F_p_neg_first_NPC)[::3, ::3],
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
    x=F_phi_pos_last_NPC.lat[::3],
    y=F_phi_pos_last_NPC.theta[::3],
    ep1=F_phi_pos_last_NPC[::3, ::3],
    ep2=F_p_pos_last_NPC[::3, ::3],
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
    x=F_phi_neg_last_NPC.lat[::3],
    y=F_phi_neg_last_NPC.theta[::3],
    ep1=F_phi_neg_last_NPC[::3, ::3],
    ep2=F_p_neg_last_NPC[::3, ::3],
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
    x=F_phi_pos_last_NPC.lat[::3],
    y=F_phi_pos_last_NPC.theta[::3],
    ep1=(F_phi_pos_last_NPC - F_phi_neg_last_NPC)[::3, ::3],
    ep2=(F_p_pos_last_NPC - F_p_neg_last_NPC)[::3, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 2],
    draw_key=True,
    key_loc=(0.7, 0.95),
)

for ax in axes.flatten():
    ax.set_ylim(280, 350)


# %%
# new plot for NAL
fig, axes = plt.subplots(2, 3, figsize=(12, 8))

# first row for first decade
div_pos_first_NAL.plot.contourf(
    ax=axes[0, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=F_phi_pos_first_NAL.lat[::3],
    y=F_phi_pos_first_NAL.theta[::3],
    ep1=F_phi_pos_first_NAL[::3, ::3],
    ep2=F_p_pos_first_NAL[::3, ::3],
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
    x=F_phi_neg_first_NAL.lat[::3],
    y=F_phi_neg_first_NAL.theta[::3],
    ep1=F_phi_neg_first_NAL[::3, ::3],
    ep2=F_p_neg_first_NAL[::3, ::3],
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
    x=F_phi_pos_first_NAL.lat[::3],
    y=F_phi_pos_first_NAL.theta[::3],
    ep1=(F_phi_pos_first_NAL - F_phi_neg_first_NAL)[::3, ::3],
    ep2=(F_p_pos_first_NAL - F_p_neg_first_NAL)[::3, ::3],
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
    x=F_phi_pos_last_NAL.lat[::3],
    y=F_phi_pos_last_NAL.theta[::3],
    ep1=F_phi_pos_last_NAL[::3, ::3],
    ep2=F_p_pos_last_NAL[::3, ::3],
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
    x=F_phi_neg_last_NAL.lat[::3],
    y=F_phi_neg_last_NAL.theta[::3],
    ep1=F_phi_neg_last_NAL[::3, ::3],
    ep2=F_p_neg_last_NAL[::3, ::3],
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
    x=F_phi_pos_last_NAL.lat[::3],
    y=F_phi_pos_last_NAL.theta[::3],
    ep1=(F_phi_pos_last_NAL - F_phi_neg_last_NAL)[::3, ::3],
    ep2=(F_p_pos_last_NAL - F_p_neg_last_NAL)[::3, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 2],
    draw_key=True,
    key_loc=(0.7, 0.95),
)

for ax in axes.flatten():
    ax.set_ylim(280, 350)

# %%
# new plot, only the difference, first row for first decade, second row for last decade
# first col for NPC, second col for NAL
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
# first row for first decade
div_diff_NPC.plot.contourf(
    ax=axes[0, 0],
    levels=levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
)
PlotEPfluxArrows(
    x=F_phi_pos_first_NPC.lat[::3],
    y=F_phi_pos_first_NPC.theta[::5],
    ep1=(F_phi_pos_first_NPC - F_phi_neg_first_NPC)[::5, ::3],
    ep2=(F_p_pos_first_NPC - F_p_neg_first_NPC)[::5, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 0],
    draw_key=True,
    key_loc=(0.1, 0.05),
)
div_diff_NAL.plot.contourf(
    ax=axes[0, 1],
    levels=levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
)
PlotEPfluxArrows(
    x=F_phi_pos_first_NAL.lat[::3],
    y=F_phi_pos_first_NAL.theta[::5],
    ep1=(F_phi_pos_first_NAL - F_phi_neg_first_NAL)[::5, ::3],
    ep2=(F_p_pos_first_NAL - F_p_neg_first_NAL)[::5, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 1],
)
# second row for last decade
div_diff_NPC_last.plot.contourf(
    ax=axes[1, 0],
    levels=levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
)
PlotEPfluxArrows(
    x=F_phi_pos_last_NPC.lat[::3],
    y=F_phi_pos_last_NPC.theta[::5],
    ep1=(F_phi_pos_last_NPC - F_phi_neg_last_NPC)[::5, ::3],
    ep2=(F_p_pos_last_NPC - F_p_neg_last_NPC)[::5, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 0],
)
div_map = div_diff_NAL_last.plot.contourf(
    ax=axes[1, 1],
    levels=levels_div,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
)
PlotEPfluxArrows(
    x=F_phi_pos_last_NAL.lat[::3],
    y=F_phi_pos_last_NAL.theta[::5],
    ep1=(F_phi_pos_last_NAL - F_phi_neg_last_NAL)[::5, ::3],
    ep2=(F_p_pos_last_NAL - F_p_neg_last_NAL)[::5, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 1],
)
for ax in axes.flatten():
    ax.set_ylim(285, 345)
    ax.set_xlim(0, 85)
    ax.set_xlabel("lat / °N")
    ax.set_ylabel(r"$\Theta_e$ / K")


# add colorbar
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = fig.colorbar(
    div_map,
    cax=cbar_ax,
    orientation="vertical",
)

# add a, b, c
for i, ax in enumerate(axes.flatten()):
    ax.text(
        0.02,
        0.95,
        f"{chr(97+i)}",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
    )

plt.tight_layout(rect=[0, 0, 0.9, 1])  # Leave space on the right for the colorbar
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/EP_flux_isentropes_diff.pdf", dpi=300, bbox_inches="tight")
# %%
