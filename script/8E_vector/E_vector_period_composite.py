# %%
import xarray as xr
import numpy as np
import pandas as pd
import logging
import glob
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# %%
logging.basicConfig(level=logging.INFO)

# %%
import src.composite.composite as composite
import src.extremes.extreme_read as ext_read
import src.composite.composite_plot as composite_plot

# %%
from src.composite.composite import composite_variable

# %%
plev = 25000
# %%
uhat_first10_pos, uhat_first10_neg = composite_variable("ua", plev, "hat", "first10")
uhat_last10_pos, uhat_last10_neg = composite_variable("ua", plev, "hat", "last10")
# %%
M_first10_pos, M_first10_neg = composite_variable("E_M", plev, "prime", "first10")
M_last10_pos, M_last10_neg = composite_variable("E_M", plev, "prime", "last10")
# %%
N_first10_pos, N_first10_neg = composite_variable("E_N", plev, "prime", "first10")
N_last10_pos, N_last10_neg = composite_variable("E_N", plev, "prime", "last10")
# %%
E_M_first10_pos = -2 * M_first10_pos
E_M_last10_pos = -2 * M_last10_pos
E_N_first10_pos = -N_first10_pos
E_N_last10_pos = -N_last10_pos

E_M_first10_neg = -2 * M_first10_neg
E_M_last10_neg = -2 * M_last10_neg
E_N_first10_neg = -N_first10_neg
E_N_last10_neg = -N_last10_neg


# %%
def plot_E(E_M, E_N, u_hat, ax):

    lon = E_M.lon.values
    lat = E_M.lat.values

    skip = 3
    wind_levels = np.arange(-20, 25, 5)
    wind_levels = wind_levels[(wind_levels < -3) | (wind_levels > 3)]
    ax.coastlines(color="grey", linewidth=0.5)
    lines = u_hat.plot.contourf(
        ax=ax,
        levels=wind_levels,
        extend="both",
        kwargs=dict(inline=True),
        alpha=0.6,
        add_colorbar=False,
        transform=ccrs.PlateCarree(),
    )

    arrows = ax.quiver(
        lon[::skip],
        lat[::skip],
        E_M[::skip, ::skip],
        E_N[::skip, ::skip],
        scale=1000,
    )

    ax.set_extent([-180, 180, 0, 90], ccrs.PlateCarree())

    ax.quiverkey(arrows, X=0.85, Y=1.25, U=100, label=r"$100 m^2/s^2$", labelpos="E")

    return ax, lines, arrows


# %%
fig, axes = plt.subplots(
    6, 2, figsize=(17, 17), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -5
interval_lag = 2


start_lag = start_lag
length_lag = 6
interval_lag = interval_lag
stop_lag = start_lag + length_lag * interval_lag
extreme_type = "pos"

lag_days = np.arange(start_lag, stop=stop_lag, step=interval_lag)
periods = ["first10", "last10"]

uhat_data = [uhat_first10_pos, uhat_last10_pos]
E_M_data = [E_M_first10_pos, E_M_last10_pos]
E_N_data = [E_N_first10_pos, E_N_last10_pos]

for i, period in enumerate(periods):
    for j, lag in enumerate(lag_days):
        _, lines, arrows = plot_E(
            E_M_data[i].sel(time=lag),
            E_N_data[i].sel(time=lag),
            uhat_data[i].sel(time=lag),
            axes[j, i],
        )
        axes[j, i].set_title(f"{period} {extreme_type} lag {lag}")

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(lines, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of positive extremes")
plt.tight_layout(rect=[0, 0.1, 1, 1])

# plt.savefig(
#     "/work/mh0033/m300883/High_frequecy_flow/docs/plots/E_vector/E_vector_pos_arrow.png",
#     dpi=300,
# )

# %%
# same for negative extremes
fig, axes = plt.subplots(
    6, 2, figsize=(17, 17), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -10
interval_lag = 2

start_lag = start_lag
length_lag = 6
interval_lag = interval_lag
stop_lag = start_lag + length_lag * interval_lag
extreme_type = "neg"

lag_days = np.arange(start_lag, stop=stop_lag, step=interval_lag)
periods = ["first10", "last10"]

uhat_data = [uhat_first10_neg, uhat_last10_neg]
E_M_data = [E_M_first10_neg, E_M_last10_neg]
E_N_data = [E_N_first10_neg, E_N_last10_neg]

for i, period in enumerate(periods):
    for j, lag in enumerate(lag_days):
        _, lines, arrows = plot_E(
            E_M_data[i].sel(time=lag),
            E_N_data[i].sel(time=lag),
            uhat_data[i].sel(time=lag),
            axes[j, i],
        )
        axes[j, i].set_title(f"{period} {extreme_type} lag {lag}")

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(lines, cax=cbar_ax, orientation="horizontal")

plt.suptitle("Composite of negative extremes")
plt.tight_layout(rect=[0, 0.1, 1, 1])

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/E_vector/E_vector_neg_arrow.png",
    dpi=300,
)

# %%
