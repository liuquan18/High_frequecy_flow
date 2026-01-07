# %%
import xarray as xr
import numpy as np
import os
import sys
import glob
import matplotlib.pyplot as plt
import logging
import src.plotting.util as util

logging.basicConfig(level=logging.INFO)


# %%
def fldmean(decade, var="steady_eddy_heat_d2y2"):

    data_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/{var}_daily/"

    std_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/{var}_std_decmean/"

    ds = xr.open_mfdataset(
        glob.glob(os.path.join(data_dir, f"r*i1p1f1/*{decade}.nc")),
        combine="nested",
        concat_dim="ens",
    )
    ds = ds.sel(plev=85000)

    std = xr.open_dataset(glob.glob(os.path.join(std_dir, f"*{decade}*.nc"))[0])
    std = std.mean(dim="time").sel(plev=85000)

    # count how many days the value of ds is above 1 std of the decade
    # Get the variable name from the dataset
    var_name = list(ds.data_vars)[0]
    
    # Broadcast std to match ds dimensions for comparison
    diff = ds[var_name] - std['std']
    
    # Count where values are above std (> 0)
    above_std = (diff > 0)
    
    # Count along time dimension, keeping ens, lat, lon
    above_std_count = above_std.sum(dim=("time", "ens"))

    # 0-360 longitude to -180 to 180 longitude
    above_std_count = util.lon360to180(above_std_count)

    # high latitude for the cwb -120-60 to match the zonal mean calculation
    count_cwb = above_std_count.sel(lat=slice(70, 90), lon=slice(-120, 60)).mean(dim=("lat", "lon"))

    # mid latitude for the awb 30-60 to match the zonal mean calculation
    count_awb = above_std_count.sel(lat=slice(50, 70), lon = slice(-120, 60)).mean(dim=("lat", "lon"))
    
    return count_awb, count_cwb


# %%
decade = sys.argv[1]
decade = int(decade)
logging.info(f"Processing decade {decade}")

awb_mean = fldmean(decade, "anticyclonic")
cwb_mean = fldmean(decade, "cyclonic")

awb_mean = awb_mean.expand_dims(decade=[decade]).set_index(decade="decade")
cwb_mean = cwb_mean.expand_dims(decade=[decade]).set_index(decade="decade")

# %%
awb_mean.to_netcdf(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_anticyclonic_fldmean/awb_fldmean_{decade}.nc"
)
# cwb_mean.to_netcdf(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_cyclonic_fldmean/cwb_fldmean_{decade}.nc")
