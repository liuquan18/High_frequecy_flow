#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.path as mpath
import matplotlib.ticker as mticker


from src.dynamics.EP_flux import PlotEPfluxArrows
from src.data_helper import read_composite
from src.plotting.util import erase_white_line, map_smooth
import importlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
from src.data_helper.read_variable import read_climatology
from metpy.units import units
import numpy as np
import metpy.calc as mpcalc
import src.plotting.util as util

importlib.reload(read_composite)
importlib.reload(util)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var
clip_map = util.clip_map
# %%
eke_first = read_climatology('eke',1850, name = 'eke', model_dir='MPI_GE_CMIP6')
# %%
eke_last = read_climatology('eke',2090, name = 'eke', model_dir='MPI_GE_CMIP6')
# %%
vpetp_first = read_climatology('vpetp',1850, name = 'vpetp', model_dir='MPI_GE_CMIP6_allplev')
vpetp_last = read_climatology('vpetp',2090, name = 'vpetp', model_dir='MPI_GE_CMIP6_allplev')
#%%%
# read zg'
zg_first = read_climatology('zg_steady',1850, name = 'zg', model_dir='MPI_GE_CMIP6_allplev')
zg_last = read_climatology('zg_steady',2090, name = 'zg', model_dir='MPI_GE_CMIP6_allplev')

# %%
vsets_first = read_climatology('vsets',1850, name = 'vsets', model_dir='MPI_GE_CMIP6_allplev')
vsets_last = read_climatology('vsets',2090, name = 'vsets', model_dir='MPI_GE_CMIP6_allplev')
# %%
# Compute weights as cos(lat) in radians
def coslat_weights(ds):
    lat = ds['lat']
    weights = np.cos(np.deg2rad(lat))
    # Normalize weights so they sum to 1 over the selected latitudes
    return weights / weights.sum()

# For vpetp (lat: 40 to 80)
vpetp_lat_slice = vpetp_first.sel(lat=slice(20, 60)).lat
vpetp_weights = coslat_weights(vpetp_first.sel(lat=slice(20, 60)))
vpetp_first_profile = vpetp_first.sel(lat=slice(20, 60)).weighted(vpetp_weights).mean(dim='lat')
vpetp_last_profile = vpetp_last.sel(lat=slice(20, 60)).weighted(vpetp_weights).mean(dim='lat')

# For vsets (lat: 40 to 90)
vsets_lat_slice = vsets_first.sel(lat=slice(20, 60)).lat
vsets_weights = coslat_weights(vsets_first.sel(lat=slice(40, 90)))
vsets_first_profile = vsets_first.sel(lat=slice(20, 60)).weighted(vsets_weights).mean(dim='lat')
vsets_last_profile = vsets_last.sel(lat=slice(20, 60)).weighted(vsets_weights).mean(dim='lat')
# %%
vptp_levels = np.arange(-10, 11, 2)
vsts_levels = np.arange(-10, 11, 2)

def shift_longitude(ds):
    """Shift longitude from 0-360 to -180,180."""
    if 'lon' in ds.coords:
        ds = ds.assign_coords(lon=(((ds.lon + 180) % 360) - 180))
        ds = ds.sortby('lon')
    return ds

# Shift longitude for profiles
vpetp_first_profile_shifted = shift_longitude(vpetp_first_profile)
vpetp_last_profile_shifted = shift_longitude(vpetp_last_profile)
vsets_first_profile_shifted = shift_longitude(vsets_first_profile)
vsets_last_profile_shifted = shift_longitude(vsets_last_profile)

# plot the profiles
fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
# vpetp
cf1 = vpetp_first_profile_shifted.plot.contourf(
    ax=axes[0],
    levels=vptp_levels,
    cmap='RdBu_r',
    add_colorbar=False,
    extend='both',
)
vpetp_last_profile_shifted.plot.contour(
    ax=axes[0],
    levels=[l for l in vptp_levels if l != 0],
    colors='k',
    linewidths=1,
    add_colorbar=False,
)

# vsets
cf2 = vsets_first_profile_shifted.plot.contourf(
    ax=axes[1],
    levels=vsts_levels,
    cmap='RdBu_r',
    add_colorbar=False,
    extend='both',
)
vsets_last_profile_shifted.plot.contour(
    ax=axes[1],
    levels=[l for l in vsts_levels if l != 0],
    colors='k',
    linewidths=1,
    add_colorbar=False,
)

for ax in axes:
    ax.set_ylim(100000, 10000)
    ax.set_xlim(-180, 180)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Pressure (Pa)')

# Add a colorbar at the bottom
cbar = fig.colorbar(cf1, ax=axes, orientation='horizontal', fraction=0.05, pad=0.15)
cbar.set_label(r"$v'\theta'$ (K m s$^{-1}$)", fontsize=12)
plt.tight_layout()
fig.subplots_adjust(bottom=0.25)
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eddy_heat_flux_profile.pdf",
            bbox_inches='tight', dpi=300)

# %%
eke_levels = np.arange(80, 120, 5)
zg_levels = np.arange(-100, 101, 20)
#%%
fig, axes = plt.subplots(
    1,
    2,
    figsize=(12, 6),
    subplot_kw={"projection": ccrs.Orthographic(-40, 80)},
)

for ax in axes:
    ax.coastlines(color='grey', linewidth=1)
    ax.gridlines()
    ax.set_global()

# Plot vpetp
eke_first.sel(plev = 25000).plot.contourf(
    ax=axes[0],
    levels=eke_levels,
    cmap='viridis',
    add_colorbar=True,
    extend='max',
    transform=ccrs.PlateCarree(),
    cbar_kwargs={'label': r"$eke$ (m$^2$ s$^{-2}$)", "shrink": 0.6},
)

erase_white_line(eke_last).sel(plev = 25000).plot.contour(
    ax=axes[0],
    levels=[l for l in eke_levels if l != 0],
    colors='k',
    linewidths=1,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

# plot zg
erase_white_line(zg_first).sel(plev = 25000).plot.contourf(
    ax=axes[1],
    levels=zg_levels,
    cmap='RdBu_r',
    add_colorbar=True,
    extend='both',
    transform=ccrs.PlateCarree(),
    cbar_kwargs={'label': r"zg (m)", "shrink": 0.6},
)
erase_white_line(zg_last).sel(plev = 25000).plot.contour(
    ax=axes[1],
    levels=[l for l in zg_levels if l != 0],
    colors='k',
    linewidths=1,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
axes[0].set_title("")
axes[1].set_title("")

# add a, b
axes[0].text(0.1, 1., "a", transform=axes[0].transAxes, fontsize=16, fontweight='bold')
axes[1].text(0.1, 1., "b", transform=axes[1].transAxes, fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eke_zg_250hPa.pdf",
            bbox_inches='tight', dpi=300)
# %%
