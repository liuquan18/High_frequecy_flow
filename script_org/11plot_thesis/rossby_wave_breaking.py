#%%
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import clip_map
import numpy as np
import matplotlib.ticker as mticker

# %%
fig, axes = plt.subplots(
    1,2, figsize=(12, 6), subplot_kw={'projection': ccrs.Orthographic(central_longitude=-30, central_latitude=70)}
)

for ax in axes:
    # ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.coastlines(linewidth=1)
    ax.add_feature(ccrs.cartopy.feature.LAND, facecolor='lightgray', edgecolor='black')
    ax.set_extent([-180, 180, 20, 90], crs=ccrs.PlateCarree())
    # add gridlines
    gl = ax.gridlines(draw_labels=False, linewidth=1, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.bottom_labels = False
    gl.left_labels = False
    gl.xlocator = mticker.FixedLocator(np.arange(-180, 181, 30))
    gl.ylocator = mticker.FixedLocator(np.arange(20, 91, 20))
    clip_map(ax)

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0thesis/rossby_wave_breaking_map.svg", dpi=300, bbox_inches="tight", transparent=True)
# %%
