from src.plotting.util import erase_white_line
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

# %%
def plot_uhat(ax, uhat_first, u_hat_last=None, levels=np.arange(-12, 13, 2)):

    ax.coastlines()
    ax.set_global()

    uhat_first = erase_white_line(uhat_first)

    umap =  uhat_first.plot.contourf(
        ax=ax,
        transform=ccrs.PlateCarree(),
        add_colorbar=False,
        levels=levels,
    )
    if u_hat_last is not None:
        u_hat_last = erase_white_line(u_hat_last)
        u_hat_last.plot.contour(
            ax=ax,
            transform=ccrs.PlateCarree(),
            colors="w",
            add_colorbar=False,
            levels=levels[levels != 0],
        )
    return ax, umap