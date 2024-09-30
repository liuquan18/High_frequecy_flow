# %%
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec
# %%
# Set the background color to black
plt.rcParams['figure.facecolor'] = 'black'
plt.rcParams['axes.facecolor'] = 'black'

# Set the lines and labels to white
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['axes.edgecolor'] = 'white'
plt.rcParams['lines.color'] = 'white'

#%%
# Set default font sizes
plt.rcParams['axes.titlesize'] = 20  # Title font size
plt.rcParams['axes.labelsize'] = 15  # X and Y label font size
plt.rcParams['xtick.labelsize'] = 12  # X tick label font size
plt.rcParams['ytick.labelsize'] = 12  # Y tick label font size
plt.rcParams['legend.fontsize'] = 13  # Legend font size

# %%
pos_ens = 38
neg_ens = 3
# %%
pos_extreme = pd.read_csv(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/pos_extreme_events/pos_extreme_events_first10/troposphere_pos_extreme_events_1850_1859_r{pos_ens}.csv"
)
pos_extreme = pos_extreme[pos_extreme["plev"] == 25000]
# select the row with the maximum value of the 'extreme_duration'
pos_extreme = pos_extreme.loc[pos_extreme["extreme_duration"].idxmax()]
pos_start_date = pos_extreme["sign_start_time"]
pos_end_date = pos_extreme["sign_end_time"]

pos_extreme_start_date = pos_extreme["extreme_start_time"]
pos_extreme_end_date = pos_extreme["extreme_end_time"]

# pc
pos_pc = xr.open_dataset(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_first10/troposphere_pc_MJJAS_ano_1850_1859_r{pos_ens}.nc"
)
pos_pc = pos_pc.pc.sel(plev=25000)
pos_pc = pos_pc.sel(time=slice(pos_start_date, pos_end_date))

# uhat
pos_uhat = xr.open_dataset(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_first10_hat/ua_day_MPI-ESM1-2-LR_historical_r{pos_ens}i1p1f1_gn_18500501-18590931.nc"
)
pos_uhat = pos_uhat.ua.sel(plev=slice(100000, 70000)).mean(dim="plev")
pos_uhat = pos_uhat.sel(time=slice(pos_start_date, pos_end_date))
pos_uhat = pos_uhat.sel(lon=slice(260, 350)).mean(dim="lon")

# mf
pos_mf = xr.open_dataset(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/E_N_MJJAS_first10_prime/E_N_day_MPI-ESM1-2-LR_historical_r{pos_ens}i1p1f1_gn_18500501-18590931.nc"
).ua
# eddy driven jet
pos_mf_zonal = pos_mf.sel(plev=slice(100000, 70000)).mean(dim="plev")
pos_mf_zonal = pos_mf_zonal.sel(lon=slice(260, 350)).mean(dim="lon")
pos_mf_zonal = pos_mf_zonal.sel(time=slice(pos_start_date, pos_end_date))
pos_mf_event = pos_mf.sel(time=pos_start_date, plev=25000).squeeze()
# zg
pos_zg = xr.open_dataset(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily_global/zg_MJJAS_first10/zg_day_MPI-ESM1-2-LR_historical_r{pos_ens}i1p1f1_gn_18500501-18590931.nc"
)
pos_zg = pos_zg.sel(time=pos_extreme_start_date, plev=25000, method="nearest").zg

# %%
# negative extreme
neg_extreme = pd.read_csv(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/neg_extreme_events/neg_extreme_events_first10/troposphere_neg_extreme_events_1850_1859_r{neg_ens}.csv"
)
neg_extreme = neg_extreme[neg_extreme["plev"] == 25000]
# select the row with the maximum value of the 'extreme_duration'
neg_extreme = neg_extreme.loc[neg_extreme["extreme_duration"].idxmax()]
neg_start_date = neg_extreme["sign_start_time"]
neg_end_date = neg_extreme["sign_end_time"]

neg_extreme_start_date = neg_extreme["extreme_start_time"]
neg_extreme_end_date = neg_extreme["extreme_end_time"]

# pc
neg_pc = xr.open_dataset(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_first10/troposphere_pc_MJJAS_ano_1850_1859_r{neg_ens}.nc"
)
neg_pc = neg_pc.pc.sel(plev=25000)
neg_pc = neg_pc.sel(time=slice(neg_start_date, neg_end_date))

# uhat
neg_uhat = xr.open_dataset(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_first10_hat/ua_day_MPI-ESM1-2-LR_historical_r{neg_ens}i1p1f1_gn_18500501-18590931.nc"
)
# eddy driven jet (average between plev 1000hPa - 700hPa )
neg_uhat = neg_uhat.ua.sel(plev=slice(100000, 70000)).mean(dim="plev")
# select the time period of the extreme event
neg_uhat = neg_uhat.sel(time=slice(neg_start_date, neg_end_date))
# select the region of interest
neg_uhat = neg_uhat.sel(lon=slice(260, 350)).mean(dim="lon")

# mf
neg_mf = xr.open_dataset(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/E_N_MJJAS_first10_prime/E_N_day_MPI-ESM1-2-LR_historical_r{neg_ens}i1p1f1_gn_18500501-18590931.nc"
).ua
# eddy driven jet
neg_mf_zonal = neg_mf.sel(plev=slice(100000, 70000)).mean(dim="plev")
neg_mf_zonal = neg_mf_zonal.sel(lon=slice(260, 350)).mean(dim="lon")
neg_mf_zonal = neg_mf_zonal.sel(time=slice(neg_start_date, neg_end_date))
neg_mf_event = neg_mf.sel(time=neg_start_date, plev=25000).squeeze()

# zg
neg_zg = xr.open_dataset(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily_global/zg_MJJAS_first10/zg_day_MPI-ESM1-2-LR_historical_r{neg_ens}i1p1f1_gn_18500501-18590931.nc"
)
neg_zg = neg_zg.sel(time=neg_extreme_start_date, plev=25000, method="nearest").zg

# %%
fig = plt.figure(figsize=(15, 10))

gs = gridspec.GridSpec(3, 2)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

pos_pc.plot(ax=ax1)
neg_pc.plot(ax=ax2)

# hline at y = 1.5 for ax1, y = -1.5 for ax2
ax1.axhline(y=1.5, color="r", linestyle="--")
ax2.axhline(y=-1.5, color="r", linestyle="--")

ax1.set_title("example NAO+ event")
ax2.set_title("example NAO- event")

# # twin ax of ax1 and ax2 to plot zonal mean of mf_zonal
ax1_twin = ax1.twinx()
ax2_twin = ax2.twinx()
pos_mf_mermean = pos_mf_zonal.sel(lat=slice(30, 60)).mean(dim="lat")
neg_mf_mermean = neg_mf_zonal.sel(lat=slice(30, 60)).mean(dim="lat")

pos_mf_mermean['time'] = pos_pc.time
neg_mf_mermean['time'] = neg_pc.time

# pos_mf_mermean.plot(
#      ax=ax1_twin, color="w", linestyle="--"
# )
# neg_mf_mermean.plot(
#     ax=ax2_twin, color="w", linestyle="--"
# )
ax1_twin.set_title(None)
ax2_twin.set_title(None)

ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

cs_pos = pos_uhat.T.plot.contour(
    ax=ax3,
    colors="w",
    levels=np.arange(4, 10, 1),
    kwargs=dict(inline=True),
)
cs_neg = neg_uhat.T.plot.contour(
    ax=ax4,
    colors="w",
    levels=np.arange(4, 10, 1),
    kwargs=dict(inline=True),
)

# mf_zonal_plot_pos = pos_mf_zonal.T.plot.contourf(
#     ax=ax3, levels=np.arange(-8, 9, 2), add_colorbar=False
# )
# mf_zonal_plot_neg = neg_mf_zonal.T.plot.contourf(
#     ax=ax4, levels=np.arange(-8, 9, 2), add_colorbar=False
# )


ax3.clabel(cs_pos, inline=True, fontsize=10)
ax4.clabel(cs_neg, inline=True, fontsize=10)

# add colorbar at the bottom
# plt.colorbar(mf_zonal_plot_pos, ax=[ax3, ax4], orientation='horizontal', label='m/s', aspect=50)

ax3.set_ylim(0, None)
ax4.set_ylim(0, None)

ax3.set_title("eddy driven jet location (NAO+)")
ax4.set_title("eddy driven jet location (NAO-)")


# ax5 = fig.add_subplot(gs[2, 0], projection=ccrs.PlateCarree(-50))
# ax6 = fig.add_subplot(gs[2, 1], projection=ccrs.PlateCarree(-50))

# cs_zg_pos = pos_zg.plot.contour(
#     ax=ax5,
#     transform=ccrs.PlateCarree(),
#     levels=np.arange(9100, 10500, 50),
#     kwargs=dict(inline=True),
#     colors="w",
# )
# cs_zg_neg = neg_zg.plot.contour(
#     ax=ax6,
#     transform=ccrs.PlateCarree(),
#     levels=np.arange(9100, 10500, 50),
#     kwargs=dict(inline=True),
#     colors="w",
# )

# co_mf_pos = pos_mf_event.plot.contourf(
#     ax=ax5,
#     transform=ccrs.PlateCarree(),
#     levels=np.arange(-250, 251, 50),
#     add_colorbar=False,
# )
# co_mf_neg = neg_mf_event.plot.contourf(
#     ax=ax6,
#     transform=ccrs.PlateCarree(),
#     levels=np.arange(-250, 251, 50),
#     add_colorbar=False,
# )


# ax5.clabel(cs_zg_pos, inline=True, fontsize=10)
# ax6.clabel(cs_zg_neg, inline=True, fontsize=10)

# ax5.coastlines(alpha=0.5, linewidth=2)
# ax6.coastlines(alpha=0.5, linewidth=2)

# ax5.set_extent([280, 360, 0, 90])
# ax6.set_extent([280, 360, 0, 90])

# ax5.set_aspect("auto")
# ax6.set_aspect("auto")
ax3.set_ylabel("Latitude")
ax4.set_ylabel("Latitude")

# Adjust the layout to make space for the colorbar
plt.subplots_adjust( hspace = 0.8)
# plt.tight_layout(rect=[0, 0.1, 1, 1])

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/imprs_retreat_2024/extreme_example_noshading.png", dpi=300)

# %%
fig = plt.figure(figsize=(15, 10))

gs = gridspec.GridSpec(3, 2)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

pos_pc.plot(ax=ax1)
neg_pc.plot(ax=ax2)

# hline at y = 1.5 for ax1, y = -1.5 for ax2
ax1.axhline(y=1.5, color="r", linestyle="--")
ax2.axhline(y=-1.5, color="r", linestyle="--")

ax1.set_title("example NAO+ event")
ax2.set_title("example NAO- event")

# # twin ax of ax1 and ax2 to plot zonal mean of mf_zonal
ax1_twin = ax1.twinx()
ax2_twin = ax2.twinx()
pos_mf_mermean = pos_mf_zonal.sel(lat=slice(30, 60)).mean(dim="lat")
neg_mf_mermean = neg_mf_zonal.sel(lat=slice(30, 60)).mean(dim="lat")

pos_mf_mermean['time'] = pos_pc.time
neg_mf_mermean['time'] = neg_pc.time

# pos_mf_mermean.plot(
#      ax=ax1_twin, color="w", linestyle="--"
# )
# neg_mf_mermean.plot(
#     ax=ax2_twin, color="w", linestyle="--"
# )

ax1_twin.set_title(None)
ax2_twin.set_title(None)

ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

cs_pos = pos_uhat.T.plot.contour(
    ax=ax3,
    colors="k",
    levels=np.arange(4, 10, 1),
    kwargs=dict(inline=True),
)
cs_neg = neg_uhat.T.plot.contour(
    ax=ax4,
    colors="k",
    levels=np.arange(4, 10, 1),
    kwargs=dict(inline=True),
)

mf_zonal_plot_pos = pos_mf_zonal.T.plot.contourf(
    ax=ax3, levels=np.arange(-8, 9, 2), add_colorbar=False
)
mf_zonal_plot_neg = neg_mf_zonal.T.plot.contourf(
    ax=ax4, levels=np.arange(-8, 9, 2), add_colorbar=False
)


ax3.clabel(cs_pos, inline=True, fontsize=10)
ax4.clabel(cs_neg, inline=True, fontsize=10)

# add colorbar at the bottom
# plt.colorbar(mf_zonal_plot_pos, ax=[ax3, ax4], orientation='horizontal', label='m/s', aspect=50)

ax3.set_ylim(0, None)
ax4.set_ylim(0, None)

ax3.set_title("eddy driven jet location (NAO+)")
ax4.set_title("eddy driven jet location (NAO-)")


# ax5 = fig.add_subplot(gs[2, 0], projection=ccrs.PlateCarree(-50))
# ax6 = fig.add_subplot(gs[2, 1], projection=ccrs.PlateCarree(-50))

# cs_zg_pos = pos_zg.plot.contour(
#     ax=ax5,
#     transform=ccrs.PlateCarree(),
#     levels=np.arange(9100, 10500, 50),
#     kwargs=dict(inline=True),
#     colors="w",
# )
# cs_zg_neg = neg_zg.plot.contour(
#     ax=ax6,
#     transform=ccrs.PlateCarree(),
#     levels=np.arange(9100, 10500, 50),
#     kwargs=dict(inline=True),
#     colors="w",
# )

# co_mf_pos = pos_mf_event.plot.contourf(
#     ax=ax5,
#     transform=ccrs.PlateCarree(),
#     levels=np.arange(-250, 251, 50),
#     add_colorbar=False,
# )
# co_mf_neg = neg_mf_event.plot.contourf(
#     ax=ax6,
#     transform=ccrs.PlateCarree(),
#     levels=np.arange(-250, 251, 50),
#     add_colorbar=False,
# )


# ax5.clabel(cs_zg_pos, inline=True, fontsize=10)
# ax6.clabel(cs_zg_neg, inline=True, fontsize=10)

# ax5.coastlines(alpha=0.5, linewidth=2)
# ax6.coastlines(alpha=0.5, linewidth=2)

# ax5.set_extent([280, 360, 0, 90])
# ax6.set_extent([280, 360, 0, 90])

# ax5.set_aspect("auto")
# ax6.set_aspect("auto")

# Adjust the layout to make space for the colorbar

plt.subplots_adjust( hspace = 0.8)
ax3.set_ylabel("Latitude")
ax4.set_ylabel("Latitude")

# add horizontal colorbar
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(mf_zonal_plot_neg, cax=cbar_ax, orientation="horizontal")
cbar.set_label(r"$m^2/s^2$ (zonal mean scaled by 1/5)", loc="center")

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/imprs_retreat_2024/extreme_example_shading.png", dpi=300)


# %%
