
# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.path as mpath
import matplotlib.ticker as mticker
import matplotlib.ticker as ticker


from src.dynamics.EP_flux import PlotEPfluxArrows
from src.data_helper import read_composite
from src.plotting.util import erase_white_line, map_smooth, NA_box
import importlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
from src.data_helper.read_variable import read_climatology, read_climatology_decmean
from metpy.units import units
import numpy as np
import os
import cartopy
from matplotlib.patches import Rectangle
from shapely.geometry import Polygon
from matplotlib.ticker import FuncFormatter
import metpy.calc as mpcalc
import src.plotting.util as util

importlib.reload(read_composite)
importlib.reload(util)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var
clip_map = util.clip_map
# %%
awb_pos_first = read_comp_var('wb_anticyclonic', 'pos', 1850, time_window=(-10, 5), method='sum', name = 'flag', model_dir = 'MPI_GE_CMIP6_allplev')
awb_neg_first = read_comp_var('wb_anticyclonic', 'neg', 1850, time_window=(-10, 5), method='sum', name = 'flag', model_dir = 'MPI_GE_CMIP6_allplev')
# %%
awb_pos_last = read_comp_var('wb_anticyclonic', 'pos', 2090, time_window=(-10, 5), method='sum', name = 'flag', model_dir = 'MPI_GE_CMIP6_allplev')
awb_neg_last = read_comp_var('wb_anticyclonic', 'neg', 2090, time_window=(-10, 5), method='sum', name = 'flag', model_dir = 'MPI_GE_CMIP6_allplev')
# %%
cwb_pos_first = read_comp_var('wb_cyclonic', 'pos', 1850, time_window=(-10, 5), method='sum', name = 'flag', model_dir = 'MPI_GE_CMIP6_allplev')
cwb_neg_first = read_comp_var('wb_cyclonic', 'neg', 1850, time_window=(-10, 5), method='sum', name = 'flag', model_dir = 'MPI_GE_CMIP6_allplev')
cwb_pos_last = read_comp_var('wb_cyclonic', 'pos', 2090, time_window=(-10, 5), method='sum', name = 'flag', model_dir = 'MPI_GE_CMIP6_allplev')
cwb_neg_last = read_comp_var('wb_cyclonic', 'neg', 2090, time_window=(-10, 5), method='sum', name = 'flag', model_dir = 'MPI_GE_CMIP6_allplev')

# #%%
# # divided by 50 ensemble members
# awb_pos_first = awb_pos_first / 50
# awb_neg_first = awb_neg_first / 50
# awb_pos_last = awb_pos_last / 50
# awb_neg_last = awb_neg_last / 50

# cwb_pos_first = cwb_pos_first / 50
# cwb_neg_first = cwb_neg_first / 50
# cwb_pos_last = cwb_pos_last / 50
# cwb_neg_last = cwb_neg_last / 50
#%%
# smooth the data
awb_pos_first = map_smooth(awb_pos_first, lon_win = 3, lat_win = 3)
awb_neg_first = map_smooth(awb_neg_first, lon_win = 3, lat_win = 3)
awb_pos_last = map_smooth(awb_pos_last, lon_win = 3, lat_win = 3)
awb_neg_last = map_smooth(awb_neg_last, lon_win = 3, lat_win = 3)

cwb_pos_first = map_smooth(cwb_pos_first, lon_win = 5, lat_win = 5)
cwb_neg_first = map_smooth(cwb_neg_first, lon_win = 5, lat_win = 5)
cwb_pos_last = map_smooth(cwb_pos_last, lon_win = 5, lat_win = 5)
cwb_neg_last = map_smooth(cwb_neg_last, lon_win = 5, lat_win = 5)
# %%
awb_diff_first = awb_pos_first - awb_neg_first
awb_diff_last = awb_pos_last - awb_neg_last
cwb_diff_first = cwb_pos_first - cwb_neg_first
cwb_diff_last = cwb_pos_last - cwb_neg_last
# %%
def add_sector_polygon(ax, lat_min=30, lat_max=80, lon_min=-60, lon_max=30, color='yellow'):
    
    # add sector polygon with smooth latitude circle (lat 30-80, lon -60 to 30)
    lons = np.linspace(lon_min, lon_max, 100)
    lats_north = np.full_like(lons, lat_max)
    lats_south = np.full_like(lons, lat_min)

    # upper edge (lat=80, lon -60 to 30), lower edge (lat=30, lon 30 to -60)
    poly_lons = np.concatenate([lons, lons[::-1]])
    poly_lats = np.concatenate([lats_north, lats_south[::-1]])

    sector_polygon = Polygon(np.column_stack([poly_lons, poly_lats]))
    ax.add_geometries([sector_polygon], crs=ccrs.PlateCarree(),
                            facecolor='none', edgecolor=color, linewidth=2,
                            linestyle='--', label='Sector')

#%%
awb_levels = np.arange(-50., 50.1, 5) # for contourf
awb_levels_div = np.arange(-50., 50.1, 5)  # for difference
cwb_levels = np.arange(-40., 40.1, 5) 
cwb_levels_div = np.arange(-40., 40.1, 5)  # for difference

#%%
fig, axes = plt.subplots(
    nrows=2, ncols=3, figsize=(10, 8),
    subplot_kw={"projection": ccrs.Orthographic(central_longitude=-60, central_latitude=70)},
    constrained_layout=True,
)

# --- First row: uhat (jet stream) ---
# positive phase, first decade in contourf
cf_hat_pos_first = awb_pos_first.plot.contourf(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap='RdBu_r',
    add_colorbar=True,
    extend='both',
    levels=awb_levels,
    cbar_kwargs={
        'label': 'AWB (days)',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.05,
        'aspect':30,
       'format': '%.0f'
    }
)

# last decade in contour
cf_hat_pos_last = awb_pos_last.plot.contour(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
    extend='both',
    linewidths=1,
    colors='black',
    levels=[l for l in awb_levels if l != 0],  # exclude zero
)

# negative phase, first decade in contourf
cf_hat_neg_first = awb_neg_first.plot.contourf(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap='RdBu_r',
    add_colorbar=True,
    extend='both',
    levels=awb_levels,
    cbar_kwargs={
        'label': 'AWB (days)',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.05,
        'aspect':30,
       'format': '%.0f'
    }
)
# last decade in contour
cf_hat_neg_last = awb_neg_last.plot.contour(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
    extend='both',
    linewidths=1,
    colors='black',
    levels=[l for l in awb_levels if l != 0],  # exclude zero
)   

# difference, first decade in contourf
cf_hat_diff_first = awb_diff_first.plot.contourf(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap='RdBu_r',
    add_colorbar=True,
    extend='both',
    levels=awb_levels_div,
    cbar_kwargs={
        'label': r'$\Delta$ AWB (days)',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.05,
        'aspect':30,
       'format': '%.0f'
    }
)
# last decade in contour
cf_hat_diff_last = awb_diff_last.plot.contour(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
    extend='both',
    linewidths=1,
    colors='black',
    levels=[l for l in awb_levels_div if l != 0],  # exclude zero
)
# --- Second row: baroclinicity (eddy growth rate) ---

# positive phase, first decade in contourf
cf_cwb_pos_first = cwb_pos_first.plot.contourf(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap='RdBu_r',
    add_colorbar=True,
    extend='both',
    levels=cwb_levels,
    cbar_kwargs={
        'label': 'CWB (days)',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.05,
        'aspect':30,
       'format': '%.0f'
    }
)

# last decade in contour
cf_cwb_pos_last = cwb_pos_last.plot.contour(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
    extend='both',
    linewidths=1,
    colors='black',
    levels=[l for l in cwb_levels if l != 0],  # exclude zero
)

# negative phase, first decade in contourf
cf_cwb_neg_first = cwb_neg_first.plot.contourf(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap='RdBu_r',
    add_colorbar=True,
    extend='both',
    levels=cwb_levels,
    cbar_kwargs={
        'label': 'CWB (days)',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.05,
        'aspect':30,
       'format': '%.0f'
    }
)

# last decade in contour
cf_cwb_neg_last = cwb_neg_last.plot.contour(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
    extend='both',
    linewidths=1,
    colors='black',
    levels=[l for l in cwb_levels if l != 0],  # exclude zero
)
# difference, first decade in contourf
cf_cwb_diff_first = cwb_diff_first.plot.contourf(       
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap='RdBu_r',
    add_colorbar=True,
    extend='both',
    levels=cwb_levels_div,
    cbar_kwargs={
        'label': r'$\Delta$ CWB (days)',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.05,
        'aspect':30,
       'format': '%.0f'
    }
)



# last decade in contour
cf_cwb_diff_last = cwb_diff_last.plot.contour(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
    extend='both',
    linewidths=1,
    colors='black',
    levels=[l for l in cwb_levels_div if l != 0],  # exclude zero
)

add_sector_polygon(axes[0, 2], lat_min=30, lat_max=70, lon_min=-60, lon_max=30, color='purple')
add_sector_polygon(axes[1, 2], lat_min=45, lat_max=75, lon_min=-100, lon_max=-30, color='purple')


# --- Formatting ---
for i, ax in enumerate(axes.flatten()):
    ax.coastlines(color="grey", linewidth=1)
    ax.gridlines(draw_labels=False, linewidth=1, color="grey", alpha=0.5, linestyle="--")
    # Set extent: [west_lon, east_lon, south_lat, north_lat]
    ax.set_global()
    ax.set_extent([-150, 30, 10, 90], crs=ccrs.PlateCarree())
    ax.set_global()
    ax.set_title("")
    # add a, b, c labels
    ax.text(0.1, 0.98, chr(97 + i),
            transform=ax.transAxes, fontsize=14, fontweight='bold',
            va='top', ha='right',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    # clip_map(ax, 180, 360, 0, 180)  # clip the map to the sector


# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0mean_flow/wave_breaking_comp_ano.pdf",
#             bbox_inches='tight', dpi=300, transparent=True)

# %%
