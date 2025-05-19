#%%
import xarray as xr
import metpy.calc as mpcalc
from metpy.interpolate import interpolate_to_isosurface
from metpy.units import units

# %%
theta = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/equiv_theta_daily/r1i1p1f1/equiv_theta_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc"
).etheta

uwnd = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily/r1i1p1f1/ua_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc"
).ua

vwnd = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily/r1i1p1f1/va_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc"
).va
# %%
theta = theta.metpy.assign_crs(
    grid_mapping_name='latitude_longitude',
    earth_radius=6371229.0
)
uwnd = uwnd.metpy.assign_crs(
    grid_mapping_name='latitude_longitude',
    earth_radius=6371229.0
)
vwnd = vwnd.metpy.assign_crs(
    grid_mapping_name='latitude_longitude',
    earth_radius=6371229.0
)


#%%
theta = theta.isel(time = 0)
uwnd = uwnd.isel(time = 0)
vwnd = vwnd.isel(time = 0)
#%%
# units
theta = theta*units('K')
uwnd = uwnd*units('m/s')
vwnd = vwnd*units('m/s')
#%%
theta = theta.rename({theta.metpy.vertical.name: 'pres'})
uwnd = uwnd.rename({uwnd.metpy.vertical.name: 'pres'})
vwnd = vwnd.rename({vwnd.metpy.vertical.name: 'pres'})

#%%
pres = uwnd.pres
lons = uwnd.lon
lats = uwnd.lat
#%%
pres = pres*units('Pa')
lons = lons*units('degrees')
lats = lats*units('degrees')
#%%
dx, dy = mpcalc.lat_lon_grid_deltas(lons, lats)

# %%
# calculate the potential vorticity
pv = mpcalc.potential_vorticity_baroclinic(
    theta,
    pres,
    uwnd,
    vwnd,

)
# %%
# Define the target PVU level
target_pvu = 2.0 * pv.metpy.units

# %%
theta_on_2pvu = interpolate_to_isosurface(pv.values*pv.metpy.units, theta.values*units.kelvin, target_pvu)

# %%
theta_on_2pvu_xr = xr.DataArray(
    theta_on_2pvu,
    coords={
        'lat': theta.lat,
        'lon': theta.lon,
    },
    dims=['lat', 'lon']
)
# %%
