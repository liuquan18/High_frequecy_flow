# %%
import glob
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.path as mpath
import matplotlib.ticker as mticker
import matplotlib.ticker as ticker


from src.dynamics.EP_flux import PlotEPfluxArrows
from src.data_helper import read_composite
from src.plotting.util import erase_white_line, map_smooth, NA_box
import importlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
from src.data_helper.read_variable import read_climatology, read_climatology_decmean
from metpy.units import units
import numpy as np
import os
import cartopy
from matplotlib.patches import Rectangle
from shapely.geometry import Polygon
from matplotlib.ticker import FuncFormatter
import metpy.calc as mpcalc
import src.plotting.util as util

importlib.reload(read_composite)
importlib.reload(util)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var
clip_map = util.clip_map

####################################
# read transient simulation data
# %%
ua_pos_first = read_comp_var(
    "ua",
    "pos",
    1850,
    time_window=(-10, 5),
    method="mean",
    name="ua",
    model_dir="MPI_GE_CMIP6_allplev",
)
ua_neg_first = read_comp_var(
    "ua",
    "neg",
    1850,
    time_window=(-10, 5),
    method="mean",
    name="ua",
    model_dir="MPI_GE_CMIP6_allplev",
)
# %%
ua_pos_last = read_comp_var(
    "ua",
    "pos",
    2090,
    time_window=(-10, 5),
    method="mean",
    name="ua",
    model_dir="MPI_GE_CMIP6_allplev",
)
ua_neg_last = read_comp_var(
    "ua",
    "neg",
    2090,
    time_window=(-10, 5),
    method="mean",
    name="ua",
    model_dir="MPI_GE_CMIP6_allplev",
)
# %%
baroc_pos_first = read_comp_var(
    "eady_growth_rate",
    "pos",
    1850,
    time_window=(-10, 5),
    method="mean",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
baroc_neg_first = read_comp_var(
    "eady_growth_rate",
    "neg",
    1850,
    time_window=(-10, 5),
    method="mean",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
baroc_pos_last = read_comp_var(
    "eady_growth_rate",
    "pos",
    2090,
    time_window=(-10, 5),
    method="mean",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
baroc_neg_last = read_comp_var(
    "eady_growth_rate",
    "neg",
    2090,
    time_window=(-10, 5),
    method="mean",
    name="eady_growth_rate",
    model_dir="MPI_GE_CMIP6_allplev",
)
# %%
# baroclinicity from s-1 to day-1
baroc_pos_first = baroc_pos_first * 86400
baroc_neg_first = baroc_neg_first * 86400
baroc_pos_last = baroc_pos_last * 86400
baroc_neg_last = baroc_neg_last * 86400


# %%
# ua select 25000
ua_pos_first = ua_pos_first.sel(plev=25000)
ua_neg_first = ua_neg_first.sel(plev=25000)
ua_pos_last = ua_pos_last.sel(plev=25000)
ua_neg_last = ua_neg_last.sel(plev=25000)
# %%
# baroc select 85000
baroc_pos_first = baroc_pos_first.sel(plev=85000)
baroc_neg_first = baroc_neg_first.sel(plev=85000)
baroc_pos_last = baroc_pos_last.sel(plev=85000)
baroc_neg_last = baroc_neg_last.sel(plev=85000)

# %%
ua_diff_first = ua_pos_first - ua_neg_first
ua_diff_last = ua_pos_last - ua_neg_last
baroc_diff_first = baroc_pos_first - baroc_neg_first
baroc_diff_last = baroc_pos_last - baroc_neg_last

# %%
# change from lon 0-360 to -180 to 180
ua_pos_first = util.lon360to180(ua_pos_first)
ua_neg_first = util.lon360to180(ua_neg_first)
ua_pos_last = util.lon360to180(ua_pos_last)
ua_neg_last = util.lon360to180(ua_neg_last)
ua_diff_first = util.lon360to180(ua_diff_first)
ua_diff_last = util.lon360to180(ua_diff_last)

baroc_pos_first = util.lon360to180(baroc_pos_first)
baroc_neg_first = util.lon360to180(baroc_neg_first)
baroc_pos_last = util.lon360to180(baroc_pos_last)
baroc_neg_last = util.lon360to180(baroc_neg_last)
baroc_diff_first = util.lon360to180(baroc_diff_first)
baroc_diff_last = util.lon360to180(baroc_diff_last)
# %%
# zonal mean
ua_pos_first_zm = ua_pos_first.sel(lon=slice(-120, 60)).mean(dim="lon")
ua_neg_first_zm = ua_neg_first.sel(lon=slice(-120, 60)).mean(dim="lon")
ua_pos_last_zm = ua_pos_last.sel(lon=slice(-120, 60)).mean(dim="lon")
ua_neg_last_zm = ua_neg_last.sel(lon=slice(-120, 60)).mean(dim="lon")
ua_diff_first_zm = ua_diff_first.sel(lon=slice(-120, 60)).mean(dim="lon")
ua_diff_last_zm = ua_diff_last.sel(lon=slice(-120, 60)).mean(dim="lon")
# %%
baroc_pos_first_zm = baroc_pos_first.sel(lon=slice(-120, 0)).mean(dim="lon")
baroc_neg_first_zm = baroc_neg_first.sel(lon=slice(-120, 0)).mean(dim="lon")
baroc_pos_last_zm = baroc_pos_last.sel(lon=slice(-120, 0)).mean(dim="lon")
baroc_neg_last_zm = baroc_neg_last.sel(lon=slice(-120, 0)).mean(dim="lon")
baroc_diff_first_zm = baroc_diff_first.sel(lon=slice(-120, 0)).mean(dim="lon")
baroc_diff_last_zm = baroc_diff_last.sel(lon=slice(-120, 0)).mean(dim="lon")

# %%
# calculate the data and load the data for plotting
ua_pos_first_zm = ua_pos_first_zm.compute()
ua_neg_first_zm = ua_neg_first_zm.compute()
ua_pos_last_zm = ua_pos_last_zm.compute()
ua_neg_last_zm = ua_neg_last_zm.compute()
ua_diff_first_zm = ua_diff_first_zm.compute()
ua_diff_last_zm = ua_diff_last_zm.compute()
# %%
baroc_pos_first_zm = baroc_pos_first_zm.compute()
baroc_neg_first_zm = baroc_neg_first_zm.compute()
baroc_pos_last_zm = baroc_pos_last_zm.compute()
baroc_neg_last_zm = baroc_neg_last_zm.compute()
baroc_diff_first_zm = baroc_diff_first_zm.compute()
baroc_diff_last_zm = baroc_diff_last_zm.compute()
# %%
# only northern hemisphere
ua_pos_first_zm = ua_pos_first_zm.sel(lat=slice(0, 90))
ua_neg_first_zm = ua_neg_first_zm.sel(lat=slice(0, 90))
ua_pos_last_zm = ua_pos_last_zm.sel(lat=slice(0, 90))
ua_neg_last_zm = ua_neg_last_zm.sel(lat=slice(0, 90))
ua_diff_first_zm = ua_diff_first_zm.sel(lat=slice(0, 90))
ua_diff_last_zm = ua_diff_last_zm.sel(lat=slice(0, 90))

baroc_pos_first_zm = baroc_pos_first_zm.sel(lat=slice(0, 90))
baroc_neg_first_zm = baroc_neg_first_zm.sel(lat=slice(0, 90))
baroc_pos_last_zm = baroc_pos_last_zm.sel(lat=slice(0, 90))
baroc_neg_last_zm = baroc_neg_last_zm.sel(lat=slice(0, 90))
baroc_diff_first_zm = baroc_diff_first_zm.sel(lat=slice(0, 90))
baroc_diff_last_zm = baroc_diff_last_zm.sel(lat=slice(0, 90))

# %%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# read eddy forcing and feedback


# Anomaly calculation
def anomaly(ds, ds_clima):
    ds = ds.sel(time=slice(-10, 5)).mean(dim=("time", "event", "lon"))
    ds_clima = ds_clima.mean(dim=("lon"))
    anomaly = ds - ds_clima
    return anomaly.load()


#####
# momentum forcing from transient eddies
# Read transient and steady EP flux for positive and negative phase, first and last decade, and climatology
Tdivphi_pos_first = read_EP_flux(
    phase="pos", decade=1850, eddy="transient", ano=False, lon_mean=False, region=None
)[2]
Tdivphi_neg_first = read_EP_flux(
    phase="neg", decade=1850, eddy="transient", ano=False, lon_mean=False, region=None
)[2]
Tdivphi_pos_last = read_EP_flux(
    phase="pos", decade=2090, eddy="transient", ano=False, lon_mean=False, region=None
)[2]
Tdivphi_neg_last = read_EP_flux(
    phase="neg", decade=2090, eddy="transient", ano=False, lon_mean=False, region=None
)[2]
Tdivphi_clima_first = read_EP_flux(
    phase="clima", decade=1850, eddy="transient", ano=False, lon_mean=False, region=None
)[2]
Tdivphi_clima_last = read_EP_flux(
    phase="clima", decade=2090, eddy="transient", ano=False, lon_mean=False, region=None
)[2]


# %%
Tdiv_phi_pos_first_anomaly = anomaly(Tdivphi_pos_first, Tdivphi_clima_first)
Tdiv_phi_neg_first_anomaly = anomaly(Tdivphi_neg_first, Tdivphi_clima_first)
Tdiv_phi_pos_last_anomaly = anomaly(Tdivphi_pos_last, Tdivphi_clima_last)
Tdiv_phi_neg_last_anomaly = anomaly(Tdivphi_neg_last, Tdivphi_clima_last)
# %%
Tdiv_phi_pos_first_anomaly = Tdiv_phi_pos_first_anomaly.sel(
    plev=25000, lat=slice(0, 90)
)
Tdiv_phi_neg_first_anomaly = Tdiv_phi_neg_first_anomaly.sel(
    plev=25000, lat=slice(0, 90)
)
Tdiv_phi_pos_last_anomaly = Tdiv_phi_pos_last_anomaly.sel(plev=25000, lat=slice(0, 90))
Tdiv_phi_neg_last_anomaly = Tdiv_phi_neg_last_anomaly.sel(plev=25000, lat=slice(0, 90))

# %%
# climatology of Tdiv_phi std for the first and last decade
Tdiv_phi_std_first = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/Fdiv_phi_transient_std_decmean/Fdiv_phi_transient_std_monmean_ensmean_185005_185909.nc"
)["std"]
Tdiv_phi_std_last = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/Fdiv_phi_transient_std_decmean/Fdiv_phi_transient_std_monmean_ensmean_209005_209909.nc"
)["std"]

Tdiv_phi_std_first = (
    Tdiv_phi_std_first.sel(plev=25000, lat=slice(0, 90))
    .mean(dim=("lon", "time"))
    .compute()
)
Tdiv_phi_std_last = (
    Tdiv_phi_std_last.sel(plev=25000, lat=slice(0, 90))
    .mean(dim=("lon", "time"))
    .compute()
)
# %%
Tdiv_phi_std_last_ratio = Tdiv_phi_std_last / Tdiv_phi_std_first
# %%
############
# thermal feedback from quasi-stationary eddies
steady_pos_first = read_comp_var(
    "steady_eddy_heat_d2y2",
    "pos",
    1850,
    time_window=(-10, 5),
    method="no_stat",
    name="eddy_heat_d2y2",
    model_dir="MPI_GE_CMIP6_allplev",
)
steady_neg_first = read_comp_var(
    "steady_eddy_heat_d2y2",
    "neg",
    1850,
    time_window=(-10, 5),
    method="no_stat",
    name="eddy_heat_d2y2",
    model_dir="MPI_GE_CMIP6_allplev",
)
steady_pos_last = read_comp_var(
    "steady_eddy_heat_d2y2",
    "pos",
    2090,
    time_window=(-10, 5),
    method="no_stat",
    name="eddy_heat_d2y2",
    model_dir="MPI_GE_CMIP6_allplev",
)
steady_neg_last = read_comp_var(
    "steady_eddy_heat_d2y2",
    "neg",
    2090,
    time_window=(-10, 5),
    method="no_stat",
    name="eddy_heat_d2y2",
    model_dir="MPI_GE_CMIP6_allplev",
)
# %%
steady_clima_first = read_climatology(
    "steady_eddy_heat_d2y2",
    1850,
    name="eddy_heat_d2y2",
    model_dir="MPI_GE_CMIP6_allplev",
)
steady_clima_last = read_climatology(
    "steady_eddy_heat_d2y2",
    2090,
    name="eddy_heat_d2y2",
    model_dir="MPI_GE_CMIP6_allplev",
)
# %%
steady_pos_first_anomaly = anomaly(steady_pos_first, steady_clima_first)
steady_neg_first_anomaly = anomaly(steady_neg_first, steady_clima_first)
steady_pos_last_anomaly = anomaly(steady_pos_last, steady_clima_last)
steady_neg_last_anomaly = anomaly(steady_neg_last, steady_clima_last)
# %%

steady_pos_first_anomaly = steady_pos_first_anomaly.sel(plev=85000, lat=slice(0, 90))
steady_neg_first_anomaly = steady_neg_first_anomaly.sel(plev=85000, lat=slice(0, 90))
steady_pos_last_anomaly = steady_pos_last_anomaly.sel(plev=85000, lat=slice(0, 90))
steady_neg_last_anomaly = steady_neg_last_anomaly.sel(plev=85000, lat=slice(0, 90))

# %%
# running media
window = 5
steady_pos_first_anomaly = (
    steady_pos_first_anomaly.rolling(lat=window, center=True).median().dropna("lat")
)
steady_neg_first_anomaly = (
    steady_neg_first_anomaly.rolling(lat=window, center=True).median().dropna("lat")
)
steady_pos_last_anomaly = (
    steady_pos_last_anomaly.rolling(lat=window, center=True).median().dropna("lat")
)
steady_neg_last_anomaly = (
    steady_neg_last_anomaly.rolling(lat=window, center=True).median().dropna("lat")
)


# %%
# climatology of steady eddy heat d2y2 std for the first and last decade
steady_clima_std_first = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/steady_eddy_heat_d2y2_std_decmean/steady_eddy_heat_d2y2_std_monmean_ensmean_185005_185909.nc"
)["std"]
steady_clima_std_last = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/steady_eddy_heat_d2y2_std_decmean/steady_eddy_heat_d2y2_std_monmean_ensmean_209005_209909.nc"
)["std"]

steady_clima_std_first = (
    steady_clima_std_first.sel(plev=85000, lat=slice(0, 90))
    .mean(dim=("lon", "time"))
    .compute()
)
steady_clima_std_last = (
    steady_clima_std_last.sel(plev=85000, lat=slice(0, 90))
    .mean(dim=("lon", "time"))
    .compute()
)

steady_clima_std_last_ratio = steady_clima_std_last / steady_clima_std_first
# %%
# New plot: 2x2 layout for jet stream (UA) analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12), sharey=True)

# Define bar width for all subplots
bar_width = 2  # degrees latitude

# axes[0, 0]: Composite difference (Pos - Neg) for first and last periods
lat = ua_diff_first_zm.lat.values

# Plot difference lines
ua_diff_first = ua_diff_first_zm.values
ua_diff_last = ua_diff_last_zm.values
(line1,) = axes[0, 0].plot(ua_diff_first, lat, "k-", label="1850s", linewidth=2)
(line2,) = axes[0, 0].plot(ua_diff_last, lat, "k--", label="2090s", linewidth=2)
axes[0, 0].axvline(0, color="black", linestyle=":", alpha=0.5)
axes[0, 0].set_xlabel(r"u at 250 hPa / $ms^{-1}$", fontsize=12)
axes[0, 0].set_ylabel("Latitude [°]", fontsize=12)
axes[0, 0].set_title("upper-level zonal Jet stream")

# Secondary x-axis: plot change as bars
ax_bar = axes[0, 0].twiny()
ua_change = ua_diff_last_zm - ua_diff_first_zm

# Scale the data by 2 so that when displayed, it appears at half value
bar1 = ax_bar.barh(
    lat, ua_change * 2, height=bar_width, alpha=0.3, color="red", label="2090s - 1850s"
)

# Now align the axes - they should have the same limits
xlim1 = axes[0, 0].get_xlim()
ax_bar.set_xlim(xlim1)


# Format tick labels to show half the actual value
def half_formatter(x, pos):
    return f"{x/2:.1f}"


ax_bar.xaxis.set_major_formatter(FuncFormatter(half_formatter))

ax_bar.axvline(0, color="red", linestyle=":", alpha=0.5)
ax_bar.set_xlabel(r"$\Delta u$ at 250 hPa / $ms^{-1}$", fontsize=12, color="red")
ax_bar.tick_params(axis="x", labelcolor="red")

# Combined legend
axes[0, 0].legend(
    [line1, line2, bar1], ["1850s", "2090s", "2090s - 1850s"], loc="lower right"
)

#  axes[0, 1]: line plot showing Tdiv_phi_pos_first_anomaly - Tdiv_phi_neg_first_anomaly and Tdiv_phi_pos_last_anomaly - Tdiv_phi_neg_last_anomaly
# bar plot showing Tdiv_phi_std_last_ratio, vline at x = 1
lat = Tdiv_phi_pos_first_anomaly.lat.values

# Calculate differences
Tdiv_phi_diff_first = Tdiv_phi_pos_first_anomaly - Tdiv_phi_neg_first_anomaly
Tdiv_phi_diff_last = Tdiv_phi_pos_last_anomaly - Tdiv_phi_neg_last_anomaly

# Plot difference lines
(line1,) = axes[0, 1].plot(Tdiv_phi_diff_first, lat, "k-", label="1850s", linewidth=2)
(line2,) = axes[0, 1].plot(Tdiv_phi_diff_last, lat, "k--", label="2090s", linewidth=2)
axes[0, 1].axvline(0, color="black", linestyle=":", alpha=0.5)
axes[0, 1].set_xlabel(
    r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ / m $s^{-1}$ day $^{-1}$",
    fontsize=12,
)
axes[0, 1].set_title(
    "Transient Eddy Momentum Forcing",
    fontsize=14,
)


# Secondary x-axis: plot change as bars
ax_bar = axes[0, 1].twiny()
Tdiv_phi_change = Tdiv_phi_diff_last - Tdiv_phi_diff_first

# Scale the data by 2 so that when displayed, it appears at half value
bar1 = ax_bar.barh(
    lat,
    Tdiv_phi_change * 2,
    height=bar_width,
    alpha=0.3,
    color="red",
    label="2090s - 1850s",
)

# Now align the axes - they should have the same limits
xlim1 = axes[0, 1].get_xlim()
ax_bar.set_xlim(xlim1)


# Format tick labels to show half the actual value
def half_formatter_eddy(x, pos):
    return f"{x/2:.2f}"


ax_bar.xaxis.set_major_formatter(FuncFormatter(half_formatter_eddy))

ax_bar.axvline(0, color="red", linestyle=":", alpha=0.5)
ax_bar.set_xlabel(
    r"$\Delta$ $-\frac{\partial}{\partial y} (\overline{u'v'})$ / m $s^{-1}$ day $^{-1}$",
    fontsize=12,
    color="red",
)
ax_bar.tick_params(axis="x", labelcolor="red")

# Combined legend
axes[0, 1].legend(
    [line1, line2, bar1], ["1850s", "2090s", "2090s - 1850s"], loc="lower right"
)


# axes[1, 0]: Composite difference (Pos - Neg) for first and last periods
lat = baroc_diff_first_zm.lat.values

# Plot difference lines
baroc_diff_first = baroc_diff_first_zm.values
baroc_diff_last = baroc_diff_last_zm.values
(line1,) = axes[1, 0].plot(baroc_diff_first, lat, "k-", label="1850s", linewidth=2)
(line2,) = axes[1, 0].plot(baroc_diff_last, lat, "k--", label="2090s", linewidth=2)
axes[1, 0].axvline(0, color="black", linestyle=":", alpha=0.5)
axes[1, 0].set_xlabel("Eady growth rate / $day^{-1}$", fontsize=12)
axes[1, 0].set_ylabel("Latitude [°]", fontsize=12)
axes[1, 0].set_title(
    "Lower-level baroclinicity",
    fontsize=14,
)

# Secondary x-axis: plot change as bars
ax_bar = axes[1, 0].twiny()
baroc_change = baroc_diff_last_zm - baroc_diff_first_zm

# Scale the data by 2 so that when displayed, it appears at half value
bar1 = ax_bar.barh(
    lat, baroc_change * 2, height=bar_width, alpha=0.3, color="red", label="2090s - 1850s"
)

# Now align the axes - they should have the same limits
xlim1 = axes[1, 0].get_xlim()
ax_bar.set_xlim(xlim1)


# Format tick labels to show half the actual value
def half_formatter(x, pos):
    return f"{x/2:.2f}"


ax_bar.xaxis.set_major_formatter(FuncFormatter(half_formatter))

ax_bar.axvline(0, color="red", linestyle=":", alpha=0.5)
ax_bar.set_xlabel(r"$\Delta$ Eady growth rate / $day^{-1}$", fontsize=12, color="red")
ax_bar.tick_params(axis="x", labelcolor="red")

# Combined legend
axes[1, 0].legend(
    [line1, line2, bar1], ["1850s", "2090s", "2090s - 1850s"], loc="lower right"
)

#  axes[1, 1]: line plot showing steady_pos_first_anomaly - steady_neg_first_anomaly and steady_pos_last_anomaly - steady_neg_last_anomaly
# bar plot showing steady_clima_std_last_ratio, vline at x = 1
lat = steady_pos_first_anomaly.lat.values
# Calculate differences
steady_diff_first = steady_pos_first_anomaly - steady_neg_first_anomaly
steady_diff_last = steady_pos_last_anomaly - steady_neg_last_anomaly
# Plot difference lines
(line1,) = axes[1, 1].plot(steady_diff_first, lat, "k-", label="1850s", linewidth=2)
(line2,) = axes[1, 1].plot(steady_diff_last, lat, "k--", label="2090s", linewidth=2)
axes[1, 1].axvline(0, color="black", linestyle=":", alpha=0.5)
axes[1, 1].set_xlabel(
    r"$-\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta'}}{\overline{\theta}_p} \right)$ / m $s^{-1}$ day $^{-1}$",
    fontsize=12,
)
axes[1, 1].set_title(
    "Quasi-stationary Eddy Thermal Feedback",
    fontsize=14,
)


# Secondary x-axis: plot change as bars
ax_bar = axes[1, 1].twiny()
lat = steady_pos_first_anomaly.lat.values
steady_change = steady_diff_last - steady_diff_first

# Scale the data by 2 so that when displayed, it appears at half value
bar1 = ax_bar.barh(
    lat,
    steady_change * 2,
    height=bar_width,
    alpha=0.3,
    color="red",
    label="2090s - 1850s",
)

# Now align the axes - they should have the same limits
axes[1, 1].set_xlim(-7*1e-12, 5*1e-12)
xlim1 = axes[1, 1].get_xlim()
ax_bar.set_xlim(xlim1)


# Format tick labels to show half the actual value
# def half_formatter_steady(x, pos):
#     return f"{x/2:.2e}"


# ax_bar.xaxis.set_major_formatter(FuncFormatter(half_formatter_steady))

ax_bar.axvline(0, color="red", linestyle=":", alpha=0.5)
ax_bar.set_xlabel(
    r"$\Delta$ $-\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta'}}{\overline{\theta}_p} \right)$ / m $s^{-1}$ day $^{-1}$",
    fontsize=12,
    color="red",
)
ax_bar.tick_params(axis="x", labelcolor="red")

# Combined legend
axes[1, 1].legend(
    [line1, line2, bar1], ["1850s", "2090s", "2090s - 1850s"], loc="upper right"
)

plt.tight_layout()
# %%
