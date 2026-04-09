# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import cmocean
import os
import matplotlib
from src.plotting.util import lon360to180

from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, FuncFormatter

from src.plotting.util import map_smooth
import src.plotting.util as util
import metpy.calc as mpcalc
from metpy.units import units
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec

# %%
data_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0composite_feedback"

def _load(name):
    return xr.open_dataarray(os.path.join(data_dir, f"{name}.nc"))

# Jet stream
ua_pos_first = _load("ua_pos_1850")
ua_neg_first = _load("ua_neg_1850")
ua_pos_last  = _load("ua_pos_2090")
ua_neg_last  = _load("ua_neg_2090")

# Convergence of eddy momentum flux
Fdiv_transient_pos_first = _load("Fdiv_phi_transient_pos_1850")
Fdiv_transient_neg_first = _load("Fdiv_phi_transient_neg_1850")
Fdiv_transient_pos_last  = _load("Fdiv_phi_transient_pos_2090")
Fdiv_transient_neg_last  = _load("Fdiv_phi_transient_neg_2090")


# %%# upvp
upvp_pos_first = _load("upvp_pos_1850")
upvp_neg_first = _load("upvp_neg_1850")
upvp_pos_last  = _load("upvp_pos_2090")
upvp_neg_last  = _load("upvp_neg_2090")

#%%
awb_pos_first = _load("wb_anticyclonic_pos_1850")
awb_neg_first = _load("wb_anticyclonic_neg_1850")
awb_pos_last  = _load("wb_anticyclonic_pos_2090")
awb_neg_last  = _load("wb_anticyclonic_neg_2090")

#%%
cwb_pos_first = _load("wb_cyclonic_pos_1850")
cwb_neg_first = _load("wb_cyclonic_neg_1850")
cwb_pos_last  = _load("wb_cyclonic_pos_2090")
cwb_neg_last  = _load("wb_cyclonic_neg_2090")

# %%
ua_pos_first=ua_pos_first.sel(plev = 25000)
ua_neg_first=ua_neg_first.sel(plev = 25000)
ua_pos_last=ua_pos_last.sel(plev = 25000)
ua_neg_last=ua_neg_last.sel(plev = 25000)

#%%
upvp_pos_first=upvp_pos_first.sel(plev = 25000)
upvp_neg_first=upvp_neg_first.sel(plev = 25000)
upvp_pos_last=upvp_pos_last.sel(plev = 25000)
upvp_neg_last=upvp_neg_last.sel(plev = 25000)

#%%

# fldmean over
def to_dataframe(ds, var_name, phase, decade, lat_slice = slice(50, 70)):
    ds = ds.sel(lat=lat_slice)    
    # create weights
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"

    ds = ds.weighted(weights).mean(dim = ('lat'))

    df = ds.to_dataframe(var_name).reset_index()
    df["phase"] = phase
    df["decade"] = decade
    return df

#%%
# awb_lat_slice = slice(40, 60)
# cwb_lat_slice = slice(50, 70)
awb_pos_first_df = to_dataframe(awb_pos_first, "awb", "pos", 1850, lat_slice = slice(40, 60))
awb_neg_first_df = to_dataframe(awb_neg_first, "awb", "neg", 1850, lat_slice = slice(40, 60))
awb_pos_last_df  = to_dataframe(awb_pos_last,  "awb", "pos", 2090, lat_slice = slice(40, 60))
awb_neg_last_df  = to_dataframe(awb_neg_last,  "awb", "neg", 2090, lat_slice = slice(40, 60))

cwb_pos_first_df = to_dataframe(cwb_pos_first, "cwb", "pos", 1850, lat_slice = slice(50, 70))
cwb_neg_first_df = to_dataframe(cwb_neg_first, "cwb", "neg", 1850, lat_slice = slice(50, 70))
cwb_pos_last_df  = to_dataframe(cwb_pos_last,  "cwb", "pos", 2090, lat_slice = slice(50, 70))
cwb_neg_last_df  = to_dataframe(cwb_neg_last,  "cwb", "neg", 2090, lat_slice = slice(50, 70))
#%%
Fdiv_transient_pos_first_df = to_dataframe(Fdiv_transient_pos_first, "Fdiv_transient", "pos", 1850)
Fdiv_transient_neg_first_df = to_dataframe(Fdiv_transient_neg_first, "Fdiv_transient", "neg", 1850)
Fdiv_transient_pos_last_df  = to_dataframe(Fdiv_transient_pos_last,  "Fdiv_transient", "pos", 2090)
Fdiv_transient_neg_last_df  = to_dataframe(Fdiv_transient_neg_last,  "Fdiv_transient", "neg", 2090)

#%%
# Fdiv_steady

#%%

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
# _plot_quartet(main_axes[1][1], Fdiv_steady_pos_first_df, Fdiv_steady_neg_first_df, Fdiv_steady_pos_last_df, Fdiv_steady_neg_last_df, "momentum_flux_divergence")
_plot_diff_bars(bar_axes[1][0], Fdiv_transient_pos_first_df, Fdiv_transient_neg_first_df, Fdiv_transient_pos_last_df, Fdiv_transient_neg_last_df, "Fdiv_transient")
# _plot_diff_bars(bar_axes[1][1], Fdiv_steady_pos_first_df, Fdiv_steady_neg_first_df, Fdiv_steady_pos_last_df, Fdiv_steady_neg_last_df, "momentum_flux_divergence")

# %%
