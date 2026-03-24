# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import seaborn.objects as so

from src.data_helper import read_composite
from src.data_helper.read_variable import read_climatology
import importlib
import matplotlib
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var
# %%
steady_pos_first = read_comp_var(
    "zg_steady",
    "pos",
    1850,
    time_window=(0, 10),
    name="zg",
    model_dir = 'MPI_GE_CMIP6_allplev'
)
# %%
steady_neg_first = read_comp_var(
    "zg_steady",
    "neg",
    1850,
    time_window=(0, 10),
    name="zg",
    model_dir = 'MPI_GE_CMIP6_allplev'
)
# %%
steady_pos_last = read_comp_var(
    "zg_steady",
    "pos",
    2090,
    time_window=(0, 10),
    name="zg",
    model_dir = 'MPI_GE_CMIP6_allplev'
)

steady_neg_last = read_comp_var(
    "zg_steady",
    "neg",
    2090,
    time_window=(0, 10),
    name="zg",
    model_dir = 'MPI_GE_CMIP6_allplev'
)
# %%
pos_first_850 = steady_pos_first.sel(plev=85000, method="nearest")
neg_first_850 = steady_neg_first.sel(plev=85000, method="nearest")
diff_first_850 = pos_first_850 - neg_first_850

pos_last_850 = steady_pos_last.sel(plev=85000, method="nearest")
neg_last_850 = steady_neg_last.sel(plev=85000, method="nearest")
diff_last_850 = pos_last_850 - neg_last_850

#%%
# ready eddy kinetic energy

us_pos_first = read_comp_var(
    "ua_steady",
    "pos",
    1850,
    time_window=(0, 10),
    name="ua",
    model_dir = 'MPI_GE_CMIP6_allplev'
)
us_neg_first = read_comp_var(
    "ua_steady",
    "neg",
    1850,
    time_window=(0, 10),
    name="ua",
    model_dir = 'MPI_GE_CMIP6_allplev'
)

us_pos_last = read_comp_var(
    "ua_steady",
    "pos",
    2090,
    time_window=(0, 10),
    name="ua",
    model_dir = 'MPI_GE_CMIP6_allplev'
)

us_neg_last = read_comp_var(
    "ua_steady",
    "neg",
    2090,
    time_window=(0, 10),
    name="ua",
    model_dir = 'MPI_GE_CMIP6_allplev'
)

vs_pos_first = read_comp_var(
    "va_steady",
    "pos",
    1850,
    time_window=(0, 10),
    name="va",
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vs_neg_first = read_comp_var(
    "va_steady",
    "neg",
    1850,
    time_window=(0, 10),
    name="va",
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vs_pos_last = read_comp_var(
    "va_steady",
    "pos",
    2090,
    time_window=(0, 10),
    name="va",
    model_dir = 'MPI_GE_CMIP6_allplev'
)
vs_neg_last = read_comp_var(
    "va_steady",
    "neg",
    2090,
    time_window=(0, 10),
    name="va",
    model_dir = 'MPI_GE_CMIP6_allplev'
)

# %%
# function to calculate eddy kinetic energy
def calculate_eke(u, v):
    return 0.5 * (u**2 + v**2)
seke_pos_first = calculate_eke(us_pos_first, vs_pos_first)  # using u for both u and v as a placeholder
seke_neg_first = calculate_eke(us_neg_first, vs_neg_first)  # using u for both u and v as a placeholder
seke_diff_first = seke_pos_first - seke_neg_first

seke_pos_last = calculate_eke(us_pos_last, vs_pos_last)  # using u for both u and v as a placeholder
seke_neg_last = calculate_eke(us_neg_last, vs_neg_last)  # using u for both u and v as a placeholder
seke_diff_last = seke_pos_last - seke_neg_last

#%%
eke_pos_first_850 = seke_pos_first.sel(plev=85000, method="nearest")
eke_neg_first_850 = seke_neg_first.sel(plev=85000, method="nearest")
eke_diff_first_850 = eke_pos_first_850 - eke_neg_first_850

eke_pos_last_850 = seke_pos_last.sel(plev=85000, method="nearest")
eke_neg_last_850 = seke_neg_last.sel(plev=85000, method="nearest")
eke_diff_last_850 = eke_pos_last_850 - eke_neg_last_850


#%%
zg_levels = np.arange(-100, 101, 20)
contour_zg_levels = zg_levels[zg_levels != 0]

eke_levels = np.arange(-20, 21, 5)
contour_eke_levels = eke_levels[eke_levels != 0]
#%%
fig, axes = plt.subplots(
    nrows=2,
    ncols=3,
    figsize=(8.0, 6.0),
    subplot_kw={"projection": ccrs.Orthographic(-30, 70)},
    constrained_layout=False,
)
fig.subplots_adjust(left=0.04, right=0.98, top=0.94, bottom=0.14, wspace=0.02, hspace=0.16)

# zg*
pos_map = pos_first_850.plot.contourf(
    ax=axes[0, 0],
    levels=zg_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
neg_map = neg_first_850.plot.contourf(
    ax=axes[0, 1],
    levels=zg_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

diff_map = diff_first_850.plot.contourf(
    ax=axes[0, 2],
    levels=zg_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

pos_last_850.plot.contour(
    ax=axes[0, 0],
    levels=contour_zg_levels,
    colors="k",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    linewidths=0.9,
)
neg_last_850.plot.contour(
    ax=axes[0, 1],
    levels=contour_zg_levels,
    colors="k",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    linewidths=0.9,
)
diff_last_850.plot.contour(
    ax=axes[0, 2],
    levels=contour_zg_levels,
    colors="k",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    linewidths=0.9,
)


# eke
# first
eke_map = eke_pos_first_850.plot.contourf(
    ax=axes[1, 0],
    levels=eke_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
eke_neg_first_850.plot.contourf(
    ax=axes[1, 1],
    levels=eke_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
eke_diff_first_850.plot.contourf(
    ax=axes[1, 2],
    levels=eke_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
# eke last
eke_pos_last_850.plot.contour(
    ax=axes[1, 0],
    levels=contour_eke_levels,
    colors="k",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    linewidths=0.9,
)
eke_neg_last_850.plot.contour(
    ax=axes[1, 1],
    levels=contour_eke_levels,
    colors="k",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    linewidths=0.9,
)
eke_diff_last_850.plot.contour(
    ax=axes[1, 2],
    levels=contour_eke_levels,
    colors="k",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    linewidths=0.9,
)

# --- Formatting ---
for i, ax in enumerate(axes.flatten()):
    ax.coastlines(color="grey", linewidth=1)
    ax.gridlines(
        draw_labels=False, linewidth=1, color="grey", alpha=0.5, linestyle="--"
    )
    ax.set_global()
    ax.set_title("")

panel_labels = ["a", "b", "c", "d", "e", "f"]
for label, ax in zip(panel_labels, axes.flatten()):
    ax.text(
        0.03,
        0.97,
        label,
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=11,
        fontweight="bold",
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.75, "pad": 1.5},
    )

cbar_top = fig.colorbar(
    pos_map,
    ax=axes[0, :],
    orientation="vertical",
    fraction=0.03,
    pad=0.02,
    aspect=28,
)
cbar_top.set_label(r"$\overline{zg^*}$/ m", fontsize=10)
cbar_top.ax.tick_params(labelsize=9)

cbar_bottom = fig.colorbar(
    eke_map,
    ax=axes[1, :],
    orientation="vertical",
    fraction=0.03,
    pad=0.02,
    aspect=28,
)
cbar_bottom.set_label("eke / m$^2$ s$^{-2}$", fontsize=10)
cbar_bottom.ax.tick_params(labelsize=9)

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0after_defense/steady_eddy_composite.pdf",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.05,
)

# %%
