# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line, lat2y, lon2x
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns
from src.moisture.longitudinal_contrast import read_NAO_extremes


# %%
def read_ensmean(var, name, plev = None):
    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_ensmean/"
    first_data = xr.open_dataset(f"{base_dir}{var}_ensmean_1850.nc")
    last_data = xr.open_dataset(f"{base_dir}{var}_ensmean_2090.nc")

    first_data = first_data[name]
    last_data = last_data[name]

    first_data = erase_white_line(first_data)
    last_data = erase_white_line(last_data)

    first_data = first_data.squeeze()
    last_data = last_data.squeeze()

    if plev:
        first_data = first_data.sel(plev=plev)
        last_data = last_data.sel(plev=plev)

    return first_data.compute(), last_data.compute()
#%%
tprime_first, tprime_last = read_ensmean("ta_prime", 'ta', plev=50000)
qprime_first, qprime_last = read_ensmean("hus_prime", 'hus', plev=50000)
ieke_first, ieke_last = read_ensmean("ieke", 'ieke')
#%%


# %%
prec_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_seq.txt"
)
prec_cmap_seq = mcolors.ListedColormap(prec_cmap_seq, name="prec_div")

prec_cmap_div = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_div.txt"
)
prec_cmap_div = mcolors.ListedColormap(prec_cmap_div, name="prec_div")
# %%
fig = plt.figure(figsize=(12, 10))
gs = fig.add_gridspec(
    2,
    3,
    width_ratios=[1, 1, 1],
    height_ratios=[0.8, 1],
)

axes = np.empty((2, 3), dtype=object)
axes[0, 0] = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree(-90))
axes[0, 1] = fig.add_subplot(gs[0, 1], projection=ccrs.PlateCarree(-90))
axes[0, 2] = fig.add_subplot(gs[0, 2], projection=ccrs.PlateCarree(-90))
axes[1, 0] = fig.add_subplot(gs[1, 0])
axes[1, 1] = fig.add_subplot(gs[1, 1])
axes[1, 2] = fig.add_subplot(gs[1, 2])

ivke_first.plot.contourf(
    ax=axes[0, 0],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_seq,
    levels=np.arange(0, 301, 20),
    extend="max",
    cbar_kwargs={
        "label": r"$q'^2 \, eke \, / \, g^2 \, kg^{-2} \, m^2 \, s^{-2}$",
        "orientation": "horizontal",
        "pad": 0.05,
    },
)
ivke_last.plot.contourf(
    ax=axes[0, 1],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_seq,
    levels=np.arange(0, 301, 20),
    extend="max",
    cbar_kwargs={
        "label": r"$q'^2 \, eke \, / \, g^2 \, kg^{-2} \, m^2 \, s^{-2}$",
        "orientation": "horizontal",
        "pad": 0.05,
    },
)
ivke_diff.plot.contourf(
    ax=axes[0, 2],
    transform=ccrs.PlateCarree(),
    cmap=prec_cmap_div,
    levels=np.arange(-100, 101, 10),
    extend="both",
    cbar_kwargs={
        "label": r"$q'^2 \, eke \, / \, g^2 \, kg^{-2} \, m^2 \, s^{-2}$",
        "orientation": "horizontal",
        "pad": 0.05,
    },
)

# hline at 30 and 60
# vlines at 120, 230, 285, 345
axes[0, 2].axhline(lat2y(30, axes[0, 2]), color="black", linestyle="--", linewidth=0.5)
axes[0, 2].axhline(lat2y(60, axes[0, 2]), color="black", linestyle="--", linewidth=0.5)
axes[0, 2].axvline(
    lon2x(120, axes[0, 2]),
    ymin=0.65,
    ymax=0.85,
    color="black",
    linestyle="--",
    linewidth=0.5,
)
axes[0, 2].axvline(
    lon2x(220, axes[0, 2]),
    ymin=0.65,
    ymax=0.85,
    color="black",
    linestyle="--",
    linewidth=0.5,
)
axes[0, 2].axvline(
    lon2x(285, axes[0, 2]),
    ymin=0.65,
    ymax=0.85,
    color="black",
    linestyle="--",
    linewidth=0.5,
)
axes[0, 2].axvline(
    lon2x(345, axes[0, 2]),
    ymin=0.65,
    ymax=0.85,
    color="black",
    linestyle="--",
    linewidth=0.5,
)

for ax in axes[0, :].flat:
    ax.coastlines()

sns.lineplot(
    data=final_merge,
    x="decade",
    y="ivke_NPC",
    ax=axes[1, 0],
    label="iveke NPC",
    color="k",
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="ivke_NAL",
    ax=axes[1, 0],
    label="iveke NAL",
    color="k",
    linewidth=2,
    linestyle="--",
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="count_awb",
    ax=axes[1, 1],
    label="AWB",
    color="k",
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="count_cwb",
    ax=axes[1, 1],
    label="CWB",
    color="k",
    linestyle="--",
    linewidth=2,
)

sns.lineplot(
    data=final_merge,
    x="decade",
    y="days_pos",
    ax=axes[1, 2],
    label="NAO pos",
    color="k",
    linewidth=2,
)
sns.lineplot(
    data=final_merge,
    x="decade",
    y="days_neg",
    ax=axes[1, 2],
    label="NAO neg",
    color="k",
    linestyle="--",
    linewidth=2,
)
axes[0, 0].set_title("1850")
axes[0, 1].set_title("2090")
axes[0, 2].set_title("2090-1850")

axes[1, 0].set_ylabel(r"Integrated vapor eke")
axes[1, 1].set_ylabel("wave breaking")
axes[1, 2].set_ylabel("extreme NAO days")

for ax in axes[1, :].flat:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# add a, b, c
for i, ax in enumerate(axes.flat):
    ax.text(
        -0.1,
        1.05,
        f"{chr(97+i)}",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
    )
plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/transients_response.pdf", dpi=300)
# %%
