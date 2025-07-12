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

read_comp_var = read_composite.read_comp_var
# %%
transient_pos_first = read_comp_var('transient_eddy_heat_d2y2', 'pos', 1850, time_window='all', method = 'no_stat', name = 'eddy_heat_d2y2', model_dir = 'MPI_GE_CMIP6_allplev')
transient_neg_first = read_comp_var('transient_eddy_heat_d2y2', 'neg', 1850, time_window='all', method = 'no_stat', name = 'eddy_heat_d2y2', model_dir = 'MPI_GE_CMIP6_allplev')
transient_pos_last = read_comp_var('transient_eddy_heat_d2y2', 'pos', 2090, time_window='all', method = 'no_stat', name = 'eddy_heat_d2y2', model_dir = 'MPI_GE_CMIP6_allplev')
transient_neg_last = read_comp_var('transient_eddy_heat_d2y2', 'neg', 2090, time_window='all', method = 'no_stat', name = 'eddy_heat_d2y2', model_dir = 'MPI_GE_CMIP6_allplev')
# %%
steady_pos_first = read_comp_var('steady_eddy_heat_d2y2', 'pos', 1850, time_window='all', method = 'no_stat', name = 'eddy_heat_d2y2', model_dir = 'MPI_GE_CMIP6_allplev')
steady_neg_first = read_comp_var('steady_eddy_heat_d2y2', 'neg', 1850, time_window='all', method = 'no_stat', name = 'eddy_heat_d2y2', model_dir = 'MPI_GE_CMIP6_allplev')
steady_pos_last = read_comp_var('steady_eddy_heat_d2y2', 'pos', 2090, time_window ='all', method = 'no_stat', name = 'eddy_heat_d2y2', model_dir = 'MPI_GE_CMIP6_allplev')
steady_neg_last = read_comp_var('steady_eddy_heat_d2y2', 'neg',       2090, time_window='all', method = 'no_stat', name = 'eddy_heat_d2y2', model_dir = 'MPI_GE_CMIP6_allplev')

#%%
transient_clima_first = read_climatology('transient_eddy_heat_d2y2', 1850, name = 'eddy_heat_d2y2', model_dir = 'MPI_GE_CMIP6_allplev')
transient_clima_last = read_climatology('transient_eddy_heat_d2y2', 2090, name = 'eddy_heat_d2y2', model_dir = 'MPI_GE_CMIP6_allplev')
steady_clima_first = read_climatology('steady_eddy_heat_d2y2', 1850, name = 'eddy_heat_d2y2', model_dir = 'MPI_GE_CMIP6_allplev')
steady_clima_last = read_climatology('steady_eddy_heat_d2y2', 2090, name = 'eddy_heat_d2y2', model_dir = 'MPI_GE_CMIP6_allplev')
#%%
# %%
def anomaly(ds, ds_clima):
    """
    Calculate the anomaly of a dataset with respect to a climatology.
    """
    # average over time and events
    ds = ds.sel(time = slice(-10, 5)).mean(dim=('time', 'event', 'lon'))
    ds_clima = ds_clima.mean(dim=('lon'))
    anomaly = ds - ds_clima
    return anomaly.compute()
#%%
transient_pos_first_anom = anomaly(transient_pos_first, transient_clima_first)
transient_neg_first_anom = anomaly(transient_neg_first, transient_clima_first)
transient_pos_last_anom = anomaly(transient_pos_last, transient_clima_last)
transient_neg_last_anom = anomaly(transient_neg_last, transient_clima_last)
#%%
steady_pos_first_anom = anomaly(steady_pos_first, steady_clima_first)
steady_neg_first_anom = anomaly(steady_neg_first, steady_clima_first)
steady_pos_last_anom = anomaly(steady_pos_last, steady_clima_last)
steady_neg_last_anom = anomaly(steady_neg_last, steady_clima_last)

#%%
sum_pos_first_anomaly = transient_pos_first_anom + steady_pos_first_anom
sum_neg_first_anomaly = transient_neg_first_anom + steady_neg_first_anom
sum_pos_last_anomaly = transient_pos_last_anom + steady_pos_last_anom
sum_neg_last_anomaly = transient_neg_last_anom + steady_neg_last_anom


#%%
# fldmean over
def to_dataframe(ds, ds_clima, var_name, phase, decade, plev = 85000, lat_slice = slice(40, 60)):
    ds = ds.sel(lat=lat_slice, plev = plev)
    ds_clima = ds_clima.sel(lat=lat_slice, plev = plev)

    anomaly = ds - ds_clima

    # create weights
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"

    anomaly = anomaly.weighted(weights).mean(dim = ('lat', 'lon'))

    df = anomaly.to_dataframe(var_name).reset_index()
    df["phase"] = phase
    df["decade"] = decade
    return df
#%%
transient_pos_first_df = to_dataframe(transient_pos_first, transient_clima_first, "eddy_heat_d2y2", "pos", "1850")
transient_neg_first_df = to_dataframe(transient_neg_first, transient_clima_first, "eddy_heat_d2y2", "neg", "1850")
transient_pos_last_df = to_dataframe(transient_pos_last, transient_clima_last, "eddy_heat_d2y2", "pos", "2090")
transient_neg_last_df = to_dataframe(transient_neg_last, transient_clima_last, "eddy_heat_d2y2", "neg", "2090")

#%%
steady_pos_first_df = to_dataframe(steady_pos_first, steady_clima_first, "eddy_heat_d2y2", "pos", "1850")
steady_neg_first_df = to_dataframe(steady_neg_first, steady_clima_first, "eddy_heat_d2y2", "neg", "1850")
steady_pos_last_df = to_dataframe(steady_pos_last, steady_clima_last, "eddy_heat_d2y2", "pos", "2090")
steady_neg_last_df = to_dataframe(steady_neg_last, steady_clima_last, "eddy_heat_d2y2", "neg", "2090")

#%%
sum_pos_first_df = transient_pos_first_df.copy()
sum_pos_first_df["eddy_heat_d2y2"] = transient_pos_first_df["eddy_heat_d2y2"] + steady_pos_first_df["eddy_heat_d2y2"]

sum_neg_first_df = transient_neg_first_df.copy()
sum_neg_first_df["eddy_heat_d2y2"] = transient_neg_first_df["eddy_heat_d2y2"] + steady_neg_first_df["eddy_heat_d2y2"]

sum_pos_last_df = transient_pos_last_df.copy()
sum_pos_last_df["eddy_heat_d2y2"] = transient_pos_last_df["eddy_heat_d2y2"] + steady_pos_last_df["eddy_heat_d2y2"]
sum_neg_last_df = transient_neg_last_df.copy()
sum_neg_last_df["eddy_heat_d2y2"] = transient_neg_last_df["eddy_heat_d2y2"] + steady_neg_last_df["eddy_heat_d2y2"]



#%%
sum_levels = np.arange(-0.4, 0.41, 0.04)
transient_levels = np.arange(-0.2, 0.21, 0.02)
steady_levels = np.arange(-0.2, 0.21, 0.02)
# %%
fig, axes = plt.subplots(3, 3, figsize=(12, 12), sharex=False, sharey="row")
# first row pos
# sum
cf_sum_pos_first = sum_pos_first_anomaly.plot.contourf(
    ax = axes[0, 0],
    x = 'lat',
    y = 'plev',
    levels = sum_levels,
    cmap = 'RdBu_r',
    add_colorbar = False,
    ylim = (100000, 10000),
    xlim = (0, 90),
    extend = 'both',
)
sum_pos_last_anomaly.plot.contour(
    ax = axes[0, 0],
    x = 'lat',
    y = 'plev',
    levels = [l for l in sum_levels if l != 0],
    colors = 'black',
    linewidths = 1,
    add_colorbar = False,
    ylim = (100000, 10000),
    xlim = (0, 90),
)

# transient
cf_transient_pos_first = transient_pos_first_anom.plot.contourf(
    ax = axes[0, 1],
    x = 'lat',
    y = 'plev',
    levels = transient_levels,
    cmap = 'RdBu_r',
    add_colorbar = False,
    ylim = (100000, 10000),
    xlim = (0, 90),
    extend = 'both',
)
transient_pos_last_anom.plot.contour(
    ax = axes[0, 1],
    x = 'lat',
    y = 'plev',
    levels = [l for l in transient_levels if l != 0],
    colors = 'black',
    linewidths = 1,
    add_colorbar = False,
    ylim = (100000, 10000),
    xlim = (0, 90),
)

# steady
cf_steady_pos_first = steady_pos_first_anom.plot.contourf(
    ax = axes[0, 2],
    x = 'lat',
    y = 'plev',
    levels = steady_levels,
    cmap = 'RdBu_r',
    add_colorbar = False,
    ylim = (100000, 10000),
    xlim = (0, 90),
    extend = 'both',
)
steady_pos_last_anom.plot.contour(
    ax = axes[0, 2],
    x = 'lat',
    y = 'plev',
    levels = [l for l in steady_levels if l != 0],
    colors = 'black',
    linewidths = 1,
    add_colorbar = False,
    ylim = (100000, 10000),
    xlim = (0, 90),
)

# second row neg
# sum
cf_sum_neg_first = sum_neg_first_anomaly.plot.contourf(
    ax = axes[1, 0],
    x = 'lat',
    y = 'plev',
    levels = sum_levels,
    cmap = 'RdBu_r',
    add_colorbar = False,
    ylim = (100000, 10000),
    xlim = (0, 90),
    extend = 'both',
)
sum_neg_last_anomaly.plot.contour(
    ax = axes[1, 0],
    x = 'lat',
    y = 'plev',
    levels = [l for l in sum_levels if l != 0],
    colors = 'black',
    linewidths = 1,
    add_colorbar = False,
    ylim = (100000, 10000),
    xlim = (0, 90),
)
# transient
cf_transient_neg_first = transient_neg_first_anom.plot.contourf(
    ax = axes[1, 1],
    x = 'lat',
    y = 'plev',
    levels = transient_levels,
    cmap = 'RdBu_r',
    add_colorbar = False,
    ylim = (100000, 10000),
    xlim = (0, 90),
    extend = 'both',
)
transient_neg_last_anom.plot.contour(
    ax = axes[1, 1],
    x = 'lat',
    y = 'plev',
    levels = [l for l in transient_levels if l != 0],
    colors = 'black',
    linewidths = 1,
    add_colorbar = False,
    ylim = (100000, 10000),
    xlim = (0, 90),
)
# steady
cf_steady_neg_first = steady_neg_first_anom.plot.contourf(
    ax = axes[1, 2],
    x = 'lat',
    y = 'plev',
    levels = steady_levels,
    cmap = 'RdBu_r',
    add_colorbar = False,
    ylim = (100000, 10000),
    xlim = (0, 90),
    extend = 'both',
)
steady_neg_last_anom.plot.contour(
    ax = axes[1, 2],
    x = 'lat',
    y = 'plev',
    levels = [l for l in steady_levels if l != 0],
    colors = 'black',
    linewidths = 1,
    add_colorbar = False,
    ylim = (100000, 10000),
    xlim = (0, 90),
)

# third row line plots
custom_palette = {'1850': 'black', '2090': 'red'}

# sum
sns.lineplot(
    data=sum_pos_first_df,
    x='time',
    y='eddy_heat_d2y2',
    color='black',
    ax=axes[2, 0],
    linestyle='solid',
    errorbar=("ci", 95),
)
sns.lineplot(
    data=sum_neg_first_df,
    x='time',
    y='eddy_heat_d2y2',
    color='black',
    ax=axes[2, 0],
    linestyle='dashed',
    errorbar=("ci", 95),
)
sns.lineplot(
    data=sum_pos_last_df,
    x='time',
    y='eddy_heat_d2y2',
    color='red',
    ax=axes[2, 0],
    linestyle='solid',
    errorbar=("ci", 95),
)
sns.lineplot(
    data=sum_neg_last_df,
    x='time',
    y='eddy_heat_d2y2',
    color='red',
    ax=axes[2, 0],
    linestyle='dashed',
    errorbar=("ci", 95),
)
# transient
sns.lineplot(
    data=transient_pos_first_df,
    x='time',
    y='eddy_heat_d2y2',
    color='black',
    ax=axes[2, 1],
    linestyle='solid',
    errorbar=("ci", 95),
)
sns.lineplot(
    data=transient_neg_first_df,
    x='time',
    y='eddy_heat_d2y2',
    color='black',
    ax=axes[2, 1],
    linestyle='dashed',
    errorbar=("ci", 95),
)
sns.lineplot(
    data=transient_pos_last_df,
    x='time',
    y='eddy_heat_d2y2',
    color='red',
    ax=axes[2, 1],
    linestyle='solid',
    errorbar=("ci", 95),
)
sns.lineplot(
    data=transient_neg_last_df,
    x='time',
    y='eddy_heat_d2y2',
    color='red',
    ax=axes[2, 1],
    linestyle='dashed',
    errorbar=("ci", 95),
)

# steady
sns.lineplot(
    data=steady_pos_first_df,
    x='time',
    y='eddy_heat_d2y2',
    color='black',
    ax=axes[2, 2],
    linestyle='solid',
    errorbar=("ci", 95),
)
sns.lineplot(
    data=steady_neg_first_df,
    x='time',
    y='eddy_heat_d2y2',
    color='black',
    ax=axes[2, 2],
    linestyle='dashed',
    errorbar=("ci", 95),
)
sns.lineplot(
    data=steady_pos_last_df,
    x='time',
    y='eddy_heat_d2y2',
    color='red',
    ax=axes[2, 2],
    linestyle='solid',
    errorbar=("ci", 95),
)
sns.lineplot(
    data=steady_neg_last_df,
    x='time',
    y='eddy_heat_d2y2',
    color='red',
    ax=axes[2, 2],
    linestyle='dashed',
    errorbar=("ci", 95),
)

# Add colorbars for each contourf plot in the top two rows
cbar_sum = fig.colorbar(
    cf_sum_pos_first,
    ax=axes[:2, 0],
    orientation="horizontal",
    fraction=0.04,
    pad=0.12,
    aspect=30,
    shrink=0.8,
    label = r"-∂/∂y (v'θ') [K s⁻¹]"
)
cbar_transient = fig.colorbar(
    cf_transient_pos_first,
    ax=axes[:2, 1],
    orientation="horizontal",
    fraction=0.04,
    pad=0.12,
    aspect=30,
    shrink=0.8,
    label = r"-∂/∂y (v'θ') [K s⁻¹]"
)
cbar_steady = fig.colorbar(
    cf_steady_pos_first,  
    ax=axes[:2, 2],
    orientation="horizontal",
    fraction=0.04,
    pad=0.12,
    aspect=30,
    shrink=0.8,
    label = r"-∂/∂y (v'θ') [K s⁻¹]"
)

# Set ticks for colorbars to avoid overlapping
cbar_sum.set_ticks([-0.4, 0.0, 0.4])
cbar_transient.set_ticks([-0.2, 0.0, 0.2])
cbar_steady.set_ticks([-0.2, 0.0, 0.2])

# Custom legend handles
decade_handles = [
    Line2D([0], [0], color="black", lw=2, label="1850"),
    Line2D([0], [0], color="red", lw=2, label="2090"),
]
phase_handles = [
    Line2D([0], [0], color="black", lw=2, linestyle="-", label="pos NAO"),
    Line2D([0], [0], color="black", lw=2, linestyle="--", label="neg NAO"),
]
decade_legend = axes[2, 2].legend(
    handles=decade_handles,
    title="Decade",
    loc="upper left",
    bbox_to_anchor=(0., 0.3),
    frameon=False,
)
phase_legend = axes[2, 2].legend(
    handles=phase_handles,
    title="Phase",
    loc="upper left",
    bbox_to_anchor=(0.4, 0.3),
    frameon=False,
)
axes[2, 2].add_artist(decade_legend)
axes[2, 2].add_artist(phase_legend)

axes[2, 2].set_ylabel("")

for ax in axes[:, 1:].flat:
    ax.set_ylabel("")
axes[2, 0].set_ylabel(
    r"-∂/∂y (v'θ') [K s⁻¹]"
)

# for the first column, set y-label for pressure (Pa to hPa)
for ax in axes[:2, 0].flat:
    ax.set_ylabel("Pressure [hPa]")
    ax.set_yticks([100000, 90000, 80000, 70000, 60000, 50000, 40000, 30000, 20000, 10000])
    ax.set_yticklabels([str(int(tick / 100)) for tick in ax.get_yticks()])  # Convert Pa to hPa
for ax in axes[1, :].flat:
    ax.set_xlabel("Latitude [°N]")
for ax in axes[0, :].flat:
    ax.set_xlabel("")

for ax in axes[2, :].flat:
    ax.set_xlabel("Days relative to extreme onset")

# remove top and right spines
for ax in axes[2, :].flat:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.axvline(0, color="k", linestyle="-", lw=0.5, zorder=0)
    ax.set_xlim(-20, 20)

# add a,b,c
for i, ax in enumerate(axes.flat):
    ax.text(
        -0.06,
        1.02,
        chr(97 + i),
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        va="bottom",
        ha="right",
    )


# # save
# plt.savefig(
#     "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eddy_heat_d2y2_together.pdf",
#     dpi=300,
#     bbox_inches="tight",
#     transparent=True,
#     metadata={"Creator": __file__},
# )

# %%
