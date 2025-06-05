#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from aostools.climate import ComputeEPfluxDivXr, PlotEPfluxArrows, GetWavesXr
# %%
t = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ta_hat_daily/r1i1p1f1/ta_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc").ta
#################
#%%
lon='lon'
lat='lat'
pres='plev'
time='time'
ref='mean'
w=None
do_ubar=False
wave=0

# %%
upvp = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/upvp_hat_daily/r1i1p1f1/upvp_1850.nc").upvp
vptp = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vptp_hat_daily/r1i1p1f1/vptp_1850.nc").vptp    


# %%
# constants
a0    = 6371000.  # earth radius in m
Omega = 7.292e-5 #[1/s]

# geometry
coslat = np.cos(np.deg2rad(upvp['lat']))
sinlat = np.sin(np.deg2rad(upvp['lat']))
R      = 1./(a0*coslat)
f      = 2*Omega*sinlat


#%%
# dthdp
t_bar = t.mean('lon')
dthdp = t_bar.differentiate('plev',edge_order=2) # dthdp = d(theta_bar)/dp
dthdp = dthdp.where(dthdp != 0)
dthdp = dthdp.mean('time')
#%%
# absolute vorticity
if do_ubar:
    ubar = u.mean(lon)
    fhat = R*np.rad2deg((ubar*coslat)).differentiate('lat',edge_order=2)
else:
    fhat = 0.
fhat = f - fhat # [1/s]
#
# %%
vptp = vptp.mean('lon')
t_bar = vptp/dthdp
# %%
vertEddy = t_bar
# %%
## compute the horizontal component
if do_ubar:
    shear = ubar.differentiate(pres,edge_order=2) # [m/s.hPa]
else:
    shear = 0.

upvp = upvp.mean('lon')
ep1_cart = -upvp + shear*vertEddy # [m2/s2 + m/s.hPa*m.hPa/s] = [m2/s2]


# %%
ep2_cart = fhat*vertEddy # [1/s*m.hPa/s] = [m.hPa/s2]

#
#
# We now have to make sure we get the geometric terms right
# With our definition,
#  div1 = 1/(a.cosphi)*d/dphi[a*cosphi*ep1_cart*cosphi],
#    where a*cosphi comes from using cartesian, and cosphi from the derivative
# With some algebra, we get
#  div1 = cosphi d/d phi[ep1_cart] - 2 sinphi*ep1_cart
div1 = coslat*(np.rad2deg(ep1_cart).differentiate('lat',edge_order=2)) \
        - 2*sinlat*ep1_cart
# Now, we want acceleration, which is div(F)/a.cosphi [m/s2]
div1 = R*div1 # [m/s2]
#
# Similarly, we want acceleration = 1/a.coshpi*a.cosphi*d/dp[ep2_cart] [m/s2]
div2 = ep2_cart.differentiate('plev',edge_order=2) # [m/s2]
#
# convert to m/s/day
div1 = div1*86400
div2 = div2*86400
#
initial_order = upvp.dims
# make sure order is the same as input
new_order = [d for d in initial_order if d != lon]
if not isinstance(wave,list) and wave < 0:
    new_order = ['k'] + new_order
# give the DataArrays their names
ep1_cart.name = 'ep1'
ep2_cart.name = 'ep2'
div1.name = 'div1'
div2.name = 'div2'

# %%
div = div1 + div2
ep1_cart = ep1_cart.isel(time =0)
ep2_cart = ep2_cart.isel(time =0)
div = div.isel(time = 0)
#%%
ep1_cart = ep1_cart.transpose('plev', 'lat')
ep2_cart = ep2_cart.transpose('plev', 'lat')
# %%
fig, ax = plt.subplots(figsize=(10, 10))
div.T.plot.contourf(
    ax = ax,
    cmap = 'RdBu_r',
    add_colorbar = False,
    extend = 'both',
    levels = np.arange(-20, 21, 2),
    ylim = [100000, 10000],
    xlim = [0, 90],
)


PlotEPfluxArrows(
    x = ep1_cart.lat[::3],
    y = ep1_cart.plev,
    ep1 = ep1_cart[:, ::3],
    ep2 = ep2_cart[:, ::3],
    fig = fig,
    ax = ax,
    xlim = [0, 90],
    ylim = [100000, 10000],
)
