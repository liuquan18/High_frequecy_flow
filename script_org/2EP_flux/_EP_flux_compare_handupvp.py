#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from aostools.climate import ComputeEPfluxDivXr, PlotEPfluxArrows, GetWavesXr, ComputeVertEddy
# %%
u = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_daily/r1i1p1f1/ua_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc").ua
v = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/va_daily/r1i1p1f1/va_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc").va
t = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ta_daily/r1i1p1f1/ta_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc").ta
#%%
u = u.isel(time = 0)
v = v.isel(time = 0)
t = t.isel(time = 0)
#%%
u_bar = u.mean('lon')
up = u - u_bar
v_bar = v.mean('lon')
vp = v - v_bar
#%%
upvp = (up*vp).mean('lon')

#%%

uqvq = GetWavesXr(
    u,
    v,
    dim = 'lon',
    wave = 0,  
)

#%%
usvs = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/usvs_daily/r1i1p1f1/usvs_1850.nc").usvs
usvs = usvs.isel(time = 0).mean(dim = 'lon')

#%%
bb = u_bar*v_bar
usvs = usvs + bb

#%%
# calculate EP flux divergence
upvp = usvs
# %%
# %%
# constants
a0    = 6371000.  # earth radius in m
Omega = 7.292e-5 #[1/s]

# geometry
coslat = np.cos(np.deg2rad(upvp['lat']))
sinlat = np.sin(np.deg2rad(upvp['lat']))
R      = 1./(a0*coslat)
f      = 2*Omega*sinlat


# %%
#

fhat = f
#
# add wavenumber dimension if needed

## compute thickness weighted heat flux [m.hPa/s]
vbar,vertEddy = ComputeVertEddy(v,t,u['plev'],1e5,0) # vertEddy = bar(v'Th'/(dTh_bar/dp))
#

# %%
