# %%
import xarray as xr
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import seaborn as sns

import os
import sys
import glob
import matplotlib.colors as mcolors
from scipy.ndimage import gaussian_filter
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


import logging

logging.basicConfig(level=logging.INFO)


# %%
def read_Cxy(var1="hus_std", var2="va", region="NAL", pixel_wise=True):

    members = np.arange(1, 51)
    coherence = []

    for member in members:
        logging.info(f"Processing member {member}")
        if pixel_wise:
            base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var1}_{var2}_coherence_pixelwise/r{member}i1p1f1/"
        else:
            base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var1}_{var2}_coherence/r{member}i1p1f1/"

        if region is not None:
            files = glob.glob(base_dir + f"*{region}*.nc")
        else:
            logging.warning(
                "No region specified, reading all files except those with 'NAL' or 'NPC'"
            )
            files = glob.glob(base_dir + "*.nc")
            files = [f for f in files if "NAL" not in f and "NPC" not in f]

        cxy = xr.open_mfdataset(
            files, combine="by_coords", chunks={"time": -1, "lat": -1, "lon": -1}
        )

        coherence.append(cxy)
    coherence = xr.concat(coherence, dim="ens")
    coherence["ens"] = members

    return coherence


# %%
hus_va_Cxy_NAL = read_Cxy("hus_std", "va", "NAL", pixel_wise=True)
hus_va_Cxy_NPC = read_Cxy("hus_std", "va", "NPC", pixel_wise=True)

tas_va_Cxy_NAL = read_Cxy("tas_std", "va", "NAL", pixel_wise=True)
tas_va_Cxy_NPC = read_Cxy("tas_std", "va", "NPC", pixel_wise=True)

vt_va_Cxy = read_Cxy("vt", "va", None)
# %%
hus_va_Cxy_NAL.load()
hus_va_Cxy_NPC.load()

tas_va_Cxy_NAL.load()
tas_va_Cxy_NPC.load()

vt_va_Cxy.load()


# %%
def plot_coherence(
    f, Cxy_mean, Cxy_5, Cxy_95, ax, color_line="k", color_shading="gray", label=None
):
    ax.plot(1 / f, Cxy_mean, label=label, color=color_line)
    ax.set_xlabel("Period [days]")
    ax.set_ylabel("Coherence")

    ax.set_xticks(np.arange(0, 31, 6))

    # fill between
    ax.fill_between(
        1 / f,
        Cxy_5,
        Cxy_95,
        color=color_shading,
        alpha=0.5,
        label=r"5-95$\%$ ens spread",
    )

    ax.set_xlim(0, 30)

    return ax


# %%
def get_plot_data(Cxy, globe_mean=True, period=None):

    if period == "first":
        Cxy = Cxy.sel(time="1850")
    elif period == "last":
        Cxy = Cxy.sel(time="2090")

    else:
        logging.warning("No period specified, using all data")

    if globe_mean:
        Cxy = Cxy.mean(dim=("lat", "lon", "time"))
    else:
        Cxy = Cxy.mean(dim="time")

    Cxy_mean = Cxy["coherence"].mean(dim=("ens"))
    Cxy_95 = Cxy["coherence"].quantile(0.95, dim=("ens"))
    Cxy_05 = Cxy["coherence"].quantile(0.05, dim=("ens"))

    return Cxy_mean, Cxy_95, Cxy_05


# %%
hus_va_NAL_mean, hus_va_NAL_95, hus_va_NAL_05 = get_plot_data(hus_va_Cxy_NAL)
hus_va_NPC_mean, hus_va_NPC_95, hus_va_NPC_05 = get_plot_data(hus_va_Cxy_NPC)

vt_va_mean, vt_va_95, vt_va_05 = get_plot_data(vt_va_Cxy, globe_mean=True)
# %%
hus_va_NAL_mean_first, hus_va_NAL_95_first, hus_va_NAL_05_first = get_plot_data(
    hus_va_Cxy_NAL, period="first"
)
hus_va_NPC_mean_first, hus_va_NPC_95_first, hus_va_NPC_05_first = get_plot_data(
    hus_va_Cxy_NPC, period="first"
)

vt_va_mean_first, vt_va_95_first, vt_va_05_first = get_plot_data(
    vt_va_Cxy, globe_mean=True, period="first"
)
# %%
hus_va_NAL_mean_last, hus_va_NAL_95_last, hus_va_NAL_05_last = get_plot_data(
    hus_va_Cxy_NAL, period="last"
)
hus_va_NPC_mean_last, hus_va_NPC_95_last, hus_va_NPC_05_last = get_plot_data(
    hus_va_Cxy_NPC, period="last"
)

vt_va_mean_last, vt_va_95_last, vt_va_05_last = get_plot_data(
    vt_va_Cxy, globe_mean=True, period="last"
)
# %%
tas_va_NAL_mean, tas_va_NAL_95, tas_va_NAL_05 = get_plot_data(tas_va_Cxy_NAL)
tas_va_NPC_mean, tas_va_NPC_95, tas_va_NPC_05 = get_plot_data(tas_va_Cxy_NPC)

tas_va_NAL_mean_first, tas_va_NAL_95_first, tas_va_NAL_05_first = get_plot_data(
    tas_va_Cxy_NAL, period="first"
)
tas_va_NPC_mean_first, tas_va_NPC_95_first, tas_va_NPC_05_first = get_plot_data(
    tas_va_Cxy_NPC, period="first"
)

tas_va_NAL_mean_last, tas_va_NAL_95_last, tas_va_NAL_05_last = get_plot_data(
    tas_va_Cxy_NAL, period="last"
)
tas_va_NPC_mean_last, tas_va_NPC_95_last, tas_va_NPC_05_last = get_plot_data(
    tas_va_Cxy_NPC, period="last"
)
# %%
# ERA5


def read_Cxy_ERA5(var1="hus", var2="va", region="NAL", pixel_wise=True):

    if pixel_wise:
        base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/{var1}_{var2}_coherence_pixelwise/"
    else:
        base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/{var1}_{var2}_coherence/"

    if region is not None:
        files = glob.glob(base_dir + f"*{region}*.nc")
    else:
        logging.warning(
            "No region specified, reading all files except those with 'NAL' or 'NPC'"
        )
        files = glob.glob(base_dir + "*.nc")
        files = [f for f in files if "NAL" not in f and "NPC" not in f]

    # sort files
    files.sort()

    cxy = xr.open_mfdataset(files, combine="nested", concat_dim="time", parallel=True)

    cxy["time"] = np.arange(1979, 2025, 1)

    return cxy


# %%
ERA5_hus_va_Cxy_NAL = read_Cxy_ERA5("hus", "va", "NAL", pixel_wise=True)
ERA5_hus_va_Cxy_NPC = read_Cxy_ERA5("hus", "va", "NPC", pixel_wise=True)
# %%
ERA5_tas_va_Cxy_NAL = read_Cxy_ERA5("tas", "va", "NAL", pixel_wise=True)
ERA5_tas_va_Cxy_NPC = read_Cxy_ERA5("tas", "va", "NPC", pixel_wise=True)

# %%
ERA5_hus_va_Cxy_NAL.load()
ERA5_hus_va_Cxy_NPC.load()
# %%
ERA5_tas_va_Cxy_NAL.load()
ERA5_tas_va_Cxy_NPC.load()

# %%
# vt_va_Cxy.load()

# %%
# %%
ERA5_hus_va_NAL_mean = ERA5_hus_va_Cxy_NAL.mean(dim=("time", "lat", "lon"))
ERA5_hus_va_NPC_mean = ERA5_hus_va_Cxy_NPC.mean(dim=("time", "lat", "lon"))

ERA5_tas_va_NAL_mean = ERA5_tas_va_Cxy_NAL.mean(dim=("time", "lat", "lon"))
ERA5_tas_va_NPC_mean = ERA5_tas_va_Cxy_NPC.mean(dim=("time", "lat", "lon"))


# %%
def smooth_period(cxy, period=1.5):

    # smoothed_period = np.arange(0.1, 31, period)
    # smoothed_frequency = 1 / smoothed_period

    # cxy_smooth = cxy.interp(frequency = smoothed_frequency)

    # cxy_smooth = cxy.rolling(frequency = period, center = True).mean()
    cxy_smooth = gaussian_filter(cxy.coherence, sigma=period)

    return cxy_smooth


# %%
ERA5_hus_va_NAL_mean_smooth = smooth_period(ERA5_hus_va_NAL_mean)
ERA5_hus_va_NPC_mean_smooth = smooth_period(ERA5_hus_va_NPC_mean)

ERA5_tas_va_NAL_mean_smooth = smooth_period(ERA5_tas_va_NAL_mean)
ERA5_tas_va_NPC_mean_smooth = smooth_period(ERA5_tas_va_NPC_mean)


# %%

# %%
temp_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/temp_seq.txt"
)
temp_cmap_seq = mcolors.ListedColormap(temp_cmap_seq, name="temp_div")


prec_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_seq.txt"
)
prec_cmap_seq = mcolors.ListedColormap(prec_cmap_seq, name="prec_div")

# %%
# plot all ensemble members
fig, axes = plt.subplots(2, 3, figsize=(10, 7))

# Move the first column to the last column
axes[0, 2] = plot_coherence(
    vt_va_Cxy["frequency"], vt_va_mean, vt_va_05, vt_va_95, axes[0, 2]
)

# Plot hus_std va NPC and tas_std va NPC on the same axis
plot_coherence(
    tas_va_Cxy_NPC["frequency"],
    tas_va_NPC_mean,
    tas_va_NPC_05,
    tas_va_NPC_95,
    axes[0, 0],
    color_line=temp_cmap_seq(0.7),
    color_shading=temp_cmap_seq(0.5),
    label=r"$\Delta T$ ~ $va$ ",
)
plot_coherence(
    hus_va_Cxy_NPC["frequency"],
    hus_va_NPC_mean,
    hus_va_NPC_05,
    hus_va_NPC_95,
    axes[0, 0],
    color_line=prec_cmap_seq(0.9),
    color_shading=prec_cmap_seq(0.5),
    label=r"$\Delta q$ ~ $va$ ",
)


# Plot hus_std va NAL and tas_std va NAL on the same axis
plot_coherence(
    tas_va_Cxy_NAL["frequency"],
    tas_va_NAL_mean,
    tas_va_NAL_05,
    tas_va_NAL_95,
    axes[0, 1],
    color_line=temp_cmap_seq(0.7),
    color_shading=temp_cmap_seq(0.5),
    label=r"$\Delta T$ ~ $va$ ",
)
plot_coherence(
    hus_va_Cxy_NAL["frequency"],
    hus_va_NAL_mean,
    hus_va_NAL_05,
    hus_va_NAL_95,
    axes[0, 1],
    color_line=prec_cmap_seq(0.9),
    color_shading=prec_cmap_seq(0.5),
    label=r"$\Delta q$ ~ $va$ ",
)


# Add vertical lines at days = 2 and days = 12
axes[0, 2].axvline(x=2, color="r", linestyle="--")
# axes[0, 2].axvline(x=6, color='r', linestyle='--')
axes[0, 2].axvline(x=12, color="r", linestyle="--")

# Add double arrow lines and labels
axes[0, 2].annotate(
    r"$v^{\prime}$",
    xy=(2, 0.40),
    xytext=(12, 0.399),
    arrowprops=dict(arrowstyle="<->", color="blue"),
    color="blue",
)
# axes[0, 2].annotate(r'$v^{\prime\prime}$', xy=(2, 0.41), xytext=(6, 0.409),
#              arrowprops=dict(arrowstyle='<->', color='green'), color='green')


# ERA5
f = ERA5_hus_va_Cxy_NAL.frequency.values
axes[1, 0].plot(
    1 / f,
    ERA5_hus_va_NPC_mean.coherence,
    label=r"$\Delta q$ ~ $va$",
    color=prec_cmap_seq(0.9),
    linewidth=0.5,
)
axes[1, 0].plot(
    1 / f,
    ERA5_tas_va_NPC_mean.coherence,
    label=r"$\Delta T$ ~ $va$",
    color=temp_cmap_seq(0.7),
    linewidth=0.5,
)

axes[1, 1].plot(
    1 / f,
    ERA5_hus_va_NAL_mean.coherence,
    label=r"$\Delta q$ ~ $va$",
    color=prec_cmap_seq(0.9),
    linewidth=0.5,
)
axes[1, 1].plot(
    1 / f,
    ERA5_tas_va_NAL_mean.coherence,
    label=r"$\Delta T$ ~ $va$",
    color=temp_cmap_seq(0.7),
    linewidth=0.5,
)

# smooth
axes[1, 0].plot(
    1 / f,
    ERA5_hus_va_NPC_mean_smooth,
    color=prec_cmap_seq(0.9),
    linewidth=2,
    linestyle="--",
)
axes[1, 0].plot(
    1 / f,
    ERA5_tas_va_NPC_mean_smooth,
    color=temp_cmap_seq(0.7),
    linewidth=2,
    linestyle="--",
)

axes[1, 1].plot(
    1 / f,
    ERA5_hus_va_NAL_mean_smooth,
    color=prec_cmap_seq(0.9),
    linewidth=2,
    linestyle="--",
)
axes[1, 1].plot(
    1 / f,
    ERA5_tas_va_NAL_mean_smooth,
    color=temp_cmap_seq(0.7),
    linewidth=2,
    linestyle="--",
)


axes[1, 0].set_xlim(0, 30)
axes[1, 1].set_xlim(0, 30)

axes[1, 0].set_ylim(0.34, 0.40)
axes[1, 1].set_ylim(0.34, 0.40)
axes[1, 0].set_xticks(np.arange(0, 31, 6))
axes[1, 1].set_xticks(np.arange(0, 31, 6))
axes[0, 2].set_xticks(np.arange(0, 31, 6))


axes[0, 2].set_xlim(0, 30)
for ax in axes[0, :2].flat:
    ax.set_ylim(0.34, 0.40)
plt.tight_layout()
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/vt_q_t_va_coherence_pixelwise.png", dpi = 300)


axes[0, 2].set_title(r"$v_{t 20-60}$, $va_{20-60}$")
axes[0, 0].set_title("NPC pixel wise")
axes[0, 1].set_title("NAL pixel wise")

for ax in axes[0, :]:
    ax.set_xlabel("")
for ax in axes[1, :]:
    ax.set_xlabel("Period [days]")
axes[0, 2].set_xlabel("Period [days]")

for ax in axes[:, :2].flat:
    ax.set_ylabel("")
for ax in axes[:, 2]:
    ax.set_ylabel("Coherence")


# customed legend
custom_lines = [
    Line2D([0], [0], color="k", lw=1, label=r"$v_{t}$ ~ $va$ MPI-GE"),
    Line2D([0], [0], color=temp_cmap_seq(0.7), lw=1, label=r"$\Delta T$ ~ $va$ MPI-GE"),
    Line2D([0], [0], color=prec_cmap_seq(0.9), lw=1, label=r"$\Delta q$ ~ $va$ MPI-GE"),
    # ERA5
    Line2D(
        [0],
        [0],
        color=temp_cmap_seq(0.7),
        lw=1,
        linestyle="--",
        label=r"$\Delta T$ ~ $va$ ERA5",
    ),
    Line2D(
        [0],
        [0],
        color=prec_cmap_seq(0.9),
        lw=1,
        linestyle="--",
        label=r"$\Delta q$ ~ $va$ ERA5",
    ),
    # shading for 5-95% ens spread
    Patch(facecolor="gray", edgecolor="gray", alpha=0.5, label=r"5-95$\%$ ens spread"),
    Line2D([0], [0], color="r", linestyle="--", lw=1, label="Days = 2 and 12"),
]

# Add title to the legend
axes[1, 2].legend(handles=custom_lines, frameon=False, loc="center")
# remove all spines, ticks, and labels from axes[1,2]
axes[1, 2].spines[["top", "right", "bottom", "left"]].set_visible(False)
axes[1, 2].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
axes[1, 2].set_xlabel("")
axes[1, 2].set_ylabel("")

# add a, b, c labels for each subplots
axes[0, 2].text(
    -0.1,
    1.1,
    "a",
    transform=axes[0, 2].transAxes,
    size=12,
    weight="bold",
)

axes[0, 0].text(
    -0.1,
    1.1,
    "b",
    transform=axes[0, 0].transAxes,
    size=12,
    weight="bold",
)

axes[0, 1].text(
    -0.1,
    1.1,
    "c",
    transform=axes[0, 1].transAxes,
    size=12,
    weight="bold",
)

axes[1, 0].text(
    -0.1,
    1.1,
    "d",
    transform=axes[1, 0].transAxes,
    size=12,
    weight="bold",
)

axes[1, 1].text(
    -0.1,
    1.1,
    "e",
    transform=axes[1, 1].transAxes,
    size=12,
    weight="bold",
)


plt.tight_layout()

# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/vt_q_t_va_coherence_pixelwise.png", dpi = 300)
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/vt_q_t_va_coherence_pixelwise.pdf",
    dpi=300,
)

# %%
