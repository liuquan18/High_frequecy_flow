# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line, lat2y, lon2x
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns
from src.data_helper.read_NAO_extremes import read_NAO_extremes
from src.data_helper.read_variable import read_climatology_decmean
import glob

import logging

logging.basicConfig(level=logging.INFO)


# %% NAO
def NAO_extremes(return_days=False, threshold=7):
    NAO_pos_counts = pd.DataFrame(columns=["decade", "count"])
    NAO_neg_counts = pd.DataFrame(columns=["decade", "count"])

    for i, dec in enumerate(range(1850, 2100, 10)):
        NAO_pos = read_NAO_extremes(dec, "positive")
        NAO_neg = read_NAO_extremes(dec, "negative")

        # filter only duration above 7 days
        NAO_pos = NAO_pos[NAO_pos["extreme_duration"] >= threshold]
        NAO_neg = NAO_neg[NAO_neg["extreme_duration"] >= threshold]

        if return_days:
            # NAO duration sum
            NAO_pos_count = NAO_pos["extreme_duration"].sum() / 50
            NAO_neg_count = NAO_neg["extreme_duration"].sum() / 50

        else:
            NAO_pos_count = NAO_pos.shape[0] / 50
            NAO_neg_count = NAO_neg.shape[0] / 50

        NAO_pos_counts.loc[i] = [dec, NAO_pos_count]
        NAO_neg_counts.loc[i] = [dec, NAO_neg_count]

    return NAO_pos_counts, NAO_neg_counts


# %%
NAO_pos_count, NAO_neg_count = NAO_extremes(False, 5)
NAO_pos_days, NAO_neg_days = NAO_extremes(True, 5)
# %%
NAO_pos_days = NAO_pos_days.rename(columns={"count": "days"})
NAO_neg_days = NAO_neg_days.rename(columns={"count": "days"})
# %%
NAO_count_merge = pd.merge(
    NAO_pos_count, NAO_neg_count, on="decade", suffixes=("_pos", "_neg")
)
NAO_days_merge = pd.merge(
    NAO_pos_days, NAO_neg_days, on="decade", suffixes=("_pos", "_neg")
)
NAO_merge = pd.merge(NAO_count_merge, NAO_days_merge, on="decade")
# %%
NAO_merge["decade"] = NAO_merge["decade"].astype(int)

# %%
jet = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/ua_decmean_ensmean_25000hPa.nc"
)
baroclinic = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/eady_growth_rate_decmean_ensmean_85000hPa.nc"
)

transient_momentum = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/Fdiv_phi_transient_decmean_ensmean_25000hPa.nc"
)
steady_momentum = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/Fdiv_phi_steady_decmean_ensmean_25000hPa.nc"
)

sum_momentum = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/Fdiv_phi_transient_Fdiv_phi_steady_sum_decmean_ensmean_25000hPa.nc"
)

transient_heat = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/transient_eddy_heat_d2y2_decmean_ensmean_85000hPa.nc"
)
steady_heat = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/steady_eddy_heat_d2y2_decmean_ensmean_85000hPa.nc"
)


# %%
def to_dataframe(ds, var_name, base=None):
    """Convert xarray dataset to pandas DataFrame."""
    df = ds["std"].squeeze().to_dataframe(var_name).reset_index()
    df["decade"] = (df["time"].dt.year // 10) * 10

    if base is None:
        # use the same
        base = df[df["decade"] == 1850][var_name].values[0]
    else:
        base = base["std"].squeeze().to_dataframe(var_name).reset_index()
        base["decade"] = (base["time"].dt.year // 10) * 10
        base = base[base["decade"] == 1850][var_name].values[0]

    # standardize the var_name coloumn name
    df[var_name] = df[var_name] / base
    return df


# %%
jet = to_dataframe(jet, "jet_stream")
baroclinic = to_dataframe(baroclinic, "baroclinic")
transient_heat = to_dataframe(transient_heat, "heat_flux")
steady_heat = to_dataframe(steady_heat, "heat_flux")

# %%
transient_momentum = to_dataframe(transient_momentum, "momentum_flux")
steady_momentum = to_dataframe(steady_momentum, "momentum_flux")
sum_momentum = to_dataframe(sum_momentum, "momentum_flux_sum")

# %%
awbs = xr.open_mfdataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_anticyclonic_fldmean/*.nc",
    combine="by_coords",
)

# %%
cwbs = xr.open_mfdataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_cyclonic_fldmean/*.nc",
    combine="by_coords",
)
# %%
awbs_df = awbs.to_dataframe().reset_index()
cwbs_df = cwbs.to_dataframe().reset_index()

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
fig, axes = plt.subplots(4, 1, figsize=(6, 12))
fig.subplots_adjust(hspace=0.06)

# NAO
sns.lineplot(
    data=NAO_merge,
    x="decade",
    y="days_pos",
    ax=axes[0],
    label="pos NAO",
    color="k",
    linewidth=2,
)
sns.lineplot(
    data=NAO_merge,
    x="decade",
    y="days_neg",
    ax=axes[0],
    label="neg NAO",
    color="k",
    linestyle="--",
    linewidth=2,
)

# wave breaking
sns.lineplot(
    data=awbs_df,
    x="decade",
    y="flag",
    ax=axes[1],
    label="anticyclonic",
    color="k",
    linewidth=2,
)
sns.lineplot(
    data=cwbs_df,
    x="decade",
    y="flag",
    ax=axes[1],
    label="cyclonic",
    color="k",
    linestyle="--",
    linewidth=2,
)

# momentum flux
sns.lineplot(
    data=sum_momentum,
    x="decade",
    y="momentum_flux_sum",
    ax=axes[2],
    label="transient + stationary",
    color="k",
    linestyle=":",
    linewidth=2,
)
sns.lineplot(
    data=transient_momentum,
    x="decade",
    y="momentum_flux",
    ax=axes[2],
    label="transient",
    color="k",
    linewidth=2,
)

# heat flux
sns.lineplot(
    data=transient_heat,
    x="decade",
    y="heat_flux",
    ax=axes[3],
    label="transient",
    color="k",
    linewidth=2,
)
sns.lineplot(
    data=steady_heat,
    x="decade",
    y="heat_flux",
    ax=axes[3],
    label="stationary",
    color="k",
    linestyle="--",
    linewidth=2,
)

# format axes: alternate y-axis side, show only bottom spine on last row, hide top spine everywhere
for i, ax in enumerate(axes):
    ax.spines["top"].set_visible(False)
    # alternate y-axis side: even indices -> left, odd -> right
    if i % 2 == 0:
        ax.yaxis.set_label_position("left")
        ax.yaxis.tick_left()
        ax.spines["left"].set_visible(True)
        ax.spines["right"].set_visible(False)
        visible_spine = "left"
    else:
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        ax.spines["right"].set_visible(True)
        ax.spines["left"].set_visible(False)
        visible_spine = "right"
    # only last row shows bottom spine and x tick labels
    ax.spines["bottom"].set_visible(i == 3)
    if i != 3:
        # remove x ticks and labels on top three subplots
        ax.tick_params(
            axis="x", which="both", bottom=False, top=False, labelbottom=False
        )
    else:
        # ensure bottom subplot has x ticks/labels (if you want them)
        ax.tick_params(axis="x", which="both", bottom=True, top=False, labelbottom=True)
    ax.tick_params(axis="both", labelsize=14)

    # set y-axis color to match the primary line color (first line plotted on this ax)
    lines = ax.get_lines()
    axis_color = lines[0].get_color() if len(lines) > 0 else "k"
    # color the visible spine
    ax.spines[visible_spine].set_color(axis_color)
    # color tick labels and y label
    ax.tick_params(axis="y", colors=axis_color)
    if ax.yaxis.get_label() is not None:
        ax.yaxis.label.set_color(axis_color)

    leg = ax.get_legend()
    if leg is not None:
        ax.legend(
            loc="lower center",
            bbox_to_anchor=(0.5, -0.22),
            ncol=1,
            fontsize=12,
            frameon=False,
        )

axes[0].set_ylabel("extreme NAO days", fontsize=14)
axes[1].set_ylabel("wave breaking days", fontsize=14)
axes[2].set_ylabel(r"std of $-\partial \overline{u'v'}/\partial y$", fontsize=14)
axes[3].set_ylabel(
    r"std of $\partial^2 \overline{v'\theta'}/\partial y^2$", fontsize=14
)

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/GHG_forced_changes.png",
    dpi=500,
    bbox_inches="tight",
    metadata={"Creator": __file__},
    transparent=True,
)
# %%
fig, axes = plt.subplots(2, 1, figsize=(6, 8))
fig.subplots_adjust(hspace=0.06)

# momentum flux (top)
sns.lineplot(
    data=sum_momentum,
    x="decade",
    y="momentum_flux_sum",
    ax=axes[0],
    label="transient + stationary",
    color="k",
    linestyle=":",
    linewidth=2,
)
sns.lineplot(
    data=transient_momentum,
    x="decade",
    y="momentum_flux",
    ax=axes[0],
    label="transient",
    color="k",
    linewidth=2,
)

# heat flux (bottom)
sns.lineplot(
    data=transient_heat,
    x="decade",
    y="heat_flux",
    ax=axes[1],
    label="transient",
    color="k",
    linewidth=2,
)
sns.lineplot(
    data=steady_heat,
    x="decade",
    y="heat_flux",
    ax=axes[1],
    label="stationary",
    color="k",
    linestyle="--",
    linewidth=2,
)

# format 2-row axes: top -> left y-axis, bottom -> right y-axis (per user request alternate)
for i, ax in enumerate(axes):
    ax.spines["top"].set_visible(False)
    if i % 2 == 0:
        ax.yaxis.set_label_position("left")
        ax.yaxis.tick_left()
        ax.spines["left"].set_visible(True)
        ax.spines["right"].set_visible(False)
        visible_spine = "left"
    else:
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        ax.spines["right"].set_visible(True)
        ax.spines["left"].set_visible(False)
        visible_spine = "right"
    # only bottom subplot shows bottom spine
    ax.spines["bottom"].set_visible(i == (len(axes) - 1))
    if i != (len(axes) - 1):
        ax.tick_params(labelbottom=False)
    ax.tick_params(axis="both", labelsize=14)

    # color y-axis to match the primary line
    lines = ax.get_lines()
    axis_color = lines[0].get_color() if len(lines) > 0 else "k"
    ax.spines[visible_spine].set_color(axis_color)
    ax.tick_params(axis="y", colors=axis_color)
    if ax.yaxis.get_label() is not None:
        ax.yaxis.label.set_color(axis_color)

axes[0].legend(frameon=False, fontsize=12)
axes[1].legend(frameon=False, fontsize=12)
axes[0].set_ylabel("")
axes[1].set_ylabel("")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/decade_poster.pdf",
    dpi=500,
    bbox_inches="tight",
    transparent=True,
)
# %%
fig, axes = plt.subplots(4, 1, figsize=(6, 8))
plt.subplots_adjust(hspace=0.2)


# NAO
sns.lineplot(
    data=NAO_merge,
    x="decade",
    y="days_pos",
    ax=axes[0],
    label="pos NAO",
    color="#FF514A",
    linewidth=1.5,
)
sns.lineplot(
    data=NAO_merge,
    x="decade",
    y="days_neg",
    ax=axes[0],
    label="neg NAO",
    color="#FF514A",
    linestyle="--",
    linewidth=1.5,
)

# wave breaking
sns.lineplot(
    data=awbs_df,
    x="decade",
    y="flag",
    ax=axes[1],
    label="anticyclonic",
    color="#006E66",
    linewidth=1.5,
)
sns.lineplot(
    data=cwbs_df,
    x="decade",
    y="flag",
    ax=axes[1],
    label="cyclonic",
    color="#006E66",
    linestyle="--",
    linewidth=1.5,
)

# momentum flux
sns.lineplot(
    data=sum_momentum,
    x="decade",
    y="momentum_flux_sum",
    ax=axes[2],
    label="transient + stationary",
    color="k",
    linestyle=":",
    linewidth=1.5,
)
sns.lineplot(
    data=transient_momentum,
    x="decade",
    y="momentum_flux",
    ax=axes[2],
    label="transient",
    color="k",
    linewidth=1.5,
)

# heat flux
sns.lineplot(
    data=transient_heat,
    x="decade",
    y="heat_flux",
    ax=axes[3],
    label="transient",
    color="k",
    linewidth=1.5,
)
sns.lineplot(
    data=steady_heat,
    x="decade",
    y="heat_flux",
    ax=axes[3],
    label="stationary",
    color="k",
    linestyle="--",
    linewidth=1.5,
)

for i, ax in enumerate(axes):
    ax.spines["top"].set_visible(False)
    ax.set_facecolor("none")
    ax.set_ylabel("")
    # remove all ticks at x-axis except bottom plot
    if i % 2 == 0:
        ax.yaxis.set_label_position("left")
        ax.yaxis.tick_left()
        ax.spines["left"].set_visible(True)
        ax.spines["right"].set_visible(False)
        visible_spine = "left"
        # set color

    else:
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        ax.spines["right"].set_visible(True)
        ax.spines["left"].set_visible(False)
        visible_spine = "right"
    ax.spines["bottom"].set_visible(i == 3)
    if i != 3:
        # remove x ticks and labels on top three subplots
        ax.tick_params(
            axis="x", which="both", bottom=False, top=False, labelbottom=False
        )
    else:
        ax.tick_params(axis="x", which="both", bottom=True, top=False, labelbottom=True)
    ax.set_xlabel("")
    # remove legends and label them next to the lines
    leg = ax.get_legend()
    if leg is not None:
        ax.legend().remove()

    # color the visible y-axis to match the primary line on this axis
    lines = ax.get_lines()
    axis_color = lines[0].get_color() if len(lines) > 0 else "k"
    ax.spines[visible_spine].set_color(axis_color)
    ax.tick_params(axis="y", colors=axis_color)
    if ax.yaxis.get_label() is not None:
        ax.yaxis.label.set_color(axis_color)

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/GHG_forced_changes_nolegend.png",
    dpi=500,
    bbox_inches="tight",
    metadata={"Creator": __file__},
    transparent=True,
)
# %%
