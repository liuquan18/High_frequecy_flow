# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import os
from pathlib import Path


# %%
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator


# %%
heat_dir = "/work/mh0033/m300883/High_frequecy_flow/data/defense/eddy_heat/"
momentum_dir = "/work/mh0033/m300883/High_frequecy_flow/data/defense/eddy_momentum/"
# %%
# read heat
# first
heat_transient_pos_first_df = pd.read_csv(
    os.path.join(heat_dir, "transient_pos_first_df.csv")
)

heat_transient_neg_first_df = pd.read_csv(
    os.path.join(heat_dir, "transient_neg_first_df.csv")
)

# steady first
heat_steady_pos_first_df = pd.read_csv(
    os.path.join(heat_dir, "steady_pos_first_df.csv")
)

heat_steady_neg_first_df = pd.read_csv(
    os.path.join(heat_dir, "steady_neg_first_df.csv")
)

# last
# transient last
heat_transient_pos_last_df = pd.read_csv(
    os.path.join(heat_dir, "transient_pos_last_df.csv")
)
heat_transient_neg_last_df = pd.read_csv(
    os.path.join(heat_dir, "transient_neg_last_df.csv")
)
# steady last
heat_steady_pos_last_df = pd.read_csv(os.path.join(heat_dir, "steady_pos_last_df.csv"))
heat_steady_neg_last_df = pd.read_csv(os.path.join(heat_dir, "steady_neg_last_df.csv"))
# %%
# heat keep time between -20 and 20
heat_transient_pos_first_df = heat_transient_pos_first_df[
    (heat_transient_pos_first_df["time"] >= -20)
    & (heat_transient_pos_first_df["time"] <= 20)
]
heat_transient_neg_first_df = heat_transient_neg_first_df[
    (heat_transient_neg_first_df["time"] >= -20)
    & (heat_transient_neg_first_df["time"] <= 20)
]
heat_steady_pos_first_df = heat_steady_pos_first_df[
    (heat_steady_pos_first_df["time"] >= -20) & (heat_steady_pos_first_df["time"] <= 20)
]
heat_steady_neg_first_df = heat_steady_neg_first_df[
    (heat_steady_neg_first_df["time"] >= -20) & (heat_steady_neg_first_df["time"] <= 20)
]

heat_transient_pos_last_df = heat_transient_pos_last_df[
    (heat_transient_pos_last_df["time"] >= -20)
    & (heat_transient_pos_last_df["time"] <= 20)
]
heat_transient_neg_last_df = heat_transient_neg_last_df[
    (heat_transient_neg_last_df["time"] >= -20)
    & (heat_transient_neg_last_df["time"] <= 20)
]
heat_steady_pos_last_df = heat_steady_pos_last_df[
    (heat_steady_pos_last_df["time"] >= -20) & (heat_steady_pos_last_df["time"] <= 20)
]
heat_steady_neg_last_df = heat_steady_neg_last_df[
    (heat_steady_neg_last_df["time"] >= -20) & (heat_steady_neg_last_df["time"] <= 20)
]

# %%
# read momentum
# first
moment_transient_first_df = pd.read_csv(
    os.path.join(momentum_dir, "transient_first_ano_plev25000.csv")
)
# %%
moment_transient_pos_first_df = moment_transient_first_df[
    moment_transient_first_df["phase"] == "pos"
]
moment_transient_neg_first_df = moment_transient_first_df[
    moment_transient_first_df["phase"] == "neg"
]
# %%
moment_steady_first_df = pd.read_csv(
    os.path.join(momentum_dir, "steady_first_ano_plev25000.csv")
)

moment_steady_pos_first_df = moment_steady_first_df[
    moment_steady_first_df["phase"] == "pos"
]
moment_steady_neg_first_df = moment_steady_first_df[
    moment_steady_first_df["phase"] == "neg"
]
# %%
# last
moment_transient_last_df = pd.read_csv(
    os.path.join(momentum_dir, "transient_last_ano_plev25000.csv")
)
moment_transient_pos_last_df = moment_transient_last_df[
    moment_transient_last_df["phase"] == "pos"
]
moment_transient_neg_last_df = moment_transient_last_df[
    moment_transient_last_df["phase"] == "neg"
]
# %%
moment_steady_last_df = pd.read_csv(
    os.path.join(momentum_dir, "steady_last_ano_plev25000.csv")
)
moment_steady_pos_last_df = moment_steady_last_df[
    moment_steady_last_df["phase"] == "pos"
]
moment_steady_neg_last_df = moment_steady_last_df[
    moment_steady_last_df["phase"] == "neg"
]
# %%

# after imports, increase default font sizes
plt.rcParams.update(
    {
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.labelsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 12,
    }
)

# %%
# share y only within each row
fig, axes = plt.subplots(2, 2, figsize=(12, 10), sharey="row", sharex=True)

# momentum transient first
sns.lineplot(
    data=moment_transient_pos_first_df,
    x="time",
    y="N",
    color="black",
    style="phase",
    ax=axes[0, 0],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
)
sns.lineplot(
    data=moment_transient_neg_first_df,
    x="time",
    y="N",
    color="black",
    linestyle="dashed",
    ax=axes[0, 0],
    errorbar=("ci", 95),
    lw=2,
)

# momentum steady first
sns.lineplot(
    data=moment_steady_pos_first_df,
    x="time",
    y="N",
    color="black",
    ax=axes[0, 1],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
)
sns.lineplot(
    data=moment_steady_neg_first_df,
    x="time",
    y="N",
    color="black",
    linestyle="dashed",
    ax=axes[0, 1],
    errorbar=("ci", 95),
    lw=2,
)

# heat transient first
sns.lineplot(
    data=heat_transient_pos_first_df,
    x="time",
    y="eddy_heat_d2y2",
    color="black",
    ax=axes[1, 0],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
)
sns.lineplot(
    data=heat_transient_neg_first_df,
    x="time",
    y="eddy_heat_d2y2",
    color="black",
    linestyle="dashed",
    ax=axes[1, 0],
    errorbar=("ci", 95),
    lw=2,
)

# heat steady first
sns.lineplot(
    data=heat_steady_pos_first_df,
    x="time",
    y="eddy_heat_d2y2",
    color="black",
    ax=axes[1, 1],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
)
sns.lineplot(
    data=heat_steady_neg_first_df,
    x="time",
    y="eddy_heat_d2y2",
    color="black",
    linestyle="dashed",
    ax=axes[1, 1],
    errorbar=("ci", 95),
    lw=2,
)

# last as red for all axes
# momentum transient last
sns.lineplot(
    data=moment_transient_pos_last_df,
    x="time",
    y="N",
    color="none",
    style="phase",
    ax=axes[0, 0],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
)
sns.lineplot(
    data=moment_transient_neg_last_df,
    x="time",
    y="N",
    color="none",
    linestyle="dashed",
    ax=axes[0, 0],
    errorbar=("ci", 95),
    lw=2,
)
# momentum steady last
sns.lineplot(
    data=moment_steady_pos_last_df,
    x="time",
    y="N",
    color="none",
    ax=axes[0, 1],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
)
sns.lineplot(
    data=moment_steady_neg_last_df,
    x="time",
    y="N",
    color="none",
    linestyle="dashed",
    ax=axes[0, 1],
    errorbar=("ci", 95),
    lw=2,
)
# heat transient last
sns.lineplot(
    data=heat_transient_pos_last_df,
    x="time",
    y="eddy_heat_d2y2",
    color="none",
    ax=axes[1, 0],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
)
sns.lineplot(
    data=heat_transient_neg_last_df,
    x="time",
    y="eddy_heat_d2y2",
    color="none",
    linestyle="dashed",
    ax=axes[1, 0],
    errorbar=("ci", 95),
    lw=2,
)
# heat steady last
sns.lineplot(
    data=heat_steady_pos_last_df,
    x="time",
    y="eddy_heat_d2y2",
    color="none",
    ax=axes[1, 1],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
)
sns.lineplot(
    data=heat_steady_neg_last_df,
    x="time",
    y="eddy_heat_d2y2",
    color="none",
    linestyle="dashed",
    ax=axes[1, 1],
    errorbar=("ci", 95),
    lw=2,
)


# remove top and right spines
for ax in axes.flatten():
    sns.despine(ax=ax)
    # vline at x = 0
    ax.axvline(0, color="gray", linestyle="dotted", lw=2)
    # ensure axis labels and ticks are larger
    ax.tick_params(axis="both", labelsize=20)
    ax.set_ylabel("")
    ax.set_xlabel("Days relative to extreme onset", fontsize=20)

# remove legend
axes[0, 0].legend_.remove()
plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/eddy_line_plot_first.png", dpi=500, bbox_inches="tight", transparent=True)

# %%
