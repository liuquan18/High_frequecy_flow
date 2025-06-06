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
levels_vq = np.arange(-3, 3.1, 0.5)
levels_uv = np.arange(-0.6, 0.61, 0.1)
levels_vt = np.arange(-3, 3.1, 0.5)
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
# read climatological EP flux 
Tphi_clima_first, Tp_clima_first, Tdivphi_clima_first, Tdiv_p_clima_first = read_EP_flux(
    phase="clima", decade=1850, eddy="transient", ano=False,lon_mean=True,
)
Tphi_clima_last, Tp_clima_last, Tdivphi_clima_last, Tdiv_p_clima_last = read_EP_flux(
    phase="clima", decade=2090, eddy="transient", ano=False,lon_mean=True,
)
#%%
Tdivphi_pos_first_ano = Tdivphi_pos_first - Tdivphi_clima_first
Tdiv_p_pos_first_ano = Tdiv_p_pos_first - Tdiv_p_clima_first

Tdivphi_neg_first_ano = Tdivphi_neg_first - Tdivphi_clima_first
Tdiv_p_neg_first_ano = Tdiv_p_neg_first - Tdiv_p_clima_first

Tdivphi_pos_last_ano = Tdivphi_pos_last - Tdivphi_clima_last
Tdiv_p_pos_last_ano = Tdiv_p_pos_last - Tdiv_p_clima_last

Tdivphi_neg_last_ano = Tdivphi_neg_last - Tdivphi_clima_last
Tdiv_p_neg_last_ano = Tdiv_p_neg_last - Tdiv_p_clima_last
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
#%%
# read climatological EP flux
Sphi_clima_first, Sp_clima_first, Sdivphi_clima_first, Sdiv_p_clima_first = read_EP_flux(
    phase="clima", decade=1850, eddy="steady", ano=False,lon_mean=True,
)
Sphi_clima_last, Sp_clima_last, Sdivphi_clima_last, Sdiv_p_clima_last = read_EP_flux(
    phase="clima", decade=2090, eddy="steady", ano=False,lon_mean=True,
)
#%%
# anomaly
Sdivphi_pos_first_ano = Sdivphi_pos_first - Sdivphi_clima_first
Sdiv_p_pos_first_ano = Sdiv_p_pos_first - Sdiv_p_clima_first

Sdivphi_neg_first_ano = Sdivphi_neg_first - Sdivphi_clima_first
Sdiv_p_neg_first_ano = Sdiv_p_neg_first - Sdiv_p_clima_first

Sdivphi_pos_last_ano = Sdivphi_pos_last - Sdivphi_clima_last
Sdiv_p_pos_last_ano = Sdiv_p_pos_last - Sdiv_p_clima_last

Sdivphi_neg_last_ano = Sdivphi_neg_last - Sdivphi_clima_last
Sdiv_p_neg_last_ano = Sdiv_p_neg_last - Sdiv_p_clima_last


# %%
# transient eddies
fig, axes = plt.subplots(2, 3, figsize=(12, 8), sharey=True, sharex=True)
# first row for pos
# contourf for first decade
# contour for last decade
# first col for v'q'
vq_color = (Tdivphi_pos_first_ano + Tdiv_p_pos_first_ano).plot.contourf(
    ax=axes[0, 0], levels=levels_vq, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
(Tdivphi_pos_last_ano + Tdiv_p_pos_last_ano).plot.contour(
    ax=axes[0, 0], levels=[l for l in levels_vq if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)

# second col for u'v'
uv_color = Tdivphi_pos_first_ano.plot.contourf(
    ax=axes[0, 1], levels=levels_uv, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
Tdivphi_pos_last_ano.plot.contour(
    ax=axes[0, 1], levels=[l for l in levels_uv if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)

# third col for v't'
vt_color = Tdiv_p_pos_first_ano.plot.contourf(
    ax=axes[0, 2], levels=levels_vt, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
Tdiv_p_pos_last_ano.plot.contour(
    ax=axes[0, 2], levels=[l for l in levels_vt if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)

# second row for neg
# first col for v'q'
pos_color = (Tdivphi_neg_first_ano + Tdiv_p_neg_first_ano).plot.contourf(
    ax=axes[1, 0], levels=levels_vq, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
(Tdivphi_neg_last_ano + Tdiv_p_neg_last_ano).plot.contour(
    ax=axes[1, 0], levels=[l for l in levels_vq if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
# second col for u'v'
neg_color = Tdivphi_neg_first_ano.plot.contourf(
    ax=axes[1, 1], levels=levels_uv, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
Tdivphi_neg_last_ano.plot.contour(
    ax=axes[1, 1], levels=[l for l in levels_uv if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
# third col for v't'    
diff_color = Tdiv_p_neg_first_ano.plot.contourf(
    ax=axes[1, 2], levels=levels_vt, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
Tdiv_p_neg_last_ano.plot.contour(
    ax=axes[1, 2], levels=[l for l in levels_vt if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)   


# add cax under the second row

fig.colorbar(
    vq_color,
    ax=axes[:, 0],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"$v'q'$ [m$^2$ s$^{-1} day^{-1}$]",
)

fig.colorbar(
    uv_color,
    ax=axes[:, 1],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"$-\frac{\partial}{\partial y} \overline{u'v'}$ [m$^2$ s$^{-1} day^{-1}$]",
)

fig.colorbar(
    vt_color,
    ax=axes[:, 2],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"$\frac{\partial}{\partial z} (\frac{f_0}{N^2}\overline{v'\theta_e'})$ [m$^2$ s$^{-1} day^{-1}$]",
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
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0EP_flux/transient_flux_component.pdf",
    bbox_inches="tight",
    dpi=300,
)

# %%
# steady eddies
fig, axes = plt.subplots(2, 3, figsize=(12, 8), sharey=True, sharex=True)

# first row for pos
# v'q'
vq_color = (Sdivphi_pos_first_ano + Sdiv_p_pos_first_ano).plot.contourf(
    ax=axes[0, 0], levels=levels_vq, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
(Sdivphi_pos_last_ano + Sdiv_p_pos_last_ano).plot.contour(
    ax=axes[0, 0], levels=[l for l in levels_vq if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)

# u'v'
uv_color = Sdivphi_pos_first_ano.plot.contourf(
    ax=axes[0, 1], levels=levels_uv, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
Sdivphi_pos_last_ano.plot.contour(
    ax=axes[0, 1], levels=[l for l in levels_uv if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)

# v't'
vt_color = Sdiv_p_pos_first_ano.plot.contourf(
    ax=axes[0, 2], levels=levels_vt, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
Sdiv_p_pos_last_ano.plot.contour(
    ax=axes[0, 2], levels=[l for l in levels_vt if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)

# second row for neg
# v'q'
(Sdivphi_neg_first_ano + Sdiv_p_neg_first_ano).plot.contourf(
    ax=axes[1, 0], levels=levels_vq, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
(Sdivphi_neg_last_ano + Sdiv_p_neg_last_ano).plot.contour(
    ax=axes[1, 0], levels=[l for l in levels_vq if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
# u'v'
Sdivphi_neg_first_ano.plot.contourf(
    ax=axes[1, 1], levels=levels_uv, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
Sdivphi_neg_last_ano.plot.contour(
    ax=axes[1, 1], levels=[l for l in levels_uv if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
# v't'
Sdiv_p_neg_first_ano.plot.contourf(
    ax=axes[1, 2], levels=levels_vt, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
Sdiv_p_neg_last_ano.plot.contour(
    ax=axes[1, 2], levels=[l for l in levels_vt if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)

fig.colorbar(
    vq_color,
    ax=axes[:, 0],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"$v'q'$ [m$^2$ s$^{-1} day^{-1}$]",
)

fig.colorbar(
    uv_color,
    ax=axes[:, 1],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"$- \frac{\partial}{\partial y} \overline{u'v'}$ [m$^2$ s$^{-1} day^{-1}$]",
)

fig.colorbar(
    vt_color,
    ax=axes[:, 2],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"$\frac{\partial}{\partial z} (\frac{f_0}{N^2}\overline{v'\theta_e'})$ [m$^2$ s$^{-1} day^{-1}$]",
)

for ax in axes[0, :]:
    ax.set_xlabel("")
for ax in axes[:, 0]:
    ax.set_ylabel("Pressure [Pa]")

for ax in axes[:, 1:].flat:
    ax.set_ylabel("")

for ax in axes[1, :]:
    ax.set_xlabel("Latitude [°N]")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0EP_flux/steady_flux_component.pdf",
    bbox_inches="tight",
    dpi=300,
)
# %%
levels_vq_clima = np.arange(-30, 30.1, 5)
levels_uv_clima = np.arange(-1, 1.1, 0.1)
levels_vt_clima = np.arange(-30, 30.1, 5)

#%%
# plot the climatology
fig, axes = plt.subplots(2, 3, figsize=(12, 8), sharey=True, sharex=True)
# v'q' transient
vq_color = (Tdivphi_clima_first + Tdiv_p_clima_first).plot.contourf(
    ax=axes[0, 0], levels=levels_vq_clima, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
(Tdivphi_clima_last + Tdiv_p_clima_last).plot.contour(
    ax=axes[0, 0], levels=[l for l in levels_vq_clima if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)

# u'v' transient
uv_color = Tdivphi_clima_first.plot.contourf(
    ax=axes[0, 1], levels=levels_uv_clima, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
Tdivphi_clima_last.plot.contour(
    ax=axes[0, 1], levels=[l for l in levels_uv_clima if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)

# v't' transient
vt_color = Tdiv_p_clima_first.plot.contourf(
    ax=axes[0, 2], levels=levels_vt_clima, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
Tdiv_p_clima_last.plot.contour(
    ax=axes[0, 2], levels=[l for l in levels_vt_clima if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)

# v'q' steady
(Sdivphi_clima_first + Sdiv_p_clima_first).plot.contourf(
    ax=axes[1, 0], levels=levels_vq_clima, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
(Sdivphi_clima_last + Sdiv_p_clima_last).plot.contour(
    ax=axes[1, 0], levels=[l for l in levels_vq_clima if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
# u'v' steady
Sdivphi_clima_first.plot.contourf(
    ax=axes[1, 1], levels=levels_uv_clima, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
Sdivphi_clima_last.plot.contour(
    ax=axes[1, 1], levels=[l for l in levels_uv_clima if l != 0], colors="k", linewidths=0.5,  
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
# v't' steady
Sdiv_p_clima_first.plot.contourf(
    ax=axes[1, 2], levels=levels_vt_clima, cmap="RdBu_r", add_colorbar=False,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)
Sdiv_p_clima_last.plot.contour(
    ax=axes[1, 2], levels=[l for l in levels_vt_clima if l != 0], colors="k", linewidths=0.5,
    ylim=[100000, 10000],
    xlim=[0, 90],
    extend="both",
)

fig.colorbar(
    vq_color,
    ax=axes[:, 0],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"$v'q'$ [m$^2$ s$^{-1} day^{-1}$]",
)
fig.colorbar(
    uv_color,
    ax=axes[:, 1],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"$- \frac{\partial}{\partial y} \overline{u'v'}$ [m$^2$ s$^{-1} day^{-1}$]",
)
fig.colorbar(
    vt_color,
    ax=axes[:, 2],
    orientation="horizontal",
    fraction=0.05,
    pad=0.1,
    label=r"$\frac{\partial}{\partial z} (\frac{f_0}{N^2}\overline{v'\theta_e'})$ [m$^2$ s$^{-1} day^{-1}$]",
)
for ax in axes[0, :]:
    ax.set_xlabel("")
for ax in axes[:, 0]:
    ax.set_ylabel("Pressure [Pa]")
for ax in axes[:, 1:].flat:
    ax.set_ylabel("")
for ax in axes[1, :]:
    ax.set_xlabel("Latitude [°N]")
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0EP_flux/climatological_flux_component.pdf",
    bbox_inches="tight",
    dpi=300,
)

# %%
