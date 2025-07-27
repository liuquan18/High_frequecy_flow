#%%
import xarray as xr
import numpy as np
import os
import sys
import glob
import matplotlib.pyplot as plt
import logging
logging.basicConfig(level=logging.INFO)
# %%
def fldmean(decade, wb_type='anticyclonic'):
    
    data_dir=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_{wb_type}_daily/"
    
    wb = xr.open_mfdataset(
        glob.glob(os.path.join(data_dir, f'r*i1p1f1/*{decade}.nc')),
        combine='nested',
        concat_dim='ens',
    )
    
    wb1 = wb.sel(lat = slice(50, 70), lon = slice(0, 40))
    wb2 = wb.sel(lat = slice(50, 70), lon = slice(270, 360))
    wb = xr.concat([wb1, wb2], dim='lon')
    
    wb_mean = wb.mean(dim=('lon','lat')).sum(dim=('time','ens'))

    return wb_mean


#%%
decade = sys.argv[1]
decade = int(decade)
logging.info(f"Processing decade {decade}")

awb_mean = fldmean(decade, 'anticyclonic')
cwb_mean = fldmean(decade, 'cyclonic')

awb_mean = awb_mean.expand_dims(decade=[decade]).set_index(decade='decade')
cwb_mean = cwb_mean.expand_dims(decade=[decade]).set_index(decade='decade')

# %%
awb_mean.to_netcdf(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_anticyclonic_fldmean/awb_fldmean_{decade}.nc")
# cwb_mean.to_netcdf(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_cyclonic_fldmean/cwb_fldmean_{decade}.nc")