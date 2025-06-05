#%%
import xarray as xr
import numpy as np
from src.plotting.util import erase_white_line
import pandas as pd
# %%
def read_comp_var(var, phase, decade, time_window=(-5, 5), **kwargs):
    name = kwargs.get("name", var)
    method = kwargs.get("method", "mean")
    suffix = kwargs.get("suffix", "")
    remove_zonmean = kwargs.get("remove_zonmean", False)
    erase_empty = kwargs.get("erase_zero_line", True)
    comp_path = kwargs.get("comp_path", "0composite_range")
    model_dir = kwargs.get("model_dir", "MPI_GE_CMIP6")
    
    basedir = (
        f"/work/mh0033/m300883/High_frequecy_flow/data/{model_dir}/{comp_path}/"
    )
    file_name = basedir + f"{var}{suffix}_NAO_{phase}_{decade}.nc"
    ds = xr.open_dataset(file_name)[name]
    ds = ds.sel(time=slice(*time_window))
    if erase_empty:
        ds = erase_white_line(ds)
    if method == "mean":
        ds = ds.mean(dim=("time", "ens"))
        if remove_zonmean:
            ds = ds - ds.mean(dim="lon", keep_attrs=True)
    elif method == "sum":
        ds = ds.sum(dim=("time", "ens"))
    elif method == "no_stat":
        pass
    return ds


#%%
def read_comp_var_dist(var, phase, decade, suffix = "_ano", **kwargs):
    name = kwargs.get("name", var)
    time_window = kwargs.get("time_window", (-5, 5))
    dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0composite_distribution/{var}{suffix}_NAO_{phase}_{decade}.nc"
    ds = xr.open_dataset(dir)
    ds = ds[name]
    ds = ds.sel(time=slice(*time_window))

    return ds

def read_EP_flux(
    phase, decade, eddy="transient", ano=False, isentrope=False, region="western"
):
    EP_flux_dir = (
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0EP_flux/"
    )

    F_phi = xr.open_dataarray(f"{EP_flux_dir}{eddy}_F_phi_{phase}_{decade}_ano{ano}.nc")
    F_p = xr.open_dataarray(f"{EP_flux_dir}{eddy}_F_p_{phase}_{decade}_ano{ano}.nc")

    div_phi = xr.open_dataarray(f"{EP_flux_dir}{eddy}_div_phi_{phase}_{decade}_ano{ano}.nc")
    div_p = xr.open_dataarray(f"{EP_flux_dir}{eddy}_div_p_{phase}_{decade}_ano{ano}.nc")


    if region == "western":
        F_phi = xr.concat(
            [F_phi.sel(lon = slice(240, None)),
            F_phi.sel(lon = slice(0, 60))], dim = "lon"
        )
        F_p = xr.concat(
            [F_p.sel(lon = slice(240, None)),
            F_p.sel(lon = slice(0, 60))], dim = "lon"
        )

        div_phi = xr.concat(
            [div_phi.sel(lon = slice(240, None)),
            div_phi.sel(lon = slice(0, 60))], dim = "lon"
        )
        div_p = xr.concat(
            [div_p.sel(lon = slice(240, None)),
            div_p.sel(lon = slice(0, 60))], dim = "lon"
        )

    elif region is None:
        # do nothing, return the data as is
        pass


    return F_phi, F_p, div_phi, div_p
