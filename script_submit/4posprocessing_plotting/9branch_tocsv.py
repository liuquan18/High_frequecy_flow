# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import cmocean
import os

from src.data_helper import read_composite
from src.data_helper.read_variable import read_climatology
import importlib
import matplotlib
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

from src.plotting.util import map_smooth
import src.plotting.util as util

importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var


# %%
MODEL_DIR = "MPI_GE_CMIP6_allplev"


def _read_all(var_name, suffix = '', name=None, method="no_stat", phase = 'pos', chunks=None):
    """Read pos composites for all decades, concatenated along a 'decade' dimension.

    Returns an xarray object with a new 'decade' coordinate.
    """
    kwargs = dict(time_window="all", model_dir=MODEL_DIR)
    if method is not None:
        kwargs["method"] = method
    if name is not None:
        kwargs["name"] = name
    if chunks is not None:
        kwargs["chunks"] = chunks
    kwargs["comp_path"] = "0composite_alldec"
    kwargs["erase_zero_line"] = False
    decades = np.arange(1850, 2100, 10)
    datasets = [
        read_comp_var(var_name, phase, decade, suffix=suffix, **kwargs).assign_coords(decade=decade)
        for decade in decades
    ]
    return xr.concat(datasets, dim="event")

# %%
jet_loc_pos = _read_all("jetloc_", name = 'lat', method="no_stat", phase="pos")
# %%
awb_pos = _read_all("wb_anticyclonic_allisen", name = 'smooth_pv', method="no_stat", phase="pos")
# %%
jet_loc_pos_E2M = jet_loc_pos.sel(time = slice(-5, 5)).mean(dim = 'time')
awb_pos_E2M = awb_pos.sel(time = slice(-5, 5)).mean(dim = 'time')
# %%
jet_loc_pos_M2E = jet_loc_pos.sel(time = slice(10, 20)).mean(dim = 'time')
awb_pos_M2E = awb_pos.sel(time = slice(10, 20)).mean(dim = 'time')
# %%
jet_loc_E2M_df = jet_loc_pos_E2M.to_dataframe().reset_index()
awb_E2M_df = awb_pos_E2M.to_dataframe('awb').reset_index()
# %%
jet_loc_M2E_df = jet_loc_pos_M2E.to_dataframe().reset_index()
awb_M2E_df = awb_pos_M2E.to_dataframe('awb').reset_index()
# %%
E2M_df = pd.merge(jet_loc_E2M_df, awb_E2M_df, on=['event', 'decade'])
M2E_df = pd.merge(jet_loc_M2E_df, awb_M2E_df, on=['event', 'decade'])
# %%


levels = np.arange(0.2, 1.0, 0.2)

#%%
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
# sns.scatterplot(data=E2M_df, x='lat', y='awb', ax=axes[0], size = 1)
sns.kdeplot(data=E2M_df, x='lat', y='awb', ax=axes[0], levels=levels, cmap='Reds', extend='max', linewidths=1)
# sns.scatterplot(data=M2E_df, x='lat', y='awb', ax=axes[1], size = 1)
sns.kdeplot(data=M2E_df, x='lat', y='awb', ax=axes[1], levels=levels, cmap='Reds', extend='max', linewidths=1)

axes[0].set_ylim(-0.02, 0.25)
axes[1].set_ylim(-0.02, 0.25)
axes[0].set_title('E2M')
axes[1].set_title('M2E')
# %%
import matplotlib.colors as mcolors

# --- Bin edges derived from data ---
x_bins = np.linspace(E2M_df['lat'].min(), E2M_df['lat'].max(), 50)
y_bins = np.linspace(0, max(E2M_df['awb'].max(), M2E_df['awb'].max()), 50)
x_centers = (x_bins[:-1] + x_bins[1:]) / 2
y_centers = (y_bins[:-1] + y_bins[1:]) / 2
X, Y = np.meshgrid(x_centers, y_centers)

def compute_jpdf(df, x_col, y_col, x_bins, y_bins):
    """2D histogram normalized to joint probability density."""
    H, _, _ = np.histogram2d(df[x_col], df[y_col], bins=[x_bins, y_bins], density=True)
    return np.ma.masked_where(H.T == 0, H.T)

# Compute both JPDFs and find shared color range
H_E2M = compute_jpdf(E2M_df, 'lat', 'awb', x_bins, y_bins)
H_M2E = compute_jpdf(M2E_df, 'lat', 'awb', x_bins, y_bins)

fill_levels = np.arange(0., 1, 0.1)
contour_levels = np.arange(0.2, 1, 0.2)

# --- Figure layout: 1 row x 2 cols ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True, sharex=True)

decade_colors = {1850: 'purple', 2090: 'gold'}

for ax, H, df, title in zip(axes, [H_E2M, H_M2E], [E2M_df, M2E_df], ['E2M', 'M2E']):
    pcm = ax.contourf(X, Y, H, levels=fill_levels, cmap='Reds', extend='max')
    ax.contour(X, Y, H, levels=contour_levels, colors='k', linewidths=0.7)

    for decade, color in decade_colors.items():
        df_dec = df[df['decade'] == decade]
        H_dec = compute_jpdf(df_dec, 'lat', 'awb', x_bins, y_bins)
        ax.contour(X, Y, H_dec, levels=[0.9], colors=color, linewidths=4)

    ax.set_title(title)
    ax.set_xlabel('lat')
    ax.set_ylabel('awb')
    ax.set_ylim(0., 0.2)

legend_handles = [Line2D([0], [0], color=c, linewidth=2, label=str(d))
                  for d, c in decade_colors.items()]
axes[-1].legend(handles=legend_handles, title='decade', loc='upper left')

fig.colorbar(pcm, ax=axes, label='JPDF', pad=0.02, shrink=0.8)
# plt.tight_layout()
plt.show()
# %%



