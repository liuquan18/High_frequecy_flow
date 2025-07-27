#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
# %%
awbs = xr.open_mfdataset("data/MPI_GE_CMIP6/wb_anticyclonic_fldmean/*.nc",
                        combine='by_coords')
                         
                         
                         
                         # %%
cwbs = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0wb_stat/cwb_stat.nc").flag
# %%
fig, ax = plt.subplots()
awbs.plot.line(
    ax=ax,
    x = 'decade',
    color = 'k',
    linestyle='-',
    label='AWB')

#%%
fig, ax = plt.subplots()

cwbs.plot.line(
    ax=ax,
    x = 'decade',
    color = 'k',
    linestyle='--',
    label='CWB')