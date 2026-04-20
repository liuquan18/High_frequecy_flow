# %%
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

from matplotlib.lines import Line2D

from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec

#%%
# Load dataframes from saved CSV files

def _load_csv(name, anomaly=False):
    if anomaly:
        load_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pd/anomaly"
    else:
        load_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pd/non_anomaly"
    return pd.read_csv(os.path.join(load_dir, f"{name}.csv"))

#%%
# non ano
awb_pos_first_df = _load_csv("awb_pos_first_df")
awb_neg_first_df = _load_csv("awb_neg_first_df")
awb_pos_last_df = _load_csv("awb_pos_last_df")
awb_neg_last_df = _load_csv("awb_neg_last_df")

# the old data was averaged over isentropic levels, rather than summed.
awb_pos_first_df["awb"] *= 13 # 13 levels
awb_neg_first_df["awb"] *= 13
awb_pos_last_df["awb"] *= 13
awb_neg_last_df["awb"] *= 13


#%%
cwb_pos_first_df = _load_csv("cwb_pos_first_df")
cwb_neg_first_df = _load_csv("cwb_neg_first_df")
cwb_pos_last_df = _load_csv("cwb_pos_last_df")
cwb_neg_last_df = _load_csv("cwb_neg_last_df")
#
cwb_pos_first_df["cwb"] *= 13 # 13 levels
cwb_neg_first_df["cwb"] *= 13
cwb_pos_last_df["cwb"] *= 13
cwb_neg_last_df["cwb"] *= 13

Fdiv_transient_pos_first_df = _load_csv("Fdiv_transient_pos_first_df")
Fdiv_transient_neg_first_df = _load_csv("Fdiv_transient_neg_first_df")
Fdiv_transient_pos_last_df = _load_csv("Fdiv_transient_pos_last_df")
Fdiv_transient_neg_last_df = _load_csv("Fdiv_transient_neg_last_df")

Fdiv_steady_pos_first_df = _load_csv("Fdiv_steady_pos_first_df")
Fdiv_steady_neg_first_df = _load_csv("Fdiv_steady_neg_first_df")
Fdiv_steady_pos_last_df = _load_csv("Fdiv_steady_pos_last_df")
Fdiv_steady_neg_last_df = _load_csv("Fdiv_steady_neg_last_df")

#%%

eke_pos_first_df = _load_csv("eke_pos_first_df")
eke_neg_first_df = _load_csv("eke_neg_first_df")
eke_pos_last_df = _load_csv("eke_pos_last_df")
eke_neg_last_df = _load_csv("eke_neg_last_df")

baroc_pos_first_df = _load_csv("baroc_pos_first_df")    
baroc_neg_first_df = _load_csv("baroc_neg_first_df")
baroc_pos_last_df = _load_csv("baroc_pos_last_df")    
baroc_neg_last_df = _load_csv("baroc_neg_last_df")

# anomaly
transient_eddy_heat_d2y2_pos_first_df = _load_csv("transient_eddy_heat_d2y2_pos_first_df", anomaly=True)
transient_eddy_heat_d2y2_neg_first_df = _load_csv("transient_eddy_heat_d2y2_neg_first_df", anomaly=True)
transient_eddy_heat_d2y2_pos_last_df = _load_csv("transient_eddy_heat_d2y2_pos_last_df", anomaly=True)
transient_eddy_heat_d2y2_neg_last_df = _load_csv("transient_eddy_heat_d2y2_neg_last_df", anomaly=True)

steady_eddy_heat_d2y2_pos_first_df = _load_csv("steady_eddy_heat_d2y2_pos_first_df", anomaly=True)
steady_eddy_heat_d2y2_neg_first_df = _load_csv("steady_eddy_heat_d2y2_neg_first_df", anomaly=True)
steady_eddy_heat_d2y2_pos_last_df = _load_csv("steady_eddy_heat_d2y2_pos_last_df", anomaly=True)
steady_eddy_heat_d2y2_neg_last_df = _load_csv("steady_eddy_heat_d2y2_neg_last_df", anomaly=True)

#%%
def mean_diff_vs_1std(first_df, last_df, var_name):
    """Return mean(last)-mean(first) per time step.
    Significance threshold: 95% CI half-width of first (1.96 * SEM),
    consistent with the seaborn errorbar=("ci", 95) shading.
    """
    first_stats = (
        first_df.groupby("time")[var_name]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    first_stats.columns = ["time", "first_mean", "first_std", "first_n"]
    # 95% CI half-width (matches seaborn shading for large n)
    first_stats["ci95"] = 1.96 * first_stats["first_std"] / first_stats["first_n"].pow(0.5)

    last_mean = last_df.groupby("time")[var_name].mean().reset_index()
    last_mean.columns = ["time", "last_mean"]

    result = first_stats.merge(last_mean, on="time")
    result["diff"] = result["last_mean"] - result["first_mean"]
    return result

fig = plt.figure(figsize=(10, 18))
gs = GridSpec(
    11, 2, figure=fig,
    height_ratios=[3, 1, 0.5, 3, 1, 0.5, 3, 1, 0.5, 3, 1],
    hspace=0.08, wspace=0.35,
)

# Main axes (rows 0,3,6,9) and bar axes (rows 1,4,7,10); rows 2,5,8 are spacers
main_axes = [[fig.add_subplot(gs[3 * r, c]) for c in range(2)] for r in range(4)]
bar_axes  = [[fig.add_subplot(gs[3 * r + 1, c], sharex=main_axes[r][c]) for c in range(2)] for r in range(4)]

# Share y-axis within row 1 (momentum) and row 3 (heat)
main_axes[1][1].sharey(main_axes[1][0])
main_axes[3][1].sharey(main_axes[3][0])
bar_axes[0][1].sharey(bar_axes[0][0])
bar_axes[1][1].sharey(bar_axes[1][0])

COLOR_POS = "#E57200"  # MPI orange
COLOR_NEG = "#006C66"  # MPI green

def _plot_quartet(ax, pos_first, neg_first, pos_last, neg_last, y):
    """Plot 4 lines (pos/neg × first/last) on one axis."""
    kw = dict(x="time", errorbar=("ci", 95), lw=2, legend=False)
    sns.lineplot(data=pos_first, y=y, color=COLOR_POS, linestyle="solid",  ax=ax, **kw)
    sns.lineplot(data=neg_first, y=y, color=COLOR_NEG, linestyle="solid",  ax=ax, **kw)
    sns.lineplot(data=pos_last,  y=y, color=COLOR_POS, linestyle="dashed", ax=ax, **kw)
    sns.lineplot(data=neg_last,  y=y, color=COLOR_NEG, linestyle="dashed", ax=ax, **kw)

def _plot_diff_bars(ax, pos_first, neg_first, pos_last, neg_last, var_name):
    """Bar subplot: mean(last)-mean(first) per time step.
    Positive phase: orange; significant if diff > 95% CI half-width of first.
    Negative phase: green;  significant if diff < -95% CI half-width of first.
    Non-significant bars use alpha=0.2.
    """
    pos_diff = mean_diff_vs_1std(pos_first, pos_last, var_name)
    neg_diff = mean_diff_vs_1std(neg_first, neg_last, var_name)
    for _, row in pos_diff.iterrows():
        significant = row["diff"] > row["ci95"]
        ax.bar(row["time"], row["diff"],
               color=COLOR_POS if significant else "none",
               alpha=0.5 if significant else 1.0,
               edgecolor=COLOR_POS, linewidth=0.8, width=1.0)
    for _, row in neg_diff.iterrows():
        significant = row["diff"] < -row["ci95"]
        ax.bar(row["time"], row["diff"],
               color=COLOR_NEG if significant else "none",
               alpha=0.5 if significant else 1.0,
               edgecolor=COLOR_NEG, linewidth=0.8, width=1.0)
    ax.axhline(0, color="k", lw=0.5)
    sns.despine(ax=ax, bottom=True)
    ax.tick_params(bottom=False)

# ===== Row 0: AWB / CWB =====
_plot_quartet(main_axes[0][0], awb_pos_first_df, awb_neg_first_df, awb_pos_last_df, awb_neg_last_df, "awb")
_plot_quartet(main_axes[0][1], cwb_pos_first_df, cwb_neg_first_df, cwb_pos_last_df, cwb_neg_last_df, "cwb")
_plot_diff_bars(bar_axes[0][0], awb_pos_first_df, awb_neg_first_df, awb_pos_last_df, awb_neg_last_df, "awb")
_plot_diff_bars(bar_axes[0][1], cwb_pos_first_df, cwb_neg_first_df, cwb_pos_last_df, cwb_neg_last_df, "cwb")

# ===== Row 1: Transient momentum / Steady momentum =====
_plot_quartet(main_axes[1][0], Fdiv_transient_pos_first_df, Fdiv_transient_neg_first_df, Fdiv_transient_pos_last_df, Fdiv_transient_neg_last_df, "Fdiv_transient")
_plot_quartet(main_axes[1][1], Fdiv_steady_pos_first_df, Fdiv_steady_neg_first_df, Fdiv_steady_pos_last_df, Fdiv_steady_neg_last_df, "Fdiv_steady")
_plot_diff_bars(bar_axes[1][0], Fdiv_transient_pos_first_df, Fdiv_transient_neg_first_df, Fdiv_transient_pos_last_df, Fdiv_transient_neg_last_df, "Fdiv_transient")
_plot_diff_bars(bar_axes[1][1], Fdiv_steady_pos_first_df, Fdiv_steady_neg_first_df, Fdiv_steady_pos_last_df, Fdiv_steady_neg_last_df, "Fdiv_steady")

# ===== Row 2: EKE / Baroclinicity =====
_plot_quartet(main_axes[2][0], eke_pos_first_df, eke_neg_first_df, eke_pos_last_df, eke_neg_last_df, "eke")
_plot_quartet(main_axes[2][1], baroc_pos_first_df, baroc_neg_first_df, baroc_pos_last_df, baroc_neg_last_df, "baroclinicity")
_plot_diff_bars(bar_axes[2][0], eke_pos_first_df, eke_neg_first_df, eke_pos_last_df, eke_neg_last_df, "eke")
_plot_diff_bars(bar_axes[2][1], baroc_pos_first_df, baroc_neg_first_df, baroc_pos_last_df, baroc_neg_last_df, "baroclinicity")

# ===== Row 3: Transient heat / Steady heat =====
_plot_quartet(main_axes[3][0], transient_eddy_heat_d2y2_pos_first_df, transient_eddy_heat_d2y2_neg_first_df, transient_eddy_heat_d2y2_pos_last_df, transient_eddy_heat_d2y2_neg_last_df, "transient_eddy_heat_d2y2")
_plot_quartet(main_axes[3][1], steady_eddy_heat_d2y2_pos_first_df, steady_eddy_heat_d2y2_neg_first_df, steady_eddy_heat_d2y2_pos_last_df, steady_eddy_heat_d2y2_neg_last_df, "steady_eddy_heat_d2y2")
_plot_diff_bars(bar_axes[3][0], transient_eddy_heat_d2y2_pos_first_df, transient_eddy_heat_d2y2_neg_first_df, transient_eddy_heat_d2y2_pos_last_df, transient_eddy_heat_d2y2_neg_last_df, "transient_eddy_heat_d2y2")
_plot_diff_bars(bar_axes[3][1], steady_eddy_heat_d2y2_pos_first_df, steady_eddy_heat_d2y2_neg_first_df, steady_eddy_heat_d2y2_pos_last_df, steady_eddy_heat_d2y2_neg_last_df, "steady_eddy_heat_d2y2")

# ===== Titles =====
main_axes[0][0].set_title("AWB")
main_axes[0][1].set_title("CWB")
main_axes[1][0].set_title("eddy momentum forcing \n (transient)")
main_axes[1][1].set_title("eddy momentum forcing \n (Quasi-stationary)")
main_axes[2][0].set_title("EKE")
main_axes[2][1].set_title("Baroclinicity")
main_axes[3][0].set_title("eddy thermal feedback ano\n (transient)")
main_axes[3][1].set_title("eddy thermal feedback ano\n (Quasi-stationary)")

# ===== y-labels =====
main_axes[0][0].set_ylabel("Rossby wave breaking index")
main_axes[1][0].set_ylabel(r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ / m $s^{-1}$ day$^{-1}$")
main_axes[2][0].set_ylabel("EKE / m$^2$ s$^{-2}$")
main_axes[2][1].set_ylabel("Eady growth rate / day$^{-1}$")
main_axes[3][0].set_ylabel(r"$\frac{\partial^2}{\partial y^2} (v'\theta')$ / K $m^{-1}$ s$^{-1}$")
main_axes[0][1].set_ylabel("")
main_axes[1][1].set_ylabel("")
main_axes[3][1].set_ylabel("")

# ===== x-labels: only bottom bar row =====
for r in range(4):
    for c in range(2):
        main_axes[r][c].set_xlabel("")
        plt.setp(main_axes[r][c].get_xticklabels(), visible=False)
        if r < 3:
            bar_axes[r][c].set_xlabel("")
            plt.setp(bar_axes[r][c].get_xticklabels(), visible=False)
        else:
            bar_axes[r][c].set_xlabel("Days relative to extreme onset")

# ===== Styling =====
for r in range(4):
    for c in range(2):
        sns.despine(ax=main_axes[r][c], bottom=True)
        main_axes[r][c].tick_params(bottom=False)
        main_axes[r][c].axvline(0, color="gray", linestyle="dotted", lw=1)

# ===== Legend (top-right main panel) =====
decade_handles = [
    Line2D([0], [0], color="gray",  lw=2, linestyle="-",  label="1850s"),
    Line2D([0], [0], color="gray",  lw=2, linestyle="--", label="2090s"),
]
phase_handles = [
    Line2D([0], [0], color=COLOR_POS, lw=2, label="pos NAO"),
    Line2D([0], [0], color=COLOR_NEG, lw=2, label="neg NAO"),
]
decade_legend = main_axes[1][1].legend(
    handles=decade_handles, title="decade",
    loc="lower left", bbox_to_anchor=(0.1, 0.6), frameon=False,
)
main_axes[1][1].add_artist(decade_legend)
main_axes[1][1].legend(
    handles=phase_handles, title="phase",
    loc="lower left", bbox_to_anchor=(0.5, 0.6), frameon=False,
)

# ===== Panel labels =====
panel_idx = 0
for r in range(4):
    for c in range(2):
        main_axes[r][c].text(
            -0.08, 1.02, chr(97 + panel_idx),
            transform=main_axes[r][c].transAxes,
            fontsize=14, fontweight="bold", va="bottom", ha="right",
        )
        panel_idx += 1
# for all axes, xlim -20, 20
for r in range(4):
    for c in range(2):
        main_axes[r][c].set_xlim(-20, 20)
        bar_axes[r][c].set_xlim(-20, 20)

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0after_defense/feedback_lines_mix.pdf",
    dpi=300, bbox_inches="tight",
)

# %%
