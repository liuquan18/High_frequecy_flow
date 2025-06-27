# %%
import xarray as xr
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import seaborn as sns
import pandas as pd
import glob

# %%
import src.composite.composite as comp
from src.extremes.extreme_read import read_extremes  # NAO extremes


# %%
def read_vvar(period, ens):
    # Load data
    vvar_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_bandvar_{period}/"
    vvar_file = glob.glob(f"{vvar_path}*r{ens}i1p1f1*.nc")[0]

    vvar = xr.open_dataset(vvar_file).__xarray_dataarray_variable__
    try:
        vvar["time"] = vvar.indexes["time"].to_datetimeindex()
    except AttributeError:
        pass

    return vvar


# %%
def composite(period):

    clim_vvar = []
    NAO_pos_vvar = []
    NAO_neg_vvar = []

    for ens in range(1, 51):
        # read NAO
        NAO_pos, NAO_neg = read_extremes(period, 8, ens, 25000)
        # read vvar
        vvar = read_vvar(period, ens)
        clim_vvar.append(vvar)

        if not NAO_pos.empty:
            pos_range = comp.find_lead_lag_30days(NAO_pos, base_plev=25000)
            vvar_pos = comp.date_range_composite(vvar, pos_range)
            NAO_pos_vvar.append(vvar_pos)

        if not NAO_neg.empty:
            neg_range = comp.find_lead_lag_30days(NAO_neg, base_plev=25000)
            vvar_neg = comp.date_range_composite(vvar, neg_range)
            NAO_neg_vvar.append(vvar_neg)

    # concatenate
    NAO_pos_vvar = xr.concat(NAO_pos_vvar, dim="event")
    NAO_neg_vvar = xr.concat(NAO_neg_vvar, dim="event")
    clim_vvar = xr.concat(clim_vvar, dim="ens")

    return NAO_pos_vvar, NAO_neg_vvar, clim_vvar


# %%
first_NAO_pos_vvar, first_NAO_neg_vvar, first_clim_vvar = composite("first10")
# %%
last_NAO_pos_vvar, last_NAO_neg_vvar, last_clim_vvar = composite("last10")
# %%
levels = np.arange(100, 146, 5)

# %%
# climatology maps
fig, axes = plt.subplots(
    1, 2, subplot_kw={"projection": ccrs.PlateCarree(central_longitude=-120)}
)

first_clim_vvar.mean(dim=("ens", "time")).plot.contourf(
    x="lon",
    y="lat",
    ax=axes[0],
    levels=levels,
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
)
axes[0].set_title("First 10 years")

map = last_clim_vvar.mean(dim=("ens", "time")).plot.contourf(
    x="lon",
    y="lat",
    ax=axes[1],
    levels=levels,
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
)
axes[1].set_title("Last 10 years")

for ax in axes.flat:
    ax.coastlines(color="w")


axes[0].add_patch(
    plt.Rectangle(
        xy=[180, 40],
        width=180,
        height=10,
        edgecolor="red",
        facecolor="none",
        transform=ccrs.PlateCarree(),
    )
)

# add a red point at lat 35, lon 180
axes[0].plot(180, 45, "ro", transform=ccrs.PlateCarree())

# add colorbar
cbar_ax = fig.add_axes([0.15, 0.1, 0.7, 0.05])
fig.colorbar(map, cax=cbar_ax, orientation="horizontal")

plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/band_variance/band_variance_climatology.png",
    dpi=300,
)
# %%
# maps
fig, axes = plt.subplots(
    2,
    2,
    figsize=(8, 5),
    subplot_kw={"projection": ccrs.PlateCarree(central_longitude=-120)},
)
levels = np.arange(100, 146, 5)

first_NAO_pos_vvar.mean(dim="event").sel(time=slice(-10, 5)).mean(
    dim="time"
).plot.contourf(
    x="lon",
    y="lat",
    ax=axes[0, 0],
    levels=levels,
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
)

last_NAO_pos_vvar.mean(dim="event").sel(time=slice(-10, 5)).mean(
    dim="time"
).plot.contourf(
    x="lon",
    y="lat",
    ax=axes[0, 1],
    levels=levels,
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
)

first_NAO_neg_vvar.mean(dim="event").sel(time=slice(-10, 5)).mean(
    dim="time"
).plot.contourf(
    x="lon",
    y="lat",
    ax=axes[1, 0],
    levels=levels,
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
)

last_NAO_neg_vvar.mean(dim="event").sel(time=slice(-10, 5)).mean(
    dim="time"
).plot.contourf(
    x="lon",
    y="lat",
    ax=axes[1, 1],
    levels=levels,
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
)
axes[0, 0].set_title("First 10 years, positive NAO")
axes[0, 1].set_title("Last 10 years, positive NAO")

axes[1, 0].set_title("First 10 years, negative NAO")
axes[1, 1].set_title("Last 10 years, negative NAO")
for ax in axes.flat:
    ax.coastlines(color="w")

plt.tight_layout()

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/band_variance/band_variance_composite_maps.png",
    dpi=300,
)
# %%
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
levels = np.arange(100, 146, 5)

first_NAO_pos_vvar.sel(lat=slice(30, 60)).mean(dim=("event", "lat")).plot.contourf(
    x="lon", y="time", ax=axes[0, 0], levels=levels
)
last_NAO_pos_vvar.sel(lat=slice(30, 60)).mean(dim=("event", "lat")).plot.contourf(
    x="lon", y="time", ax=axes[0, 1], levels=levels
)

first_NAO_neg_vvar.sel(lat=slice(30, 60)).mean(dim=("event", "lat")).plot.contourf(
    x="lon", y="time", ax=axes[1, 0], levels=levels
)
last_NAO_neg_vvar.sel(lat=slice(30, 60)).mean(dim=("event", "lat")).plot.contourf(
    x="lon", y="time", ax=axes[1, 1], levels=levels
)

for ax in axes.flatten():
    ax.set_ylim(10, -10)
    ax.set_xlim(120, 360)

plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/band_variance/band_variance_composite_profile.png",
    dpi=300,
)
# %%


# %%
