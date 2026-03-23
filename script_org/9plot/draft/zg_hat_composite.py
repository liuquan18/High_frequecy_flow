# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import seaborn.objects as so

from src.data_helper import read_composite
from src.data_helper.read_variable import read_climatology
import importlib
import matplotlib
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var
# %%
steady_pos_first = read_comp_var(
    "zg_steady",
    "pos",
    1850,
    time_window=(0, 10),
    name="zg",
    model_dir = 'MPI_GE_CMIP6_allplev'
)
# %%
steady_neg_first = read_comp_var(
    "zg_steady",
    "neg",
    1850,
    time_window=(0, 10),
    name="zg",
    model_dir = 'MPI_GE_CMIP6_allplev'
)
# %%
steady_pos_last = read_comp_var(
    "zg_steady",
    "pos",
    2090,
    time_window=(0, 10),
    name="zg",
    model_dir = 'MPI_GE_CMIP6_allplev'
)

steady_neg_last = read_comp_var(
    "zg_steady",
    "neg",
    2090,
    time_window=(0, 10),
    name="zg",
    model_dir = 'MPI_GE_CMIP6_allplev'
)
# %%
pos_first_850 = steady_pos_first.sel(plev=85000, method="nearest")
neg_first_850 = steady_neg_first.sel(plev=85000, method="nearest")
diff_first_850 = pos_first_850 - neg_first_850

pos_last_850 = steady_pos_last.sel(plev=85000, method="nearest")
neg_last_850 = steady_neg_last.sel(plev=85000, method="nearest")
diff_last_850 = pos_last_850 - neg_last_850
# %%
levels = np.arange(-100, 101, 20)
contour_levels = levels[levels != 0]
#%%
fig, axes = plt.subplots(
    nrows=1,
    ncols=3,
    figsize=(8, 4),
    subplot_kw={"projection": ccrs.Orthographic(-30, 70)},
    constrained_layout=True,
)

pos_map = pos_first_850.plot.contourf(
    ax=axes[0],
    levels=levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
neg_map = neg_first_850.plot.contourf(
    ax=axes[1],
    levels=levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

diff_map = diff_first_850.plot.contourf(
    ax=axes[2],
    levels=levels,
    cmap="RdBu_r",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

pos_first_850.plot.contour(
    ax=axes[0],
    levels=contour_levels,
    colors="k",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
neg_first_850.plot.contour(
    ax=axes[1],
    levels=contour_levels,
    colors="k",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
diff_first_850.plot.contour(
    ax=axes[2],
    levels=contour_levels,
    colors="k",
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
# --- Formatting ---
for i, ax in enumerate(axes.flatten()):
    ax.coastlines(color="grey", linewidth=1)
    ax.gridlines(
        draw_labels=False, linewidth=1, color="grey", alpha=0.5, linestyle="--"
    )
    ax.set_global()
    ax.set_title("")


#%%
lat_target = 40


def prep_lon_plev_section(da, lat_value=40):
    section = da.sel(lat=lat_value, method="nearest")

    # If extra dimensions exist, average them to keep a clean lon-plev section.
    extra_dims = [d for d in section.dims if d not in ["plev", "lon"]]
    if extra_dims:
        section = section.mean(dim=extra_dims)

    if (section.lon > 180).any():
        section = section.assign_coords(lon=((section.lon + 180) % 360) - 180).sortby("lon")

    # smooth
    section_rolling = xr.concat([section, section], dim="lon").rolling(lon=20, center=True).mean()
    section_rolling = section_rolling.isel(lon=slice(section.lon.size, 2 * section.lon.size)).sortby("lon")
    return section_rolling

#%%
pos_first = prep_lon_plev_section(steady_pos_first, lat_value=lat_target)
neg_first = prep_lon_plev_section(steady_neg_first, lat_value=lat_target)
diff_first = pos_first - neg_first
#%%
pos_last = prep_lon_plev_section(steady_pos_last, lat_value=lat_target)
neg_last = prep_lon_plev_section(steady_neg_last, lat_value=lat_target)
diff_last = pos_last - neg_last
#%%
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

im_pos = pos_first.plot.contourf(
    ax=axes[0],
    levels=levels,
    cmap="RdBu_r",
    add_colorbar=False,
)
im_neg = neg_first.plot.contourf(
    ax=axes[1],
    levels=levels,
    cmap="RdBu_r",
    add_colorbar=False,
)

im_diff = diff_first.plot.contourf(
    ax=axes[2],
    levels=levels,
    cmap="RdBu_r",
    add_colorbar=False,
)

pos_last.plot.contour(
    ax=axes[0],
    levels=contour_levels,
    colors="k",
    add_colorbar=False,
)
neg_last.plot.contour(
    ax=axes[1],
    levels=contour_levels,
    colors="k",
    add_colorbar=False,
)
diff_last.plot.contour(
    ax=axes[2],
    levels=contour_levels,
    colors="k",
    add_colorbar=False,
)

for ax in axes:
    ax.set_xlabel("Longitude")
    ax.set_ylim(100000, 1000)

# %%
