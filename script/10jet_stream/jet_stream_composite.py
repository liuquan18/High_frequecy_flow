# %%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import logging


import cartopy.crs as ccrs  
import matplotlib.pyplot as plt
# %%
from src.extremes.extreme_read import read_extremes
from src.plotting.util import erase_white_line
logging.basicConfig(level=logging.INFO)

# %%
def sel_uhat(uhat, events):
    try:
        uhat["time"] = uhat.indexes["time"].to_datetimeindex()
    except AttributeError:
        pass

    uhat_extreme = []
    for i, event in events.iterrows():
        uhat_extreme.append(
            uhat.sel(time=slice(event["extreme_start_time"], event["extreme_end_time"]))
        )

    uhat_extreme = xr.concat(uhat_extreme, dim="time")

    # average over time
    uhat_extreme = uhat_extreme.mean(dim="time")

    return uhat_extreme


# %%
def extreme_uhat(period, wind = 'ua'):
    if wind == 'ua':
        basedir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_{period}_hat/"
    elif wind == 'va':
        basedir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_MJJAS_{period}_hat/"
    uhat_pos = []
    uhat_neg = []

    for ens in range(1, 51):
        logging.info(f"Processing ensemble {ens}")

        # read extremes
        pos_extreme, neg_extreme = read_extremes(period, 8, ens, plev=25000)

        # read uhat
        uhat_file = glob.glob(f"{basedir}*r{ens}i1p1f1*.nc")[0]
        uhat = xr.open_dataset(uhat_file)[wind]

        # average over plev below 700 hPa
        uhat = uhat.sel(plev=slice(None, 70000)).mean(dim="plev")

        if not pos_extreme.empty:
            uhat_pos.append(sel_uhat(uhat, pos_extreme))

        if not neg_extreme.empty:
            uhat_neg.append(sel_uhat(uhat, neg_extreme))

    uhat_pos = xr.concat(uhat_pos, dim="ens")
    uhat_neg = xr.concat(uhat_neg, dim="ens")

    # average over ens
    uhat_pos = uhat_pos.mean(dim="ens")
    uhat_neg = uhat_neg.mean(dim="ens")

    return uhat_pos, uhat_neg
#%%
vhat_pos_first10, vhat_neg_first10 = extreme_uhat("first10", wind='va')
vhat_pos_last10, vhat_neg_last10 = extreme_uhat("last10", wind='va')
# save to netcdf
#%%
vhat_pos_first10.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/jetstream_va_MJJAS_first10_pos.nc")
vhat_neg_first10.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/jetstream_va_MJJAS_first10_neg.nc")
vhat_pos_last10.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/jetstream_va_MJJAS_last10_pos.nc")
vhat_neg_last10.to_netcdf("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/jetstream_va_MJJAS_last10_neg.nc") 
# %%
def plot_uhat(ax, uhat_first, u_hat_last=None, levels=np.arange(-12, 13, 2)):

    ax.coastlines()
    ax.set_global()

    uhat_first = erase_white_line(uhat_first)

    uhat_first.plot.contourf(
        ax=ax,
        transform=ccrs.PlateCarree(),
        add_colorbar=False,
        levels=levels,
    )
    if u_hat_last is not None:
        u_hat_last = erase_white_line(u_hat_last)
        u_hat_last.plot.contour(
            ax=ax,
            transform=ccrs.PlateCarree(),
            colors="w",
            add_colorbar=False,
            levels=levels[levels != 0],
        )
    return ax
# %%
# try read data
try:
    uhat_pos_first10 = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/jetstream_MJJAS_first10_pos.nc"
    ).ua

    uhat_neg_first10 = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/jetstream_MJJAS_first10_neg.nc"
    ).ua

    uhat_pos_last10 = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/jetstream_MJJAS_last10_pos.nc"
    ).ua

    uhat_neg_last10 = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/jetstream_MJJAS_last10_neg.nc"
    ).ua

except FileNotFoundError:
    logging.warning("Data not found, reprocessing")
    uhat_pos_first10, uhat_neg_first10 = extreme_uhat("first10")
    uhat_pos_last10, uhat_neg_last10 = extreme_uhat("last10")


    # save to netcdf
    save_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/"
    uhat_pos_first10.to_netcdf(f"{save_dir}jetstream_MJJAS_first10_pos.nc")
    uhat_neg_first10.to_netcdf(f"{save_dir}jetstream_MJJAS_first10_neg.nc")

    uhat_pos_last10.to_netcdf(f"{save_dir}jetstream_MJJAS_last10_pos.nc")
    uhat_neg_last10.to_netcdf(f"{save_dir}jetstream_MJJAS_last10_neg.nc")


# %%
uhat_climatology = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/ua_Amon_MPI-ESM1-2-LR_HIST_climatology_185005-185909.nc"
)
uhat_climatology = uhat_climatology.ua.sel(plev=slice(None, 70000)).mean(dim="plev")

uhat_climatology = uhat_climatology.sel(time=slice("1859-06-01", "1859-08-31")).mean(
    dim="time"
)
# %%
fig, axes = plt.subplots(
    1, 3, figsize=(15,6), subplot_kw={"projection": ccrs.Orthographic(-20, 60)}
)

plot_uhat(axes[0], uhat_climatology)
axes[0].set_title("Climatology")


plot_uhat(axes[1], uhat_pos_first10)
axes[1].set_title("Positive NAO")

plot_uhat(axes[2], uhat_neg_first10)
axes[2].set_title("Negative NAO")

for ax in axes:
    # Add gridlines
    gl = ax.gridlines(draw_labels=False, dms=True, x_inline=False, y_inline=False)

    # Optionally, adjust gridline appearance
    gl.xlines = True
    gl.ylines = True


plt.tight_layout(pad = 1.3)
plt.suptitle("Eddy driven Zonal Jet Stream wind Composite of first 10 years", fontsize = 16)
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/jet_stream/jet_stream_composite_first10.png")

# %%
