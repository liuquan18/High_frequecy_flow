#%%
import xarray as xr
import metpy.calc as mpcalc
from metpy.interpolate import interpolate_to_isosurface
from metpy.units import units

#%%

def theta_on_2pvu(theta, uwnd, vwnd):
    # units
    theta = theta*units('K')
    uwnd = uwnd*units('m/s')
    vwnd = vwnd*units('m/s')
    #
    theta = theta.rename({theta.metpy.vertical.name: 'pres'})
    uwnd = uwnd.rename({uwnd.metpy.vertical.name: 'pres'})
    vwnd = vwnd.rename({vwnd.metpy.vertical.name: 'pres'})
    pres = uwnd.pres


    # calculate the potential vorticity
    pv = mpcalc.potential_vorticity_baroclinic(
        theta,
        pres,
        uwnd,
        vwnd,

    )

    # Define the target PVU level
    target_pvu = 2.0 * pv.metpy.units

    # 
    theta_pv = interpolate_to_isosurface(pv.values*pv.metpy.units, theta.values*units.kelvin, target_pvu)

    # 
    theta_pv_xr = xr.DataArray(
        theta_pv,
        coords={
            'lat': theta.lat,
            'lon': theta.lon,
        },
        dims=['lat', 'lon']
    )

    return theta_pv_xr

# %%
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
from metpy.units import units
import numpy as np
import xarray as xr
# %%
ds = xr.open_dataset('https://thredds.ucar.edu/thredds/dodsC/'
                     'casestudies/python-gallery/GFS_20101026_1200.nc')

# %%
ds = ds.metpy.parse_cf()
# %%
# Set subset slice for the geographic extent of data to limit download
lon_slice = slice(200, 350)
lat_slice = slice(85, 10)

# Grab lat/lon values (GFS will be 1D)
lats = ds.lat.sel(lat=lat_slice).values
lons = ds.lon.sel(lon=lon_slice).values

# Grab the pressure levels and select the data to be imported
# Need all pressure levels for Temperatures, U and V Wind, and Rel. Humidity
# Smooth with the gaussian filter from scipy
pres = ds['isobaric3'].values[:] * units('Pa')

tmpk_var = ds['Temperature_isobaric'].metpy.sel(lat=lat_slice, lon=lon_slice).squeeze()
tmpk = mpcalc.smooth_n_point(tmpk_var, 9, 2)
thta = mpcalc.potential_temperature(pres[:, None, None], tmpk)

uwnd_var = ds['u-component_of_wind_isobaric'].metpy.sel(lat=lat_slice, lon=lon_slice).squeeze()
vwnd_var = ds['v-component_of_wind_isobaric'].metpy.sel(lat=lat_slice, lon=lon_slice).squeeze()
uwnd = mpcalc.smooth_n_point(uwnd_var, 9, 2)
vwnd = mpcalc.smooth_n_point(vwnd_var, 9, 2)

# Create a clean datetime object for plotting based on time of Geopotential heights
vtime = ds.time.data[0].astype('datetime64[ms]').astype('O')
# %%
# Compute dx and dy spacing for use in vorticity calculation
dx, dy = mpcalc.lat_lon_grid_deltas(lons, lats)

# Comput the PV on all isobaric surfaces
pv = mpcalc.potential_vorticity_baroclinic(thta, pres[:, None, None], uwnd, vwnd,
                                           dx[None, :, :], dy[None, :, :],
                                           lats[None, :, None] * units('degrees'))

# Use MetPy to compute the divergence on the pressure surfaces
#%%
div = mpcalc.divergence(uwnd, vwnd)

# %%
epv = mpcalc.potential_vorticity_baroclinic(thta, pres[:, None, None], uwnd, vwnd)

# %%
thta_DT = interpolate_to_isosurface(epv[1:].values*1e6, thta[1:].values, 2)

# %%
def plot_PV(level, dist, smooth=10):
    print(f"Creating the {level}-hPa PV Map")
    #ilev = list(lev.m).index(level*100.)
    subset = dict(vertical = level*units.hPa)
    uwnd_ilev = uwnd.metpy.sel(subset).metpy.convert_units('kt')
    vwnd_ilev = vwnd.metpy.sel(subset).metpy.convert_units('kt')
    
    sped_ilev = mpcalc.wind_speed(uwnd_ilev, vwnd_ilev)
    
    if abs(dist) < 1:
        div_ilev = mpcalc.smooth_n_point(div.metpy.sel(subset), 9, smooth)
        epv_smooth = mpcalc.smooth_n_point(epv.metpy.sel(subset), 9, smooth)
    else:
        div_ilev = mpcalc.zoom_xarray(div.metpy.sel(subset), 4)
        epv_smooth = mpcalc.zoom_xarray(mpcalc.smooth_n_point(epv.metpy.sel(subset), 9, smooth), 4)

    fig = plt.figure(1, figsize=(17,15))

    # 1st panel
    ax = plt.subplot(111, projection=mapcrs)
    ax.set_extent([-130, -72, 20, 55], ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
    ax.add_feature(cfeature.STATES.with_scale('50m'))

    cf = ax.contourf(clons, clats, sped_ilev, range(10, 230, 20), cmap=plt.cm.BuPu, extend='max')
    plt.colorbar(cf, orientation='horizontal', pad=0, aspect=50, extendrect=True)

    cs = ax.contour(clons, clats, epv_smooth*1e6, range(2, 15, 1),
                    colors='black')
    plt.clabel(cs, fmt='%d')
    
    cs2 = ax.contour(clons, clats, div_ilev*1e5, range(1, 50, 3),
                     colors='grey', linestyles='dashed')
    plt.clabel(cs2, fmt='%d')

    plt.title(f'{level}-hPa PV (PVU), Divergence ($*10^5$ $s^{-1}$), and Wind Spped (kt)', loc='left')
    plt.title(f'Valid Time: {date}', loc='right')

    plt.savefig(f'{level}-hPa_PV_{date:%Y%m%d_%H}00.png', bbox_inches='tight', dpi=150)
    plt.show()
    #plt.close()
# %%
