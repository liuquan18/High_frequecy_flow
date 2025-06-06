# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


from src.dynamics.EP_flux import PlotEPfluxArrows
from src.data_helper import read_composite

import importlib
importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux


# %%
scale = 3e16
scale_div = 1e15
levels = np.arange(-20, 20.1, 5)
levels_div = np.arange(-3, 3.1, 0.5)
# %%
# read transient EP flux for positive and negative phase
# read data for first decade with region = western
Tphi_pos_first, Tp_pos_first, Tdivphi_pos_first, Tdiv_p_pos_first = read_EP_flux(
    phase="pos", decade=1850, eddy="transient", ano=False,lon_mean=True,
)
Tphi_neg_first, Tp_neg_first, Tdivphi_neg_first, Tdiv_p_neg_first = read_EP_flux(
    phase="neg", decade=1850, eddy="transient", ano=False,lon_mean=True,
)


# last decade region
Tphi_pos_last, Tp_pos_last, Tdivphi_pos_last, Tdiv_p_pos_last = read_EP_flux(
    phase="pos", decade=2090, eddy="transient", ano=False,lon_mean=True,
)
Tphi_neg_last, Tp_neg_last, Tdivphi_neg_last, Tdiv_p_neg_last = read_EP_flux(
    phase="neg", decade=2090, eddy="transient", ano=False,lon_mean=True,
)

#%% 
# read steady EP flux for positive and negative phase
Sphi_pos_first, Sp_pos_first, Sdivphi_pos_first, Sdiv_p_pos_first = read_EP_flux(
    phase="pos", decade=1850, eddy="steady", ano=False,lon_mean=True,
)
Sphi_neg_first, Sp_neg_first, Sdivphi_neg_first, Sdiv_p_neg_first = read_EP_flux(
    phase="neg", decade=1850, eddy="steady", ano=False,lon_mean=True,
)

# last decade 
Sphi_pos_last, Sp_pos_last, Sdivphi_pos_last, Sdiv_p_pos_last = read_EP_flux(
    phase="pos", decade=2090, eddy="steady", ano=False,lon_mean=True,
)
Sphi_neg_last, Sp_neg_last, Sdivphi_neg_last, Sdiv_p_neg_last = read_EP_flux(
    phase="neg", decade=2090, eddy="steady", ano=False,lon_mean=True,
)


# %%
# transient eddies
fig, axes = plt.subplots(2, 3, figsize=(12, 8), sharey=True, sharex=True)
# first row for first decade

# first col for positive phase
(Tdivphi_pos_first + Tdiv_p_pos_first).plot.contourf(
    ax=axes[0, 0], levels=levels, cmap="RdBu_r", add_colorbar=False,
    ylim = [100000, 10000],
    xlim = [0,90],
)
PlotEPfluxArrows(
    x=Tphi_pos_first.lat[::3],
    y=Tphi_pos_first.plev,
    ep1=Tphi_pos_first[:, ::3],
    ep2=Tp_pos_first[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 90],
    ylim=[100000, 10000],
    fig=fig,
    ax=axes[0, 0],
    draw_key=True,
    key_loc=(0.7, 0.95),
)
# second col for negative phase
(Tdivphi_neg_first + Tdiv_p_neg_first).plot.contourf(
    ax=axes[0, 1], levels=levels, cmap="RdBu_r", add_colorbar=False,
    ylim = [100000, 10000],
    xlim = [0,90],
)
PlotEPfluxArrows(
    x=Tphi_neg_first.lat[::3],
    y=Tphi_neg_first.plev,
    ep1=Tphi_neg_first[:, ::3],
    ep2=Tp_neg_first[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 90],
    ylim=[100000, 10000],
    fig=fig,
    ax=axes[0, 1],
    draw_key=True,
    key_loc=(0.7, 0.95),
)
# third col for difference between positive and negative
Tdiv_diff_first = (Tdivphi_pos_first - Tdivphi_neg_first) + (Tdiv_p_pos_first - Tdiv_p_neg_first)
Tdiv_diff_first.plot.contourf(
    ax=axes[0, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False,
    ylim = [100000, 10000],
    xlim = [0,90],
)
PlotEPfluxArrows(
    x=Tphi_pos_first.lat[::3],
    y=Tphi_pos_first.plev,
    ep1=(Tphi_pos_first - Tphi_neg_first)[:, ::3],
    ep2=(Tp_pos_first - Tp_neg_first)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 90],
    ylim=[100000, 10000],
    fig=fig,
    ax=axes[0, 2],
    draw_key=True,
    key_loc=(0.7, 0.95),
)

# second row for last decade
# first col for positive phase
pos_color = (Tdivphi_pos_last + Tdiv_p_pos_last).plot.contourf(
    ax=axes[1, 0], levels=levels, cmap="RdBu_r", add_colorbar=False,
    ylim = [100000, 10000],
    xlim = [0,90],
)
PlotEPfluxArrows(
    x=Tphi_pos_last.lat[::3],
    y=Tphi_pos_last.plev,
    ep1=Tphi_pos_last[:, ::3],
    ep2=Tp_pos_last[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 90],
    ylim=[100000, 10000],
    fig=fig,
    ax=axes[1, 0],
)
# second col for negative phase
neg_color = (Tdivphi_neg_last + Tdiv_p_neg_last).plot.contourf(
    ax=axes[1, 1], levels=levels, cmap="RdBu_r", add_colorbar=False,
    ylim = [100000, 10000],
    xlim = [0,90],
)
PlotEPfluxArrows(
    x=Tphi_neg_last.lat[::3],
    y=Tphi_neg_last.plev,
    ep1=Tphi_neg_last[:, ::3],
    ep2=Tp_neg_last[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 90],
    ylim=[100000, 10000],
    fig=fig,
    ax=axes[1, 1],
)
# third col for difference between positive and negative
Tdiv_diff_last = (Tdivphi_pos_last - Tdivphi_neg_last) + (Tdiv_p_pos_last - Tdiv_p_neg_last)
diff_color = Tdiv_diff_last.plot.contourf(
    ax=axes[1, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False,
    ylim = [100000, 10000],
    xlim = [0,90],
)
PlotEPfluxArrows(
    x=Tphi_pos_last.lat[::3],
    y=Tphi_pos_last.plev,
    ep1=(Tphi_pos_last - Tphi_neg_last)[:, ::3],
    ep2=(Tp_pos_last - Tp_neg_last)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 90],
    ylim=[100000, 10000],
    fig=fig,
    ax=axes[1, 2],
)

# add cax under the second row

fig.colorbar(
    pos_color,
    ax=axes[:, 0],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"$\nabla \cdot \mathcal{F}$ [m$^2$ s$^{-2}$]",
)

fig.colorbar(
    neg_color,
    ax=axes[:, 1],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"$\nabla \cdot \mathcal{F}$ [m$^2$ s$^{-2}$]",
)

fig.colorbar(
    diff_color,
    ax=axes[:, 2],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"diff $\nabla \cdot \mathcal{F}$ [m$^2$ s$^{-2}$]",
)

# no y labels from second row on, no x labels at the frist row
for ax in axes[0, :]:
    ax.set_xlabel("")
for ax in axes[:, 0]:
    ax.set_ylabel("Pressure [Pa]")

for ax in axes[:, 1:].flat:
    ax.set_ylabel("")

for ax in axes[1, :]:
    ax.set_xlabel("Latitude [°N]")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0EP_flux/transient_EP_flux.pdf",
    bbox_inches="tight",
    dpi=300,
)


# %%
# steady eddies
fig, axes = plt.subplots(2, 3, figsize=(12, 8), sharey=True, sharex=True)
# first row for first decade

# first col for positive phase
(Sdivphi_pos_first + Sdiv_p_pos_first).plot.contourf(
    ax=axes[0, 0], levels=levels, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
)
PlotEPfluxArrows(
    x=Sphi_pos_first.lat[::3],
    y=Sphi_pos_first.plev,
    ep1=Sphi_pos_first[:, ::3],
    ep2=Sp_pos_first[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 90],
    ylim=[100000, 10000],
    fig=fig,
    ax=axes[0, 0],
    draw_key=True,
    key_loc=(0.7, 0.95),
)
# second col for negative phase
(Sdivphi_neg_first + Sdiv_p_neg_first).plot.contourf(
    ax=axes[0, 1], levels=levels, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
)
PlotEPfluxArrows(
    x=Sphi_neg_first.lat[::3],
    y=Sphi_neg_first.plev,
    ep1=Sphi_neg_first[:, ::3],
    ep2=Sp_neg_first[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 90],
    ylim=[100000, 10000],
    fig=fig,
    ax=axes[0, 1],
    draw_key=True,
    key_loc=(0.7, 0.95),
)
# third col for difference between positive and negative
Sdiv_diff_first = (Sdivphi_pos_first - Sdivphi_neg_first) + (Sdiv_p_pos_first - Sdiv_p_neg_first)
Sdiv_diff_first.plot.contourf(
    ax=axes[0, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
)
PlotEPfluxArrows(
    x=Sphi_pos_first.lat[::3],
    y=Sphi_pos_first.plev,
    ep1=(Sphi_pos_first - Sphi_neg_first)[:, ::3],
    ep2=(Sp_pos_first - Sp_neg_first)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 90],
    ylim=[100000, 10000],
    fig=fig,
    ax=axes[0, 2],
    draw_key=True,
    key_loc=(0.7, 0.95),
)

# second row for last decade
# first col for positive phase
pos_color = (Sdivphi_pos_last + Sdiv_p_pos_last).plot.contourf(
    ax=axes[1, 0], levels=levels, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
)
PlotEPfluxArrows(
    x=Sphi_pos_last.lat[::3],
    y=Sphi_pos_last.plev,
    ep1=Sphi_pos_last[:, ::3],
    ep2=Sp_pos_last[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 90],
    ylim=[100000, 10000],
    fig=fig,
    ax=axes[1, 0],
)
# second col for negative phase
neg_color = (Sdivphi_neg_last + Sdiv_p_neg_last).plot.contourf(
    ax=axes[1, 1], levels=levels, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
)
PlotEPfluxArrows(
    x=Sphi_neg_last.lat[::3],
    y=Sphi_neg_last.plev,
    ep1=Sphi_neg_last[:, ::3],
    ep2=Sp_neg_last[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 90],
    ylim=[100000, 10000],
    fig=fig,
    ax=axes[1, 1],
)
# third col for difference between positive and negative
Sdiv_diff_last = (Sdivphi_pos_last - Sdivphi_neg_last) + (Sdiv_p_pos_last - Sdiv_p_neg_last)
diff_color = Sdiv_diff_last.plot.contourf(
    ax=axes[1, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
)
PlotEPfluxArrows(
    x=Sphi_pos_last.lat[::3],
    y=Sphi_pos_last.plev,
    ep1=(Sphi_pos_last - Sphi_neg_last)[:, ::3],
    ep2=(Sp_pos_last - Sp_neg_last)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 90],
    ylim=[100000, 10000],
    fig=fig,
    ax=axes[1, 2],
)

# add cax under the second row

fig.colorbar(
    pos_color,
    ax=axes[:, 0],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"$\nabla \cdot \mathcal{F}$ [m$^2$ s$^{-1} day^{-1}$]",
)

fig.colorbar(
    neg_color,
    ax=axes[:, 1],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"$\nabla \cdot \mathcal{F}$ [m$^2$ s$^{-1} day^{-1}$]",
)

fig.colorbar(
    diff_color,
    ax=axes[:, 2],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"diff $\nabla \cdot \mathcal{F}$ [m$^2$ s$^{-1} day^{-1}$]",
)

# no y labels from second row on, no x labels at the first row
for ax in axes[0, :]:
    ax.set_xlabel("")
for ax in axes[:, 0]:
    ax.set_ylabel("Pressure [Pa]")

for ax in axes[:, 1:].flat:
    ax.set_ylabel("")

for ax in axes[1, :]:
    ax.set_xlabel("Latitude [°N]")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0EP_flux/steady_EP_flux.pdf",
    bbox_inches="tight",
    dpi=300,
)

# %%
