
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
# change from lon 0-360 to -180 to 180
ua_pos_first = util.lon360to180(ua_pos_first)
ua_neg_first = util.lon360to180(ua_neg_first)
ua_pos_last = util.lon360to180(ua_pos_last)
ua_neg_last = util.lon360to180(ua_neg_last)
ua_diff_first = util.lon360to180(ua_diff_first)
ua_diff_last = util.lon360to180(ua_diff_last)

baroc_pos_first = util.lon360to180(baroc_pos_first)
baroc_neg_first = util.lon360to180(baroc_neg_first)
baroc_pos_last = util.lon360to180(baroc_pos_last)
baroc_neg_last = util.lon360to180(baroc_neg_last)
baroc_diff_first = util.lon360to180(baroc_diff_first)
baroc_diff_last = util.lon360to180(baroc_diff_last)
# %%
# zonal mean 
ua_pos_first_zm = ua_pos_first.sel(lon = slice(-120, 60)).mean(dim="lon")
ua_neg_first_zm = ua_neg_first.sel(lon = slice(-120, 60)).mean(dim="lon")
ua_pos_last_zm = ua_pos_last.sel(lon = slice(-120, 60)).mean(dim="lon")
ua_neg_last_zm = ua_neg_last.sel(lon = slice(-120, 60)).mean(dim="lon")
ua_diff_first_zm = ua_diff_first.sel(lon = slice(-120, 60)).mean(dim="lon")
ua_diff_last_zm = ua_diff_last.sel(lon = slice(-120, 60)).mean(dim="lon")
# %%
baroc_pos_first_zm = baroc_pos_first.sel(lon = slice(-120, 0)).mean(dim="lon")
baroc_neg_first_zm = baroc_neg_first.sel(lon = slice(-120, 0)).mean(dim="lon")
baroc_pos_last_zm = baroc_pos_last.sel(lon = slice(-120, 0)).mean(dim="lon")
baroc_neg_last_zm = baroc_neg_last.sel(lon = slice(-120, 0)).mean(dim="lon")
baroc_diff_first_zm = baroc_diff_first.sel(lon = slice(-120, 0)).mean(dim="lon")
baroc_diff_last_zm = baroc_diff_last.sel(lon = slice(-120, 0)).mean(dim="lon")

# %%
# calculate the data and load the data for plotting
ua_pos_first_zm = ua_pos_first_zm.compute()
ua_neg_first_zm = ua_neg_first_zm.compute()
ua_pos_last_zm = ua_pos_last_zm.compute()
ua_neg_last_zm = ua_neg_last_zm.compute()
ua_diff_first_zm = ua_diff_first_zm.compute()
ua_diff_last_zm = ua_diff_last_zm.compute()
# %%
baroc_pos_first_zm = baroc_pos_first_zm.compute()
baroc_neg_first_zm = baroc_neg_first_zm.compute()
baroc_pos_last_zm = baroc_pos_last_zm.compute()
baroc_neg_last_zm = baroc_neg_last_zm.compute()
baroc_diff_first_zm = baroc_diff_first_zm.compute()
baroc_diff_last_zm = baroc_diff_last_zm.compute()
#%%
# only northern hemisphere
ua_pos_first_zm = ua_pos_first_zm.sel(lat = slice(0,90))
ua_neg_first_zm = ua_neg_first_zm.sel(lat = slice(0,90))
ua_pos_last_zm = ua_pos_last_zm.sel(lat = slice(0,90))
ua_neg_last_zm = ua_neg_last_zm.sel(lat = slice(0,90))
ua_diff_first_zm = ua_diff_first_zm.sel(lat = slice(0,90))
ua_diff_last_zm = ua_diff_last_zm.sel(lat = slice(0,90))

baroc_pos_first_zm = baroc_pos_first_zm.sel(lat = slice(0,90))
baroc_neg_first_zm = baroc_neg_first_zm.sel(lat = slice(0,90))
baroc_pos_last_zm = baroc_pos_last_zm.sel(lat = slice(0,90))
baroc_neg_last_zm = baroc_neg_last_zm.sel(lat = slice(0,90))
baroc_diff_first_zm = baroc_diff_first_zm.sel(lat = slice(0,90))
baroc_diff_last_zm = baroc_diff_last_zm.sel(lat = slice(0,90))

# %%
# Quick check plots
fig, axes = plt.subplots(2, 3, figsize=(15, 8))

# First row: ua (jet)
# Column 1: Positive
axes[0, 0].plot(ua_pos_first_zm, ua_pos_first_zm.lat, 'k-', label='First', linewidth=2)
axes[0, 0].plot(ua_pos_last_zm, ua_pos_last_zm.lat, 'k--', label='Last', linewidth=2)
axes[0, 0].set_ylabel('Latitude')
axes[0, 0].set_xlabel('UA (m/s)')
axes[0, 0].set_title('UA - Positive')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].legend()

# Column 2: Negative
axes[0, 1].plot(ua_neg_first_zm, ua_neg_first_zm.lat, 'k-', label='First', linewidth=2)
axes[0, 1].plot(ua_neg_last_zm, ua_neg_last_zm.lat, 'k--', label='Last', linewidth=2)
axes[0, 1].set_ylabel('Latitude')
axes[0, 1].set_xlabel('UA (m/s)')
axes[0, 1].set_title('UA - Negative')
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].legend()

# Column 3: Difference
axes[0, 2].plot(ua_diff_first_zm, ua_diff_first_zm.lat, 'k-', label='First', linewidth=2)
axes[0, 2].plot(ua_diff_last_zm, ua_diff_last_zm.lat, 'k--', label='Last', linewidth=2)
axes[0, 2].axvline(0, color='gray', linestyle=':', alpha=0.5)
axes[0, 2].set_ylabel('Latitude')
axes[0, 2].set_xlabel('UA (m/s)')
axes[0, 2].set_title('UA - Difference (Pos - Neg)')
axes[0, 2].grid(True, alpha=0.3)
axes[0, 2].legend()

# Second row: baroclinicity
# Column 1: Positive
axes[1, 0].plot(baroc_pos_first_zm, baroc_pos_first_zm.lat, 'k-', label='First', linewidth=2)
axes[1, 0].plot(baroc_pos_last_zm, baroc_pos_last_zm.lat, 'k--', label='Last', linewidth=2)
axes[1, 0].set_ylabel('Latitude')
axes[1, 0].set_xlabel('Baroclinicity (day⁻¹)')
axes[1, 0].set_title('Baroclinicity - Positive')
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].legend()

# Column 2: Negative
axes[1, 1].plot(baroc_neg_first_zm, baroc_neg_first_zm.lat, 'k-', label='First', linewidth=2)
axes[1, 1].plot(baroc_neg_last_zm, baroc_neg_last_zm.lat, 'k--', label='Last', linewidth=2)
axes[1, 1].set_ylabel('Latitude')
axes[1, 1].set_xlabel('Baroclinicity (day⁻¹)')
axes[1, 1].set_title('Baroclinicity - Negative')
axes[1, 1].grid(True, alpha=0.3)
axes[1, 1].legend()

# Column 3: Difference
axes[1, 2].plot(baroc_diff_first_zm, baroc_diff_first_zm.lat, 'k-', label='First', linewidth=2)
axes[1, 2].plot(baroc_diff_last_zm, baroc_diff_last_zm.lat, 'k--', label='Last', linewidth=2)
axes[1, 2].axvline(0, color='gray', linestyle=':', alpha=0.5)
axes[1, 2].set_ylabel('Latitude')
axes[1, 2].set_xlabel('Baroclinicity (day⁻¹)')
axes[1, 2].set_title('Baroclinicity - Difference (Pos - Neg)')
axes[1, 2].grid(True, alpha=0.3)
axes[1, 2].legend()

plt.tight_layout()
plt.show()
# %%
# New plot: Difference data with horizontal bar plot showing change
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# First column: UA difference
ax1 = axes[0]
# Plot the difference lines
ax1.plot(ua_diff_first_zm, ua_diff_first_zm.lat, 'k-', label='1850', linewidth=2)
ax1.plot(ua_diff_last_zm, ua_diff_last_zm.lat, 'k--', label='2090', linewidth=2)
ax1.axvline(0, color='gray', linestyle=':', alpha=0.5)
ax1.set_ylabel('Latitude')
ax1.set_xlabel('UA Difference (m/s)')
ax1.set_title('UA (Pos - Neg)')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Create horizontal bar plot on the right side
ax1_bar = ax1.twiny()
ua_change = ua_diff_last_zm - ua_diff_first_zm
ax1_bar.barh(ua_change.lat, ua_change, height=2, alpha=0.3, color='red', label='Change (2090-1850)')
ax1_bar.set_xlabel('Change in UA Difference (m/s)', color='red')
ax1_bar.tick_params(axis='x', labelcolor='red')
# Set bar plot limits to half of line plot limits
ax1_lim = ax1.get_xlim()
ax1_bar.set_xlim(ax1_lim[0] / 2, ax1_lim[1] / 2)
ax1_bar.axvline(0, color='gray', linestyle=':', alpha=0.5)

# Second column: Baroclinicity difference
ax2 = axes[1]
# Plot the difference lines
ax2.plot(baroc_diff_first_zm, baroc_diff_first_zm.lat, 'k-', label='1850', linewidth=2)
ax2.plot(baroc_diff_last_zm, baroc_diff_last_zm.lat, 'k--', label='2090', linewidth=2)
ax2.axvline(0, color='gray', linestyle=':', alpha=0.5)
ax2.set_ylabel('Latitude')
ax2.set_xlabel('Baroclinicity Difference (day⁻¹)')
ax2.set_title('Baroclinicity (Pos - Neg)')
ax2.grid(True, alpha=0.3)
ax2.legend()

# Create horizontal bar plot on the right side
ax2_bar = ax2.twiny()
baroc_change = baroc_diff_last_zm - baroc_diff_first_zm
ax2_bar.barh(baroc_change.lat, baroc_change, height=2, alpha=0.3, color='red', label='Change (2090-1850)')
ax2_bar.set_xlabel('Change in Baroclinicity Difference (day⁻¹)', color='red')
ax2_bar.tick_params(axis='x', labelcolor='red')
# Set bar plot limits to half of line plot limits
ax2_lim = ax2.get_xlim()
ax2_bar.set_xlim(ax2_lim[0] / 2, ax2_lim[1] / 2)
ax2_bar.axvline(0, color='gray', linestyle=':', alpha=0.5)

plt.tight_layout()
plt.show()
# %%
