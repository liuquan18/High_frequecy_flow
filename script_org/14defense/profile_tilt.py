# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.path as mpath
import matplotlib.ticker as mticker
from matplotlib.colors import ListedColormap, BoundaryNorm


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
import metpy.calc as mpcalc
import src.plotting.util as util

importlib.reload(read_composite)
importlib.reload(util)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var
clip_map = util.clip_map
# %%%
# read zg'
zg_first = read_climatology(
    "zg_steady", 1850, name="zg", model_dir="MPI_GE_CMIP6_allplev"
)
zg_last = read_climatology(
    "zg_steady", 2090, name="zg", model_dir="MPI_GE_CMIP6_allplev"
)

# %%
zg_first_lon = zg_first.sel(lat=slice(0, 90), lon=slice(290, 300)).mean(dim="lon")
zg_last_lon = zg_last.sel(lat=slice(0, 90), lon=slice(290, 300)).mean(dim="lon")
# %%
# plot the profile tilt, x-lat, y-height
fig, ax = plt.subplots()
# create levels that exclude 0
levels_color = np.arange(-60, 65, 10)
levels_lines = np.concatenate((np.arange(-60, 0, 10), np.arange(10, 61, 10)))

# build a ListedColormap with one color per interval and make -10..10 intervals transparent
base_cmap = plt.get_cmap("RdBu_r", len(levels_color) - 1)
colors = [base_cmap(i) for i in range(base_cmap.N)]

# find intervals whose bounds lie within -10 and 10 and set them transparent
for i, (low, high) in enumerate(zip(levels_color[:-1], levels_color[1:])):
    if low >= -10 and high <= 10:
        colors[i] = (0, 0, 0, 0)  # transparent

listed_cmap = ListedColormap(colors)
norm = BoundaryNorm(levels_color, listed_cmap.N)

cs = ax.contourf(
    zg_first_lon["lat"],
    zg_first_lon["plev"] / 100,
    zg_first_lon,
    levels=levels_color,
    cmap=listed_cmap,
    norm=norm,
    extend="both",
)


lines = ax.contour(
    zg_last_lon["lat"],
    zg_last_lon["plev"] / 100,
    zg_last_lon,
    levels=levels_lines,
    colors="k",
)

ax.invert_yaxis()
ax.set_ylim(1000, 250)

# ax.clabel(lines, fmt="%1.0f", colors="k", fontsize=8)
manual_locations = [
    (20, 900),
    (20, 800),
    (20, 700),
    (30, 600),
    (50, 500),
    (60, 800),
    (75, 900),
    (55, 400),
]

plt.clabel(lines, fmt="%1.0f", colors="k", fontsize=8, manual=manual_locations)

ax.set_xlabel("Latitude (°N)")
ax.set_ylabel("Pressure Level (hPa)")
ax.set_title("tilt of the quasi-stationary eddies profile")

# invert y axis

fig.colorbar(cs, ax=ax, label="zg (m)")
#
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/profile_tilt_zg_first.png", dpi=500, bbox_inches="tight", transparent=True)

# %%
