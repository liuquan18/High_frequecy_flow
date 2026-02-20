# %%
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

# %%
# Read line plot data
heat_dir = "/work/mh0033/m300883/High_frequecy_flow/data/defense/eddy_heat/"
momentum_dir = "/work/mh0033/m300883/High_frequecy_flow/data/defense/eddy_momentum/"

# read heat data
heat_transient_pos_first_df = pd.read_csv(
    os.path.join(heat_dir, "transient_pos_first_df.csv")
)
heat_transient_neg_first_df = pd.read_csv(
    os.path.join(heat_dir, "transient_neg_first_df.csv")
)
heat_steady_pos_first_df = pd.read_csv(
    os.path.join(heat_dir, "steady_pos_first_df.csv")
)
heat_steady_neg_first_df = pd.read_csv(
    os.path.join(heat_dir, "steady_neg_first_df.csv")
)
heat_transient_pos_last_df = pd.read_csv(
    os.path.join(heat_dir, "transient_pos_last_df.csv")
)
heat_transient_neg_last_df = pd.read_csv(
    os.path.join(heat_dir, "transient_neg_last_df.csv")
)
heat_steady_pos_last_df = pd.read_csv(os.path.join(heat_dir, "steady_pos_last_df.csv"))
heat_steady_neg_last_df = pd.read_csv(os.path.join(heat_dir, "steady_neg_last_df.csv"))

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

# read momentum data
moment_transient_first_df = pd.read_csv(
    os.path.join(momentum_dir, "transient_first_ano_plev25000.csv")
)
moment_transient_pos_first_df = moment_transient_first_df[
    moment_transient_first_df["phase"] == "pos"
]
moment_transient_neg_first_df = moment_transient_first_df[
    moment_transient_first_df["phase"] == "neg"
]

moment_steady_first_df = pd.read_csv(
    os.path.join(momentum_dir, "steady_first_ano_plev25000.csv")
)
moment_steady_pos_first_df = moment_steady_first_df[
    moment_steady_first_df["phase"] == "pos"
]
moment_steady_neg_first_df = moment_steady_first_df[
    moment_steady_first_df["phase"] == "neg"
]

moment_transient_last_df = pd.read_csv(
    os.path.join(momentum_dir, "transient_last_ano_plev25000.csv")
)
moment_transient_pos_last_df = moment_transient_last_df[
    moment_transient_last_df["phase"] == "pos"
]
moment_transient_neg_last_df = moment_transient_last_df[
    moment_transient_last_df["phase"] == "neg"
]

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
fig, axes = plt.subplots(
    2,
    2,
    figsize=(10, 8),
    sharey="row",
    gridspec_kw={"hspace": 0.4, "height_ratios": [1, 1]},
)

# ===== Row 1: Momentum line plots =====
# transient momentum (left col)
sns.lineplot(
    data=moment_transient_pos_first_df,
    x="time",
    y="N",
    color="black",
    ax=axes[0, 0],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
    legend=False,
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
    legend=False,
)
sns.lineplot(
    data=moment_transient_pos_last_df,
    x="time",
    y="N",
    color="red",
    ax=axes[0, 0],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
    legend=False,
)
sns.lineplot(
    data=moment_transient_neg_last_df,
    x="time",
    y="N",
    color="red",
    linestyle="dashed",
    ax=axes[0, 0],
    errorbar=("ci", 95),
    lw=2,
    legend=False,
)

# steady momentum (right col)
sns.lineplot(
    data=moment_steady_pos_first_df,
    x="time",
    y="N",
    color="black",
    ax=axes[0, 1],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
    legend=False,
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
    legend=False,
)
sns.lineplot(
    data=moment_steady_pos_last_df,
    x="time",
    y="N",
    color="red",
    ax=axes[0, 1],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
    legend=False,
)
sns.lineplot(
    data=moment_steady_neg_last_df,
    x="time",
    y="N",
    color="red",
    linestyle="dashed",
    ax=axes[0, 1],
    errorbar=("ci", 95),
    lw=2,
    legend=False,
)

# ===== Row 2: Heat line plots =====
# transient heat (left col)
sns.lineplot(
    data=heat_transient_pos_first_df,
    x="time",
    y="eddy_heat_d2y2",
    color="black",
    ax=axes[1, 0],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
    legend=False,
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
    legend=False,
)
sns.lineplot(
    data=heat_transient_pos_last_df,
    x="time",
    y="eddy_heat_d2y2",
    color="red",
    ax=axes[1, 0],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
    legend=False,
)
sns.lineplot(
    data=heat_transient_neg_last_df,
    x="time",
    y="eddy_heat_d2y2",
    color="red",
    linestyle="dashed",
    ax=axes[1, 0],
    errorbar=("ci", 95),
    lw=2,
    legend=False,
)

# steady heat (right col)
sns.lineplot(
    data=heat_steady_pos_first_df,
    x="time",
    y="eddy_heat_d2y2",
    color="black",
    ax=axes[1, 1],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
    legend=False,
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
    legend=False,
)
sns.lineplot(
    data=heat_steady_pos_last_df,
    x="time",
    y="eddy_heat_d2y2",
    color="red",
    ax=axes[1, 1],
    errorbar=("ci", 95),
    linestyle="solid",
    lw=2,
    legend=False,
)
sns.lineplot(
    data=heat_steady_neg_last_df,
    x="time",
    y="eddy_heat_d2y2",
    color="red",
    linestyle="dashed",
    ax=axes[1, 1],
    errorbar=("ci", 95),
    lw=2,
    legend=False,
)

# Set labels for line plots
axes[0, 0].set_ylabel(
    r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ / m $s^{-1}$ day $^{-1}$"
)
axes[1, 0].set_ylabel(
    r"$-\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta'}}{\overline{\theta}_p} \right)$ / m $s^{-1}$ day $^{-1}$"
)

for ax in axes[:, :].flat:
    ax.set_xlabel("Days relative to extreme onset")
    sns.despine(ax=ax)
    ax.axvline(0, color="gray", linestyle="dotted", lw=1)

axes[0, 1].set_ylabel("")
axes[1, 1].set_ylabel("")

# Add a, b, c, d labels
for i, ax in enumerate(axes.flat):
    ax.text(
        -0.08,
        1.02,
        chr(97 + i),
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        va="bottom",
        ha="right",
    )

plt.tight_layout()

# Save figure
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0after_defense/eddy_momentum_heat_combined.pdf",
    dpi=300,
    bbox_inches="tight",
    transparent=True,
)
# %%
