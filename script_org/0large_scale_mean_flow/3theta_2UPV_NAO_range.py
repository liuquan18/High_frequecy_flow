#%%
import xarray as xr
import numpy as np
from src.data_helper.before_extreme import read_NAO_extremes
from src.composite.composite import range_NAO_composite
from src.data_helper.prime_data import read_prime

import logging
logging.basicConfig(level=logging.INFO)
# %%
def read_all_data(decade, **kwargs):
    
    logging.info("reading NAO extremes")

    NAO_pos = read_NAO_extremes(decade, "positive")
    NAO_neg = read_NAO_extremes(decade, "negative")

    logging.info("reading ua, va, and theta data")

    ua_data = read_prime(
        decade, var = "ua", name = 'ua', suffix = ""
    )

    va_data = read_prime(
        decade, var = "va", name = 'va', suffix = ""
    )
    theta_data = read_prime(
        decade, var = "theta", name = 'theta', suffix = ""
    )
    return NAO_pos, NAO_neg, ua_data, va_data, theta_data

#%%
def composite_single_ens(zg, pos_extreme, neg_extreme, base_plev=25000, cross_plev=1):
    pos_date_range = zg_comp.find_lead_lag_30days(
        pos_extreme, base_plev=base_plev, cross_plev=cross_plev
    )

    pos_composite = None
    neg_composite = None

    if not pos_date_range.empty:
        pos_composite = zg_comp.date_range_composite(zg, pos_date_range)

    neg_date_range = zg_comp.find_lead_lag_30days(
        neg_extreme, base_plev=25000, cross_plev=cross_plev
    )

    if not neg_date_range.empty:
        neg_composite = zg_comp.date_range_composite(zg, neg_date_range)

    return pos_composite, neg_composite

# %%
def process_data(decade, **kwargs):
    # read data
    NAO_pos, NAO_neg, ua_data, va_data, theta_data = read_all_data(decade, **kwargs)


