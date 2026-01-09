# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import importlib

from src.data_helper import read_composite

importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux

# %%
# read transient EP flux for positive and negative phase
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

# last decade
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
# read climatological EP flux
Tphi_clima_first, Tp_clima_first, Tdivphi_clima_first, Tdiv_p_clima_first = (
    read_EP_flux(
        phase="clima",
        decade=1850,
        eddy="transient",
        ano=False,
        lon_mean=False,
        region=None,
    )
)
Tphi_clima_last, Tp_clima_last, Tdivphi_clima_last, Tdiv_p_clima_last = read_EP_flux(
    phase="clima",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)


# %%
def anomaly(ds, ds_clima):
    """
    Calculate the anomaly of a dataset with respect to a climatology.
    """
    # average over time and events
    ds = ds.sel(time=slice(-10, 5)).mean(dim=("time", "event", "lon"))
    ds_clima = ds_clima.mean(dim=("lon"))
    anomaly = ds - ds_clima
    return anomaly.load()


# %%
Tdiv_phi_pos_first_anomaly = anomaly(Tdivphi_pos_first, Tdivphi_clima_first)
Tdiv_phi_neg_first_anomaly = anomaly(Tdivphi_neg_first, Tdivphi_clima_first)
Tdiv_phi_pos_last_anomaly = anomaly(Tdivphi_pos_last, Tdivphi_clima_last)
Tdiv_phi_neg_last_anomaly = anomaly(Tdivphi_neg_last, Tdivphi_clima_last)

# %%
phi_trans_levels = np.arange(-0.18, 0.19, 0.06)

fig, axes = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

# first col: positive phase
cf_phi_trans = (Tdiv_phi_pos_first_anomaly).plot.contourf(
    ax=axes[0],
    levels=phi_trans_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    xlim=(0, 90),
    ylim=(100000, 10000),
)
contour_levels = [l for l in phi_trans_levels if l != 0]
(Tdiv_phi_pos_last_anomaly).plot.contour(
    ax=axes[0],
    levels=contour_levels,
    colors="k",
    linewidths=1,
    add_colorbar=False,
    xlim=(0, 90),
    ylim=(100000, 10000),
)

# second col: negative phase
cf_phi_trans_neg = (Tdiv_phi_neg_first_anomaly).plot.contourf(
    ax=axes[1],
    levels=phi_trans_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    xlim=(0, 90),
    ylim=(100000, 10000),
)
contour_levels = [l for l in phi_trans_levels if l != 0]
(Tdiv_phi_neg_last_anomaly).plot.contour(
    ax=axes[1],
    levels=contour_levels,
    colors="k",
    linewidths=1,
    add_colorbar=False,
    xlim=(0, 90),
    ylim=(100000, 10000),
)

# Add shared colorbar on the right
cbar = fig.colorbar(
    cf_phi_trans,
    ax=axes,
    orientation="vertical",
    fraction=0.046,
    pad=0.04,
    label=r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ / m $s^{-1}$ day $^{-1}$",
)

# Set y-axis labels
axes[0].set_ylabel("Pressure [hPa]")
axes[0].set_yticks(
    [100000, 90000, 80000, 70000, 60000, 50000, 40000, 30000, 20000, 10000]
)
axes[0].set_yticklabels([str(int(tick / 100)) for tick in axes[0].get_yticks()])

for ax in axes:
    ax.set_title("")
    ax.set_xlabel("lat [°N]")

axes[1].set_ylabel("")

# Add a, b labels
axes[0].text(
    -0.08,
    1.02,
    "a",
    transform=axes[0].transAxes,
    fontsize=14,
    fontweight="bold",
    va="bottom",
    ha="right",
)
axes[1].text(
    -0.08,
    1.02,
    "b",
    transform=axes[1].transAxes,
    fontsize=14,
    fontweight="bold",
    va="bottom",
    ha="right",
)
