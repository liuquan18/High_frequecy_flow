# %%
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# %%
def read_NAO_extremes():
    """both first10 and last10 are need to standardize"""
    first_eofs = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result_first_last2091-2100/first10_eofs.nc"
    )
    last_eofs = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result_first_last2091-2100/last10_eofs.nc"
    )
    # time to year-month
    first_eofs["time"] = first_eofs["time"].dt.strftime("%Y-%m")
    last_eofs["time"] = last_eofs["time"].dt.strftime("%Y-%m")

    first_pc = first_eofs.pc.sel(mode="NAO")
    last_pc = last_eofs.pc.sel(mode="NAO")

    # standardize
    mean = first_pc.mean(dim=("time", "ens"))
    std = first_pc.std(dim=("time", "ens"))

    first_pc = (first_pc - mean) / std
    last_pc = (last_pc - mean) / std

    # find time and ens where the value of pc is above 1.5
    first_pos = first_pc.where(first_pc > 1.5)
    last_pos = last_pc.where(last_pc > 1.5)

    first_neg = first_pc.where(first_pc < -1.5)
    last_neg = last_pc.where(last_pc < -1.5)

    return first_pos, last_pos, first_neg, last_neg


# %%
def read_jet(period, NAO_phase, jet_loc, eddy=True):
    """
    Parameters
    ----------
    period : str
        first10 or last10
    NAO_phase : str
        pos or neg
    jet_loc : str
        north or south
    """
    eddy_label = "_eddy" if eddy else ""
    base_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/physics/jet_loc_count/"
    jet_path = f"{base_dir}jet_loc{eddy_label}_{NAO_phase}_{jet_loc}_{period}.nc"

    jet = xr.open_dataset(jet_path).jet_loc

    # time to year-month
    jet["time"] = jet["time"].dt.strftime("%Y-%m")

    return jet


# %%
def read_wb(period, NAO_phase, wb_type):
    """
    Parameters
    ----------
    period : str
        first10 or last10
    NAO_phase : str
        pos or neg
    wb_type : str
        AWB or CWB
    """
    base_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/physics/wave_break_count/"
    wb_path = f"{base_dir}wb_{NAO_phase}_{wb_type}_{period}.nc"

    wb = xr.open_dataset(wb_path).wb

    # time to year-month
    wb["time"] = wb["time"].dt.strftime("%Y-%m")

    return wb


# %%
def merge_NAO_jet_wb(NAO, jet, wb):
    ds = xr.merge([NAO, jet, wb], compat="minimal")
    df = ds.to_dataframe()
    # drop rows where 'pc' is NaN
    df = df.dropna(subset=["pc"]).reset_index()[["pc", "jet_loc", "wb"]]
    return df


def phy_diff(expected, unexpected):
    diff = expected - unexpected
    # keep 'pc' column no change
    diff["pc"] = expected["pc"]

    return diff


def merge_first_last(first, last):
    first["period"] = "first10"
    last["period"] = "last10"

    merged = pd.concat([first, last], ignore_index=True)
    return merged


# %%
first_pos, last_pos, first_neg, last_neg = read_NAO_extremes()

# %%
first_pos_jet_north = read_jet("first10", "pos", "north")
last_pos_jet_north = read_jet("last10", "pos", "north")
first_neg_jet_north = read_jet("first10", "neg", "north")
last_neg_jet_north = read_jet("last10", "neg", "north")

first_pos_jet_south = read_jet("first10", "pos", "south")
last_pos_jet_south = read_jet("last10", "pos", "south")
first_neg_jet_south = read_jet("first10", "neg", "south")
last_neg_jet_south = read_jet("last10", "neg", "south")
# %%
first_pos_AWB = read_wb("first10", "pos", "AWB")
last_pos_AWB = read_wb("last10", "pos", "AWB")
first_neg_CWB = read_wb("first10", "neg", "CWB")
last_neg_CWB = read_wb("last10", "neg", "CWB")

first_pos_CWB = read_wb("first10", "pos", "CWB")
last_pos_CWB = read_wb("last10", "pos", "CWB")
first_neg_AWB = read_wb("first10", "neg", "AWB")
last_neg_AWB = read_wb("last10", "neg", "AWB")

# %%
pos_NAO = merge_first_last(
    # first10 years
    phy_diff(
        merge_NAO_jet_wb(first_pos, first_pos_jet_north, first_pos_AWB),  # expected
        merge_NAO_jet_wb(first_pos, first_pos_jet_south, first_pos_CWB),  # unexpected
    ),
    # last10 years
    phy_diff(
        merge_NAO_jet_wb(last_pos, last_pos_jet_north, last_pos_AWB),  # expected
        merge_NAO_jet_wb(last_pos, last_pos_jet_south, last_pos_CWB),  # unexpected
    ),
)

neg_NAO = merge_first_last(
    # first10 years
    phy_diff(
        merge_NAO_jet_wb(first_neg, first_neg_jet_south, first_neg_CWB),  # expected
        merge_NAO_jet_wb(first_neg, first_neg_jet_north, first_neg_AWB),  # unexpected
    ),
    # last10 years
    phy_diff(
        merge_NAO_jet_wb(last_neg, last_neg_jet_south, last_neg_CWB),  # expected
        merge_NAO_jet_wb(last_neg, last_neg_jet_north, last_neg_AWB),  # unexpected
    ),
)

# %%
# density plot
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
# For the positive NAO
kde = sns.kdeplot(
    data=pos_NAO[pos_NAO["period"] == "first10"],
    x="jet_loc",
    y="wb",
    ax=axes[0],
    fill=False,
    color="grey",
    # common_norm=True,
    # hue="period",
)

axes[0].clabel(kde.collections[0], inline=True, fontsize=10)


# For the negative NAO
sns.kdeplot(
    data=neg_NAO[neg_NAO["period"] == "first10"],
    x="jet_loc",
    y="wb",
    ax=axes[1],
    fill=True,
    color="grey",
    common_norm=True,
)
sns.kdeplot(
    data=neg_NAO[neg_NAO["period"] == "last10"],
    x="jet_loc",
    y="wb",
    ax=axes[1],
    fill=False,
    color="red",
    common_norm=True,
)
# hline and vline at 0
for ax in axes:
    ax.axvline(0, color="black", linestyle="--")
    ax.axhline(0, color="black", linestyle="--")

# %%
# Create subplots with 1 row and 2 columns
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Plot for pos_NAO on axes[0]
g_pos = sns.JointGrid(data=pos_NAO, x="jet_loc", y="wb", hue="period")
g_pos.plot_joint(sns.kdeplot, fill=False, common_norm=True)
g_pos.plot_marginals(sns.histplot, kde=True)
g_pos.ax_joint = axes[0]
# hline and vline at 0
g_pos.ax_joint.axvline(0, color="black", linestyle="--")
g_pos.ax_joint.axhline(0, color="black", linestyle="--")

# Plot for neg_NAO on axes[1]
g_neg = sns.JointGrid(data=neg_NAO, x="jet_loc", y="wb", hue="period")
g_neg.plot_joint(sns.kdeplot, fill=False, common_norm=True)
g_neg.plot_marginals(sns.histplot, kde=True)
g_neg.ax_joint = axes[1]
# hline and vline at 0
g_neg.ax_joint.axvline(0, color="black", linestyle="--")
g_neg.ax_joint.axhline(0, color="black", linestyle="--")

plt.tight_layout()
# %%
fig = plt.figure(figsize=(12, 6))
gs = fig.add_gridspec(4, 8)
pos_kde_ax = fig.add_subplot(gs[1:4, 1:4])
pos_jet_ax = fig.add_subplot(gs[0, 1:4], sharex=pos_kde_ax)
pos_wb_ax = fig.add_subplot(gs[1:4, 0], sharey=pos_kde_ax)
neg_kde_ax = fig.add_subplot(gs[1:4, 4:7])
neg_jet_ax = fig.add_subplot(gs[0, 4:7], sharex=neg_kde_ax)
neg_wb_ax = fig.add_subplot(gs[1:4, 7], sharey=neg_kde_ax)

# For the positive NAO
pos_kde = sns.kdeplot(
    data=pos_NAO,
    x="jet_loc",
    y="wb",
    ax=pos_kde_ax,
    fill=False,
    color="grey",
    common_norm=True,
    hue="period",
    legend=False,
)


pos_jet = sns.histplot(
    data=pos_NAO,
    x="jet_loc",
    ax=pos_jet_ax,
    color="grey",
    hue="period",
    kde=True,
    legend=False,
)
pos_wb = sns.histplot(
    data=pos_NAO,
    y="wb",
    ax=pos_wb_ax,
    color="grey",
    hue="period",
    kde=True,
    legend=False,
)
# reverse x-axis for wb plot
pos_wb_ax.invert_xaxis()

# For the negative NAO
neg_kde = sns.kdeplot(
    data=neg_NAO,
    x="jet_loc",
    y="wb",
    ax=neg_kde_ax,
    fill=False,
    color="grey",
    common_norm=True,
    hue="period",
    legend=False,
)
neg_jet = sns.histplot(
    data=neg_NAO,
    x="jet_loc",
    ax=neg_jet_ax,
    color="grey",
    hue="period",
    kde=True,
    legend=False,
)
neg_wb = sns.histplot(
    data=neg_NAO,
    y="wb",
    ax=neg_wb_ax,
    color="grey",
    hue="period",
    kde=True,
    legend=False,
)

# hline and vline at kde plot
for ax in [pos_kde_ax, neg_kde_ax]:
    ax.axvline(0, color="black", linestyle="--")
    ax.axhline(0, color="black", linestyle="--")

# Remove labels for marginal plots
pos_jet_ax.set_xlabel("")
neg_jet_ax.set_xlabel("")
pos_wb_ax.set_ylabel("")
neg_wb_ax.set_ylabel("")

# Remove ticks and labels for marginal plots only
pos_jet_ax.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
neg_jet_ax.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
pos_wb_ax.tick_params(axis="y", which="both", left=False, labelleft=False)
neg_wb_ax.tick_params(axis="y", which="both", left=False, labelleft=False)

# plt.tight_layout()
# %%

# only histograms
fig, axes = plt.subplots(2, 2, figsize=(12, 12))
sns.histplot(
    data=pos_NAO,
    x="jet_loc",
    hue="period",
    ax=axes[0, 0],
    kde=True,
)
sns.histplot(
    data=pos_NAO,
    x="wb",
    hue="period",
    ax=axes[0, 1],
    kde=True,
)

sns.histplot(
    data=neg_NAO,
    x="jet_loc",
    hue="period",
    ax=axes[1, 0],
    kde=True,
)

sns.histplot(data=neg_NAO, x="wb", hue="period", ax=axes[1, 1], kde=True)

for ax in axes.flatten():
    # vline at hlines at 0
    ax.axvline(0, color="black", linestyle="--")
    ax.axhline(0, color="black", linestyle="--")
# %%
