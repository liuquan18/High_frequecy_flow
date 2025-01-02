# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from src.moisture.longitudinal_contrast import read_data
from sklearn.linear_model import LinearRegression

# %%
first_tas = read_data("tas", 1850, (-90, 90), meridional_mean=False, chunks = {'time': -1})
first_hus = read_data("hus", 1850, (-90, 90), meridional_mean=False, chunks = {'time': -1})
first_data = xr.Dataset({"tas": first_tas, "hus": first_hus * 1000})

# %%

last_tas = read_data("tas", 2090, (-90, 90), meridional_mean=False, chunks = {'time': -1})
last_hus = read_data("hus", 2090, (-90, 90), meridional_mean=False, chunks = {'time': -1})
last_data = xr.Dataset({"tas": last_tas, "hus": last_hus * 1000})

#%%
def regression(x, y):
    """
    Perform linear regression on reshaped arrays
    
    Parameters:
    x, y: 1D arrays of equal length
    
    Returns:
    float: regression slope
    """
    # only select the x within percentile [10,100]
    x_p10 = np.percentile(x, 10)
    X = x[x >= x_p10]
    y = y[x >= x_p10]

    # Ensure input arrays are properly shaped for sklearn
    X = np.array(X).reshape(-1, 1)
    Y = np.array(y).reshape(-1, 1)
    
    # Perform regression
    reg = LinearRegression().fit(X, Y)
    
    # Return slope as a scalar (not array)
    return float(reg.coef_[0][0])

def calculate_spatial_regression(data):
    """
    Calculate regression slopes across all spatial points
    
    Parameters:
    first_data: xarray Dataset with dimensions time, ens, lat, lon
    
    Returns:
    xarray DataArray with regression slopes
    """
    # Chunk the data appropriately
    # data = data.chunk({'time': -1, 'ens': -1, 'lat': 10, 'lon': 50})
    
    # Stack time and ensemble dimensions
    data = data.stack(combine=('time', 'ens'))
    
    # Fill NaN values
    data = data.fillna(0)
    
    # Perform regression using apply_ufunc
    slope = xr.apply_ufunc(
        regression,
        data['tas'],
        data['hus'],
        input_core_dims=[['combine'], ['combine']],
        output_core_dims=[[]],  # Empty because regression returns a scalar
        vectorize=True,
        dask='allowed',
        output_dtypes=[float],
        exclude_dims=set(('combine',)),
    )
    
    return slope

#%%
first_data.load()

#%%
first_slope = calculate_spatial_regression(first_data)
first_slope.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/first_hus_tas_slope.nc")
# %%
last_data.load()
last_slope = calculate_spatial_regression(last_data)
last_slope.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/last_hus_tas_slope.nc")
# %%

