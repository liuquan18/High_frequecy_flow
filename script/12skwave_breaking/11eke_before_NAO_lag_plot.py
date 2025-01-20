# %%
import xarray as xr
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import cartopy.crs as ccrs
import cmocean
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.axes as maxes
import cartopy.feature as cfeature
import matplotlib.colors as mcolors
#%%
#%
var = 'eke_high' # 'eke' or 'eke_high'

# %%
first_NAO_pos_eke = pd.read_csv(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_NAO_pos/{var}_NAO_pos_1850.csv",
    index_col=[0, 1],
)


first_NAO_neg_eke = pd.read_csv(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_NAO_neg/{var}_NAO_neg_1850.csv",
    index_col=[0, 1],
)

# %%
last_NAO_pos_eke = pd.read_csv(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_NAO_pos/{var}_NAO_pos_2090.csv",
    index_col=[0, 1],
)

last_NAO_neg_eke = pd.read_csv(
    f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_NAO_neg/{var}_NAO_neg_2090.csv",
    index_col=[0, 1],
)
# %%


def mean_across_event(eke):
    weight = eke["extreme_duration"]
    eke = eke[
        [
            "-20",
            "-19",
            "-18",
            "-17",
            "-16",
            "-15",
            "-14",
            "-13",
            "-12",
            "-11",
            "-10",
            "-9",
            "-8",
            "-7",
            "-6",
            "-5",
            "-4",
            "-3",
            "-2",
            "-1",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
        ]
    ]

    eke = eke.dropna(how="all")

    # weight all rows with 'extreme_duration'
    eke = eke.multiply(weight, axis=0)
    # divide by the sum of 'extreme_duration' to get the weighted mean
    eke = eke.sum(axis=0) / weight.sum()
    eke = eke.to_frame(name="eke")
    return eke


# %%
def event_average_lag(eke):
    eke_mean = eke.groupby(level=1).apply(mean_across_event)

    eke_mean = eke_mean.reset_index()

    eke_mean.columns = ["lon", "lag", "eke"]

    eke_mean["lag"] = eke_mean["lag"].astype(int)

    eke_mean = eke_mean.set_index(["lon", "lag"]).to_xarray()
    return eke_mean


# %%
first_NAO_pos_eke = event_average_lag(first_NAO_pos_eke)
first_NAO_neg_eke = event_average_lag(first_NAO_neg_eke)

last_NAO_pos_eke = event_average_lag(last_NAO_pos_eke)
last_NAO_neg_eke = event_average_lag(last_NAO_neg_eke)


# %%
def to_plot_data(eke):
    eke = eke.rename({"lag": "lat"})  # fake lat to plot correctly the lon

    # Solve the problem on 180 longitude by extending the data
    eke = eke.reindex(lon=np.append(eke.lon.values, 180), method="nearest")
    lon_values = eke.lon.values
    lon_values[-1] = 180
    eke["lon"] = lon_values

    return eke


# %%
first_NAO_pos_eke_plot = to_plot_data(first_NAO_pos_eke)
first_NAO_neg_eke_plot = to_plot_data(first_NAO_neg_eke)

last_NAO_pos_eke_plot = to_plot_data(last_NAO_pos_eke)
last_NAO_neg_eke_plot = to_plot_data(last_NAO_neg_eke)
# %%

diff_NAO_pos_eke_plot = last_NAO_pos_eke_plot - first_NAO_pos_eke_plot

diff_NAO_neg_eke_plot = last_NAO_neg_eke_plot - first_NAO_neg_eke_plot
#%%
slev_div = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/misc_div.txt"
)
slev_div = mcolors.ListedColormap(slev_div, name="temp_div")


# %%
fig, axes = plt.subplots(
    4, 2, figsize=(10, 8), subplot_kw={"projection": ccrs.PlateCarree(-90)},
    sharex=True,
    sharey=False,
)
# cmap = cmocean.cm.
cmap = slev_div
levels = np.arange(-3, 3.1, 0.5)

first_NAO_pos_eke_plot.eke.T.plot.contourf(
    transform=ccrs.PlateCarree(),
    levels=levels,
    ax=axes[0, 0],
    cmap=cmap,
    extend="both",
    cbar_kwargs={"label": "EKE"},
)

first_NAO_neg_eke_plot.eke.T.plot.contourf(
    transform=ccrs.PlateCarree(),
    levels=levels,
    ax=axes[0, 1],
    cmap=cmap,
    extend="both",
    cbar_kwargs={"label": "EKE"},
)

last_NAO_pos_eke_plot.eke.T.plot.contourf(
    transform=ccrs.PlateCarree(),
    levels=levels,
    ax=axes[1, 0],
    cmap=cmap,
    extend="both",
    cbar_kwargs={"label": "EKE"},
)

last_NAO_neg_eke_plot.eke.T.plot.contourf(
    transform=ccrs.PlateCarree(),
    levels=levels,
    ax=axes[1, 1],
    cmap=cmap,
    extend="both",
    cbar_kwargs={"label": "EKE"},
)


diff_NAO_pos_eke_plot.eke.T.plot.contourf(
    transform=ccrs.PlateCarree(),
    levels=levels,
    ax=axes[2, 0],
    cmap=cmap,
    extend="both",
    cbar_kwargs={"label": "EKE Difference"},
)

diff_NAO_neg_eke_plot.eke.T.plot.contourf(
    transform=ccrs.PlateCarree(),
    levels=levels,
    ax=axes[2, 1],
    cmap=cmap,
    extend="both",
    cbar_kwargs={"label": "EKE Difference"},
)

for ax in axes[3, :]:
    ax.coastlines()
    ax.set_extent([-180, 180, 20, 60], crs=ccrs.PlateCarree())
    # add ocean feature
    ax.add_feature(
        cfeature.NaturalEarthFeature(
            "physical", "ocean", "50m", edgecolor="face", facecolor="lightblue"
        )
    )
    # set the position of the ax
pos1 = axes[2, 0].get_position()
axes[3, 0].set_position([pos1.x0, pos1.y0 - 0.32, pos1.width, pos1.width * 1.5])

pos2 = axes[2, 1].get_position()
axes[3, 1].set_position([pos2.x0, pos2.y0 - 0.32, pos2.width, pos2.width * 1.5])

# set aspect
for ax in axes[:3,:].flat:
    ax.set_aspect(5.5)
    # draw hline at y = 0
    ax.axhline(0, color='black', linewidth=1.5, linestyle='dotted')

for ax in axes[:3,0].flat:
    ax.set_ylabel("Lag (days)")
    ax.set_yticks(np.arange(-20, 11, 5), crs=ccrs.PlateCarree())

for ax in axes[3, :].flat:
    ax.set_xticks(np.arange(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels(["180W", "120W", "60W", "0", "60E", "120E"])
    ax.set_xlabel("")

# add a,b,c,d
axes[0, 0].text(-0.2, 1.1, "a", transform=axes[0, 0].transAxes, fontsize=12, fontweight='bold')
axes[0, 1].text(-0.1, 1.1, "b", transform=axes[0, 1].transAxes, fontsize=12, fontweight='bold')
axes[1, 0].text(-0.2, 1.1, "c", transform=axes[1, 0].transAxes, fontsize=12, fontweight='bold')
axes[1, 1].text(-0.1, 1.1, "d", transform=axes[1, 1].transAxes, fontsize=12, fontweight='bold')
axes[2, 0].text(-0.2, 1.1, "e", transform=axes[2, 0].transAxes, fontsize=12, fontweight='bold')
axes[2, 1].text(-0.1, 1.1, "f", transform=axes[2, 1].transAxes, fontsize=12, fontweight='bold')

axes[0,0].set_title("1850-1859 pos")
axes[0,1].set_title("1850-1859 neg")

axes[1,0].set_title("2090-2099 pos")
axes[1,1].set_title("2090-2099 neg")

axes[2,0].set_title("2090-2099 - 1850-1859 pos")
axes[2,1].set_title("2090-2099 - 1850-1859 neg")

# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/NAO_eke_lag.png")
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/mositure_paper_v1/NAO_eke_lag.pdf", dpi = 300, bbox_inches = 'tight')

# %%
