# %%
import xarray as xr
import numpy as np
import pandas as pd
import logging
import glob
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from metpy.units import units

# Any import of metpy will activate the accessors
import metpy.calc as mpcalc
from metpy.units import units

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
# multiply units (m**2/s**2)
E_M_first10_pos = E_M_first10_pos * units("m**2/s**2")
E_M_first10_pos = E_M_first10_pos.metpy.quantify()

E_N_first10_pos = E_N_first10_pos * units("m**2/s**2")
E_N_first10_pos = E_N_first10_pos.metpy.quantify()


E_M_last10_pos = E_M_last10_pos * units("m**2/s**2")
E_M_last10_pos = E_M_last10_pos.metpy.quantify()

E_N_last10_pos = E_N_last10_pos * units("m**2/s**2")
E_N_last10_pos = E_N_last10_pos.metpy.quantify()

#%%
# smoothing
E_M_first10_pos = mpcalc.smooth_gaussian(E_M_first10_pos, 5)
E_N_first10_pos = mpcalc.smooth_gaussian(E_N_first10_pos, 5)

E_M_last10_pos = mpcalc.smooth_gaussian(E_M_last10_pos, 5)
E_N_last10_pos = mpcalc.smooth_gaussian(E_N_last10_pos, 5)


# %%
E_div_first10_pos = mpcalc.divergence(E_M_first10_pos, E_N_first10_pos)
E_div_last10_pos = mpcalc.divergence(E_M_last10_pos, E_N_last10_pos)

E_div_first10_neg = mpcalc.divergence(E_M_first10_neg, E_N_first10_neg)
E_div_last10_neg = mpcalc.divergence(E_M_last10_neg, E_N_last10_neg)


# %%
def plot_E(E_M, E_N, E_div, ax, div_levels=np.arange(-1.8e-4, 1.9e-4, 0.2e-4)):

    lon = E_M.lon.values
    lat = E_M.lat.values

    skip = 3

    ax.coastlines(color="grey", linewidth=0.5)
    lines = E_div.plot.contourf(
        ax=ax,
        levels=div_levels,
        extend="both",
        kwargs=dict(inline=True),
        # alpha=0.6,
        add_colorbar=False,
        transform=ccrs.PlateCarree(),
    )

    # arrows = ax.quiver(
    #     lon[::skip],
    #     lat[::skip],
    #     E_M[::skip, ::skip],
    #     E_N[::skip, ::skip],
    #     scale=1000,
    # )
    # ax.quiverkey(arrows, X=0.85, Y=1.25, U=100, label=r"$100 m^2/s^2$", labelpos="E")

    ax.set_extent([-180, 180, 0, 90], ccrs.PlateCarree())

    return ax, lines, arrows


# %%
fig, axes = plt.subplots(
    6, 2, figsize=(17, 17), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -10
interval_lag = 2


start_lag = start_lag
length_lag = 6
interval_lag = interval_lag
stop_lag = start_lag + length_lag * interval_lag
extreme_type = "pos"

lag_days = np.arange(start_lag, stop=stop_lag, step=interval_lag)
periods = ["first10", "last10"]

E_div_data = [E_div_first10_pos, E_div_last10_pos]
E_M_data = [E_M_first10_pos, E_M_last10_pos]
E_N_data = [E_N_first10_pos, E_N_last10_pos]

for i, period in enumerate(periods):
    for j, lag in enumerate(lag_days):
        _, lines, arrows = plot_E(
            E_M_data[i].sel(time=lag),
            E_N_data[i].sel(time=lag),
            E_div_data[i].sel(time=lag),
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
for ax in axes[-1, :]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

# add y-axis labels for the first column
for ax in axes[:, 0]:
    ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])


plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/E_vector/E_vector_pos_divergence.png"
)
# %%
# negative
fig, axes = plt.subplots(
    6, 2, figsize=(17, 17), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)
start_lag = -10
interval_lag = 2

start_lag = start_lag
length_lag = 6

lag_days = np.arange(
    start_lag, stop=start_lag + length_lag * interval_lag, step=interval_lag
)
periods = ["first10", "last10"]
extreme_type = "neg"

E_div_data = [E_div_first10_neg, E_div_last10_neg]
E_M_data = [E_M_first10_neg, E_M_last10_neg]
E_N_data = [E_N_first10_neg, E_N_last10_neg]

for i, period in enumerate(periods):
    for j, lag in enumerate(lag_days):
        _, lines, arrows = plot_E(
            E_M_data[i].sel(time=lag),
            E_N_data[i].sel(time=lag),
            E_div_data[i].sel(time=lag),
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
for ax in axes[-1, :]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

# add y-axis labels for the first column

for ax in axes[:, 0]:
    ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/E_vector/E_vector_neg_divergence.png"
)
# %%
# maps for mean between -5 and 5 days
start_lag = -10
end_lag = 5

E_div_first10_pos_mean = E_div_first10_pos.sel(time=slice(start_lag, end_lag)).mean(
    "time"
)
E_div_last10_pos_mean = E_div_last10_pos.sel(time=slice(start_lag, end_lag)).mean(
    "time"
)

E_div_first10_neg_mean = E_div_first10_neg.sel(time=slice(start_lag, end_lag)).mean(
    "time"
)
E_div_last10_neg_mean = E_div_last10_neg.sel(time=slice(start_lag, end_lag)).mean(
    "time"
)
# %%
fig, axes = plt.subplots(
    2, 2, figsize=(10, 5), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)

div_levels = np.arange(-0.6e-4, 0.7e-4, 0.1e-4)

plot_E(
    E_M_first10_pos.mean("time"),
    E_N_first10_pos.mean("time"),
    E_div_first10_pos_mean,
    axes[0, 0],
    div_levels,
)
axes[0, 0].set_title("first10 pos")

plot_E(
    E_M_last10_pos.mean("time"),
    E_N_last10_pos.mean("time"),
    E_div_last10_pos_mean,
    axes[0, 1],
    div_levels,
)
axes[0, 1].set_title("last10 pos")

plot_E(
    E_M_first10_neg.mean("time"),
    E_N_first10_neg.mean("time"),
    E_div_first10_neg_mean,
    axes[1, 0],
    div_levels,
)
axes[1, 0].set_title("first10 neg")

_, lines, arrows = plot_E(
    E_M_last10_neg.mean("time"),
    E_N_last10_neg.mean("time"),
    E_div_last10_neg_mean,
    axes[1, 1],
    div_levels,
)
axes[1, 1].set_title("last10 neg")

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(lines, cax=cbar_ax, orientation="horizontal")

plt.suptitle(f"Mean divergence between {start_lag} and {end_lag} days ")

plt.tight_layout(rect=[0, 0.1, 1, 1])
for ax in axes[-1, :]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

# add y-axis labels for the first column

for ax in axes[:, 0]:
    ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])

plt.tight_layout()
# %%
## profile lag_days v.s longitude plots
E_div_first10_pos_lag_lon = E_div_first10_pos.sel(lat=slice(45, 65)).mean("lat")
E_div_last10_pos_lag_lon = E_div_last10_pos.sel(lat=slice(45, 65)).mean("lat")
# %%
E_div_first10_neg_lag_lon = E_div_first10_neg.sel(lat=slice(45, 65)).mean("lat")
E_div_last10_neg_lag_lon = E_div_last10_neg.sel(lat=slice(45, 65)).mean("lat")
# %%
fig, axes = plt.subplots(
    2, 2, figsize=(10, 5), subplot_kw={"projection": ccrs.PlateCarree(-120)}
)

div_levels = np.arange(-1e-4, 1.1e-4, 0.2e-4)


E_div_first10_pos_lag_lon.plot.contourf(
    ax=axes[0, 0], levels=div_levels, extend="both", transform=ccrs.PlateCarree(),
    add_colorbar=False
)

p = E_div_last10_pos_lag_lon.plot.contourf(
    ax=axes[0, 1], levels=div_levels, extend="both", transform=ccrs.PlateCarree(),
    add_colorbar=False
)

E_div_first10_neg_lag_lon.plot.contourf(
    ax=axes[1, 0], levels=div_levels, extend="both", transform=ccrs.PlateCarree(),
    add_colorbar=False
)

E_div_last10_neg_lag_lon.plot.contourf(
    ax=axes[1, 1], levels=div_levels, extend="both", transform=ccrs.PlateCarree(),
    add_colorbar=False
)


for ax in axes.flat:
    ax.set_aspect("auto")

for ax in axes[-1, :]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

# add y-axis labels for the first column

for ax in axes[:, 0]:
    ax.set_yticks(range(-30,31,10))
    ax.set_yticklabels(np.arange(-30,31,10))

# add colorbar
cbar = plt.colorbar(p, ax=axes, orientation="horizontal", shrink=0.8, aspect=40)

plt.suptitle("Composite divergence between 45°N and 65°N")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/E_vector/E_vector_divergence_45_65.png"
)
# %%
