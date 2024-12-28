#%%
import xarray as xr
import glob
import logging
logging.basicConfig(level=logging.INFO)
# %%
def rolling_lon_periodic(arr, lon_window, lat_window, stat = 'std'):
    extended_arr = xr.concat([arr, arr], dim='lon')
    if stat == 'mean':
        rolled_result = extended_arr.rolling(lon=lon_window, lat=lat_window, center=True).mean()
    elif stat == 'std':
        rolled_result = extended_arr.rolling(lon=lon_window, lat=lat_window, center=True).std()
    elif stat == 'var':
        rolled_result = extended_arr.rolling(lon=lon_window, lat=lat_window, center=True).var()
    else:
        raise ValueError(f"Unsupported stat: {stat}")
    original_size = arr.sizes['lon']
    final_result = rolled_result.isel({'lon': slice(original_size-lon_window//2, 2*original_size-lon_window//2)})
    return final_result.sortby('lon')
#%%
def read_data(var, decade, latitude_slice = (-30,30), meridional_mean = False, suffix = '_std'):
    time_tag = f"{decade}0501-{decade+9}0930"
    data_path = (
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily{suffix}/"
    )
    files = glob.glob(data_path + "r*i1p1f1/" + f"{var}*{time_tag}.nc")

    data = xr.open_mfdataset(
        files, combine="nested", concat_dim="ens", chunks={"ens": 1}
    )
    try:
        data = data[var]
    except KeyError:
        pass
        logging.warning(f"Variable {var} not found in the dataset")

    # select -30 to 30 lat
    if latitude_slice is not None:
        data = data.sel(lat=slice(*latitude_slice))
        
    if meridional_mean:
        data = data.mean("lat")
    
    # change longitude from 0-360 to -180-180
    data = data.assign_coords(lon=(data.lon + 180) % 360 - 180).sortby("lon")

    return data

# %%