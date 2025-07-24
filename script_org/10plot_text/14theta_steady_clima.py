#%%
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.data_helper.read_variable import read_climatology

#%%
from src.plotting.util import map_smooth

# %%
zg_first = read_climatology("zg_steady", 1850, plev=25000, name="zg")
zg_last = read_climatology("zg_steady", 2090, plev=25000, name="zg")
# %%
# smooth the data
zg_first = map_smooth(zg_first, lon_win = 7, lat_win=3)
zg_last = map_smooth(zg_last, lon_win = 7, lat_win=3)

#%%
theta_first = read_climatology("theta_hat", 1850, plev=85000, name="theta") # remove zonal mean to get zonal anomaly
theta_last = read_climatology("theta_hat", 2090, plev=85000, name="theta")
# %%
theta_first = map_smooth(theta_first, lon_win = 7, lat_win=3)
theta_last = map_smooth(theta_last, lon_win = 7, lat_win=3)
#%%
theta_first = theta_first - theta_first.mean(dim="lon")
theta_last = theta_last - theta_last.mean(dim="lon")
#%%
etheta_first = read_climatology("equiv_theta_hat", 1850, plev=85000, name="etheta")
etheta_last = read_climatology("equiv_theta_hat", 2090, plev=85000, name="etheta")
# %%
etheta_first = map_smooth(etheta_first, lon_win = 7, lat_win=3)
etheta_last = map_smooth(etheta_last, lon_win = 7, lat_win=3)

etheta_first = etheta_first - etheta_first.mean(dim="lon")
etheta_last = etheta_last - etheta_last.mean(dim="lon")

#%%
# meridional mean
def meri_mean(zg_first, zg_last, lat_slice=slice(50, 70)):
    zg_first_mm = zg_first.sel(lat = lat_slice).mean(dim="lat")
    zg_last_mm = zg_last.sel(lat = lat_slice).mean(dim="lat")

    # change the longitude from 0-360 to -180 to 180
    zg_first_mm = zg_first_mm.assign_coords(lon=((zg_first_mm.lon + 180) % 360) - 180)
    zg_last_mm = zg_last_mm.assign_coords(lon=((zg_last_mm.lon + 180) % 360) - 180)
    
    # sort the longitude
    zg_first_mm = zg_first_mm.sortby("lon")
    zg_last_mm = zg_last_mm.sortby("lon")
    return zg_first_mm, zg_last_mm
#%%
zg_first_mm, zg_last_mm = meri_mean(zg_first, zg_last)
theta_first_mm, theta_last_mm = meri_mean(theta_first, theta_last)
etheta_first_mm, etheta_last_mm = meri_mean(etheta_first, etheta_last)
# %%
fig, axes = plt.subplots(
    1, 3, figsize = (10, 4))



# theta at 850 hPa
theta_first_mm.plot.line(
    ax=axes[0],
    x = 'lon',
    color = 'k',
    label = "1850s",
)
theta_last_mm.plot.line(
    ax=axes[0],
    x = 'lon',
    linestyle = '--',
    color = 'k',
    label = "2090s",
)
# equivalent potential temperature at 850 hPa
etheta_first_mm.plot.line(
    ax=axes[1],
    x = 'lon',
    color = 'k',
    label = "1850s",
)
etheta_last_mm.plot.line(
    ax=axes[1], 
    x = 'lon',
    linestyle = '--',
    color = 'k',
    label = "2090s",
)

# zg at 250 hPa
zg_first_mm.plot.line(
    ax=axes[2],
    x = 'lon',
    color = 'k',
    label = "1850s",
)
zg_last_mm.plot.line(
    ax=axes[2],
    x = 'lon',
    linestyle = '--',
    color = 'k',
    label = "2090s",
)


axes[0].set_title("")
axes[0].set_ylabel(r"$\overline{\theta}$ at 850 hPa (K)")
axes[1].set_title("")
axes[1].set_ylabel(r"$\overline{\theta}_e$ at 850 hPa (K)")
axes[2].set_title("")
axes[2].set_ylabel(r"$\overline{zg}$ at 250 hPa (m)")



# remove the top and right spines
for i, ax in enumerate(axes):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel("Longitude")
    ax.legend()
    ax.text(0.02, 0.98, f"{chr(97 + i)}", transform=ax.transAxes, fontsize=12, va='top', fontweight='bold')

    # leggend at bottom right
    ax.legend(loc='lower right', fontsize=10)

    # label x-tick every 60 degrees
    ax.set_xticks(np.arange(-180, 181, 90))

# vertical text "North Atlantic" at x = -50
axes[0].text(0.43, 0.7, "North Atlantic", transform=axes[0].transAxes, fontsize=10, va='center', ha='right', rotation=90)
axes[0].text(0.73, 0.4, "Eurasia", transform=axes[0].transAxes, fontsize=10, va='center', ha='right', rotation=90)



plt.tight_layout()


# save fig
plt.savefig(
"/work/mh0033/m300883/High_frequecy_flow/docs/plots/0mean_flow/theta_zg_steady_clima.pdf",
            bbox_inches='tight',
            dpi=300)
# %%
