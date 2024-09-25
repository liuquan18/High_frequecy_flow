#%%
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec

#%%
ens = 2
# %%
pos_extreme = pd.read_csv(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/pos_extreme_events/pos_extreme_events_first10/troposphere_pos_extreme_events_1850_1859_r{ens}.csv")
pos_extreme = pos_extreme[pos_extreme['plev'] == 25000]
# select the row with the maximum value of the 'extreme_duration'
pos_extreme = pos_extreme.loc[pos_extreme['extreme_duration'].idxmax()]
pos_start_date = pos_extreme['sign_start_time']
pos_end_date = pos_extreme['sign_end_time']

# %%
pos_extreme_start_date = pos_extreme['extreme_start_time']
pos_extreme_end_date = pos_extreme['extreme_end_time']

# %%
# negative extreme
neg_extreme = pd.read_csv(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/neg_extreme_events/neg_extreme_events_first10/troposphere_neg_extreme_events_1850_1859_r{ens}.csv")
neg_extreme = neg_extreme[neg_extreme['plev'] == 25000]
# select the row with the maximum value of the 'extreme_duration'
neg_extreme = neg_extreme.loc[neg_extreme['extreme_duration'].idxmax()]
neg_start_date = neg_extreme['sign_start_time']
neg_end_date = neg_extreme['sign_end_time']

#%%
neg_extreme_start_date = neg_extreme['extreme_start_time']
neg_extreme_end_date = neg_extreme['extreme_end_time']
# %%
# pc
pc = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_first10/troposphere_pc_MJJAS_ano_1850_1859_r{ens}.nc")
# %%
pc = pc.pc.sel(plev=25000)
# %%
pos_pc = pc.sel(time=slice(pos_start_date, pos_end_date))
neg_pc = pc.sel(time=slice(neg_start_date, neg_end_date))
# %%
umean = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_season_global/ua_Amon_MPI-ESM1-2-LR_HIST_ensmean_185005-185909.nc").ua.sel(plev=25000)
#%%
uhat = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_first10_hat/ua_day_MPI-ESM1-2-LR_historical_r{ens}i1p1f1_gn_18500501-18590931.nc")
# %%
pos_uhat = uhat.ua.sel(plev=25000, time=slice(pos_start_date, pos_end_date))
pos_umean = umean.sel(time=pos_start_date, method='nearest')
pos_uhat = pos_uhat + pos_umean
pos_uhat = pos_uhat.sel(lon = slice(240,360)).mean(dim='lon')
# %%
neg_uhat = uhat.ua.sel(plev=25000, time=slice(neg_start_date, neg_end_date))
neg_umean = umean.sel(time=neg_start_date, method='nearest')
neg_uhat = neg_uhat + neg_umean
neg_uhat = neg_uhat.sel(lon = slice(240,360)).mean(dim='lon')
# %%
mf = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/E_N_MJJAS_first10_prime/E_N_day_MPI-ESM1-2-LR_historical_r{ens}i1p1f1_gn_18500501-18590931.nc")
#%%
mf_zonal = mf.ua.sel(plev=25000, lon=slice(240,360)).mean(dim='lon')
pos_mf_zonal = mf_zonal.sel(time=slice(pos_start_date, pos_end_date))
neg_mf_zonal = mf_zonal.sel(time=slice(neg_start_date, neg_end_date))
# %%
zg_ano = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily_global/zg_MJJAS_ano_first10/zg_day_MPI-ESM1-2-LR_historical_r{ens}i1p1f1_gn_18500501-18590930_ano.nc")
zg_mean = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_season_global/zg_month_ensmean_1850_1859.nc")
# %%
zg_ano = zg_ano.zg.sel(plev=25000)
zg_mean = zg_mean.zg.sel(plev=25000)
# %%
pos_zg = zg_ano.sel(time=pos_extreme_start_date, method='nearest')
neg_zg = zg_ano.sel(time=neg_extreme_start_date, method='nearest')
# %%
pos_zg = pos_zg + zg_mean.sel(time=pos_extreme_start_date, method='nearest')
# %%
neg_zg = neg_zg + zg_mean.sel(time=neg_extreme_start_date, method='nearest')
# %%
pos_mf = mf.ua.sel(plev=25000, time=pos_extreme_start_date).squeeze()
neg_mf = mf.ua.sel(plev=25000, time=neg_extreme_start_date).squeeze()
# %%
fig = plt.figure(figsize=(15, 10))

gs = gridspec.GridSpec(3, 2)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

pos_pc.plot(ax=ax1)
neg_pc.plot(ax=ax2)

# hline at y = 1.5 for ax1, y = -1.5 for ax2
ax1.axhline(y=1.5, color='r', linestyle='--')
ax2.axhline(y=-1.5, color='r', linestyle='--')  

ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

cs_pos =pos_uhat.T.plot.contour(ax=ax3, colors = 'k', levels = np.arange(10,30,5),kwargs=dict(inline=True),)
cs_neg = neg_uhat.T.plot.contour(ax=ax4, colors = 'k', levels = np.arange(10,31,5),kwargs=dict(inline=True),)

mf_zonal_plot_pos = pos_mf_zonal.T.plot.contourf(ax=ax3, levels = np.arange(-50,51,10), add_colorbar=False)
mf_zonal_plot_neg = neg_mf_zonal.T.plot.contourf(ax=ax4, levels = np.arange(-50,51,10), add_colorbar=False)


ax3.clabel(cs_pos, inline=True, fontsize=10)
ax4.clabel(cs_neg, inline=True, fontsize=10)

# add colorbar at the bottom 
# plt.colorbar(mf_zonal_plot_pos, ax=[ax3, ax4], orientation='horizontal', label='m/s', aspect=50)

ax3.set_ylim(0,None)
ax4.set_ylim(0,None)


ax5 = fig.add_subplot(gs[2, 0], projection=ccrs.PlateCarree(-50))
ax6 = fig.add_subplot(gs[2, 1], projection=ccrs.PlateCarree(-50))

cs_zg_pos = pos_zg.plot.contour(ax=ax5, transform=ccrs.PlateCarree(), levels = np.arange(9100,10500, 50), kwargs=dict(inline=True),colors='k')
cs_zg_neg = neg_zg.plot.contour(ax=ax6, transform=ccrs.PlateCarree(), levels = np.arange(9100,10500, 50), kwargs=dict(inline=True), colors='k')

co_mf_pos = pos_mf.plot.contourf(ax=ax5, transform=ccrs.PlateCarree(), levels = np.arange(-250,251,50), add_colorbar=False)
co_mf_neg = neg_mf.plot.contourf(ax=ax6, transform=ccrs.PlateCarree(), levels = np.arange(-250,251,50), add_colorbar=False)


ax5.clabel(cs_zg_pos, inline=True, fontsize=10)
ax6.clabel(cs_zg_neg, inline=True, fontsize=10)

ax5.coastlines(alpha = 0.5, linewidth = 2)
ax6.coastlines(alpha = 0.5, linewidth = 2)

ax5.set_extent([280, 360, 0, 90])
ax6.set_extent([280, 360, 0, 90])

ax5.set_aspect('auto')
ax6.set_aspect('auto')

# Adjust the layout to make space for the colorbar
plt.subplots_adjust(bottom=0.1)

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(co_mf_neg, cax=cbar_ax, orientation="horizontal")
cbar.set_label(r'$m^2/s^2$ (zonal mean scaled by 1/5)', loc = 'center')
plt.tight_layout(rect=[0, 0.1, 1, 1])

# plt.savefig(f"/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave/extreme_example.png", dpi=300)
# %%
