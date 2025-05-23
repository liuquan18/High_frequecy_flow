#%%
import xarray as xr
import metpy.calc as mpcalc
from metpy.interpolate import interpolate_to_isosurface
from metpy.units import units

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

def cal_pv(ta, ua, va):

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
  
    return pv

