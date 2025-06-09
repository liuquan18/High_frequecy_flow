from cartopy.util import add_cyclic_point
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.path as mpath
import matplotlib.ticker as mticker
import numpy as np

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


def clip_map(ax, theta1 = 200, theta2 = 340, lat_min = 20, lat_max = 80):
    # ---- Create a sector-shaped boundary with a hole at the north pole ----
    # Outer sector (main wedge)
      # degrees
    n_points = 100

    # Outer arc (radius=0.5, full sector)
    theta = np.deg2rad(np.linspace(theta1, theta2, n_points))
    outer_arc = np.column_stack([0.5 + 0.5 * np.cos(theta), 0.5 + 0.5 * np.sin(theta)])

    # Inner arc (radius corresponding to 85N, creates the "hole")
    # For a polar stereographic, the pole is at (0.5, 0.5), radius=0.5 is 90N, so 85N is slightly less.
    # Approximate: r = 0.5 * (90 - lat) / (90 - 20) for 20N-90N
    r_80 = 0.5 * (90 - lat_max) / (90 - lat_min)  # scale to axes
    inner_arc = np.column_stack([0.5 + r_80 * np.cos(theta[::-1]), 0.5 + r_80 * np.sin(theta[::-1])])

    # Combine: outer arc, inner arc (reversed), close polygon
    verts = np.vstack([
        outer_arc,
        inner_arc,
        outer_arc[0]
    ])

    # Create path with a hole (using Path.CLOSEPOLY for the hole)
    codes = np.full(len(verts), mpath.Path.LINETO)
    codes[0] = mpath.Path.MOVETO
    codes[len(outer_arc)] = mpath.Path.MOVETO  # start inner arc
    codes[-1] = mpath.Path.CLOSEPOLY

    sector_path = mpath.Path(verts, codes)

    # Apply the custom boundary to the axes
    ax.set_boundary(sector_path, transform=ax.transAxes)
