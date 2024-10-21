#%%
import xarray as xr
import numpy as np
from eofs.standard import Eof

#%%
from src.Teleconnection.spatial_pattern import doeof

# %%

def wind_eof(var, period):
    base_dir=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_monthly_ano/{var}_monthly_ano_{period}/"

    ds = xr.open_mfdataset(f"{base_dir}*.nc", combine='nested',concat_dim ='ens')
    
    ds = ds[var].sel(plev=25000)
    
    ds_com = ds.stack(com = ('time','ens'))
    ds_com = ds_com.sel(lat = slice(0,90))
    
    eof_result = doeof(ds_com, 1, dim = 'com', standard='pc_temporal_std')
    return eof_result

# %%
first_va_eof = wind_eof('va', 'first10')
last_va_eof = wind_eof('va', 'last10')
# %%
first_va_eof.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/WB_before_NAO/va_eof_first10.nc")
last_va_eof.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/WB_before_NAO/va_eof_last10.nc")
# %%
