#%%
import xarray as xr
import metpy.calc as mpcalc
from metpy.interpolate import interpolate_to_isosurface
from metpy.units import units



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
    theta_on_2pvu = interpolate_to_isosurface(pv.values*pv.metpy.units, theta.values*units.kelvin, target_pvu)

    # 
    theta_on_2pvu_xr = xr.DataArray(
        theta_on_2pvu,
        coords={
            'lat': theta.lat,
            'lon': theta.lon,
        },
        dims=['lat', 'lon']
    )

    return theta_on_2pvu_xr
