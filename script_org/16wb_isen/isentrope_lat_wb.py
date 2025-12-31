# %%
import xarray as xr
import numpy as np
from src.data_helper.read_composite import read_comp_var
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.ndimage import gaussian_filter

# %% awb
awb_pos_first = read_comp_var(
    "wb_anticyclonic_allisen",
    "pos",
    1850,
    time_window="all",
    name="smooth_pv",
    method="no_stat",
)

# awb_neg_first = read_comp_var(
#     "wb_anticyclonic_allisen",
#     'neg',
#     1850,
#     time_window='all',
#     name = 'smooth_pv',
#     method='no_stat',
# )

awb_pos_last = read_comp_var(
    "wb_anticyclonic_allisen",
    "pos",
    2090,
    time_window="all",
    name="smooth_pv",
    method="no_stat",
)

# awb_neg_last = read_comp_var(
#     "wb_anticyclonic_allisen",
#     'neg',
#     2090,
#     time_window='all',
#     name = 'smooth_pv',
#     method='no_stat',
# )
# %%
# cwb
# cwb_pos_first = read_comp_var(
#     "wb_cyclonic_allisen",
#     'pos',
#     1850,
#     time_window='all',
#     name = 'smooth_pv',
#     method='no_stat',
# )

cwb_neg_first = read_comp_var(
    "wb_cyclonic_allisen",
    "neg",
    1850,
    time_window="all",
    name="smooth_pv",
    method="no_stat",
)
# cwb_pos_last = read_comp_var(
#     "wb_cyclonic_allisen",
#     'pos',
#     2090,
#     time_window='all',
#     name = 'smooth_pv',
#     method='no_stat',
# )
cwb_neg_last = read_comp_var(
    "wb_cyclonic_allisen",
    "neg",
    2090,
    time_window="all",
    name="smooth_pv",
    method="no_stat",
)
# %%
# Combined AWB (colormap) and CWB (contours) plot
fig, axes = plt.subplots(
    2, 6, figsize=(18, 8), subplot_kw={"projection": ccrs.Orthographic(-20, 60)}
)

# AWB levels for colormap
awb_levels = np.arange(4, 20, 4)
# CWB levels for contours (half of AWB)
cwb_levels = awb_levels / 2

# Select isentropic levels and time window
isen_levels = slice(315, 340)
time_window = slice(-5, 5)

# Process data
awb_first = (
    awb_pos_first.sel(time=time_window)
    .mean(dim="time")
    .sum("event")
    .sel(isen_level=isen_levels)
)
awb_last = (
    awb_pos_last.sel(time=time_window)
    .mean(dim="time")
    .sum("event")
    .sel(isen_level=isen_levels)
)
cwb_first = (
    cwb_neg_first.sel(time=time_window)
    .mean(dim="time")
    .sum("event")
    .sel(isen_level=isen_levels)
)
cwb_last = (
    cwb_neg_last.sel(time=time_window)
    .mean(dim="time")
    .sum("event")
    .sel(isen_level=isen_levels)
)


# Apply Gaussian smoothing for smoother contours
def smooth_data(data, sigma=1):
    """Apply Gaussian filter to smooth the data"""
    smoothed = xr.apply_ufunc(
        gaussian_filter,
        data,
        input_core_dims=[["lat", "lon"]],
        output_core_dims=[["lat", "lon"]],
        kwargs={"sigma": sigma, "mode": "wrap"},
        vectorize=True,
    )
    return smoothed


awb_first = smooth_data(awb_first)
awb_last = smooth_data(awb_last)
cwb_first = smooth_data(cwb_first)
cwb_last = smooth_data(cwb_last)

# First row: First period (1850s)
for i, isen in enumerate(awb_first.isen_level.values):
    ax = axes[0, i]

    # Plot AWB as solid reddish contours
    awb_data = awb_first.sel(isen_level=isen)
    awb_contour = ax.contour(
        awb_data.lon,
        awb_data.lat,
        awb_data.values,
        levels=awb_levels,
        colors="red",
        linewidths=1.5,
        linestyles="solid",
        transform=ccrs.PlateCarree(),
    )

    # Plot CWB as dashed bluish contours
    cwb_data = cwb_first.sel(isen_level=isen)
    cwb_contour = ax.contour(
        cwb_data.lon,
        cwb_data.lat,
        cwb_data.values,
        levels=cwb_levels,
        colors="blue",
        linewidths=1.5,
        linestyles="solid",
        transform=ccrs.PlateCarree(),
    )

    ax.set_global()
    ax.coastlines()
    ax.gridlines()
    ax.set_title(f"{int(isen)}K")

# Second row: Last period (2090s)
for i, isen in enumerate(awb_last.isen_level.values):
    ax = axes[1, i]

    # Plot AWB as solid reddish contours
    awb_data = awb_last.sel(isen_level=isen)
    awb_contour = ax.contour(
        awb_data.lon,
        awb_data.lat,
        awb_data.values,
        levels=awb_levels,
        colors="red",
        linewidths=1.5,
        linestyles="solid",
        transform=ccrs.PlateCarree(),
    )

    # Plot CWB as dashed bluish contours
    cwb_data = cwb_last.sel(isen_level=isen)
    cwb_contour = ax.contour(
        cwb_data.lon,
        cwb_data.lat,
        cwb_data.values,
        levels=cwb_levels,
        colors="blue",
        linewidths=1.5,
        linestyles="solid",
        transform=ccrs.PlateCarree(),
    )

    ax.set_global()
    ax.coastlines()
    ax.gridlines()
    ax.set_title(f"{int(isen)}K")

# Add legend at the bottom
fig.subplots_adjust(bottom=0.12)


legend_elements = [
    Line2D([0], [0], color="red", linewidth=1.5, linestyle="solid", label="AWB for positive NAO"),
    Line2D([0], [0], color="blue", linewidth=1.5, linestyle="dashed", label="CWB for negative NAO"),
]
fig.legend(
    handles=legend_elements,
    loc="lower center",
    bbox_to_anchor=(0.5, 0.02),
    fontsize=10,
    ncol=2,
)

plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.show()

# %%
