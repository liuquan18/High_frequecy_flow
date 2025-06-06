#%%
import xarray as xr
import numpy as np
from metpy.units import units

# %%
up = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0composite_range/ua_prime_NAO_pos_1850.nc").ua
vp = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0composite_range/va_prime_NAO_pos_1850.nc").va


#%%
up = up.sel(time =slice(-10, 5)).mean(dim = ('time', 'ens'))
vp = vp.sel(time =slice(-10, 5)).mean(dim = ('time', 'ens'))
# %%
# %%
# codes here

# compute the E-vector
Ex = vp**2 - up**2
Ey = -up*vp

# rename the variables
Ex.name = 'Ex'
Ey.name = 'Ey'

# calculate the divergence of the E-vector using spherical coordinates
a0 = 6371000.  # Earth radius in meters

lat_rad = np.deg2rad(Ey['lat'])
coslat = np.cos(lat_rad)
sinlat = np.sin(lat_rad)

# div_x: (1/(a0*cos(lat))) * dEx/dlon, with dEx/dlon in radians
div_x = (1 / (a0 * coslat)) * Ex.differentiate('lon', edge_order=2)

# div_y: cos(lat) * dEy/dlat (in radians) - 2*sin(lat)*Ey
div_y = coslat * np.rad2deg(Ey).differentiate('lat', edge_order=2) - 2 * sinlat * Ey

# %%
ep1_cart = Ey
# %%
Omega = 7.292e-5 #[1/s]

# geometry
coslat = np.cos(np.deg2rad(Ey['lat']))
sinlat = np.sin(np.deg2rad(Ey['lat']))
R      = 1./(a0*coslat)
f      = 2*Omega*sinlat


div1 = coslat*(np.rad2deg(Ey).differentiate('lat',edge_order=2)) \
        - 2*sinlat*Ey
div1 = div1 *R

# %%
# %%
import metpy.calc as mpcalc


up = up.metpy.quantify()
vp = vp.metpy.quantify()

#%%
up = up.metpy.assign_crs(
grid_mapping_name='latitude_longitude',
    earth_radius=6371229.0
    )

vp = vp.metpy.assign_crs(
grid_mapping_name='latitude_longitude',
    earth_radius=6371229.0
    )
#%%
up = up*units('m/s')
vp = vp*units('m/s')
# %%
Ex = vp**2 - up**2
Ey = -up * vp
#%%
Ex = Ex.sel(plev = 25000)
Ey = Ey.sel(plev = 25000)
#%%
lons = Ex.lon.values
lats = Ex.lat.values
#%%
dx, dy = mpcalc.lat_lon_grid_deltas(
    lons, lats
)
# #%%
# upvp = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0composite_range/upvp_NAO_pos_2090.nc").upvp

# #%%
# Ey = -1* upvp.sel(plev = 25000).mean(dim = ('time', 'ens'))
# #%%
# Ey = Ey.metpy.assign_crs(
#     grid_mapping_name='latitude_longitude',
#     earth_radius=6371229.0
# )

# Ey = Ey*units('m^2/s^2')
# %%
dExdx, dEydy = mpcalc.vector_derivative(
    Ex, Ey, return_only=('du/dx', 'dv/dy'), dx = dx, dy = dy,
)
# %%
dEydy = xr.DataArray(
    dEydy,
    coords=Ey.coords,
    dims=Ey.dims,
    attrs=Ey.attrs
)
dExdx = xr.DataArray(
    dExdx,
    coords=Ex.coords,
    dims=Ex.dims,
    attrs=Ex.attrs
)
# %%
