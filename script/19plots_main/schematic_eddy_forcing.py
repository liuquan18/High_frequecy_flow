#%%
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy
# %%
from src.data_helper.read_variable import read_composite_MPI  # noqa: E402
from src.data_helper.read_variable import read_MPI_GE_uhat
import matplotlib.colors as mcolors

#%%
# read composite mean wind


#%%
# eddy heat flux
vpetp_pos = read_composite_MPI("vpetp", "vpetp", 1850, return_as='pos')
vpetp_neg = read_composite_MPI("vpetp", "vpetp", 2090, return_as='neg')
#%%
vpetp_pos = vpetp_pos.sel(plev=85000)
vpetp_neg = vpetp_neg.sel(plev=85000)
#%%
temp_cmap_div = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/temp_seq.txt"
)
temp_cmap_div = mcolors.ListedColormap(temp_cmap_div, name="temp_div")

# %%
# draw a map with NearsidePerspective projection
fig, axes = plt.subplots(1, 2, subplot_kw={'projection': ccrs.NearsidePerspective(central_longitude=300, central_latitude=75)},
                          figsize=(15, 10))
# Set the extent of the map
# ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
# Add coastlines and gridlines
ax_pos = axes[0]
ax_neg = axes[1]
ax_pos.coastlines()
ax_pos.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')

# add feature
ax_pos.add_feature(cartopy.feature.LAND, facecolor='lightgray')
# ax.add_feature(cartopy.feature.OCEAN, facecolor='lightblue')
# same for neg
ax_neg.coastlines()
ax_neg.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
ax_neg.add_feature(cartopy.feature.LAND, facecolor='lightgray')

# # add heat flux
# vpetp_pos.plot.contourf(
#     ax=ax_pos,
#     transform=ccrs.PlateCarree(),
#     cmap='Reds',
#     levels=np.arange(0., 1.2, 0.2),
#     add_colorbar=False,
#     extend = 'max',

# )

# set global
ax_pos.set_global()
ax_pos.set_title("")
ax_neg.set_global()
ax_neg.set_title("")




plt.show()

# save as vector graphics
fig.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/schematic/schematic_eddy_forcing_base.svg", format='svg', dpi=300, bbox_inches='tight')
# %%
