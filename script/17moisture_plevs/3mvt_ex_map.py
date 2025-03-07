#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
#%%
time_label = '20900501-20990930'
# time_label = '18500501-18590930'
# %%
mvt_ex = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/mtw_daily/r1i1p1f1/vtm_day_MPI-ESM1-2-LR_r1i1p1f1_gn_{time_label}.nc")
# %%
mvt_ex = mvt_ex.__xarray_dataarray_variable__
#%%
mvt_ex = mvt_ex*(-1)
# %%
va = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily/r1i1p1f1/va_day_MPI-ESM1-2-LR_r1i1p1f1_gn_{time_label}.nc")
# %%
va = va.va.sel(plev = 50000)
#%%
vt = xr.open_dataset(f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vt_daily/r1i1p1f1/vt_day_MPI-ESM1-2-LR_r1i1p1f1_gn_{time_label}.nc")
vt = vt.vt*(-1)
vt_pos = np.abs(vt)
# %%
fig, axes = plt.subplots(4, 1, figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree(-90)})

vt.isel(time = 0).plot(ax = axes[0], transform = ccrs.PlateCarree(), cmap = 'RdBu_r', levels = np.arange(-5, 5.5, 0.5), cbar_kwargs = {'label': 'm/s'})
vt_pos.isel(time = 0).plot(ax = axes[1], transform = ccrs.PlateCarree(), cmap = 'RdBu_r', levels = np.arange(-5, 5.5, 0.5), cbar_kwargs = {'label': 'm/s'})

mvt_ex.isel(time = 0).plot(ax = axes[2], transform = ccrs.PlateCarree(), cmap = 'RdBu_r', levels = np.arange(-5, 5.5, 0.5), cbar_kwargs = {'label': 'm/s'})
va.isel(time = 0).plot(ax = axes[3], transform = ccrs.PlateCarree(), cmap = 'RdBu_r', levels = np.arange(-20, 21, 1), cbar_kwargs = {'label': 'm/s'})

for ax in axes:
    ax.coastlines()

    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
axes[0].set_title("Meridional (dry) thermal Wind ")
axes[1].set_title("absolute Meridional (dry) thermal Wind ")
axes[2].set_title("Meridional Moisture Thermal Wind (1000 - 250 hPa)")
axes[3].set_title("Meridional Wind (500 hPa)")



# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/regression_2_vp/meridional_mvt_va.png")
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/regression_2_vp/meridional_mvt_va_2090.png")

# %%
upvp = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/upvp_daily/r1i1p1f1/upvp_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc")
# %%
upvp = upvp.ua
# %%
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree(-90)})
upvp.isel(time = 0).sel(plev = 50000).plot(levels = np.arange(-25, 26, 5), cmap = 'RdBu_r', cbar_kwargs = {'label': 'm/s'})
ax.coastlines()

ax.set_extent([-90, 40, 20, 90], crs=ccrs.PlateCarree())

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/regression_2_vp/meridional_upvp_1850.png")

# %%
