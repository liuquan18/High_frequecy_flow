# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import glob
import src.composite.composite as comp
from src.extremes.extreme_read import read_extremes  # NAO extremes
import cartopy.crs as ccrs

# %%
first_var_clim = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/band_variance/first10_var_midlat.nc"
)
last_var_clim = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/band_variance/last_var_midlat.nc"
)
# %%
first_var_clim.load()
last_var_clim.load()

# %%
first_clim_vvar = first_var_clim.va
last_clim_vvar = last_var_clim.va
# %%
first_clim_vvar["plev"] = 25000
last_clim_vvar["plev"] = 25000


# %%
def read_vvar(period, ens, clim):
    # Load data
    vvar_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_bandvar_{period}/"
    vvar_file = glob.glob(f"{vvar_path}*r{ens}i1p1f1*.nc")[0]

    vvar = xr.open_dataset(vvar_file).__xarray_dataarray_variable__
    try:
        vvar["time"] = vvar.indexes["time"].to_datetimeindex()
    except AttributeError:
        pass

    vvar_ratio = vvar / clim
    return vvar_ratio


# %%
def composite(period, clim):

    clim_vvar = []
    NAO_pos_vvar = []
    NAO_neg_vvar = []

    for ens in range(1, 51):
        # read NAO
        NAO_pos, NAO_neg = read_extremes(period, 8, ens, 25000)
        # read vvar
        vvar = read_vvar(period, ens, clim)
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
    NAO_pos_vvar = xr.concat(NAO_pos_vvar, dim="event", coords="minimal")
    NAO_neg_vvar = xr.concat(NAO_neg_vvar, dim="event", coords="minimal")
    clim_vvar = xr.concat(clim_vvar, dim="ens", coords="minimal")

    return NAO_pos_vvar, NAO_neg_vvar, clim_vvar


# %%
first_NAO_pos_vvar, first_NAO_neg_vvar, first_clim_vvar = composite(
    "first10", first_var_clim
)
# %%
last_NAO_pos_vvar, last_NAO_neg_vvar, last_clim_vvar = composite(
    "last10", last_var_clim
)

# %%
first_NAO_neg_vvar = first_NAO_neg_vvar.va
first_NAO_pos_vvar = first_NAO_pos_vvar.va

last_NAO_neg_vvar = last_NAO_neg_vvar.va
last_NAO_pos_vvar = last_NAO_pos_vvar.va
# %%
levels = np.arange(0, 1.1, 0.1)
# climatology maps
fig, axes = plt.subplots(
    1, 2, subplot_kw={"projection": ccrs.PlateCarree(central_longitude=-120)}
)

first_clim_vvar.va.mean(dim=("ens", "time")).plot.contourf(
    x="lon",
    y="lat",
    ax=axes[0],
    levels=levels,
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
)
axes[0].set_title("First 10 years")

map = last_clim_vvar.va.mean(dim=("ens", "time")).plot.contourf(
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
    # Add box for sector lat 30-60, lon all
    ax.add_patch(
        plt.Rectangle(
            xy=[-180, 30],
            width=360,
            height=30,
            edgecolor="red",
            facecolor="none",
            transform=ccrs.PlateCarree(),
        )
    )

# add colorbar
cbar_ax = fig.add_axes([0.15, 0.1, 0.7, 0.05])
fig.colorbar(map, cax=cbar_ax, orientation="horizontal")
plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/band_variance/band_variance_ratio_climatology_maps.png",
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
levels = np.arange(0, 1.1, 0.1)

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
# %%
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
levels = np.arange(0, 0.9, 0.09)
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
# %%
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
levels = np.arange(0, 21, 2)

(first_NAO_pos_vvar.sel(lat=slice(30, 60)).mean(dim="lat") > 1).sum(
    dim="event"
).plot.contourf(x="lon", y="time", ax=axes[0, 0], levels=levels, extend="max")
(last_NAO_pos_vvar.sel(lat=slice(30, 60)).mean(dim="lat") > 1).sum(
    dim="event"
).plot.contourf(x="lon", y="time", ax=axes[0, 1], levels=levels, extend="max")
(first_NAO_neg_vvar.sel(lat=slice(30, 60)).mean(dim="lat") > 1).sum(
    dim="event"
).plot.contourf(x="lon", y="time", ax=axes[1, 0], levels=levels, extend="max")
occurrence = (
    (last_NAO_neg_vvar.sel(lat=slice(30, 60)).mean(dim="lat") > 1)
    .sum(dim="event")
    .plot.contourf(x="lon", y="time", ax=axes[1, 1], levels=levels, extend="max")
)

for ax in axes.flatten():
    ax.set_ylim(0, -20)
    ax.set_xlim(120, 360)


axes[0, 0].set_title("First 10 years, positive NAO")
axes[0, 1].set_title("Last 10 years, positive NAO")

axes[1, 0].set_title("First 10 years, negative NAO")
axes[1, 1].set_title("Last 10 years, negative NAO")

axes[0, 0].set_ylabel("days relative to onset of NAO extremes")
axes[1, 0].set_ylabel("days relative to onset of NAO extremes")


plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/band_variance/band_variance_ratio_composite_maps.png",
    dpi=300,
)
# %%
