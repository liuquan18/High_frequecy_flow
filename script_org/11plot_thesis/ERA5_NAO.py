#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
# %%
eofs = xr.open_dataset("/work/mh0033/m300883/Tel_MMLE/data/CR20/EOF_result/all_500_eof.nc")# %%

# %%
pattern = eofs.eof.isel(decade = 0).sel(mode = 'NAO')
index = eofs.pc.sel(mode = 'NAO')
# %%
# left for the NAO pattern with projection, right for the NAO index without projection
fig = plt.figure(figsize=(12, 4))
ax1 = fig.add_subplot(121, projection=ccrs.Orthographic(-30, 60))
ax2 = fig.add_subplot(122)

pattern.plot.contourf(
    ax=ax1,
    transform=ccrs.PlateCarree(),
    cmap="RdBu_r",
    add_colorbar=True,
    levels=np.arange(-30, 30.1, 5),
    extend="both",
    cbar_kwargs={"label": "geopotential height (m)", "shrink": 0.6},
)

ax1.coastlines(color="grey", linewidth=1)
ax1.gridlines()
ax1.set_global()

index.plot.line(
    ax=ax2,
    color="black",
    linewidth=1.5,
    label="NAO index",
)

ax2.set_xlabel("Time")
ax2.set_ylabel("NAO index")
# remove the spines
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

ax1.set_title("")
ax2.set_title("")

# add a, b
ax1.text(0., 1., "a", transform=ax1.transAxes, fontsize=14, fontweight='bold')
ax2.text(-0.1, 1., "b", transform=ax2.transAxes, fontsize=14, fontweight='bold')

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0thesis/NAO_pattern_index.pdf", dpi=300, bbox_inches='tight')
# %%
