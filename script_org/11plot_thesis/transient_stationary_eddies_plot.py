#%%
# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.path as mpath
import matplotlib.ticker as mticker



from src.data_helper import read_composite
from src.plotting.util import erase_white_line, map_smooth, NA_box
import importlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
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

clip_map = util.clip_map
# %%
zg_ano = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_monthly_state/zg_hat_monthly_mean.nc")
# %%
eke = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_monthly_stat/eke_50000_monthly_05_09.nc")


# %%
fig, axes = plt.subplots(
    1,
    2,
    figsize=(12, 6),
    subplot_kw={"projection": ccrs.Orthographic(-40, 80)},
)

for ax in axes:
    ax.coastlines(color="grey", linewidth=1)
    ax.gridlines()
    ax.set_global()

# eke 
eke.eke.isel(time = 0, plev = 0).plot.contourf(
    ax=axes[0],
    transform=ccrs.PlateCarree(),
    cmap="viridis",
    add_colorbar=True,
    levels = np.arange(90, 151, 10),
    extend = "max",
    cbar_kwargs={"label": r"$eke$ (m$^2$ s$^{-2}$)", "shrink": 0.6},
)

# zg_ano
zg_ano.var129.isel(time = 0).sel(plev = 25000).plot.contourf(
    ax=axes[1],
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": r"zg (m)", "shrink": 0.6},
    levels=np.arange(-80, 81, 20),
)

axes[0].set_title("")
axes[1].set_title("")


# add a, b
axes[0].text(0., 1.0, "a", transform=axes[0].transAxes, fontsize=16, fontweight="bold")
axes[1].text(0., 1.0, "b", transform=axes[1].transAxes, fontsize=16, fontweight="bold")
plt.tight_layout()

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0thesis/transient_stationary_eddies.pdf", dpi=300, bbox_inches="tight")
# %%
