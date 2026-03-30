# %%
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from matplotlib.lines import Line2D

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
#%%
base_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/"
#%%
awb_pos_first_df = pd.read_csv(os.path.join(base_dir, "awb_pos_first_smooth_pv_dy.csv"))
awb_neg_first_df = pd.read_csv(os.path.join(base_dir, "awb_neg_first_smooth_pv_dy.csv"))
awb_pos_last_df = pd.read_csv(os.path.join(base_dir, "awb_pos_last_smooth_pv_dy.csv"))
awb_neg_last_df = pd.read_csv(os.path.join(base_dir, "awb_neg_last_smooth_pv_dy.csv"))

#%%
cwb_pos_first_df = pd.read_csv(os.path.join(base_dir, "cwb_pos_first_smooth_pv_dy.csv"))
cwb_neg_first_df = pd.read_csv(os.path.join(base_dir, "cwb_neg_first_smooth_pv_dy.csv"))
cwb_pos_last_df = pd.read_csv(os.path.join(base_dir, "cwb_pos_last_smooth_pv_dy.csv"))
cwb_neg_last_df = pd.read_csv(os.path.join(base_dir, "cwb_neg_last_smooth_pv_dy.csv"))
#%%
eke_pos_first_df = pd.read_csv(os.path.join(base_dir, "eke_pos_first.csv"))
eke_neg_first_df = pd.read_csv(os.path.join(base_dir, "eke_neg_first.csv"))
eke_pos_last_df = pd.read_csv(os.path.join(base_dir, "eke_pos_last.csv"))
eke_neg_last_df = pd.read_csv(os.path.join(base_dir, "eke_neg_last.csv"))
#%%
baroc_pos_first_df = pd.read_csv(os.path.join(base_dir, "baroc_pos_first.csv"))
baroc_neg_first_df = pd.read_csv(os.path.join(base_dir, "baroc_neg_first.csv"))
baroc_pos_last_df = pd.read_csv(os.path.join(base_dir, "baroc_pos_last.csv"))
baroc_neg_last_df = pd.read_csv(os.path.join(base_dir, "baroc_neg_last.csv"))
#%%
baroc_pos_first_df['eady_growth_rate'] = baroc_pos_first_df['eady_growth_rate'] * 86400
baroc_neg_first_df['eady_growth_rate'] = baroc_neg_first_df['eady_growth_rate'] * 86400
baroc_pos_last_df['eady_growth_rate'] = baroc_pos_last_df['eady_growth_rate'] * 86400
baroc_neg_last_df['eady_growth_rate'] = baroc_neg_last_df['eady_growth_rate'] * 86400

# %%
fig, axes = plt.subplots(
    4,
    2,
    figsize=(10, 15),
    sharey=False,
    gridspec_kw={"hspace": 0.4, "height_ratios": [1, 1, 1, 1]},
)
# Share y-axis within row 1 (momentum) and row 3 (heat) only
axes[1, 1].sharey(axes[1, 0])
axes[3, 1].sharey(axes[3, 0])

def _plot_quartet(ax, pos_first, neg_first, pos_last, neg_last, y):
    """Plot 4 lines (pos/neg × first/last) on one axis."""
    kw = dict(x="time", errorbar=("ci", 95), lw=2, legend=False)
    sns.lineplot(data=pos_first, y=y, color="black", linestyle="solid",  ax=ax, **kw)
    sns.lineplot(data=neg_first, y=y, color="black", linestyle="dashed", ax=ax, **kw)
    sns.lineplot(data=pos_last,  y=y, color="red",   linestyle="solid",  ax=ax, **kw)
    sns.lineplot(data=neg_last,  y=y, color="red",   linestyle="dashed", ax=ax, **kw)

# Row 0: AWB (left), CWB (right)
_plot_quartet(axes[0, 0], awb_pos_first_df, awb_neg_first_df, awb_pos_last_df, awb_neg_last_df, "smooth_pv")
_plot_quartet(axes[0, 1], cwb_pos_first_df, cwb_neg_first_df, cwb_pos_last_df, cwb_neg_last_df, "smooth_pv")

# Row 1: Transient momentum (left), Steady momentum (right)
_plot_quartet(axes[1, 0], moment_transient_pos_first_df, moment_transient_neg_first_df, moment_transient_pos_last_df, moment_transient_neg_last_df, "N")
_plot_quartet(axes[1, 1], moment_steady_pos_first_df, moment_steady_neg_first_df, moment_steady_pos_last_df, moment_steady_neg_last_df, "N")

# Row 2: EKE (left), Baroclinicity (right)
_plot_quartet(axes[2, 0], eke_pos_first_df, eke_neg_first_df, eke_pos_last_df, eke_neg_last_df, "eke")
_plot_quartet(axes[2, 1], baroc_pos_first_df, baroc_neg_first_df, baroc_pos_last_df, baroc_neg_last_df, "eady_growth_rate")

# Row 3: Transient heat (left), Steady heat (right)
_plot_quartet(axes[3, 0], heat_transient_pos_first_df, heat_transient_neg_first_df, heat_transient_pos_last_df, heat_transient_neg_last_df, "eddy_heat_d2y2")
_plot_quartet(axes[3, 1], heat_steady_pos_first_df, heat_steady_neg_first_df, heat_steady_pos_last_df, heat_steady_neg_last_df, "eddy_heat_d2y2")

# ===== Titles =====
axes[0, 0].set_title("AWB")
axes[0, 1].set_title("CWB")
axes[1, 0].set_title("Transient eddies")
axes[1, 1].set_title("Quasi-stationary eddies")
axes[2, 0].set_title("EKE")
axes[2, 1].set_title("Baroclinicity")
axes[3, 0].set_title("Transient eddies")
axes[3, 1].set_title("Quasi-stationary eddies")

# ===== y-labels (left column only) =====
axes[0, 0].set_ylabel("Rossby wave breaking / day")
axes[1, 0].set_ylabel(r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ / m $s^{-1}$ day$^{-1}$")
axes[2, 0].set_ylabel("EKE / m$^2$ s$^{-2}$")
axes[3, 0].set_ylabel(r"$\frac{\partial^2}{\partial y^2} (v'\theta')$ / K $m^{-1}$ s$^{-1}$")
for ax in axes[:, 1]:
    ax.set_ylabel("")
axes[2, 1].set_ylabel("Eady growth rate / day$^{-1}$")

# ===== x-labels (bottom row only) =====
for ax in axes[:3, :].flat:
    ax.set_xlabel("")
for ax in axes[3, :]:
    ax.set_xlabel("Days relative to extreme onset")

for ax in axes.flat:
    sns.despine(ax=ax)
    ax.axvline(0, color="gray", linestyle="dotted", lw=1)

# ===== Legend =====
decade_handles = [
    Line2D([0], [0], color="black", lw=2, label="1850s"),
    Line2D([0], [0], color="red",   lw=2, label="2090s"),
]
phase_handles = [
    Line2D([0], [0], color="black", lw=2, linestyle="-",  label="pos NAO"),
    Line2D([0], [0], color="black", lw=2, linestyle="--", label="neg NAO"),
]
decade_legend = axes[1, 1].legend(
    handles=decade_handles,
    title="decade",
    loc="lower left",
    bbox_to_anchor=(0.1, 0.02),
    frameon=False,
)
axes[1, 1].add_artist(decade_legend)
phase_legend = axes[1, 1].legend(
    handles=phase_handles,
    title="phase",
    loc="lower left",
    bbox_to_anchor=(0.5, 0.02),
    frameon=False,
)

# ===== Panel labels =====
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
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0after_defense/feedback_lines.pdf", dpi=300)


# %%
