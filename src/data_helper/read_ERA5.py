import xarray as xr
import numpy as np
import glob
from src.plotting.util import erase_white_line
import src.dynamics.longitudinal_contrast as lc
import logging


# %%
def smooth(arr, lat_window=5, lon_window=5):

    arr = lc.rolling_lon_periodic(arr, lon_window, lat_window, stat="median")
    return arr


# %%
def remove_zonalmean(arr):
    arr = arr - arr.mean(dim="lon")
    return arr


# %%
def postprocess(ds, smooth_value=5, remove_zonal=False):
    if smooth_value is not None:
        ds = smooth(ds, lat_window=smooth_value, lon_window=smooth_value)
    if remove_zonal:
        ds = remove_zonalmean(ds)
    ds = erase_white_line(ds)
    return ds

#####################################################################
def read_prime_ERA5(var="eke", model="ERA5_allplev", **kwargs):

    name = kwargs.get("name", var)  # default name is the same as var
    plev = kwargs.get("plev", None)
    suffix = kwargs.get("suffix", "_ano")

    data_path = (
        f"/work/mh0033/m300883/High_frequecy_flow/data/{model}/{var}_daily{suffix}/"
    )

    files = glob.glob(data_path + "*.nc")

    files.sort()

    data = xr.open_mfdataset(
        files,
        combine="by_coords",
        chunks={"time": 10, "lat": -1, "lon": -1, "plev": 1},
        parallel=True,
    )
    data = data[name]
    if plev is not None:
        data = data.sel(plev=plev)

    return data


def read_composite_ERA5(var, name, before="15_5", return_as="diff"):
    pos_file = glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results_without_ano/ERA5_allplev_{var}_NAO_pos_{before}_mean.nc"
    )
    neg_file = glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results_without_ano/ERA5_allplev_{var}_NAO_neg_{before}_mean.nc"
    )
    if len(pos_file) == 0 or len(neg_file) == 0:
        raise ValueError(f"no file found for {var}")
    NAO_pos = xr.open_dataset(pos_file[0])
    NAO_neg = xr.open_dataset(neg_file[0])
    NAO_pos = NAO_pos[name]
    NAO_neg = NAO_neg[name]

    try:
        NAO_pos = NAO_pos.mean(dim="event").squeeze()
        NAO_neg = NAO_neg.mean(dim="event").squeeze()
    except ValueError:
        NAO_pos = NAO_pos.squeeze()
        NAO_neg = NAO_neg.squeeze()

    NAO_pos = postprocess(NAO_pos)
    NAO_neg = postprocess(NAO_neg)

    diff = NAO_pos - NAO_neg
    if return_as == "pos":
        return NAO_pos.compute()
    elif return_as == "neg":
        return NAO_neg.compute()
    else:
        return diff.compute()
