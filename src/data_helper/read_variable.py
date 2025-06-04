import xarray as xr
import numpy as np
import glob
from src.plotting.util import erase_white_line
import src.dynamics.longitudinal_contrast as lc
import logging



def read_prime(decade, var="eke", **kwargs):
    """
    read high frequency data
    """

    name = kwargs.get("name", var)  # default name is the same as var
    plev = kwargs.get("plev", None)
    suffix = kwargs.get("suffix", "_ano")
    model_dir = kwargs.get("model_dir", "MPI_GE_CMIP6")

    time_tag = f"{decade}"
    data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/{model_dir}/{var}_daily{suffix}/"
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
    data.load()
    if plev is not None:
        data = data.sel(plev=plev)

    data["ens"] = range(1, 51)

    return data

def read_prime_decmean(var="eke", NAL = True, plev = 85000, **kwargs):
    """
    read high frequency data for all decades
    """


    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/{var}_ano_decmean/"
    files = glob.glob(base_dir + "*.nc")
    if len(files) == 0:
        raise ValueError(f"no file found for {var} in decmean")
    data = xr.open_mfdataset(
        files,
        combine="by_coords",
    )
    data.load()
    # yearly mean
    data = data.groupby("time.year").mean(dim="time")
    if NAL:
        data = data.sel(lon = slice(300, 350), lat = slice(40, 80)).mean(dim=['lon', 'lat'])
    if plev is not None:
        data = data.sel(plev=plev)
    return data

def read_prime_single_ens(dec, ens, var, **kwargs):
    name = kwargs.get("name", var)  # default name is the same as var
    plev = kwargs.get("plev", None)
    suffix = kwargs.get("suffix", "_ano")
    model_dir = kwargs.get("model_dir", "MPI_GE_CMIP6")
    data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/{model_dir}/{var}_daily{suffix}/"
    files = glob.glob(data_path + f"r{ens}i1p1f1/*{dec}*")
    if len(files) == 0:
        raise ValueError(f"no file found for {var} in {ens}")
    data = xr.open_dataset(files[0])
    data = data[name]
    if plev is not None:
        data = data.sel(plev=plev)
    data = data.squeeze()

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
def vert_integrate(var, p_B = 100000, p_T = 25000):
    var = var.sortby(
        "plev", ascending=False
    )  # make sure plev is in descending order, p_B is larger than p_T
    var = var.sel(plev=slice(p_B, p_T))
    ivar = var.integrate("plev")
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
def postprocess(ds, smooth_value=5, remove_zonal=False):
    if smooth_value is not None:
        ds = smooth(ds, lat_window=smooth_value, lon_window=smooth_value)
    if remove_zonal:
        ds = remove_zonalmean(ds)
    ds = erase_white_line(ds)
    return ds


def read_composite_MPI(var, name, decade, before="15_5", return_as = 'diff', ano = False, smooth_value = 5, remove_zonal = False, **kwargs):
    model_dir = kwargs.get("model_dir", "MPI_GE_CMIP6")

    if ano:
        pos_file = glob.glob(
            f"/work/mh0033/m300883/High_frequecy_flow/data/{model_dir}/0stat_results/{var}_NAO_pos_{before}_mean_{decade}.nc"
        )
        neg_file = glob.glob(
            f"/work/mh0033/m300883/High_frequecy_flow/data/{model_dir}/0stat_results/{var}_NAO_neg_{before}_mean_{decade}.nc"
        )
    else:
        pos_file = glob.glob(
            f"/work/mh0033/m300883/High_frequecy_flow/data/{model_dir}/0stat_results_without_ano/{var}_NAO_pos_{before}_mean_{decade}.nc"
        )
        neg_file = glob.glob(
            f"/work/mh0033/m300883/High_frequecy_flow/data/{model_dir}/0stat_results_without_ano/{var}_NAO_neg_{before}_mean_{decade}.nc"
        )

    if len(pos_file) == 0 or len(neg_file) == 0:
        raise ValueError(f"no file found for {var} in {decade}")
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
        
    NAO_pos = postprocess(NAO_pos, smooth_value=smooth_value, remove_zonal=remove_zonal)
    NAO_neg = postprocess(NAO_neg, smooth_value=smooth_value, remove_zonal=remove_zonal)

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
    if return_as == 'pos':
        return NAO_pos.compute()
    elif return_as == 'neg':
        return NAO_neg.compute()
    else:
        return diff.compute()




def read_climatology(var, decade, **kwargs):

    name = kwargs.get("name", var)  # default name is the same as var
    if var == "uhat":
        data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/*{decade}*.nc"
    else:
        data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_monthly_ensmean/{var}_monmean_ensmean_{decade}*.nc"

    file = glob.glob(data_path)
    if len(file) == 0:
        raise ValueError(f"no file found for {var} in {decade}")
    data = xr.open_dataset(file[0])
    data = data[name]

    if "time" in data.dims:
        data = data.mean(dim="time")

    return data
