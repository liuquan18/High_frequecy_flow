# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.lines import Line2D

from src.data_helper import read_composite
import importlib

importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div

# Only read and process data needed for the momentum fluxes plot

# %%
# Read transient and steady EP flux for positive and negative phase, first and last decade, and climatology
Tdivphi_pos_first = read_EP_flux(
    phase="pos", decade=1850, eddy="transient", ano=False, lon_mean=False, region=None
)[2]
Tdivphi_neg_first = read_EP_flux(
    phase="neg", decade=1850, eddy="transient", ano=False, lon_mean=False, region=None
)[2]
Tdivphi_pos_last = read_EP_flux(
    phase="pos", decade=2090, eddy="transient", ano=False, lon_mean=False, region=None
)[2]
Tdivphi_neg_last = read_EP_flux(
    phase="neg", decade=2090, eddy="transient", ano=False, lon_mean=False, region=None
)[2]
Tdivphi_clima_first = read_EP_flux(
    phase="clima", decade=1850, eddy="transient", ano=False, lon_mean=False, region=None
)[2]
Tdivphi_clima_last = read_EP_flux(
    phase="clima", decade=2090, eddy="transient", ano=False, lon_mean=False, region=None
)[2]

Sdivphi_pos_first = read_EP_flux(
    phase="pos", decade=1850, eddy="steady", ano=False, lon_mean=False, region=None
)[2]
Sdivphi_neg_first = read_EP_flux(
    phase="neg", decade=1850, eddy="steady", ano=False, lon_mean=False, region=None
)[2]
Sdivphi_pos_last = read_EP_flux(
    phase="pos", decade=2090, eddy="steady", ano=False, lon_mean=False, region=None
)[2]
Sdivphi_neg_last = read_EP_flux(
    phase="neg", decade=2090, eddy="steady", ano=False, lon_mean=False, region=None
)[2]
Sdivphi_clima_first = read_EP_flux(
    phase="clima", decade=1850, eddy="steady", ano=False, lon_mean=False, region=None
)[2]
Sdivphi_clima_last = read_EP_flux(
    phase="clima", decade=2090, eddy="steady", ano=False, lon_mean=False, region=None
)[2]


# Anomaly calculation
def anomaly(ds, ds_clima):
    ds = ds.sel(time=slice(-10, 5)).mean(dim=("time", "event", "lon"))
    ds_clima = ds_clima.mean(dim=("lon"))
    anomaly = ds - ds_clima
    return anomaly.load()


# %%
Tdiv_phi_pos_first_anomaly = anomaly(Tdivphi_pos_first, Tdivphi_clima_first)
Tdiv_phi_neg_first_anomaly = anomaly(Tdivphi_neg_first, Tdivphi_clima_first)
Tdiv_phi_pos_last_anomaly = anomaly(Tdivphi_pos_last, Tdivphi_clima_last)
Tdiv_phi_neg_last_anomaly = anomaly(Tdivphi_neg_last, Tdivphi_clima_last)

Sdivphi_pos_first_anomaly = anomaly(Sdivphi_pos_first, Sdivphi_clima_first)
Sdivphi_neg_first_anomaly = anomaly(Sdivphi_neg_first, Sdivphi_clima_first)
Sdivphi_pos_last_anomaly = anomaly(Sdivphi_pos_last, Sdivphi_clima_last)
Sdivphi_neg_last_anomaly = anomaly(Sdivphi_neg_last, Sdivphi_clima_last)

div_phi_pos_first_anomaly = Tdiv_phi_pos_first_anomaly + Sdivphi_pos_first_anomaly
div_phi_neg_first_anomaly = Tdiv_phi_neg_first_anomaly + Sdivphi_neg_first_anomaly
div_phi_pos_last_anomaly = Tdiv_phi_pos_last_anomaly + Sdivphi_pos_last_anomaly
div_phi_neg_last_anomaly = Tdiv_phi_neg_last_anomaly + Sdivphi_neg_last_anomaly


# DataFrame conversion for line plots
def to_dataframe(ds, var_name, phase, decade):
    ds = ds.sel(lat=slice(50, 70))
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"
    ds = ds.weighted(weights)
    ds = ds.mean(dim=["lat", "lon"])
    df = ds.to_dataframe(var_name).reset_index()
    df["phase"] = phase
    df["decade"] = decade
    return df


Tdivphi_pos_first_df = to_dataframe(Tdivphi_pos_first, "N", "pos", 1850)
Tdivphi_neg_first_df = to_dataframe(Tdivphi_neg_first, "N", "neg", 1850)
Tdivphi_pos_last_df = to_dataframe(Tdivphi_pos_last, "N", "pos", 2090)
Tdivphi_neg_last_df = to_dataframe(Tdivphi_neg_last, "N", "neg", 2090)
Tdivphi_clima_first_df = to_dataframe(Tdivphi_clima_first, "N", "clima", 1850)
Tdivphi_clima_last_df = to_dataframe(Tdivphi_clima_last, "N", "clima", 2090)

Sdivphi_pos_first_df = to_dataframe(Sdivphi_pos_first, "N", "pos", 1850)
Sdivphi_neg_first_df = to_dataframe(Sdivphi_neg_first, "N", "neg", 1850)
Sdivphi_pos_last_df = to_dataframe(Sdivphi_pos_last, "N", "pos", 2090)
Sdivphi_neg_last_df = to_dataframe(Sdivphi_neg_last, "N", "neg", 2090)
Sdivphi_clima_first_df = to_dataframe(Sdivphi_clima_first, "N", "clima", 1850)
Sdivphi_clima_last_df = to_dataframe(Sdivphi_clima_last, "N", "clima", 2090)

# Combine dataframes for transient and steady
Tdivphi_dfs = pd.concat(
    [
        Tdivphi_pos_first_df,
        Tdivphi_neg_first_df,
        Tdivphi_pos_last_df,
        Tdivphi_neg_last_df,
        Tdivphi_clima_first_df,
        Tdivphi_clima_last_df,
    ],
    axis=0,
)
Sdivphi_dfs = pd.concat(
    [
        Sdivphi_pos_first_df,
        Sdivphi_neg_first_df,
        Sdivphi_pos_last_df,
        Sdivphi_neg_last_df,
        Sdivphi_clima_first_df,
        Sdivphi_clima_last_df,
    ],
    axis=0,
)

# Prepare for sum, transient, steady
transient_dfs = Tdivphi_dfs.reset_index(drop=True)
steady_dfs = Sdivphi_dfs.reset_index(drop=True)
transient_dfs = transient_dfs.loc[:, ~transient_dfs.columns.duplicated()]
steady_dfs = steady_dfs.loc[:, ~steady_dfs.columns.duplicated()]
transient_dfs = transient_dfs[["event", "time", "plev", "phase", "decade", "N"]]
steady_dfs = steady_dfs[["event", "time", "plev", "phase", "decade", "N"]]

# Add sum
sum_dfs = transient_dfs.copy()
sum_dfs["N"] = transient_dfs["N"] + steady_dfs["N"]

# Climatology
transient_dfs_clima = transient_dfs[transient_dfs["phase"] == "clima"]
steady_dfs_clima = steady_dfs[steady_dfs["phase"] == "clima"]
sum_dfs_clima = transient_dfs_clima.copy()
sum_dfs_clima["N"] = transient_dfs_clima["N"] + steady_dfs_clima["N"]

# Select time window
transient_dfs = transient_dfs[
    (transient_dfs["time"].between(-20, 10)) & (transient_dfs["phase"] != "clima")
]
steady_dfs = steady_dfs[
    (steady_dfs["time"].between(-20, 10)) & (steady_dfs["phase"] != "clima")
]
sum_dfs = sum_dfs[(sum_dfs["time"].between(-20, 10)) & (sum_dfs["phase"] != "clima")]

#%%
# Plotting
phi_sum_levels = np.arange(-0.3, 0.31, 0.1)
phi_trans_levels = np.arange(-0.2, 0.21, 0.05)
phi_steady_levels = np.arange(-0.2, 0.21, 0.05)

# %%
phi_trans_levels_diff = np.arange(-0.2, 0.21, 0.05)
# %%
# New plot: 1 row, 3 columns, transient anomaly for pos/neg phase and their difference

fig, axes = plt.subplots(1, 3, figsize=(10, 4), sharex=False, sharey=True)

# axes[0]: positive phase, transient anomaly
cf_phi_trans_pos = (Tdiv_phi_pos_first_anomaly).plot.contourf(
    ax=axes[0],
    levels=phi_trans_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    xlim=(0, 90),
    ylim=(100000, 10000),
)
contour_levels = [l for l in phi_trans_levels if l != 0]
(Tdiv_phi_pos_last_anomaly).plot.contour(
    ax=axes[0],
    levels=contour_levels,
    colors="k",
    linewidths=1,
    add_colorbar=False,
    xlim=(0, 90),
    ylim=(100000, 10000),
)

# axes[1]: negative phase, transient anomaly
cf_phi_trans_neg = (Tdiv_phi_neg_first_anomaly).plot.contourf(
    ax=axes[1],
    levels=phi_trans_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    xlim=(0, 90),
    ylim=(100000, 10000),
)
(Tdiv_phi_neg_last_anomaly).plot.contour(
    ax=axes[1],
    levels=contour_levels,
    colors="k",
    linewidths=1,
    add_colorbar=False,
    xlim=(0, 90),
    ylim=(100000, 10000),
)

# axes[2]: difference (last - first) for both phases, using phi_trans_levels_diff
diff_first = Tdiv_phi_pos_first_anomaly - Tdiv_phi_neg_first_anomaly
diff_last = Tdiv_phi_pos_last_anomaly - Tdiv_phi_neg_last_anomaly

# Plot positive phase difference as filled, negative phase as contour
cf_phi_trans_diff = diff_first.plot.contourf(
    ax=axes[2],
    levels=phi_trans_levels_diff,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    xlim=(0, 90),
    ylim=(100000, 10000),
)
contour_levels_diff = [l for l in phi_trans_levels_diff if l != 0]
diff_last.plot.contour(
    ax=axes[2],
    levels=contour_levels_diff,
    colors="k",
    linewidths=1,
    add_colorbar=False,
    xlim=(0, 90),
    ylim=(100000, 10000),
)

# Add a colorbar for each subplot
cbar0 = fig.colorbar(
    cf_phi_trans_pos,
    ax=axes[0],
    orientation="horizontal",
    fraction=0.08,
    pad=0.15,
    aspect=30,
    shrink=0.8,
    label=r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m $s^{-1}$ day $^{-1}$]",
)
cbar0.set_ticks([-0.2, -0.1, 0.0, 0.1, 0.2])  # Fewer ticks

cbar1 = fig.colorbar(
    cf_phi_trans_neg,
    ax=axes[1],
    orientation="horizontal",
    fraction=0.08,
    pad=0.15,
    aspect=30,
    shrink=0.8,
    label=r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m $s^{-1}$ day $^{-1}$]",
)
cbar1.set_ticks([-0.2, -0.1, 0.0, 0.1, 0.2])  # Fewer ticks

cbar2 = fig.colorbar(
    cf_phi_trans_diff,
    ax=axes[2],
    orientation="horizontal",
    fraction=0.08,
    pad=0.15,
    aspect=30,
    shrink=0.8,
    label=r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m $s^{-1}$ day $^{-1}$]",
)
cbar2.set_ticks([-0.2, -0.1, 0.0, 0.1, 0.2])  # Fewer ticks

# Axis labels
axes[0].set_ylabel("Pressure [hPa]")
axes[0].set_yticks(
    [100000, 90000, 80000, 70000, 60000, 50000, 40000, 30000, 20000, 10000]
)
axes[0].set_yticklabels([str(int(tick / 100)) for tick in axes[0].get_yticks()])
for ax in axes:
    ax.set_xlabel("lat [°N]")


axes[1].set_ylabel("")
axes[2].set_ylabel("")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/eddy_momentum_transient_only.png",
    dpi=500,
)


# %%
# New plot: 1 row, 3 columns, line plots for sum, transient, steady (axes[2,0], axes[2,1], axes[2,2] from first fig)

fig, axes = plt.subplots(1, 3, figsize=(10, 5), sharex=False, sharey=True)

# --- Transient ---
sns.lineplot(
    data=transient_first_ano,
    x="time",
    y="N",
    style="phase",
    color="black",
    ax=axes[0],
    errorbar=("ci", 95),
)
sns.lineplot(
    data=transient_last_ano,
    x="time",
    y="N",
    style="phase",
    color="red",
    ax=axes[0],
    errorbar=("ci", 95),
)
axes[0].set_ylabel(
    r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m $s^{-1}$ day $^{-1}$]"
)
axes[0].set_xlabel("Days relative to extreme onset")
axes[0].set_title("Transient", fontsize=16)

# --- Steady ---
sns.lineplot(
    data=steady_first_ano,
    x="time",
    y="N",
    style="phase",
    color="black",
    ax=axes[1],
    errorbar=("ci", 95),
)
sns.lineplot(
    data=steady_last_ano,
    x="time",
    y="N",
    style="phase",
    color="red",
    ax=axes[1],
    errorbar=("ci", 95),
)
axes[1].set_ylabel("")
axes[1].set_xlabel("Days relative to extreme onset")
axes[1].set_title("Quasi-stationary", fontsize=16)

# --- Sum ---
sns.lineplot(
    data=sum_first_ano,
    x="time",
    y="N",
    style="phase",
    color="black",
    ax=axes[2],
    errorbar=("ci", 95),
)
sns.lineplot(
    data=sum_last_ano,
    x="time",
    y="N",
    style="phase",
    color="red",
    ax=axes[2],
    errorbar=("ci", 95),
)
axes[2].set_ylabel("")
axes[2].set_xlabel("Days relative to extreme onset")
axes[2].set_title("Total", fontsize=16)

# Remove top and right spines, add vertical line at x=0
for ax in axes.flat:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.axvline(0, color="k", linestyle="-", lw=0.5, zorder=0)

# Only show legend at the bottom of the whole plot, not on individual axes
for ax in axes:
    leg = ax.get_legend()
    if leg is not None:
        leg.remove()

from matplotlib.lines import Line2D

decade_handles = [
    Line2D([0], [0], color="black", lw=2, label="1850s"),
    Line2D([0], [0], color="red", lw=2, label="2090s"),
]
phase_handles = [
    Line2D([0], [0], color="black", lw=2, linestyle="-", label="pos NAO"),
    Line2D([0], [0], color="black", lw=2, linestyle="--", label="neg NAO"),
]

# Combine handles and labels for two-column legend
handles = phase_handles + decade_handles
labels = [h.get_label() for h in handles]


plt.tight_layout(rect=[0, 0.08, 1, 1])  # leave space at bottom for legend

# Add legend at the bottom, two columns, larger font
fig.legend(
    handles,
    labels,
    loc="lower center",
    ncol=4,
    fontsize=16,
    title_fontsize=18,
    frameon=False,
    bbox_to_anchor=(0.4, -0.01),
)

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/eddy_momentum_lineplots.png",
    dpi=500,
    bbox_inches="tight",
)
