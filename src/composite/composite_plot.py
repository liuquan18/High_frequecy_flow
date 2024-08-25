# %%
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr
import numpy as np


# %%
# %%
def plot_map(zg_composite, ax, levels=np.arange(-10, 11, 1)):
    levels = levels[levels != 0] # remove 0 from the levels
    p = zg_composite.sel(lat=slice(-10, None)).plot.contour(
        levels=levels,
        extend="both",
        ax=ax,
        add_colorbar=False,
        colors="k",
        transform=ccrs.PlateCarree(),
    )

    # Add coastlines
    p.axes.coastlines(alpha=0.5)
    return p


# %%
def plot_composite(
    composite_first10,
    composite_last10,
    extreme_type="pos",
    start_lag=-8,
    interval_lag=1,
    levels = np.arange(-60, 61, 5),
):
    fig, axes = plt.subplots(
        6, 2, figsize=(15, 15), subplot_kw={"projection": ccrs.PlateCarree(180)}
    )


    extreme_type = extreme_type
    start_lag = -8
    length_lag = 6
    interval_lag = 1
    stop_lag = start_lag + length_lag * interval_lag

    lag_days = np.arange(start_lag, stop=stop_lag, step=interval_lag)
    periods = ["first10", "last10"]
    data = [composite_first10, composite_last10]

    for i, period in enumerate(periods):
        for j, lag in enumerate(lag_days):
            plot_map(data[i].sel(time=lag), axes[j, i], levels=levels)
            axes[j, i].set_title(f"{period} {extreme_type} lag {lag}")

    # add x-axis labels for the last row
    for ax in axes[-1, :]:
        ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
        ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

    # add y-axis labels for the first column
    for ax in axes[:, 0]:
        ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
        ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])
    return fig, axes
