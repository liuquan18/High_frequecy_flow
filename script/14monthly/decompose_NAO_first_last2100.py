#%%
import xarray as xr
import src.Teleconnection.spatial_pattern as ssp
import glob
import numpy as np
import pandas as pd
# %%

def read_data(
    zg_path,
    plev=None,
    remove_ens_mean=True,
    var_name = "zg",
):
    """
    read data quickly
    """
    gph_dir = zg_path
    # read MPI_onepct data
    # fix the order of ensemble members
    print("reading the gph data of all ensemble members...")
    all_ens_lists = sorted(
        glob.glob(gph_dir + "*.nc")
    )  # to make sure that the order of ensemble members is fixed
    zg_data = xr.open_mfdataset(
        all_ens_lists, combine="nested", concat_dim="ens", join="override",
    )  # consider chunks={}, # kz the file size is small (< 3G). 

    zg_data["ens"] = np.arange(zg_data.ens.size)+1
    try:
        zg_data = zg_data.var156
    except AttributeError:
        try:
            zg_data = zg_data.zg
    
        except AttributeError:
            zg_data = zg_data[var_name]

    # time to datetime
    try:
        zg_data["time"] = zg_data.indexes["time"].to_datetimeindex()
    except AttributeError:
        zg_data["time"] = pd.to_datetime(zg_data.time)

    # demean
    if remove_ens_mean:
        print(" demean the ensemble mean...")
        zg_ens_mean = zg_data.mean(dim="ens")
        zg_demean = zg_data - zg_ens_mean
    else:
        zg_demean = zg_data

    # select one altitude
    try:
        if plev is not None:
            print(" select the specific plev...")
            zg_plev = zg_demean.sel(plev=plev)
        else:
            # select the 1000hPa - 200hPa
            print(" select the 1000hPa - 200hPa...")
            zg_plev = zg_demean.sel(plev=slice(100000, 20000))
            if zg_plev.plev.size == 0:
                zg_plev = zg_demean.sel(plev=slice(20000, 100000))
    except KeyError:
        zg_plev = zg_demean # for the data only with one plev
    return zg_plev

#%%
def decompose_single_decade(xarr, timeslice, nmode=2):
    """decompose a single decade."""
    field = xarr.sortby("time") # sort the time
    field = field.sel(time=timeslice)
    field = field.stack(com=("ens", "time"))

    eof_result = ssp.doeof(field, nmode=nmode, dim="com")

    return eof_result


# %%
data_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/"
# %%
# read gph data
data_JJA = []
for month in ["Jun", "Jul", "Aug"]:
    print(f"reading the gph data of {month} ...")
    zg_path = data_dir + "zg_" + month + "/"
    data_JJA.append(read_data(zg_path, plev=25000))
data = xr.concat(data_JJA, dim="time").sortby("time")

# %%
# rechunk
data = data.chunk({ "ens":-1, "time": -1, "lat": -1, "lon": -1})
# %%
first_eof = decompose_single_decade(data, slice("1850-06-01", "1859-08-31"), nmode=2)

# %%
last_eof = decompose_single_decade(data, slice("2091-06-01", "2100-08-31"), nmode=2)
# %%
# save 
first_eof.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result_first_last2091-2100/first_eofs.nc")
last_eof.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result_first_last2091-2100/last_eofs.nc")
# %%
