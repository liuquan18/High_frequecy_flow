# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# %%
first_eofs = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vEOF/montly_pattern/va_eof_first10.nc"
)
first_eof = first_eofs.eof.squeeze()
first_exp_var = first_eofs.fra.squeeze()
# %%
last_eofs = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vEOF/montly_pattern/va_eof_last10.nc"
)
last_eof = last_eofs.eof.squeeze()
last_exp_var = last_eofs.fra.squeeze()

# %%
first_pcs = xr.open_mfdataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vEOF/daily_index/daily_index_first10/*.nc",
    combine="nested",
    concat_dim="ens",
).pc
# %%
last_pcs = xr.open_mfdataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vEOF/daily_index/daily_index_last10/*.nc",
    combine="nested",
    concat_dim="ens",
).pc

# %%
mean = first_pcs.mean(dim=("ens", "time"))
std = first_pcs.std(dim=("ens", "time"))
# %%
first_pcs_std = (first_pcs - mean) / std
last_pcs_std = (last_pcs - mean) / std


# %%
fig = plt.figure(figsize=(12, 8))

grids = fig.add_gridspec(2, 2, width_ratios=[1, 0.5])

spa_ax1 = fig.add_subplot(grids[0, 0], projection=ccrs.PlateCarree(180))

map = first_eof.isel(mode = 0).plot.contourf(
    ax=spa_ax1,
    transform=ccrs.PlateCarree(),
    levels=np.arange(-4, 4.1, 0.5),
    extend="both",
    cmap="coolwarm",
    add_colorbar=False,
)
spa_ax1.coastlines()
spa_ax1.set_title(f"EOF1 first10 ({first_exp_var[0].values * 100:.2f}%)")

spa_ax2 = fig.add_subplot(grids[1, 0], projection=ccrs.PlateCarree(180))
(last_eof.isel(mode = 0)*-1).plot.contourf( # for same sign
    ax=spa_ax2,
    transform=ccrs.PlateCarree(),
    levels=np.arange(-4, 4.1, 0.5),
    cmap="coolwarm",
    add_colorbar=False,
)
spa_ax2.coastlines()
spa_ax2.set_title("EOF1 last10 ({:.2f}%)".format(last_exp_var[0].values * 100))


hist_ax = fig.add_subplot(grids[:, 1])
first_pcs_std.isel(mode = 0).plot.hist(
    ax=hist_ax, color="k", alpha=0.5, bins=np.arange(-4, 4.1, 0.5), label="first10"
)


(last_pcs_std.isel(mode = 0)*-1).plot.hist(
    ax=hist_ax,
    color="k",
    bins=np.arange(-4, 4.1, 0.5),
    histtype="step",
    linewidth=2,
    label="last10",
)
hist_ax.legend()
hist_ax.set_title("standardized PC")
plt.title("EOF1 and PC1")

cbar_ax = fig.add_axes([0.1, 0.1, 0.5, 0.02])
cbar = plt.colorbar(map, cax=cbar_ax, orientation="horizontal")


plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/v_EOF/EOF1_PC1.png", dpi = 300)
# %%
# for mode = 1
fig = plt.figure(figsize=(12, 8))

grids = fig.add_gridspec(2, 2, width_ratios=[1, 0.5])

spa_ax1 = fig.add_subplot(grids[0, 0], projection=ccrs.PlateCarree(180))

map = first_eof.isel(mode = 1).plot.contourf(
    ax=spa_ax1,
    transform=ccrs.PlateCarree(),
    levels=np.arange(-4, 4.1, 0.5),
    extend="both",
    cmap="coolwarm",
    add_colorbar=False,
)
spa_ax1.coastlines()
spa_ax1.set_title("EOF2 first10 ({:.2f}%)".format(first_exp_var[1].values * 100))

spa_ax2 = fig.add_subplot(grids[1, 0], projection=ccrs.PlateCarree(180))
(last_eof.isel(mode = 1)*-1).plot.contourf(
    ax=spa_ax2,
    transform=ccrs.PlateCarree(),
    levels=np.arange(-4, 4.1, 0.5),
    cmap="coolwarm",
    add_colorbar=False,
)
spa_ax2.coastlines()

spa_ax2.set_title("EOF2 last10 ({:.2f}%)".format(last_exp_var[1].values * 100))

hist_ax = fig.add_subplot(grids[:, 1])
first_pcs_std.isel(mode = 1).plot.hist(
    ax=hist_ax, color="k", alpha=0.5, bins=np.arange(-4, 4.1, 0.5), label="first10"
)

(last_pcs_std.isel(mode = 1)*-1).plot.hist(
    ax=hist_ax,
    color="k",
    bins=np.arange(-4, 4.1, 0.5),
    histtype="step",
    linewidth=2,
    label="last10",
)
hist_ax.legend()
hist_ax.set_title("standardized PC")
plt.title("EOF2 and PC2")


cbar_ax = fig.add_axes([0.1, 0.1, 0.5, 0.02])
cbar = plt.colorbar(map, cax=cbar_ax, orientation="horizontal")

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/v_EOF/EOF2_PC2.png", dpi = 300)
# %%
