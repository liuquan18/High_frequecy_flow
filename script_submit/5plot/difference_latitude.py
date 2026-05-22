# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import cmocean
import os


from src.data_helper import read_composite
from src.data_helper.read_variable import read_climatology
import importlib
import matplotlib
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

from scipy import stats
from src.plotting.util import map_smooth
import src.plotting.util as util

importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var


# %%
MODEL_DIR = "MPI_GE_CMIP6_allplev"


def _read_all(var_name, suffix = '_ano', name=None, method="no_stat", chunks=None):
    """Read pos/neg x 1850/2090 composites.

    Returns a dict keyed by '{phase}_{decade}', e.g. 'pos_1850'.
    """
    kwargs = dict(time_window= 'all', model_dir=MODEL_DIR)
    if method is not None:
        kwargs["method"] = method
    if name is not None:
        kwargs["name"] = name
    if chunks is not None:
        kwargs["chunks"] = chunks
    return {
        f"{phase}_{decade}": read_comp_var(var_name, phase, decade, suffix=suffix, **kwargs)
        for phase in ("pos", "neg")
        for decade in (1850, 2090)
    }

def _zonal_mean(da, lon_min=-90, lon_max=40, time_window = (0, 20)):
    """Zonal mean over [lon_min, lon_max], handling both 0-360 and -180-180 grids."""
    if da.lon.max() > 180:
        # Convert 0-360 to -180-180
        da = da.assign_coords(lon=(da.lon + 180) % 360 - 180).sortby("lon")
    return da.sel(lon=slice(lon_min, lon_max), lat = slice(20, 90), time=slice(*time_window)).mean(dim=("lon", "time"))

#%%
#%%
# Convergence of transient eddy momentum flux
Fdiv_phi_transient = _read_all("Fdiv_phi_transient", suffix="_ano", name="div")
# %%
eke = _read_all("eke", suffix="_ano", name="eke")
## %%
Fdiv_phi_diff_pos = Fdiv_phi_transient["pos_2090"] - Fdiv_phi_transient["pos_1850"]
Fdiv_phi_diff_neg = Fdiv_phi_transient["neg_2090"] - Fdiv_phi_transient["neg_1850"]
eke_diff_pos = eke["pos_2090"] - eke["pos_1850"]
eke_diff_neg = eke["neg_2090"] - eke["neg_1850"]
#%%
Fdiv_phi_diff_pos_zm = _zonal_mean(Fdiv_phi_diff_pos)
Fdiv_phi_diff_neg_zm = _zonal_mean(Fdiv_phi_diff_neg)
eke_diff_pos_zm = _zonal_mean(eke_diff_pos)
eke_diff_neg_zm = _zonal_mean(eke_diff_neg)
# %%


COLOR_POS = "#E57200"  # MPI orange
COLOR_NEG = "#006C66"  # MPI green


def _lat_mean_and_sig(da):
    """Return (mean_lat, sig_mask) where sig_mask is True where the
    one-sided t-test against zero (in direction of the mean) is p < 0.05.
    Averages all non-(lat, event) dims first, then tests across event.
    """
    reduce_dims = [d for d in da.dims if d not in ("lat", "event")]
    if reduce_dims:
        da = da.mean(dim=reduce_dims)
    da = da.sortby("lat")
    mean_lat = da.mean(dim="event")
    # one-sample t-test against 0 across events, per latitude
    t_vals, p_two = stats.ttest_1samp(da.values, 0, axis=da.dims.index("event"))
    sig = (p_two / 2) < 0.05  # one-sided p in the direction of the observed mean
    return mean_lat, sig


def _plot_sig_bars(ax, da_zm, color, label, ylabel="Value", ylim=None):
    """Bar chart with filled bars where one-sided significant, outline only otherwise."""
    mean_lat, sig = _lat_mean_and_sig(da_zm)
    lats = mean_lat.lat.values
    vals = mean_lat.values
    for lat, val, significant in zip(lats, vals, sig):
        ax.bar(
            lat, val, width=1.0,
            color=color if significant else "none",
            edgecolor=color, linewidth=0.8,
        )
    ax.axhline(0, color="k", lw=0.5)
    ax.text(0.02, 0.97, label, transform=ax.transAxes,
            fontsize=12, fontweight="bold", va="top", ha="left")
    ax.set_xlabel("Latitude")
    ax.set_ylabel(ylabel)
    if ylim is not None:
        ax.set_ylim(ylim)
    ax.set_xticks([30, 50, 70])
    ax.set_xticklabels(["30°N", "50°N", "70°N"])
    ax.spines[["top", "right"]].set_visible(False)


fig, axes = plt.subplots(2, 2, figsize=(8, 6))

YLABEL_FDIV = r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ / m s$^{-1}$ day$^{-1}$"
YLABEL_EKE  = r"EKE / m$^2$ s$^{-2}$"

_plot_sig_bars(axes[0, 0], Fdiv_phi_diff_pos_zm, COLOR_POS, "a", ylabel=YLABEL_FDIV, ylim=(-1, 1))
_plot_sig_bars(axes[0, 1], eke_diff_pos_zm,       COLOR_POS, "b", ylabel=YLABEL_EKE,  ylim=(-1, 1))
_plot_sig_bars(axes[1, 0], Fdiv_phi_diff_neg_zm, COLOR_NEG, "c", ylabel=YLABEL_FDIV, ylim=(-1, 1))
_plot_sig_bars(axes[1, 1], eke_diff_neg_zm,       COLOR_NEG, "d", ylabel=YLABEL_EKE,  ylim=(-3, 3))

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0after_defense/difference_latitude.pdf", dpi=300, bbox_inches="tight", transparent=True)

# %%
