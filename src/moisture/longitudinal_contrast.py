#%%
import xarray as xr

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
