# %%
import xarray as xr
import numpy as np
from src.data_helper.read_composite import read_comp_var
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.ndimage import gaussian_filter
from src.dynamics.theta_on_pv import find_isentrope_at_pv
from matplotlib.patches import Patch

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
    Line2D(
        [0],
        [0],
        color="red",
        linewidth=1.5,
        linestyle="solid",
        label="AWB for positive NAO",
    ),
    Line2D(
        [0],
        [0],
        color="blue",
        linewidth=1.5,
        linestyle="dashed",
        label="CWB for negative NAO",
    ),
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

# Select isentropic levels and time window
time_window = slice(-5, 5)

# Process data
awb_first = (
    awb_pos_first.sel(time=time_window).mean(dim="time").sum("event").mean(dim="lon")
)
awb_last = (
    awb_pos_last.sel(time=time_window).mean(dim="time").sum("event").mean(dim="lon")
)

cwb_first = (
    cwb_neg_first.sel(time=time_window).mean(dim="time").sum("event").mean(dim="lon")
)
cwb_last = (
    cwb_neg_last.sel(time=time_window).mean(dim="time").sum("event").mean(dim="lon")
)

# %% Tropopause
pv_1850 = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0climatology/pv_1850.nc"
)
pv_2090 = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0climatology/pv_2090.nc"
)
# %%
pv_1850_zm = pv_1850.pv.mean(dim=("lon")) * 1e6
pv_2090_zm = pv_2090.pv.mean(dim=("lon")) * 1e6

# %%
trops_1850 = find_isentrope_at_pv(pv_1850_zm)
trops_2090 = find_isentrope_at_pv(pv_2090_zm)


# %%
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=False)

awb_first.plot.contourf(
    ax=axes[0],
    levels=np.arange(1, 6, 1),
    cmap="Reds",
    cbar_kwargs={"label": "AWB Frequency"},
    extend="max",
)
awb_contour = awb_last.plot.contour(
    ax=axes[0],
    levels=np.arange(1, 6, 1),
    colors="black",
    linewidths=1.5,
    linestyles="solid",
    extend="max",
)

# Fill between tropopause and y=0 with light colors
axes[0].fill_between(
    trops_1850.lat,
    300,
    trops_1850,
    color="red",
    alpha=0.1,
    label="Tropopause 1850s"
)
axes[0].fill_between(
    trops_2090.lat,
    300,
    trops_2090,
    color="black",
    alpha=0.1,
    label="Tropopause 2090s"
)

cwb_first.plot.contourf(
    ax=axes[1],
    levels=np.arange(1, 6, 1),
    cmap="Blues",
    cbar_kwargs={"label": "CWB Frequency"},
    extend="max",
)
cwb_contour = cwb_last.plot.contour(
    ax=axes[1],
    levels=np.arange(1, 6, 1),
    colors="black",
    linewidths=1.5,
    linestyles="solid",
    extend="max",
)

# Fill between tropopause and y=0 on second subplot
axes[1].fill_between(
    trops_1850.lat,
    300,
    trops_1850,
    color="red",
    alpha=0.1,
)
axes[1].fill_between(
    trops_2090.lat,
    300,
    trops_2090,
    color="black",
    alpha=0.1,
)

# Create custom legend elements
legend_elements = [
    # Wave breaking section
    Patch(facecolor="gray", alpha=0.5, label="Wave breaking 1850s"),
    Line2D(
        [0],
        [0],
        color="black",
        linewidth=1.5,
        linestyle="solid",
        label="Wave breaking 2090s",
    ),
    # Tropopause section
    Patch(facecolor="red", alpha=0.1, label="Tropopause 1850s"),
    Patch(facecolor="black", alpha=0.1, label="Tropopause 2090s"),
]

# Add legend to both subplots
for ax in axes:
    ax.legend(handles=legend_elements, loc="upper right", fontsize=9)

axes[0].set_xlim(22, 90)
axes[0].set_title("AWB Frequency")
axes[0].set_ylabel("isentrope (K)")
axes[1].set_xlim(22, 90)
axes[1].set_title("CWB Frequency")
axes[1].set_ylabel("")

plt.tight_layout()
plt.show()
# %%
