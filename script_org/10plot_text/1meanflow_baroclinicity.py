
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
ua_pos_first = read_comp_var('ua', 'pos', 1850, time_window=(-10, 5), method='mean', name = 'ua', model_dir = 'MPI_GE_CMIP6_allplev')
ua_neg_first = read_comp_var('ua', 'neg', 1850, time_window=(-10, 5), method='mean', name = 'ua', model_dir = 'MPI_GE_CMIP6_allplev')
# %%
ua_pos_last = read_comp_var('ua', 'pos', 2090, time_window=(-10, 5), method='mean', name = 'ua', model_dir = 'MPI_GE_CMIP6_allplev')
ua_neg_last = read_comp_var('ua', 'neg', 2090, time_window=(-10, 5), method='mean', name = 'ua', model_dir = 'MPI_GE_CMIP6_allplev')
# %%
baroc_pos_first = read_comp_var('eady_growth_rate', 'pos', 1850, time_window=(-10, 5), method='mean', name = 'eady_growth_rate', model_dir = 'MPI_GE_CMIP6_allplev')
baroc_neg_first = read_comp_var('eady_growth_rate', 'neg', 1850, time_window=(-10, 5), method='mean', name = 'eady_growth_rate', model_dir = 'MPI_GE_CMIP6_allplev')
baroc_pos_last = read_comp_var('eady_growth_rate', 'pos', 2090, time_window=(-10, 5), method='mean', name = 'eady_growth_rate', model_dir = 'MPI_GE_CMIP6_allplev')
baroc_neg_last = read_comp_var('eady_growth_rate', 'neg', 2090, time_window=(-10, 5), method='mean', name = 'eady_growth_rate', model_dir = 'MPI_GE_CMIP6_allplev')
#%%
# baroclinicity from s-1 to day-1
baroc_pos_first = baroc_pos_first * 86400
baroc_neg_first = baroc_neg_first * 86400
baroc_pos_last = baroc_pos_last * 86400
baroc_neg_last = baroc_neg_last * 86400



# %%
# ua select 25000
ua_pos_first = ua_pos_first.sel(plev=25000)
ua_neg_first = ua_neg_first.sel(plev=25000)
ua_pos_last = ua_pos_last.sel(plev=25000)
ua_neg_last = ua_neg_last.sel(plev=25000)
# %%
# baroc select 85000
baroc_pos_first = baroc_pos_first.sel(plev=85000)
baroc_neg_first = baroc_neg_first.sel(plev=85000)
baroc_pos_last = baroc_pos_last.sel(plev=85000)
baroc_neg_last = baroc_neg_last.sel(plev=85000)

#%%
# smooth the baroc
baroc_pos_first = map_smooth(baroc_pos_first, 5, 5)
baroc_neg_first = map_smooth(baroc_neg_first, 5, 5)
baroc_pos_last = map_smooth(baroc_pos_last, 5, 5)
baroc_neg_last = map_smooth(baroc_neg_last, 5, 5)
# %%
ua_diff_first = ua_pos_first - ua_neg_first
ua_diff_last = ua_pos_last - ua_neg_last
baroc_diff_first = baroc_pos_first - baroc_neg_first
baroc_diff_last = baroc_pos_last - baroc_neg_last
# %%
uhat_levels = np.arange(-30, 31, 5)
uhat_levels_div = np.arange(-15, 16, 3)  # for difference
baroc_levels = np.arange(-8, 8.1, 1) 
baroc_levels_div = np.arange(-3, 3, 0.5)  # for difference

#%%
fig, axes = plt.subplots(
    nrows=2, ncols=3, figsize=(10, 8),
    subplot_kw={"projection": ccrs.Orthographic(-30, 70)},
    constrained_layout=True,
)
# --- First row: uhat (jet stream) ---
# positive phase, first decade in contourf
cf_hat_pos_first = ua_pos_first.plot.contourf(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap='RdBu_r',
    add_colorbar=True,
    extend='both',
    levels=uhat_levels,
    cbar_kwargs={
        'label': r'$\overline{u}$ (ms$^{-1}$)',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.05,
        'aspect':30,
        'format': '%.0f'
    }
)

# last decade in contour
cf_hat_pos_last = ua_pos_last.plot.contour(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
    extend='both',
    linewidths=1,
    colors='black',
    levels=[l for l in uhat_levels if l != 0],  # exclude zero
)

# negative phase, first decade in contourf
cf_hat_neg_first = ua_neg_first.plot.contourf(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap='RdBu_r',
    add_colorbar=True,
    extend='both',
    levels=uhat_levels,
    cbar_kwargs={
        'label': r'$\overline{u}$ (ms$^{-1}$)',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.05,
        'aspect':30,
        'format': '%.0f'
    }
)
# last decade in contour
cf_hat_neg_last = ua_neg_last.plot.contour(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
    extend='both',
    linewidths=1,
    colors='black',
    levels=[l for l in uhat_levels if l != 0],  # exclude zero
)   

# difference, first decade in contourf
cf_hat_diff_first = ua_diff_first.plot.contourf(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap='RdBu_r',
    add_colorbar=True,
    extend='both',
    levels=uhat_levels_div,
    cbar_kwargs={
        'label': r'$\Delta\overline{u}$ (ms$^{-1}$)',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.05,
        'aspect':30,
        'format': '%.0f'
    }
)
# last decade in contour
cf_hat_diff_last = ua_diff_last.plot.contour(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
    extend='both',
    linewidths=1,
    colors='black',
    levels=[l for l in uhat_levels_div if l != 0],  # exclude zero
)
# --- Second row: baroclinicity (eddy growth rate) ---

# positive phase, first decade in contourf
cf_baroc_pos_first = baroc_pos_first.plot.contourf(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    cmap='RdBu_r',
    add_colorbar=True,
    extend='both',
    levels=baroc_levels,
    cbar_kwargs={
        'label': r'Eady growth rate (day$^{-1}$)',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.05,
        'aspect':30,
        'format': '%.0f'
    }
)

# last decade in contour
cf_baroc_pos_last = baroc_pos_last.plot.contour(
    ax=axes[1, 0],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
    extend='both',
    linewidths=1,
    colors='black',
    levels=[l for l in baroc_levels if l != 0],  # exclude zero
)

# negative phase, first decade in contourf
cf_baroc_neg_first = baroc_neg_first.plot.contourf(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    cmap='RdBu_r',
    add_colorbar=True,
    extend='both',
    levels=baroc_levels,
    cbar_kwargs={
        'label': r'Eady growth rate (day$^{-1}$)',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.05,
        'aspect':30,
        'format': '%.0f'
    }
)

# last decade in contour
cf_baroc_neg_last = baroc_neg_last.plot.contour(
    ax=axes[1, 1],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
    extend='both',
    linewidths=1,
    colors='black',
    levels=[l for l in baroc_levels if l != 0],  # exclude zero
)
# difference, first decade in contourf
cf_baroc_diff_first = baroc_diff_first.plot.contourf(       
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    cmap='RdBu_r',
    add_colorbar=True,
    extend='both',
    levels=baroc_levels_div,
    cbar_kwargs={
        'label': r'$\Delta$ Eady growth rate (day$^{-1}$)',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.05,
        'aspect':30,
        'format': '%.0f'
    }
)

# last decade in contour
cf_baroc_diff_last = baroc_diff_last.plot.contour(
    ax=axes[1, 2],
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
    extend='both',
    linewidths=1,
    colors='black',
    levels=[l for l in baroc_levels_div if l != 0],  # exclude zero
)

# --- Formatting ---
for i, ax in enumerate(axes.flatten()):
    ax.coastlines(color="grey", linewidth=1)
    ax.gridlines(draw_labels=False, linewidth=1, color="grey", alpha=0.5, linestyle="--")
    ax.set_global()
    ax.set_title("")
    # add a, b, c labels
    ax.text(0.1, 0.98, chr(97 + i),
            transform=ax.transAxes, fontsize=14, fontweight='bold',
            va='top', ha='right',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0mean_flow/upper_jet_lower_baroclinicity.pdf",
            bbox_inches='tight', dpi=300, transparent=True)

    # %%
