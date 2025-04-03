import xarray as xr
import numpy as np
import glob
from src.plotting.util import erase_white_line
import src.moisture.longitudinal_contrast as lc


def read_prime(decade, var="eke", **kwargs):
    """
    read high frequency data
    """

    name = kwargs.get("name", var)  # default name is the same as var
    plev = kwargs.get("plev", None)
    suffix = kwargs.get("suffix", "_ano")

    time_tag = f"{decade}"
    data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily{suffix}/"
    files = glob.glob(data_path + "r*i1p1f1/" + f"*{time_tag}*.nc")
    # sort files
    files.sort(key=lambda x: int(x.split("/")[-2][1:].split("i")[0]))

    data = xr.open_mfdataset(
        files,
        combine="nested",
        concat_dim="ens",
        chunks={"ens": 1, "time": -1, "lat": -1, "lon": -1, "plev": 1},
        parallel=True,
    )
    data = data[name]
    if plev is not None:
        data = data.sel(plev=plev)

    data["ens"] = range(1, 51)

    return data


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


# %%
def vert_integrate(var):
    var = var.sortby(
        "plev", ascending=False
    )  # make sure plev is in descending order, p_B is larger than p_T
    d_var_dp = var.differentiate("plev")
    ivar = d_var_dp.integrate("plev")
    ivar = -1 * ivar / 9.81
    ivar.name = f"i{var.name}"
    return ivar


# %%
def smooth(arr, lat_window=5, lon_window=5):

    arr = lc.rolling_lon_periodic(arr, lon_window, lat_window, stat="median")
    return arr


# %%
def remove_zonalmean(arr):
    arr = arr - arr.mean(dim="lon")
    return arr


# %%
def postprocess(ds, do_smooth=True, remove_zonal=False):
    if do_smooth:
        ds = smooth(ds)
    if remove_zonal:
        ds = remove_zonalmean(ds)
    ds = erase_white_line(ds)
    return ds


def read_composite_MPI(var, name, decade, before="15_5", return_as = 'diff'):
    pos_file = glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_pos_{before}_mean_{decade}.nc"
    )
    neg_file = glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/{var}_NAO_neg_{before}_mean_{decade}.nc"
    )
    if len(pos_file) == 0 or len(neg_file) == 0:
        raise ValueError(f"no file found for {var} in {decade}")
    NAO_pos = xr.open_dataset(pos_file[0])
    NAO_neg = xr.open_dataset(neg_file[0])
    NAO_pos = NAO_pos[name]
    NAO_neg = NAO_neg[name]

    NAO_pos = NAO_pos.mean(dim="event").squeeze()
    NAO_neg = NAO_neg.mean(dim="event").squeeze()

    NAO_pos = postprocess(NAO_pos)
    NAO_neg = postprocess(NAO_neg)

    diff = NAO_pos - NAO_neg

    if return_as == 'pos':
        return NAO_pos.compute()
    elif return_as == 'neg':
        return NAO_neg.compute()
    else:
        return diff.compute()


# %%
def read_composite_ERA5(var, name, before="15_5", return_as = 'diff'):
    pos_file = glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results/ERA5_allplev_{var}_NAO_pos_{before}_mean.nc"
    )
    neg_file = glob.glob(
        f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/0stat_results/ERA5_allplev_{var}_NAO_neg_{before}_mean.nc"
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
    if return_as == 'pos':
        return NAO_pos.compute()
    elif return_as == 'neg':
        return NAO_neg.compute()
    else:
        return diff.compute()


# %%
def read_MPI_GE_uhat():
    uhat_composiste = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/"
    uhat_pos_first10 = xr.open_dataarray(
        f"{uhat_composiste}jetstream_MJJAS_first10_pos.nc"
    )
    uhat_neg_first10 = xr.open_dataarray(
        f"{uhat_composiste}jetstream_MJJAS_first10_neg.nc"
    )

    uhat_pos_last10 = xr.open_dataarray(
        f"{uhat_composiste}jetstream_MJJAS_last10_pos.nc"
    )
    uhat_neg_last10 = xr.open_dataarray(
        f"{uhat_composiste}jetstream_MJJAS_last10_neg.nc"
    )

    uhat_NAO_first = uhat_pos_first10 - uhat_neg_first10
    uhat_NAO_last = uhat_pos_last10 - uhat_neg_last10

    uhat_NAO_first = postprocess(uhat_NAO_first)
    uhat_NAO_last = postprocess(uhat_NAO_last)
    return uhat_NAO_first, uhat_NAO_last
