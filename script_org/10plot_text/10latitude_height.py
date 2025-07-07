# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import seaborn.objects as so

from src.data_helper import read_composite
import importlib
import matplotlib
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var

from src.data_helper.read_variable import read_climatology
# %%
levels_vq = np.arange(-3, 3.1, 0.5)
levels_uv = np.arange(-1.5, 1.6, 0.5)
levels_vt = np.arange(-3, 3.1, 0.5)
# %%
# read transient EP flux for positive and negative phase
# read data for first decade with region = western
Tphi_pos_first, Tp_pos_first, Tdivphi_pos_first, Tdiv_p_pos_first = read_EP_flux(
    phase="pos",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)
Tphi_neg_first, Tp_neg_first, Tdivphi_neg_first, Tdiv_p_neg_first = read_EP_flux(
    phase="neg",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)


# last decade region
Tphi_pos_last, Tp_pos_last, Tdivphi_pos_last, Tdiv_p_pos_last = read_EP_flux(
    phase="pos",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)
Tphi_neg_last, Tp_neg_last, Tdivphi_neg_last, Tdiv_p_neg_last = read_EP_flux(
    phase="neg",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)
# %%
Tdivphi_clima_first = read_climatology("Fdiv_phi_transient", decade=1850, name = 'div')
# %%
Tdivphi_clima_last = read_climatology("Fdiv_phi_transient", decade=2090, name = 'div')
#%%
Tdivp_clima_first = read_climatology("Fdiv_p_transient", decade=1850, name = 'div2')
# %%
Tdivp_clima_last = read_climatology("Fdiv_p_transient", decade=2090, name = 'div2')
# %%
# %%
# read steady EP flux for positive and negative phase
Sphi_pos_first, Sp_pos_first, Sdivphi_pos_first, Sdiv_p_pos_first = read_EP_flux(
    phase="pos",
    decade=1850,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)
Sphi_neg_first, Sp_neg_first, Sdivphi_neg_first, Sdiv_p_neg_first = read_EP_flux(
    phase="neg",
    decade=1850,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)

# last decade
Sphi_pos_last, Sp_pos_last, Sdivphi_pos_last, Sdiv_p_pos_last = read_EP_flux(
    phase="pos",
    decade=2090,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)
Sphi_neg_last, Sp_neg_last, Sdivphi_neg_last, Sdiv_p_neg_last = read_EP_flux(
    phase="neg",
    decade=2090,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)

# %%
# read climatology for steady EP flux
Sdivphi_clima_first = read_climatology("Fdiv_phi_steady", decade=1850, name = 'div')
Sdivphi_clima_last = read_climatology("Fdiv_phi_steady", decade=2090, name = 'div')
# %%
Sdivp_clima_first = read_climatology("Fdiv_p_steady", decade=1850, name = 'div2')
Sdivp_clima_last = read_climatology("Fdiv_p_steady", decade=2090, name = 'div2')
# %%
# read E_div_x

TEx_pos_first, TEy_pos_first = read_E_div(
    phase="pos",
    decade=1850,
    eddy="transient",
    keep_time=True,
)
TEx_neg_first, TEy_neg_first = read_E_div(
    phase="neg",
    decade=1850,
    eddy="transient",
    keep_time=True,
)
TEx_pos_last, TEy_pos_last = read_E_div(
    phase="pos",
    decade=2090,
    eddy="transient",
    keep_time=True,
)
TEx_neg_last, TEy_neg_last = read_E_div(
    phase="neg",
    decade=2090,
    eddy="transient",
    keep_time=True,
)

# read climatological E_div_x
TEx_clima_first, TEy_clima_first = read_E_div(
    phase="clima",
    decade=1850,
    eddy="transient",
    keep_time=False,
)
TEx_clima_last, TEy_clima_last = read_E_div(
    phase="clima",
    decade=2090,
    eddy="transient",
    keep_time=False,
)

# %%
# read E_div_x for steady eddies
SEx_pos_first, SEy_pos_first = read_E_div(
    phase="pos",
    decade=1850,
    eddy="steady",
    keep_time=True,
)
SEx_neg_first, SEy_neg_first = read_E_div(
    phase="neg",
    decade=1850,
    eddy="steady",
    keep_time=True,
)

SEx_pos_last, SEy_pos_last = read_E_div(
    phase="pos",
    decade=2090,
    eddy="steady",
    keep_time=True,
)
SEx_neg_last, SEy_neg_last = read_E_div(
    phase="neg",
    decade=2090,
    eddy="steady",
    keep_time=True,
)
# read climatological E_div_x for steady
SEx_clima_first, SEy_clima_first = read_E_div(
    phase="clima",
    decade=1850,
    eddy="steady",
    keep_time=False,  # climatology is in the old folder
)
SEx_clima_last, SEy_clima_last = read_E_div(
    phase="clima",
    decade=2090,
    eddy="steady",
    keep_time=False,
)

# %%
def anomaly(ds, ds_clima):
    """
    Calculate the anomaly of a dataset with respect to a climatology.
    """
    # average over time and events
    ds = ds.sel(time = slice(-10, 5)).mean(dim=('time', 'event', 'lon'))
    ds_clima = ds_clima.mean(dim=('lon'))
    anomaly = ds - ds_clima
    return anomaly.load()
# %%
Tdiv_phi_pos_first_anomaly = anomaly(Tdivphi_pos_first, Tdivphi_clima_first)
Tdiv_phi_neg_first_anomaly = anomaly(Tdivphi_neg_first, Tdivphi_clima_first)
Tdiv_phi_pos_last_anomaly = anomaly(Tdivphi_pos_last, Tdivphi_clima_last)
Tdiv_phi_neg_last_anomaly = anomaly(Tdivphi_neg_last, Tdivphi_clima_last)
# %%
Tdiv_p_pos_first_anomaly = anomaly(Tdiv_p_pos_first, Tdivp_clima_first)
Tdiv_p_neg_first_anomaly = anomaly(Tdiv_p_neg_first, Tdivp_clima_first)
Tdiv_p_pos_last_anomaly = anomaly(Tdiv_p_pos_last, Tdivp_clima_last)
Tdiv_p_neg_last_anomaly = anomaly(Tdiv_p_neg_last, Tdivp_clima_last)
# %%
Sdivphi_pos_first_anomaly = anomaly(Sdivphi_pos_first, Sdivphi_clima_first)
Sdivphi_neg_first_anomaly = anomaly(Sdivphi_neg_first, Sdivphi_clima_first)
Sdivphi_pos_last_anomaly = anomaly(Sdivphi_pos_last, Sdivphi_clima_last)
Sdivphi_neg_last_anomaly = anomaly(Sdivphi_neg_last, Sdivphi_clima_last)
# %%
Sdiv_p_pos_first_anomaly = anomaly(Sdiv_p_pos_first, Sdivp_clima_first)
Sdiv_p_neg_first_anomaly = anomaly(Sdiv_p_neg_first, Sdivp_clima_first)
Sdiv_p_pos_last_anomaly = anomaly(Sdiv_p_pos_last, Sdivp_clima_last)
Sdiv_p_neg_last_anomaly = anomaly(Sdiv_p_neg_last, Sdivp_clima_last)
#%%
# sum of transient and steady EP fluxes
div_phi_pos_first_anomaly = Tdiv_phi_pos_first_anomaly + Sdivphi_pos_first_anomaly
div_phi_neg_first_anomaly = Tdiv_phi_neg_first_anomaly + Sdivphi_neg_first_anomaly
div_phi_pos_last_anomaly = Tdiv_phi_pos_last_anomaly + Sdivphi_pos_last_anomaly
div_phi_neg_last_anomaly = Tdiv_phi_neg_last_anomaly + Sdivphi_neg_last_anomaly
# %%
div_p_pos_first_anomaly = Tdiv_p_pos_first_anomaly + Sdiv_p_pos_first_anomaly
div_p_neg_first_anomaly = Tdiv_p_neg_first_anomaly + Sdiv_p_neg_first_anomaly
div_p_pos_last_anomaly = Tdiv_p_pos_last_anomaly + Sdiv_p_pos_last_anomaly
div_p_neg_last_anomaly = Tdiv_p_neg_last_anomaly + Sdiv_p_neg_last_anomaly
# %%
sum_sum_levels = np.arange(-3, 3.1, 0.5)
sum_trans_levels = np.arange(-1.5, 1.6, 0.3)
sum_steady_levels = np.arange(-3, 3.1, 0.5)

phi_sum_levels = np.arange(-.5,.6, 0.1)
phi_trans_levels = np.arange(-.5,.6, 0.1)
phi_steady_levels = np.arange(-0.2,0.2, 0.05)

p_sum_levels = np.arange(-3, 3.1, 0.5)
p_trans_levels = np.arange(-1.5, 1.6, 0.3)
p_steady_levels = np.arange(-3, 3.1, 0.5)

#%%
# for positive, plot "last" data as contour lines (no 0 line), using the same levels

fig, axes = plt.subplots(
    3, 3, figsize=(12, 12), sharex=False, sharey=False,
)

# first row sum of momentum fluxes and heat fluxes
cf = (div_phi_pos_first_anomaly + div_p_pos_first_anomaly).plot.contourf(
    ax=axes[0, 0],
    levels=sum_sum_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in sum_sum_levels if l != 0]
(div_phi_pos_last_anomaly + div_p_pos_last_anomaly).plot.contour(
    ax=axes[0, 0],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

(Tdiv_phi_pos_first_anomaly + Tdiv_p_pos_first_anomaly).plot.contourf(
    ax=axes[0, 1],
    levels=sum_trans_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in sum_trans_levels if l != 0]
(Tdiv_phi_pos_last_anomaly + Tdiv_p_pos_last_anomaly).plot.contour(
    ax=axes[0, 1],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

(Sdivphi_pos_first_anomaly + Sdiv_p_pos_first_anomaly).plot.contourf(
    ax=axes[0, 2],
    levels=sum_steady_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in sum_steady_levels if l != 0]
(Sdivphi_pos_last_anomaly + Sdiv_p_pos_last_anomaly).plot.contour(
    ax=axes[0, 2],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

# second row momentum fluxes Phi
cf_phi_sum = (div_phi_pos_first_anomaly).plot.contourf(
    ax=axes[1, 0],
    levels=phi_sum_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in phi_sum_levels if l != 0]
(div_phi_pos_last_anomaly).plot.contour(
    ax=axes[1, 0],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_phi_trans = (Tdiv_phi_pos_first_anomaly).plot.contourf(
    ax=axes[1, 1],
    levels=phi_trans_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in phi_trans_levels if l != 0]
(Tdiv_phi_pos_last_anomaly).plot.contour(
    ax=axes[1, 1],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_phi_steady = (Sdivphi_pos_first_anomaly).plot.contourf(
    ax=axes[1, 2],
    levels=phi_steady_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in phi_steady_levels if l != 0]
(Sdivphi_pos_last_anomaly).plot.contour(
    ax=axes[1, 2],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

# third row heat fluxes P
cf_p_sum = (div_p_pos_first_anomaly).plot.contourf(
    ax=axes[2, 0],
    levels=p_sum_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in p_sum_levels if l != 0]
(div_p_pos_last_anomaly).plot.contour(
    ax=axes[2, 0],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_p_trans = (Tdiv_p_pos_first_anomaly).plot.contourf(
    ax=axes[2, 1],
    levels=p_trans_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in p_trans_levels if l != 0]
(Tdiv_p_pos_last_anomaly).plot.contour(
    ax=axes[2, 1],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_p_steady = (Sdiv_p_pos_first_anomaly).plot.contourf(
    ax=axes[2, 2],
    levels=p_steady_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in p_steady_levels if l != 0]
(Sdiv_p_pos_last_anomaly).plot.contour(
    ax=axes[2, 2],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

# Set colorbar titles for first, second and third rows
cf.colorbar.set_label('sum')
cf_phi_trans.colorbar.set_label('sum')
cf_phi_steady.colorbar.set_label('sum')

for cf in [cf_phi_sum, cf_phi_trans, cf_phi_steady]:
    cf.colorbar.set_label(r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m $s^{-1}$ day $^{-1}$]")

for cf in [cf_p_sum, cf_p_trans, cf_p_steady]:
    cf.colorbar.set_label(r"$\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta'}}{\overline{\theta}_p} \right)$ [m $s^{-1}$ day $^{-1}$]")

for ax in axes[:, 1:].flat:
    ax.set_yticklabels([])
    ax.set_ylabel("")

# for the first column, set y-label from Pa to hPa
for ax in axes[:, 0]:
    ax.set_ylabel("Pressure [hPa]")
    ax.set_yticks([100000, 90000, 80000, 70000, 60000, 50000, 40000, 30000, 20000, 10000])
    ax.set_yticklabels([str(int(tick / 100)) for tick in ax.get_yticks()])  # Convert Pa to hPa


plt.tight_layout()

# %%
fig, axes = plt.subplots(
    3, 3, figsize=(12, 12), sharex=False, sharey=False,
)

# first row sum of momentum fluxes and heat fluxes (negative phase)
cf = (div_phi_neg_first_anomaly + div_p_neg_first_anomaly).plot.contourf(
    ax=axes[0, 0],
    levels=sum_sum_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
# overlay last as contour, skip 0
contour_levels = [l for l in sum_sum_levels if l != 0]
(div_phi_neg_last_anomaly + div_p_neg_last_anomaly).plot.contour(
    ax=axes[0, 0],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_sum_trans = (Tdiv_phi_neg_first_anomaly + Tdiv_p_neg_first_anomaly).plot.contourf(
    ax=axes[0, 1],
    levels=sum_trans_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in sum_trans_levels if l != 0]
(Tdiv_phi_neg_last_anomaly + Tdiv_p_neg_last_anomaly).plot.contour(
    ax=axes[0, 1],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_sum_steady = (Sdivphi_neg_first_anomaly + Sdiv_p_neg_first_anomaly).plot.contourf(
    ax=axes[0, 2],
    levels=sum_steady_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in sum_steady_levels if l != 0]
(Sdivphi_neg_last_anomaly + Sdiv_p_neg_last_anomaly).plot.contour(
    ax=axes[0, 2],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

# second row momentum fluxes Phi (negative phase)
cf_phi_sum = (div_phi_neg_first_anomaly).plot.contourf(
    ax=axes[1, 0],
    levels=phi_sum_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in phi_sum_levels if l != 0]
(div_phi_neg_last_anomaly).plot.contour(
    ax=axes[1, 0],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_phi_trans = (Tdiv_phi_neg_first_anomaly).plot.contourf(
    ax=axes[1, 1],
    levels=phi_trans_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in phi_trans_levels if l != 0]
(Tdiv_phi_neg_last_anomaly).plot.contour(
    ax=axes[1, 1],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_phi_steady = (Sdivphi_neg_first_anomaly).plot.contourf(
    ax=axes[1, 2],
    levels=phi_steady_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in phi_steady_levels if l != 0]
(Sdivphi_neg_last_anomaly).plot.contour(
    ax=axes[1, 2],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

# third row heat fluxes P (negative phase)
cf_p_sum = (div_p_neg_first_anomaly).plot.contourf(
    ax=axes[2, 0],
    levels=p_sum_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in p_sum_levels if l != 0]
(div_p_neg_last_anomaly).plot.contour(
    ax=axes[2, 0],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_p_trans = (Tdiv_p_neg_first_anomaly).plot.contourf(
    ax=axes[2, 1],
    levels=p_trans_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in p_trans_levels if l != 0]
(Tdiv_p_neg_last_anomaly).plot.contour(
    ax=axes[2, 1],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_p_steady = (Sdiv_p_neg_first_anomaly).plot.contourf(
    ax=axes[2, 2],
    levels=p_steady_levels,
    cmap="RdBu_r",
    add_colorbar=True,
    xlim=(0, 90),
    ylim=(100000, 10000)
)
contour_levels = [l for l in p_steady_levels if l != 0]
(Sdiv_p_neg_last_anomaly).plot.contour(
    ax=axes[2, 2],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

# Set colorbar titles for first, second and third rows
cf.colorbar.set_label('sum')
cf_sum_trans.colorbar.set_label('sum')
cf_sum_steady.colorbar.set_label('sum')

for cf in [cf_phi_sum, cf_phi_trans, cf_phi_steady]:
    cf.colorbar.set_label(r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m $s^{-1}$ day $^{-1}$]")

for cf in [cf_p_sum, cf_p_trans, cf_p_steady]:
    cf.colorbar.set_label(r"$\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta'}}{\overline{\theta}_p} \right)$ [m $s^{-1}$ day $^{-1}$]")


for ax in axes[:, 1:].flat:
    ax.set_yticklabels([])
    ax.set_ylabel("")

# for the first column, set y-label for eddy momentum flux (Pa to hPa)
for ax in axes[:, 0]:
    ax.set_ylabel("Pressure [hPa]")
    ax.set_yticks([100000, 90000, 80000, 70000, 60000, 50000, 40000, 30000, 20000, 10000])
    ax.set_yticklabels([str(int(tick / 100)) for tick in ax.get_yticks()])  # Convert Pa to hPa

plt.tight_layout()

# %%
