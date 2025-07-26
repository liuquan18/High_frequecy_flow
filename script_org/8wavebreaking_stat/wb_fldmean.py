#%%
import xarray as xr
import numpy as np
import os
import sys
import glob
import matplotlib.pyplot as plt
# %%
def fldmean(decade, wb_type='anticyclonic'):
    
    data_dir=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_{wb_type}_daily/"
    
    wb = xr.open_mfdataset(
        glob.glob(os.path.join(data_dir, f'r*i1p1f1/*{decade}.nc')),
        combine='nested',
        concat_dim='ens',
    )
    
    if wb_type == 'anticyclonic':
        wb1 = wb.sel(lat = slice(30, 70), lon = slice(300, 360))
        wb2 = wb.sel(lat = slice(30, 70), lon = slice(0, 30))
        wb = xr.concat([wb1, wb2], dim='lon')
    else:
        wb = wb.sel(lat = slice(45, 75), lon = slice(260, 330))

    
    wb_mean = wb.mean(dim=('lon','lat')).sum(dim=('time','ens'))

    return wb_mean
# %%

awbs = []
cwbs = []

for decade in np.arange(1850, 2100, 10):
    
    awb_mean = fldmean(decade, 'anticyclonic')
    cwb_mean = fldmean(decade, 'cyclonic')

    awb_mean = awb_mean.expand_dims(decade=[decade]).set_index(decade='decade')
    cwb_mean = cwb_mean.expand_dims(decade=[decade]).set_index(decade='decade')

    awbs.append(awb_mean)
    cwbs.append(cwb_mean)

awbs = xr.concat(awbs, dim='decade')
cwbs = xr.concat(cwbs, dim='decade')
#%%
awbs.compute()
cwbs.compute()
#%%
# save
awbs.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0wb_stat/awb_stat.nc")
cwbs.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0wb_stat/cwb_stat.nc")

# %%
fig, ax = plt.subplots()
awbs.flag.plot.line(
    ax=ax,
    x = 'decade',
    color = 'k',
    linestyle='-',
    label='AWB')
cwbs.flag.plot.line(
    ax=ax,
    x = 'decade',
    color = 'k',
    linestyle='--',
    label='CWB')
# %%
