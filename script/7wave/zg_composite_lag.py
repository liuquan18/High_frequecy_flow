# %%
import xarray as xr
import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# %%
import src.composite.composite as zg_comp

# %%
import importlib

importlib.reload(zg_comp)


# %%
def composite_single_ens(zg, pos_extreme, neg_extreme, base_plev=25000, cross_plev=1):
    pos_date_range = zg_comp.lead_lag_30days(
        pos_extreme, base_plev=base_plev, cross_plev=cross_plev
    )

    pos_composite = None
    neg_composite = None

    if not pos_date_range.empty:
        pos_composite = zg_comp.event_composite(zg, pos_date_range)

    neg_date_range = zg_comp.lead_lag_30days(
        neg_extreme, base_plev=25000, cross_plev=cross_plev
    )

    if not neg_date_range.empty:
        neg_composite = zg_comp.event_composite(zg, neg_date_range)

    return pos_composite, neg_composite


# %%
def composite_lag_longitude_allens(
    period="first10", base_plev=25000, cross_plev=1, stat="mean", zg="zg_mermean"
):
    """
    parameters:
        period: str
        zg: str # zg_mermean or zg_MJJAS_ano

    """
    tags = {"first10": "18500501-18590930", "last10": "20910501-21000930"}
    scenario = {"first10": "historical", "last10": "ssp585"}
    scenario_tag = scenario[period]
    tag = tags[period]
    zg_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily_global/{zg}_{period}/"
    pos_zg = []
    neg_zg = []
    for i in range(1, 51):
        zg = xr.open_dataset(
            f"{zg_path}zg_day_MPI-ESM1-2-LR_{scenario_tag}_r{str(i)}i1p1f1_gn_{tag}_ano.nc"
        )
        zg = zg.zg
        pos_extreme, neg_extreme = zg_comp.read_extremes(period, 8, i)
        pos_composite, neg_composite = composite_single_ens(
            zg, pos_extreme, neg_extreme, base_plev=base_plev, cross_plev=cross_plev
        )

        pos_zg.append(pos_composite)
        neg_zg.append(neg_composite)

    logging.info("all ensembles are processed")
    # drop empty elements from list pos_zg
    pos_zg = [x for x in pos_zg if x is not None]
    neg_zg = [x for x in neg_zg if x is not None]

    # concatenate the list of xarray datasets into a single xarray dataset
    pos_zg = xr.concat(pos_zg, dim="event")
    neg_zg = xr.concat(neg_zg, dim="event")

    if stat == "mean":
        pos_zg_composite = pos_zg.mean(dim="event")
        neg_zg_composite = neg_zg.mean(dim="event")
    elif stat == "sum":
        pos_zg_composite = pos_zg.sum(dim="event")
        neg_zg_composite = neg_zg.sum(dim="event")

    return pos_zg_composite, neg_zg_composite


# %%
def remove_zonalmean(zg):
    """
    remove zonal mean from the data
    """
    zg = zg - zg.mean(dim="lon")
    return zg


# %%
################### for zg maps ############################

pos_zg_composite_first10, neg_zg_composite_first10 = composite_lag_longitude_allens(
    period="first10", cross_plev=1, base_plev=25000, stat="mean", zg="zg_MJJAS_ano"
)

# %%
pos_zg_composite_last10, neg_zg_composite_last10 = composite_lag_longitude_allens(
    period="last10", cross_plev=1, base_plev=25000, stat="mean", zg="zg_MJJAS_ano"
)


# %%
def plot_zg_composite(zg_composite, ax, plev=50000, levels=np.arange(-10, 11, 1)):
    levels = levels[levels != 0]
    p = (
        remove_zonalmean(zg_composite)
        .sel(plev=plev, lat=slice(-10, None))
        .plot.contour(
            levels=levels,
            extend="both",
            ax=ax,
            add_colorbar=False,
            colors="k",
            transform=ccrs.PlateCarree(),
        )
    )

    # Add coastlines
    p.axes.coastlines(alpha=0.5)
    return p


# %%
fig, axes = plt.subplots(
    6, 2, figsize=(15, 15), subplot_kw={"projection": ccrs.PlateCarree(180)}
)

levels = np.arange(-40, 41, 5)
plev = 50000

extreme_type = "pos"
start_lag = -24
step_lag = 5

length = 6
end_lag = start_lag + length * step_lag

lag_days = np.arange(start_lag, stop=end_lag, step=step_lag)
periods = ["first10", "last10"]
data = [pos_zg_composite_first10, pos_zg_composite_last10]


for i, period in enumerate(periods):
    for j, lag in enumerate(lag_days):
        plot_zg_composite(data[i].sel(time=lag), axes[j, i], plev=plev, levels=levels)
        axes[j, i].set_title(f"{period} {extreme_type} lag {lag}")

# add x-axis labels for the last row
for ax in axes[-1, :]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

# add y-axis labels for the first column
for ax in axes[:, 0]:
    ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])
plt.suptitle("zg500 composite mean lag of positive NAO extremes (contour interval 5)")
plt.tight_layout()
# plt.savefig(
#     "/work/mh0033/m300883/High_frequecy_flow/docs/plots/zg_composite/zg500_composite_mean_lag_pos_subzonal.png"
# )
# %%
# negative
fig, axes = plt.subplots(
    6, 2, figsize=(15, 15), subplot_kw={"projection": ccrs.PlateCarree(180)}
)

levels = np.arange(-40, 41, 5)
start_lag = -27
step_lag = 5

length = 6
end_lag = start_lag + length * step_lag
lag_days = np.arange(start_lag, stop=end_lag, step=step_lag)

periods = ["first10", "last10"]
extreme_type = "neg"
data = [neg_zg_composite_first10, neg_zg_composite_last10]

for i, period in enumerate(periods):
    for j, lag in enumerate(lag_days):
        plot_zg_composite(data[i].sel(time=lag), axes[j, i], plev=plev, levels=levels)
        axes[j, i].set_title(f"{period} {extreme_type} lag {lag}")

# add x-axis labels for the last row
for ax in axes[-1, :]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

# add y-axis labels for the first column
for ax in axes[:, 0]:
    ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])
plt.suptitle("zg500 composite mean lag of negative NAO extremes (contour interval 5)")
plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/zg_composite/zg500_composite_mean_lag_neg_subzonal.png"
)
# %%
