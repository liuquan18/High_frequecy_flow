#%%
import xarray as xr
import numpy as np


# %%
def read_comp_var(var, phase, decade, time_window=(-5, 5), **kwargs):
    name = kwargs.get("name", var)
    method = kwargs.get("method", "mean")
    suffix = kwargs.get("suffix", "")
    remove_zonmean = kwargs.get("remove_zonmean", False)
    basedir = (
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_range/"
    )
    file_name = basedir + f"{var}{suffix}_NAO_{phase}_{decade}.nc"
    ds = xr.open_dataset(file_name)[name]
    ds = ds.sel(time=slice(*time_window))
    if method == "mean":
        ds = ds.mean(dim=("time", "ens"))
        if remove_zonmean:
            ds = ds - ds.mean(dim="lon", keep_attrs=True)
    elif method == "sum":
        ds = ds.sum(dim=("time", "ens"))
    return ds
