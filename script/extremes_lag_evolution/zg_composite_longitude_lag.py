# %%
import xarray as xr
import pandas as pd
import numpy as np
import logging

# %%
import src.composite.zg_mermean_composite as zg_comp

# %%
import importlib

importlib.reload(zg_comp)


# %%
def select_zg_mermean(zg, pos_extreme, neg_extreme, base_plev=25000, cross_plev=1):
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
def composite_lag_longitude(period="first10", base_plev=25000, cross_plev=1):
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
        pos_composite, neg_composite = select_zg_mermean(
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

    pos_zg_composite = pos_zg.mean(dim="event")
    neg_zg_composite = neg_zg.mean(dim="event")

    return pos_zg_composite, neg_zg_composite


# %%
pos_zg_composite_first10, neg_zg_composite_first10 = composite_lag_longitude(
    period="first10"
)

#%%
pos_zg_composite_last10, neg_zg_composite_last10 = composite_lag_longitude(
    period="last10"
)

# %%
pos_zg_composite.sel(plev=25000, lat=0).plot.contourf(
    levels=np.arange(-100, 101, 20), extend="both"
)
# %%
neg_zg_composite.sel(plev=25000, lat=0).plot.contourf(
    levels=np.arange(-100, 101, 20), extend="both"
)
# %%
pos_composite, neg_composite = select_zg_mermean(
    zg, pos_extreme, neg_extreme, base_plev=base_plev, cross_plev=cross_plev
)
