#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
# %%
ex = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/pv_daily/r1i1p1f1/pv_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc")
# %%
zonalmean = ex.mean(dim = ('time','lon'))
# %%
zonalmean = zonalmean*1e6
# %%
trops = find_isentrope_at_pv(zonalmean.pv)
# %%
# %%

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

# Usage:
# isen_at_pv2 = find_isentrope_at_pv(pv_zm, target_pv=2)