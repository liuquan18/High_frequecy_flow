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
transient_pos_first = read_comp_var(
    "transient_eddy_heat_dy",
    "pos",
    1850,
    time_window="all",
    method="no_stat",
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)
transient_neg_first = read_comp_var(
    "transient_eddy_heat_dy",
    "neg",
    1850,
    time_window="all",
    method="no_stat",
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)
transient_pos_last = read_comp_var(
    "transient_eddy_heat_dy",
    "pos",
    2090,
    time_window="all",
    method="no_stat",
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)
transient_neg_last = read_comp_var(
    "transient_eddy_heat_dy",
    "neg",
    2090,
    time_window="all",
    method="no_stat",
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)
# %%
steady_pos_first = read_comp_var(
    "steady_eddy_heat_dy",
    "pos",
    1850,
    time_window="all",
    method="no_stat",
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)
steady_neg_first = read_comp_var(
    "steady_eddy_heat_dy",
    "neg",
    1850,
    time_window="all",
    method="no_stat",
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)
steady_pos_last = read_comp_var(
    "steady_eddy_heat_dy",
    "pos",
    2090,
    time_window="all",
    method="no_stat",
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)
steady_neg_last = read_comp_var(
    "steady_eddy_heat_dy",
    "neg",
    2090,
    time_window="all",
    method="no_stat",
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)

# %%
transient_clima_first = read_climatology(
    "transient_eddy_heat_dy",
    1850,
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)
transient_clima_last = read_climatology(
    "transient_eddy_heat_dy",
    2090,
    name="eddy_heat_dy",
    model_dir="MPI_GE_CMIP6_allplev",
)
steady_clima_first = read_climatology(
    "steady_eddy_heat_dy", 1850, name="eddy_heat_dy", model_dir="MPI_GE_CMIP6_allplev"
)
steady_clima_last = read_climatology(
    "steady_eddy_heat_dy", 2090, name="eddy_heat_dy", model_dir="MPI_GE_CMIP6_allplev"
)


# %%
# %%
def anomaly(ds, ds_clima):
    """
    Calculate the anomaly of a dataset with respect to a climatology.
    """
    # average over time and events
    ds = ds.sel(time=slice(0, 10)).mean(dim=("time", "event", "lon"))
    ds_clima = ds_clima.mean(dim=("lon"))
    anomaly = ds - ds_clima
    return anomaly.compute()


# %%
transient_pos_first_anom = anomaly(transient_pos_first, transient_clima_first)
transient_neg_first_anom = anomaly(transient_neg_first, transient_clima_first)
transient_pos_last_anom = anomaly(transient_pos_last, transient_clima_last)
transient_neg_last_anom = anomaly(transient_neg_last, transient_clima_last)
# %%
steady_pos_first_anom = anomaly(steady_pos_first, steady_clima_first)
steady_neg_first_anom = anomaly(steady_neg_first, steady_clima_first)
steady_pos_last_anom = anomaly(steady_pos_last, steady_clima_last)
steady_neg_last_anom = anomaly(steady_neg_last, steady_clima_last)

# %%
sum_pos_first_anomaly = transient_pos_first_anom + steady_pos_first_anom
sum_neg_first_anomaly = transient_neg_first_anom + steady_neg_first_anom
sum_pos_last_anomaly = transient_pos_last_anom + steady_pos_last_anom
sum_neg_last_anomaly = transient_neg_last_anom + steady_neg_last_anom

#%%
transient_pos_first_anom = transient_pos_first_anom.rolling(lat=3, center=True).mean()
transient_neg_first_anom = transient_neg_first_anom.rolling(lat=3, center=True).mean()
transient_pos_last_anom = transient_pos_last_anom.rolling(lat=3, center=True).mean()
transient_neg_last_anom = transient_neg_last_anom.rolling(lat=3, center=True).mean()


#%%
# smooth the map over lat to smooth
steady_pos_first_anom = steady_pos_first_anom.rolling(lat=3, center=True).mean()
steady_neg_first_anom = steady_neg_first_anom.rolling(lat=3, center=True).mean()
steady_pos_last_anom = steady_pos_last_anom.rolling(lat=3, center=True).mean()
steady_neg_last_anom = steady_neg_last_anom.rolling(lat=3, center=True).mean()

# %%
sum_levels = np.arange(-0.4, 0.41, 0.04)
transient_levels = np.arange(-0.3, 0.31, 0.03)
steady_levels = np.arange(-0.3, 0.31, 0.03)

#%%
fig, axes = plt.subplots(2, 3, figsize=(12, 8), sharey=True, )


# first row: now place transient in col 0, steady in col 1, sum in col 2
# transient (was middle -> now left)
cf_transient_pos_first = transient_pos_first_anom.plot.contourf(
    ax=axes[0, 0],
    x="lat",
    y="plev",
    levels=transient_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    ylim=(100000, 10000),
    xlim=(0, 90),
    extend="both",
)
transient_pos_last_anom.plot.contour(
    ax=axes[0, 0],
    x="lat",
    y="plev",
    levels=[l for l in transient_levels if l != 0],
    colors="black",
    linewidths=1,
    add_colorbar=False,
    ylim=(100000, 10000),
    xlim=(0, 90),
)

# second row: same reordering for neg
# transient (now left)
cf_transient_neg_first = transient_neg_first_anom.plot.contourf(
    ax=axes[0, 1],
    x="lat",
    y="plev",
    levels=transient_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    ylim=(100000, 10000),
    xlim=(0, 90),
    extend="both",
)
transient_neg_last_anom.plot.contour(
    ax=axes[0, 1],
    x="lat",
    y="plev",
    levels=[l for l in transient_levels if l != 0],
    colors="black",
    linewidths=1,
    add_colorbar=False,
    ylim=(100000, 10000),
    xlim=(0, 90),
)
# difference 
transient_diff_first = transient_pos_first_anom - transient_neg_first_anom
transient_diff_last = transient_pos_last_anom - transient_neg_last_anom
cf_transient_diff_first = transient_diff_first.plot.contourf(
    ax=axes[0, 2],
    x="lat",
    y="plev",
    levels=transient_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    ylim=(100000, 10000),
    xlim=(0, 90),
    extend="both",
)
transient_diff_last.plot.contour(
    ax=axes[0, 2],
    x="lat",
    y="plev",
    levels=[l for l in transient_levels if l != 0],
    colors="black",
    linewidths=1,
    add_colorbar=False,
    ylim=(100000, 10000),
    xlim=(0, 90),
)


# steady (was right -> now middle)
cf_steady_pos_first = steady_pos_first_anom.plot.contourf(
    ax=axes[1, 0],
    x="lat",
    y="plev",
    levels=steady_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    ylim=(100000, 10000),
    xlim=(0, 90),
    extend="both",
)
steady_pos_last_anom.plot.contour(
    ax=axes[1, 0],
    x="lat",
    y="plev",
    levels=[l for l in steady_levels if l != 0],
    colors="black",
    linewidths=1,
    add_colorbar=False,
    ylim=(100000, 10000),
    xlim=(0, 90),
)

# steady (now middle)
cf_steady_neg_first = steady_neg_first_anom.plot.contourf(
    ax=axes[1, 1],
    x="lat",
    y="plev",
    levels=steady_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    ylim=(100000, 10000),
    xlim=(0, 90),
    extend="both",
)
steady_neg_last_anom.plot.contour(
    ax=axes[1, 1],
    x="lat",
    y="plev",
    levels=[l for l in steady_levels if l != 0],
    colors="black",
    linewidths=1,
    add_colorbar=False,
    ylim=(100000, 10000),
    xlim=(0, 90),
)

# difference
steady_diff_first = steady_pos_first_anom - steady_neg_first_anom
steady_diff_last = steady_pos_last_anom - steady_neg_last_anom
cf_steady_diff_first = steady_diff_first.plot.contourf(
    ax=axes[1, 2],
    x="lat",
    y="plev",
    levels=steady_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    ylim=(100000, 10000),
    xlim=(0, 90),
    extend="both",
)
steady_diff_last.plot.contour(
    ax=axes[1, 2],  
    x="lat",
    y="plev",
    levels=[l for l in steady_levels if l != 0],
    colors="black",
    linewidths=1,
    add_colorbar=False,
    ylim=(100000, 10000),
    xlim=(0, 90),
)



# add colorbar for each row
cbar_transient = fig.colorbar(
    cf_transient_pos_first,
    ax=axes[0, :],
    orientation="vertical",
    fraction=0.04,
    pad=0.02,
    aspect=30,
    shrink=0.8,
    label=r"$\frac{\partial}{\partial y} (v'\theta')$ / K s$^{-1}$",
)
cbar_steady = fig.colorbar(
    cf_steady_pos_first,
    ax=axes[1, :],
    orientation="vertical",
    fraction=0.04,
    pad=0.02,
    aspect=30,
    shrink=0.8,
    label=r"$\frac{\partial}{\partial y} (v'\theta')$ / K s$^{-1}$",
)

# Set ticks for colorbars
cbar_transient.set_ticks([-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3])
cbar_steady.set_ticks([-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3])
# change y-ticks to hPa
for ax in axes.flat:
    ax.set_yticks(
        [100000, 90000, 80000, 70000, 60000, 50000, 40000, 30000, 20000, 10000]
    )
    ax.set_yticklabels(
        [str(int(tick / 100)) for tick in ax.get_yticks()]
    )  # Convert Pa to hPa
    ax.set_ylim(100000, 50000)
    ax.set_ylabel("Pressure / hPa")
    ax.set_xlabel("Latitude / °N")

# add a, b, c
first_col_labels = ["a", "d"]
for i, ax in enumerate(axes[:, 0].flat):
    axes[0,0].text(
        -0.2,
        0.95,
        first_col_labels[i],
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        va="bottom",
        ha="right",
    )


rest_labels = ["b", "c", "e", "f"]
for i, ax in enumerate(axes[:, 1:].flat):
    ax.set_ylabel("")
    ax.text(
        -0.05,
        0.95,
        rest_labels[i],
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        va="bottom",
        ha="right",
    )

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0after_defense/eddy_heat_dy_d2y2_profile.pdf", dpi=300, bbox_inches="tight", transparent=True, metadata={"Creator": __file__})

# %%
