# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


import src.EP_flux.EP_flux as EP_flux_module
import importlib
from src.EP_flux.EP_flux import (
    EP_flux,
    NPC_mean,
    PlotEPfluxArrows,
    NAL_mean,)
#%%
# read all the above isentrope data
read_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0EP_flux_isen/"
F_phi_pos_first = xr.open_dataarray(read_dir + "F_phi_pos_first.nc")
F_p_pos_first = xr.open_dataarray(read_dir + "F_p_pos_first.nc")
F_phi_neg_first = xr.open_dataarray(read_dir + "F_phi_neg_first.nc")
F_p_neg_first = xr.open_dataarray(read_dir + "F_p_neg_first.nc")
F_phi_pos_last = xr.open_dataarray(read_dir + "F_phi_pos_last.nc")
F_p_pos_last = xr.open_dataarray(read_dir + "F_p_pos_last.nc")
F_phi_neg_last = xr.open_dataarray(read_dir + "F_phi_neg_last.nc")
F_p_neg_last = xr.open_dataarray(read_dir + "F_p_neg_last.nc")
div_pos_first = xr.open_dataarray(read_dir + "div_pos_first.nc")
div_neg_first = xr.open_dataarray(read_dir + "div_neg_first.nc")
div_pos_last = xr.open_dataarray(read_dir + "div_pos_last.nc")
div_neg_last = xr.open_dataarray(read_dir + "div_neg_last.nc")


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
scale = 1e17
scale_div = 1e16
levels = np.arange(-5, 5.1, 0.5)
levels_div = np.arange(-0.8, 0.81, 0.1)

# %%
# plot NPC
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
lat = F_phi_pos_first.lat
theta = F_phi_pos_first.theta
# first row for first decade
div_pos_first_NPC.T.plot.contourf(
    ax=axes[0, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y =theta,
    ep1=F_phi_pos_first_NPC[::3],
    ep2=F_p_pos_first_NPC[::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 0],
)
div_neg_first_NPC.T.plot.contourf(
    ax=axes[0, 1], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=theta,
    ep1=F_phi_neg_first_NPC[::3],
    ep2=F_p_neg_first_NPC[::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 1],
)

# third col for difference between positive and negative
div_diff_NPC = div_pos_first_NPC - div_neg_first_NPC
div_diff_NPC.T.plot.contourf(
    ax=axes[0, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=theta,
    ep1=(F_phi_pos_first_NPC - F_phi_neg_first_NPC)[::3],
    ep2=(F_p_pos_first_NPC - F_p_neg_first_NPC)[::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 2],
)

# second row for last decade
div_pos_last_NPC.T.plot.contourf(
    ax=axes[1, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=F_phi_pos_last_NPC.lat[::3],
    y=F_phi_pos_last_NPC.theta,
    ep1=F_phi_pos_last_NPC[::3],
    ep2=F_p_pos_last_NPC[::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 0],
)
div_neg_last_NPC.T.plot.contourf(
    ax=axes[1, 1], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=F_phi_neg_last_NPC.lat[::3],
    y=F_phi_neg_last_NPC.theta,
    ep1=F_phi_neg_last_NPC[::3],
    ep2=F_p_neg_last_NPC[::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 1],
)
# third col for difference between positive and negative
div_diff_NPC_last = div_pos_last_NPC - div_neg_last_NPC
div_diff_NPC_last.T.plot.contourf(
    ax=axes[1, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
diff = F_phi_pos_last_NPC - F_phi_neg_last_NPC
PlotEPfluxArrows(
    x=diff.lat[::3],
    y=diff.theta,
    ep1=(F_phi_pos_last_NPC - F_phi_neg_last_NPC)[::3],
    ep2=(F_p_pos_last_NPC - F_p_neg_last_NPC)[::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 2],
)

for ax in axes.flat:
    # invert y axis
    ax.invert_yaxis()

# %%
# new plot for NAL
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
lat = F_phi_pos_first.lat
theta = F_phi_pos_first.theta
# first row for first decade
div_pos_first_NAL.T.plot.contourf(
    ax=axes[0, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=theta,
    ep1=F_phi_pos_first_NAL[::3],
    ep2=F_p_pos_first_NAL[::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 0],
)
div_neg_first_NAL.T.plot.contourf(
    ax=axes[0, 1], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=theta,
    ep1=F_phi_neg_first_NAL[::3],
    ep2=F_p_neg_first_NAL[::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 1],
)
# third col for difference between positive and negative
div_diff_NAL = div_pos_first_NAL - div_neg_first_NAL
div_diff_NAL.T.plot.contourf(
    ax=axes[0, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=lat[::3],
    y=theta,
    ep1=(F_phi_pos_first_NAL - F_phi_neg_first_NAL)[::3],
    ep2=(F_p_pos_first_NAL - F_p_neg_first_NAL)[::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[0, 2],
)

# second row for last decade
div_pos_last_NAL.T.plot.contourf(
    ax=axes[1, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=F_phi_pos_last_NAL.lat[::3],
    y=F_phi_pos_last_NAL.theta,
    ep1=F_phi_pos_last_NAL[::3],
    ep2=F_p_pos_last_NAL[::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 0],
)
div_neg_last_NAL.T.plot.contourf(
    ax=axes[1, 1], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=F_phi_neg_last_NAL.lat[::3],
    y=F_phi_neg_last_NAL.theta,
    ep1=F_phi_neg_last_NAL[::3],
    ep2=F_p_neg_last_NAL[::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 1],
)
# third col for difference between positive and negative
div_diff_NAL_last = div_pos_last_NAL - div_neg_last_NAL
div_diff_NAL_last.T.plot.contourf(
    ax=axes[1, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
diff = F_phi_pos_last_NAL - F_phi_neg_last_NAL
PlotEPfluxArrows(
    x=diff.lat[::3],
    y=diff.theta,
    ep1=(F_phi_pos_last_NAL - F_phi_neg_last_NAL)[::3],
    ep2=(F_p_pos_last_NAL - F_p_neg_last_NAL)[::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    fig=fig,
    ax=axes[1, 2],
)
for ax in axes.flat:
    # invert y axis
    ax.invert_yaxis()
# %%

# new plot, only the difference, first row for first decade, second row for last decade
# first col for NPC, second col for NAL
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
# first row for first decade
div_diff_NPC.plot.T.contourf(
    ax=axes[0, 0], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
diff_pos_first = F_phi_pos_first_NPC - F_phi_neg_first_NPC
PlotEPfluxArrows(
    x=diff_pos_first.lat[::3],
    y =diff_pos_first.theta,
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
div_diff_NAL.plot.T.contourf(
    ax=axes[0, 1], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
diff_pos_first_NAL = F_phi_pos_first_NAL - F_phi_neg_first_NAL
PlotEPfluxArrows(
    x=diff_pos_first_NAL.lat[::3],
    y =diff_pos_first_NAL.theta,
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
div_diff_NPC_last.T.plot.contourf(
    ax=axes[1, 0], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
diff_pos_last = F_phi_pos_last_NPC - F_phi_neg_last_NPC
PlotEPfluxArrows(
    x=diff_pos_last.lat[::3],
    y =diff_pos_last.theta,
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

divergence = div_diff_NAL_last.T.plot.contourf(
    ax=axes[1, 1], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
diff_pos_last_NAL = F_phi_pos_last_NAL - F_phi_neg_last_NAL
PlotEPfluxArrows(
    x=diff_pos_last_NAL.lat[::3],
    y =diff_pos_last_NAL.theta,
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
cbar.set_label(r"$ hPa \: K^{-1}$")
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
# plt.savefig(
#     "/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/moist_EP_flux.pdf",
#     bbox_inches="tight",
#     dpi=300,
# )
# %%
