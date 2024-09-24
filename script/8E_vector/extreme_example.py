#%%
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import matplotlib.gridspec as gridspec
import logging
logging.basicConfig(level=logging.WARNING)
# Any import of metpy will activate the accessors
import metpy.calc as mpcalc
from metpy.units import units
from src.extremes.extreme_read import sel_event_above_duration

# %%
#%%
# %%
def read_pos(ens):

    # positive extreme
    pos_extreme = pd.read_csv(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/pos_extreme_events/pos_extreme_events_first10/troposphere_pos_extreme_events_1850_1859_r{ens}.csv")
    pos_extreme = pos_extreme[pos_extreme['plev'] == 25000]
    pos_extreme['extreme_end_time'] = pd.to_datetime(pos_extreme['extreme_end_time'])
    
    # select the row with the maximum value of the 'extreme_duration'
    pos_extreme = pos_extreme.loc[pos_extreme['extreme_end_time'].dt.month <= 8]
    pos_extreme = pos_extreme.loc[pos_extreme['extreme_duration'].idxmax()]
    pos_start_date = pos_extreme['sign_start_time']
    pos_end_date = pos_extreme['sign_end_time']
    pos_extreme_start_date = pos_extreme['extreme_start_time']
    pos_extreme_end_date = pos_extreme['extreme_end_time']

    # pc
    pc = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_first10/troposphere_pc_MJJAS_ano_1850_1859_r{ens}.nc")
    pc = pc.pc.sel(plev=25000)
    pos_pc = pc.sel(time=slice(pos_start_date, pos_end_date))

    # uhat
    umean = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_season_global/ua_Amon_MPI-ESM1-2-LR_HIST_ensmean_185005-185909.nc").ua.sel(plev=25000)
    uhat = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_ano_first10_hat/ua_day_MPI-ESM1-2-LR_historical_r{ens}i1p1f1_gn_18500501-18590931_ano.nc")
    pos_uhat = uhat.ua.sel(plev=25000, time = pos_extreme_start_date)
    pos_umean = umean.sel(time=pos_extreme_start_date, method='nearest')
    pos_uhat = (pos_uhat + pos_umean).isel(time = 0)

    # E
    M = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_M_daily_global/E_M_MJJAS_ano_first10_prime/E_M_day_MPI-ESM1-2-LR_historical_r{ens}i1p1f1_gn_18500501-18590931_ano.nc").ua.sel(plev=25000)
    N = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/E_N_MJJAS_ano_first10_prime/E_N_day_MPI-ESM1-2-LR_historical_r{ens}i1p1f1_gn_18500501-18590931_ano.nc").ua.sel(plev=25000)
    M['time'] = M.indexes['time'].to_datetimeindex()
    N['time'] = N.indexes['time'].to_datetimeindex()
    E_M = -2*M
    E_N = -N
    pos_E_M = E_M.sel(time=slice(pos_extreme_start_date, pos_extreme_end_date)).mean(dim = 'time')
    pos_E_N = E_N.sel(time=slice(pos_extreme_start_date, pos_extreme_end_date)).mean(dim = 'time')

    return pos_pc, pos_uhat,pos_E_M,pos_E_N

def read_neg(ens):
    
    # negative extreme
    neg_extreme = pd.read_csv(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/neg_extreme_events/neg_extreme_events_first10/troposphere_neg_extreme_events_1850_1859_r{ens}.csv")
    neg_extreme = neg_extreme[neg_extreme['plev'] == 25000]
    neg_extreme['extreme_end_time'] = pd.to_datetime(neg_extreme['extreme_end_time'])

    # select the row with the maximum value of the 'extreme_duration'
    neg_extreme = neg_extreme.loc[neg_extreme['extreme_end_time'].dt.month <= 8]
    neg_extreme = neg_extreme.loc[neg_extreme['extreme_duration'].idxmax()]
    neg_start_date = neg_extreme['sign_start_time']
    neg_end_date = neg_extreme['sign_end_time']
    neg_extreme_start_date = neg_extreme['extreme_start_time']
    neg_extreme_end_date = neg_extreme['extreme_end_time']

    # pc
    pc = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_first10/troposphere_pc_MJJAS_ano_1850_1859_r{ens}.nc")
    pc = pc.pc.sel(plev=25000)
    neg_pc = pc.sel(time=slice(neg_start_date, neg_end_date))

    # uhat
    umean = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_season_global/ua_Amon_MPI-ESM1-2-LR_HIST_ensmean_185005-185909.nc").ua.sel(plev=25000)
    uhat = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_first10_hat/ua_day_MPI-ESM1-2-LR_historical_r{ens}i1p1f1_gn_18500501-18590931.nc")
    neg_uhat = uhat.ua.sel(plev=25000, time = neg_extreme_start_date)
    neg_umean = umean.sel(time=neg_extreme_start_date, method='nearest')
    neg_uhat = (neg_uhat + neg_umean).isel(time = 0)

    # E
    M = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_M_daily_global/E_M_MJJAS_first10_prime/E_M_day_MPI-ESM1-2-LR_historical_r{ens}i1p1f1_gn_18500501-18590931.nc").ua.sel(plev=25000)
    N = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/E_N_MJJAS_first10_prime/E_N_day_MPI-ESM1-2-LR_historical_r{ens}i1p1f1_gn_18500501-18590931.nc").ua.sel(plev=25000)
    M['time'] = M.indexes['time'].to_datetimeindex()
    N['time'] = N.indexes['time'].to_datetimeindex()
    E_M = -2*M
    E_N = -N
    neg_E_M = E_M.sel(time=slice(neg_extreme_start_date, neg_extreme_end_date)).mean(dim='time')
    neg_E_N = E_N.sel(time=slice(neg_extreme_start_date, neg_extreme_end_date)).mean(dim='time')

    return neg_pc, neg_uhat,neg_E_M,neg_E_N


# %%
def plot_E(E_M, E_N, u_hat, ax):


    lon = E_M.lon.values
    lat = E_M.lat.values

    skip = 3
    
    ax.coastlines(color = 'grey', linewidth = 0.5)
    lines = u_hat.plot.contourf(ax=ax, levels = np.arange(10,36,5),kwargs=dict(inline=True),alpha = 0.5, extend = 'max', add_colorbar = False)

    arrows = ax.quiver(lon[::skip], lat[::skip], E_M[::skip,::skip], E_N[::skip,::skip], scale = 4000)

    ax.set_extent([-180, 180, 0, 90], ccrs.PlateCarree())

    ax.quiverkey(arrows, X=0.85, Y=1.25, U=250, label=r'$250 m^2/s^2$', labelpos='E')

    return ax, lines, arrows


#%%
pos_pc, pos_uhat,pos_E_M,pos_E_N = read_pos(2)
#%%
neg_pc, neg_uhat,neg_E_M,neg_E_N = read_neg(8)

#%%
# calculate divergence
div_pos = mpcalc.divergence(pos_E_M, pos_E_N)
div_neg = mpcalc.divergence(neg_E_M, neg_E_N)



# %%
fig = plt.figure(figsize=(15, 15))

gs = gridspec.GridSpec(3, 2)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

pos_pc.plot(ax=ax1)
neg_pc.plot(ax=ax2)

# hline at y = 1.5 for ax1, y = -1.5 for ax2
ax1.axhline(y=1.5, color='r', linestyle='--')
ax2.axhline(y=-1.5, color='r', linestyle='--')  


ax3 = fig.add_subplot(gs[1, 0], projection=ccrs.PlateCarree(-120))
ax4 = fig.add_subplot(gs[1, 1], projection=ccrs.PlateCarree(-120))

_,p,_ = plot_E(pos_E_M, pos_E_N, pos_uhat, ax3)
plot_E(neg_E_M, neg_E_N, neg_uhat, ax4)


ax5 = fig.add_subplot(gs[2, 0], projection=ccrs.PlateCarree(-120))
ax6 = fig.add_subplot(gs[2, 1], projection=ccrs.PlateCarree(-120))

for ax in [ax5, ax6]:
    ax.coastlines(color = 'grey', linewidth = 0.5)
    ax.set_extent([-180, 180, 0, 90], ccrs.PlateCarree())

div_pos.plot.contourf(ax=ax5, levels = np.arange(-4e-4, 4.1e-4, 1e-4), 
extend = 'both', transform=ccrs.PlateCarree(), cmap = 'RdBu_r', add_colorbar = False)
d = div_neg.plot.contourf(ax=ax6, levels = np.arange(-4e-4, 4.1e-4, 1e-4), extend = 'both', transform=ccrs.PlateCarree(), cmap = 'RdBu_r', add_colorbar = False)


# add colorbar at the bottom
plt.colorbar(p, ax=[ax3, ax4], orientation='horizontal', label='u (m/s)', aspect=50)
plt.colorbar(d, ax=[ax5, ax6], orientation='horizontal', label='divergence ', aspect=50)

# plt.savefig('/work/mh0033/m300883/High_frequecy_flow/docs/plots/E_vector/extreme_example.png', dpi=300)
# %%
