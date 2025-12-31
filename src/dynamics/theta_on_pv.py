#%%
import xarray as xr
import metpy.calc as mpcalc
from metpy.interpolate import interpolate_to_isosurface
from metpy.calc import isentropic_interpolation_as_dataset
from metpy.units import units
import numpy as np
#%%

def cal_theta_on2pvu(ta, ua, va):

    ds = xr.Dataset({'ua': ua, 'va': va, 'ta': ta})
    ds = ds.metpy.parse_cf()

    pres = ds['plev']* units('Pa')

    tmpk_var = ds['ta']
    tmpk = mpcalc.smooth_n_point(tmpk_var, 5, 2)
    thta = mpcalc.potential_temperature(pres, tmpk)
    thta = thta.transpose('time', 'plev','lat','lon')

    uwnd_var = ds['ua'].squeeze()
    vwnd_var = ds['va'].squeeze()   
    uwnd = mpcalc.smooth_n_point(uwnd_var, 5, 2)
    vwnd = mpcalc.smooth_n_point(vwnd_var, 5, 2)


    lons = ds.lon
    lats = ds.lat
    # Compute dx and dy spacing for use in vorticity calculation
    dx, dy = mpcalc.lat_lon_grid_deltas(lons, lats)

    # Comput the PV on all isobaric surfaces
    pv = mpcalc.potential_vorticity_baroclinic(thta,
                                                pres, 
                                                uwnd, 
                                                vwnd,
                                           )

    theta_DT = xr.apply_ufunc(
        interpolate_to_isosurface,
        pv.squeeze().isel(plev=slice(1, None)) * 1e6,
        thta.squeeze().isel(plev=slice(1, None)),
        input_core_dims=[["plev", "lat", "lon"], ["plev", "lat", "lon"]],
        output_core_dims=[['lat', 'lon']],
        vectorize=True,
        dask='parallelized',
        exclude_dims =set(("plev",)),
        kwargs={"level": 2},
    )


    # only northern hemisphere
    theta_DT = theta_DT.sel(lat=slice(0, 90))


    return pv, theta_DT

#%%

def interpolate_isent(tmpk, pv, isentlevs, pres):
    """
    Interpolate the potential vorticity to the isentropic surface.
    """
    _, isent_pv = mpcalc.isentropic_interpolation(
        isentlevs * units('K'),
        pres * units('Pa'),
        tmpk * units('K'),
        pv * units("kelvin meter^2 / kilogram / second"),
    )



    return isent_pv
#%%

def cal_pv_isent(ta, ua, va):

    ds = xr.Dataset({'ua': ua, 'va': va, 'ta': ta})
    ds = ds.metpy.parse_cf()

    pres = ds['plev']* units('Pa')

    tmpk_var = ds['ta']
    tmpk = mpcalc.smooth_n_point(tmpk_var, 5, 2)
    thta = mpcalc.potential_temperature(pres, tmpk)
    thta = thta.transpose('time', 'plev','lat','lon')

    uwnd_var = ds['ua'].squeeze()
    vwnd_var = ds['va'].squeeze()   
    uwnd = mpcalc.smooth_n_point(uwnd_var, 5, 2)
    vwnd = mpcalc.smooth_n_point(vwnd_var, 5, 2)


    lons = ds.lon
    lats = ds.lat
    # Compute dx and dy spacing for use in vorticity calculation
    dx, dy = mpcalc.lat_lon_grid_deltas(lons, lats)

    # Comput the PV on all isobaric surfaces
    pv = mpcalc.potential_vorticity_baroclinic(thta,
                                                pres, 
                                                uwnd, 
                                                vwnd,
                                           )
  
    pv.name = 'pv'
    # Define isentropic levels as a numpy array with units
    isentlevs = np.arange(300, 361, 5)



    ds_isent = xr.Dataset({'pv': pv, 'temperature': tmpk}) 


    pv_isent = ds_isent.groupby('time').apply(
        lambda x: isentropic_interpolation_as_dataset(
            isentlevs * units('K'),
            x.temperature.isel(time=0),
            x.pv.isel(time=0),
        )
    )

    pv_isent = pv_isent.pv

    return pv_isent


def find_isentrope_at_pv(pv_zm, target_pv=2):
    """
    Find the isentropic level where PV equals target_pv for each latitude.
    
    Parameters
    ----------
    pv_zm : xr.DataArray
        Zonal mean PV with dimensions (isentropic_level, lat)
    target_pv : float
        Target PV value (default: 2)
    
    Returns
    -------
    isen_at_target : xr.DataArray
        Isentropic level at target PV for each latitude
    """
    # Interpolate along isentropic_level dimension to find where pv equals target_pv
    # We need to swap dimensions so pv becomes the coordinate
    isen_at_target = pv_zm.swap_dims({'isentropic_level': 'pv'}).interp(pv=target_pv)
    
    # Alternative method if swap_dims doesn't work:
    # Use apply_ufunc with scipy interpolation
    from scipy.interpolate import interp1d
    
    def interpolate_pv(pv_vals, isen_vals, target):
        # Filter out NaNs
        valid = ~np.isnan(pv_vals)
        if valid.sum() < 2:
            return np.nan
        
        pv_valid = pv_vals[valid]
        isen_valid = isen_vals[valid]
        
        # Check if target is within range
        if target < pv_valid.min() or target > pv_valid.max():
            return np.nan
        
        # Interpolate
        f = interp1d(pv_valid, isen_valid, bounds_error=False, fill_value=np.nan)
        return f(target)
    
    isen_levels = pv_zm.isentropic_level.values
    
    result = xr.apply_ufunc(
        interpolate_pv,
        pv_zm,
        input_core_dims=[['isentropic_level']],
        output_core_dims=[[]],
        vectorize=True,
        kwargs={'isen_vals': isen_levels, 'target': target_pv}
    )
    
    result.name = f'isen_at_pv_{target_pv}'
    result.attrs['long_name'] = f'Isentropic level at PV={target_pv}'
    result.attrs['units'] = 'K'
    
    return result
