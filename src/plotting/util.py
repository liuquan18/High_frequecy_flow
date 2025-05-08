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

def map_smooth(ds, lon_win=25, lat_win=3):
    extended_ds = xr.concat([ds, ds], dim="lon")
    ds_rolling = extended_ds.rolling(lon=lon_win, lat=lat_win).mean()

    original_lonsize = ds.lon.size
    ds_rolling = ds_rolling.isel(lon=slice(original_lonsize, 2 * original_lonsize))
    return ds_rolling.sortby("lon")


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

def x2lon(x, ax):
    """
    Convert x-coordinates to corresponding longitude.
    """
    lon_coord = ax.projection.transform_point(x, 0, ccrs.PlateCarree())[0]

    return lon_coord

