from cartopy.util import add_cyclic_point
import xarray as xr
import cartopy.crs as ccrs

# function to erase the white line
def erase_white_line(data):
    """
    erase the white line aroung 180 degree.
    """
    data = data.transpose(..., "lon")  # make the lon as the last dim
    dims = data.dims  # all the dims
    res_dims = tuple(dim for dim in dims if dim != "lon")  # dims apart from lon
    res_coords = [data.coords[dim] for dim in res_dims]  # get the coords

    # add one more longitude to the data
    data_value, lons = add_cyclic_point(data, coord=data.lon, axis=-1)

    # make the lons as index
    lon_dim = xr.IndexVariable(
        "lon", lons, attrs={"standard_name": "longitude", "units": "degrees_east"}
    )

    # the new coords with changed lon
    new_coords = res_coords + [lon_dim]  # changed lon but new coords

    new_data = xr.DataArray(data_value, coords=new_coords, name=data.name)

    return new_data

def lat2y(latitude, ax):
    """
    Convert latitude to corresponding y-coordinates.
    """
    y_coord = ax.projection.transform_point(0, latitude, ccrs.PlateCarree())[1]

    return y_coord


def lon2x(longitude, ax):
    """
    Convert longitude to corresponding x-coordinates.
    """
    x_coord = ax.projection.transform_point(longitude, 0, ccrs.PlateCarree())[0]

    return x_coord