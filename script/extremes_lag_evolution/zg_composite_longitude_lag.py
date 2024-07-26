# %%
import xarray as xr
import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt
# %%
import src.composite.zg_mermean_composite as zg_comp

# %%
import importlib

importlib.reload(zg_comp)


# %%
def composite_single_ens(zg, pos_extreme, neg_extreme, base_plev=25000, cross_plev=1):
    pos_date_range = zg_comp.lead_lag_time(
        pos_extreme, base_plev=base_plev, cross_plev=cross_plev
    )

    pos_composite = None
    neg_composite = None

    if not pos_date_range.empty:
        pos_composite = zg_comp.composite_zg_mermean(zg, pos_date_range)

    neg_date_range = zg_comp.lead_lag_time(
        neg_extreme, base_plev=25000, cross_plev=cross_plev
    )

    if not neg_date_range.empty:
        neg_composite = zg_comp.composite_zg_mermean(zg, neg_date_range)

    return pos_composite, neg_composite


# %%
def composite_lag_longitude_allens(period="first10", base_plev=25000, cross_plev=1, stat = "mean"):
    tags = {"first10": "18500501-18590930", "last10": "20910501-21000930"}
    scenario = {"first10": "historical", "last10": "ssp585"}
    scenario_tag = scenario[period]
    tag = tags[period]
    zg_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily_global/zg_mermean_{period}/"
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
        pos_zg = pos_zg.mean(dim="event")
        neg_zg = neg_zg.mean(dim="event")
    elif stat == "sum":
        pos_zg_composite = pos_zg.sum(dim="event")
        neg_zg_composite = neg_zg.sum(dim="event")

    return pos_zg_composite, neg_zg_composite


# %%
pos_zg_composite_first10, neg_zg_composite_first10 = composite_lag_longitude_allens(
    period="first10",cross_plev=1, base_plev=50000, stat='mean'
)

#%%
pos_zg_composite_last10, neg_zg_composite_last10 = composite_lag_longitude_allens(
    period="last10",cross_plev=1, base_plev=50000, stat='mean'
)

#%%
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# levels = np.arange(-5000, 5500, 500
levels = np.arange(-100, 110, 10)
plev = 50000
pos_zg_composite_first10.sel(plev=plev, lat=0).plot.contourf(
    levels = levels, extend="both", ax = axes[0,0]
)

neg_zg_composite_first10.sel(plev=plev, lat=0).plot.contourf(
   levels = levels,extend="both", ax = axes[0,1]
)

pos_zg_composite_last10.sel(plev=plev, lat=0).plot.contourf(
    levels = levels,extend="both", ax = axes[1,0]
)

neg_zg_composite_last10.sel(plev=plev, lat=0).plot.contourf(
    levels = levels,extend="both", ax = axes[1,1]
)
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/composite/zg_composite_lag_longitude_250hPa_mean.png")
# %%
