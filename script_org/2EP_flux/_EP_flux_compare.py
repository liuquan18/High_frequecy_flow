#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from aostools.climate import ComputeEPfluxDivXr, PlotEPfluxArrows, GetWavesXr
# %%
u = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_daily/r1i1p1f1/ua_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc").ua
v = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/va_daily/r1i1p1f1/va_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc").va
t = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ta_daily/r1i1p1f1/ta_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc").ta
#%%
u = u.isel(time = 0)
v = v.isel(time = 0)
t = t.isel(time = 0)
# %%
eq1, eq2, div1, div2 = ComputeEPfluxDivXr(
    u,
    v,
    t,
    lat = 'lat',
    lon = 'lon',
    pres = 'plev',
    wave = -1,
)
div = div1 + div2
#%%
eq1 = eq1.sel(k = slice(1, 6)).sum('k')
eq2 = eq2.sel(k = slice(1, 6)).sum('k')
div = div.sel(k = slice(1, 6)).sum('k')
# %%
fig, ax = plt.subplots(figsize=(10, 10))

div.plot.contourf(
    ax = ax,
    cmap = 'RdBu_r',
    add_colorbar = False,
    extend = 'both',
    levels = np.arange(-20, 21, 2),
)
PlotEPfluxArrows(
    x = eq1.lat[::3],
    y = eq1.plev,
    ep1 = eq1[:, ::3],
    ep2 = eq2[:, ::3],
    fig = fig,
    ax = ax,
    xlim = [0, 90],
    ylim = [100000, 10000],
    

)
#################
# %%
