# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import importlib

from src.data_helper import read_composite

importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux

# %%
# read transient EP flux for positive and negative phase
Tphi_pos_first, Tp_pos_first, Tdivphi_pos_first, Tdiv_p_pos_first = read_EP_flux(
    phase="pos",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)
Tphi_neg_first, Tp_neg_first, Tdivphi_neg_first, Tdiv_p_neg_first = read_EP_flux(
    phase="neg",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)

# last decade
Tphi_pos_last, Tp_pos_last, Tdivphi_pos_last, Tdiv_p_pos_last = read_EP_flux(
    phase="pos",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)
Tphi_neg_last, Tp_neg_last, Tdivphi_neg_last, Tdiv_p_neg_last = read_EP_flux(
    phase="neg",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)

# %%
# read climatological EP flux
Tphi_clima_first, Tp_clima_first, Tdivphi_clima_first, Tdiv_p_clima_first = (
    read_EP_flux(
        phase="clima",
        decade=1850,
        eddy="transient",
        ano=False,
        lon_mean=False,
        region=None,
    )
)
Tphi_clima_last, Tp_clima_last, Tdivphi_clima_last, Tdiv_p_clima_last = read_EP_flux(
    phase="clima",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)


# %%
def anomaly(ds, ds_clima):
    """
    Calculate the anomaly of a dataset with respect to a climatology.
    """
    # average over time and events
    ds = ds.sel(time=slice(-10, 5)).mean(dim=("time", "event", "lon"))
    ds_clima = ds_clima.mean(dim=("lon"))
    anomaly = ds - ds_clima
    return anomaly.load()


# %%
Tdiv_phi_pos_first_anomaly = anomaly(Tdivphi_pos_first, Tdivphi_clima_first)
Tdiv_phi_neg_first_anomaly = anomaly(Tdivphi_neg_first, Tdivphi_clima_first)
Tdiv_phi_pos_last_anomaly = anomaly(Tdivphi_pos_last, Tdivphi_clima_last)
Tdiv_phi_neg_last_anomaly = anomaly(Tdivphi_neg_last, Tdivphi_clima_last)

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
phi_trans_levels = np.arange(-0.18, 0.19, 0.06)

fig, axes = plt.subplots(
    3,
    2,
    figsize=(10, 12),
    sharey="row",
    gridspec_kw={"hspace": 0.4, "height_ratios": [1, 0.9, 0.9]},
)

# ===== Row 1: Contour plots =====
# first col: positive phase
cf_phi_trans = (Tdiv_phi_pos_first_anomaly).plot.contourf(
    ax=axes[0, 0],
    levels=phi_trans_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    xlim=(0, 90),
    ylim=(100000, 10000),
)
contour_levels = [l for l in phi_trans_levels if l != 0]
(Tdiv_phi_pos_last_anomaly).plot.contour(
    ax=axes[0, 0],
    levels=contour_levels,
    colors="k",
    linewidths=1,
    add_colorbar=False,
    xlim=(0, 90),
    ylim=(100000, 10000),
)

# second col: negative phase
cf_phi_trans_neg = (Tdiv_phi_neg_first_anomaly).plot.contourf(
    ax=axes[0, 1],
    levels=phi_trans_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    xlim=(0, 90),
    ylim=(100000, 10000),
)
contour_levels = [l for l in phi_trans_levels if l != 0]
(Tdiv_phi_neg_last_anomaly).plot.contour(
    ax=axes[0, 1],
    levels=contour_levels,
    colors="k",
    linewidths=1,
    add_colorbar=False,
    xlim=(0, 90),
    ylim=(100000, 10000),
)

# ===== Row 2: Momentum line plots =====
# transient momentum (left col)
sns.lineplot(
    data=moment_transient_pos_first_df,
    x="time",
    y="N",
    color="black",
    ax=axes[1, 0],
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
    ax=axes[1, 0],
    errorbar=("ci", 95),
    lw=2,
    legend=False,
)
sns.lineplot(
    data=moment_transient_pos_last_df,
    x="time",
    y="N",
    color="red",
    ax=axes[1, 0],
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
    ax=axes[1, 0],
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
    ax=axes[1, 1],
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
    ax=axes[1, 1],
    errorbar=("ci", 95),
    lw=2,
    legend=False,
)
sns.lineplot(
    data=moment_steady_pos_last_df,
    x="time",
    y="N",
    color="red",
    ax=axes[1, 1],
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
    ax=axes[1, 1],
    errorbar=("ci", 95),
    lw=2,
    legend=False,
)

# ===== Row 3: Heat line plots =====
# transient heat (left col)
sns.lineplot(
    data=heat_transient_pos_first_df,
    x="time",
    y="eddy_heat_d2y2",
    color="black",
    ax=axes[2, 0],
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
    ax=axes[2, 0],
    errorbar=("ci", 95),
    lw=2,
    legend=False,
)
sns.lineplot(
    data=heat_transient_pos_last_df,
    x="time",
    y="eddy_heat_d2y2",
    color="red",
    ax=axes[2, 0],
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
    ax=axes[2, 0],
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
    ax=axes[2, 1],
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
    ax=axes[2, 1],
    errorbar=("ci", 95),
    lw=2,
    legend=False,
)
sns.lineplot(
    data=heat_steady_pos_last_df,
    x="time",
    y="eddy_heat_d2y2",
    color="red",
    ax=axes[2, 1],
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
    ax=axes[2, 1],
    errorbar=("ci", 95),
    lw=2,
    legend=False,
)

# Add colorbar for contour plots
cbar = fig.colorbar(
    cf_phi_trans,
    ax=axes[0, :],
    orientation="horizontal",
    fraction=0.046,
    pad=0.12,
    label=r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ / m $s^{-1}$ day $^{-1}$",
)

# Set y-axis labels for contour plots (row 1)
axes[0, 0].set_ylabel("Pressure / hPa")
axes[0, 0].set_yticks(
    [100000, 90000, 80000, 70000, 60000, 50000, 40000, 30000, 20000, 10000]
)
axes[0, 0].set_yticklabels([str(int(tick / 100)) for tick in axes[0, 0].get_yticks()])
axes[0, 1].set_ylabel("")

# Set titles and labels for contour plots
for ax in axes[0, :]:
    ax.set_title("")
    ax.set_xlabel("lat [°N]")

# Set labels for line plots (rows 2-3)
axes[1, 0].set_ylabel(
    r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ / m $s^{-1}$ day $^{-1}$"
)
axes[2, 0].set_ylabel(
    r"$-\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta'}}{\overline{\theta}_p} \right)$ / m $s^{-1}$ day $^{-1}$"
)

for ax in axes[1:, :].flat:
    ax.set_xlabel("Days relative to extreme onset")
    sns.despine(ax=ax)
    ax.axvline(0, color="gray", linestyle="dotted", lw=1)

axes[1, 1].set_ylabel("")
axes[2, 1].set_ylabel("")

# Add a, b, c, d, e, f labels
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
