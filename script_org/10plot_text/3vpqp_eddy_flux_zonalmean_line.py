# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import seaborn.objects as so

from src.data_helper import read_composite
import importlib
import matplotlib
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var

# %%
levels_vq = np.arange(-3, 3.1, 0.5)
levels_uv = np.arange(-1.5, 1.6, 0.5)
levels_vt = np.arange(-3, 3.1, 0.5)
# %%
# read transient EP flux for positive and negative phase
# read data for first decade with region = western
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


# last decade region
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
# read steady EP flux for positive and negative phase
Sphi_pos_first, Sp_pos_first, Sdivphi_pos_first, Sdiv_p_pos_first = read_EP_flux(
    phase="pos",
    decade=1850,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)
Sphi_neg_first, Sp_neg_first, Sdivphi_neg_first, Sdiv_p_neg_first = read_EP_flux(
    phase="neg",
    decade=1850,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)

# last decade
Sphi_pos_last, Sp_pos_last, Sdivphi_pos_last, Sdiv_p_pos_last = read_EP_flux(
    phase="pos",
    decade=2090,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)
Sphi_neg_last, Sp_neg_last, Sdivphi_neg_last, Sdiv_p_neg_last = read_EP_flux(
    phase="neg",
    decade=2090,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)
# %%
# read climatological EP flux
Sphi_clima_first, Sp_clima_first, Sdivphi_clima_first, Sdiv_p_clima_first = (
    read_EP_flux(
        phase="clima",
        decade=1850,
        eddy="steady",
        ano=False,
        lon_mean=False,
        region=None,
    )
)
Sphi_clima_last, Sp_clima_last, Sdivphi_clima_last, Sdiv_p_clima_last = read_EP_flux(
    phase="clima",
    decade=2090,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)
# %%
# read E_div_x

TEx_pos_first, TEy_pos_first = read_E_div(
    phase="pos",
    decade=1850,
    eddy="transient",
    keep_time=True,
)
TEx_neg_first, TEy_neg_first = read_E_div(
    phase="neg",
    decade=1850,
    eddy="transient",
    keep_time=True,
)
TEx_pos_last, TEy_pos_last = read_E_div(
    phase="pos",
    decade=2090,
    eddy="transient",
    keep_time=True,
)
TEx_neg_last, TEy_neg_last = read_E_div(
    phase="neg",
    decade=2090,
    eddy="transient",
    keep_time=True,
)

# read climatological E_div_x
TEx_clima_first, TEy_clima_first = read_E_div(
    phase="clima",
    decade=1850,
    eddy="transient",
    keep_time=False,
)
TEx_clima_last, TEy_clima_last = read_E_div(
    phase="clima",
    decade=2090,
    eddy="transient",
    keep_time=False,
)

# %%
# read E_div_x for steady eddies
SEx_pos_first, SEy_pos_first = read_E_div(
    phase="pos",
    decade=1850,
    eddy="steady",
    keep_time=True,
)
SEx_neg_first, SEy_neg_first = read_E_div(
    phase="neg",
    decade=1850,
    eddy="steady",
    keep_time=True,
)

SEx_pos_last, SEy_pos_last = read_E_div(
    phase="pos",
    decade=2090,
    eddy="steady",
    keep_time=True,
)
SEx_neg_last, SEy_neg_last = read_E_div(
    phase="neg",
    decade=2090,
    eddy="steady",
    keep_time=True,
)
# read climatological E_div_x for steady
SEx_clima_first, SEy_clima_first = read_E_div(
    phase="clima",
    decade=1850,
    eddy="steady",
    keep_time=False,  # climatology is in the old folder
)
SEx_clima_last, SEy_clima_last = read_E_div(
    phase="clima",
    decade=2090,
    eddy="steady",
    keep_time=False,
)


# %%
def anomaly(ds, ds_clima):
    """
    Calculate the anomaly of a dataset with respect to a climatology.
    """
    # average over time and events
    ds = ds.sel(time = slice(-10, 5)).mean(dim=('time', 'event', 'lon'))
    ds_clima = ds_clima.mean(dim=('lon'))
    anomaly = ds - ds_clima
    return anomaly.load()
# %%

Tdiv_phi_pos_first_anomaly = anomaly(Tdivphi_pos_first, Tdivphi_clima_first)
Tdiv_phi_neg_first_anomaly = anomaly(Tdivphi_neg_first, Tdivphi_clima_first)
Tdiv_phi_pos_last_anomaly = anomaly(Tdivphi_pos_last, Tdivphi_clima_last)
Tdiv_phi_neg_last_anomaly = anomaly(Tdivphi_neg_last, Tdivphi_clima_last)
# %%
Tdiv_p_pos_first_anomaly = anomaly(Tdiv_p_pos_first, Tdiv_p_clima_first)
Tdiv_p_neg_first_anomaly = anomaly(Tdiv_p_neg_first, Tdiv_p_clima_first)
Tdiv_p_pos_last_anomaly = anomaly(Tdiv_p_pos_last, Tdiv_p_clima_last)
Tdiv_p_neg_last_anomaly = anomaly(Tdiv_p_neg_last, Tdiv_p_clima_last)
# %%
Sdivphi_pos_first_anomaly = anomaly(Sdivphi_pos_first, Sdivphi_clima_first)
Sdivphi_neg_first_anomaly = anomaly(Sdivphi_neg_first, Sdivphi_clima_first)
Sdivphi_pos_last_anomaly = anomaly(Sdivphi_pos_last, Sdivphi_clima_last)
Sdivphi_neg_last_anomaly = anomaly(Sdivphi_neg_last, Sdivphi_clima_last)
# %%
Sdiv_p_pos_first_anomaly = anomaly(Sdiv_p_pos_first, Sdiv_p_clima_first)
Sdiv_p_neg_first_anomaly = anomaly(Sdiv_p_neg_first, Sdiv_p_clima_first)
Sdiv_p_pos_last_anomaly = anomaly(Sdiv_p_pos_last, Sdiv_p_clima_last)
Sdiv_p_neg_last_anomaly = anomaly(Sdiv_p_neg_last, Sdiv_p_clima_last)
#%%
# sum of transient and steady EP fluxes
div_phi_pos_first_anomaly = Tdiv_phi_pos_first_anomaly + Sdivphi_pos_first_anomaly
div_phi_neg_first_anomaly = Tdiv_phi_neg_first_anomaly + Sdivphi_neg_first_anomaly
div_phi_pos_last_anomaly = Tdiv_phi_pos_last_anomaly + Sdivphi_pos_last_anomaly
div_phi_neg_last_anomaly = Tdiv_phi_neg_last_anomaly + Sdivphi_neg_last_anomaly
# %%
div_p_pos_first_anomaly = Tdiv_p_pos_first_anomaly + Sdiv_p_pos_first_anomaly
div_p_neg_first_anomaly = Tdiv_p_neg_first_anomaly + Sdiv_p_neg_first_anomaly
div_p_pos_last_anomaly = Tdiv_p_pos_last_anomaly + Sdiv_p_pos_last_anomaly
div_p_neg_last_anomaly = Tdiv_p_neg_last_anomaly + Sdiv_p_neg_last_anomaly

# %%
# 
def to_dataframe(ds, var_name, phase, decade):

    ds = ds.sel(lat=slice(50, 70))
    # create weights
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"
    ds = ds.weighted(weights)

    ds = ds.mean(dim=["lat", "lon"])

    df = ds.to_dataframe(var_name).reset_index()
    df["phase"] = phase
    df["decade"] = decade
    return df


# %%
Tdivphi_pos_first = to_dataframe(Tdivphi_pos_first, "N", "pos", 1850)
Tdivphi_neg_first = to_dataframe(Tdivphi_neg_first, "N", "neg", 1850)
Tdivphi_pos_last = to_dataframe(Tdivphi_pos_last, "N", "pos", 2090)
Tdivphi_neg_last = to_dataframe(Tdivphi_neg_last, "N", "neg", 2090)
Tdivphi_clima_first = to_dataframe(Tdivphi_clima_first, "N", "clima", 1850)
Tdivphi_clima_last = to_dataframe(Tdivphi_clima_last, "N", "clima", 2090)

# join Tdivphi dataframes
Tdivphi_dfs = [
    Tdivphi_pos_first,
    Tdivphi_neg_first,
    Tdivphi_pos_last,
    Tdivphi_neg_last,
    Tdivphi_clima_first,
    Tdivphi_clima_last,
]
Tdivphi_dfs = pd.concat(Tdivphi_dfs, axis=0)

# %%
Tdiv_p_pos_first = to_dataframe(Tdiv_p_pos_first, "P", "pos", 1850)
Tdiv_p_neg_first = to_dataframe(Tdiv_p_neg_first, "P", "neg", 1850)
Tdiv_p_pos_last = to_dataframe(Tdiv_p_pos_last, "P", "pos", 2090)
Tdiv_p_neg_last = to_dataframe(Tdiv_p_neg_last, "P", "neg", 2090)
Tdiv_p_clima_first = to_dataframe(Tdiv_p_clima_first, "P", "clima", 1850)
Tdiv_p_clima_last = to_dataframe(Tdiv_p_clima_last, "P", "clima", 2090)

# join Tdiv_p dataframes
Tdiv_p_dfs = [
    Tdiv_p_pos_first,
    Tdiv_p_neg_first,
    Tdiv_p_pos_last,
    Tdiv_p_neg_last,
    Tdiv_p_clima_first,
    Tdiv_p_clima_last,
]
Tdiv_p_dfs = pd.concat(Tdiv_p_dfs, axis=0)
# %%
# Tex
TEx_pos_first_df = to_dataframe(TEx_pos_first, "M2", "pos", 1850)
TEx_neg_first_df = to_dataframe(TEx_neg_first, "M2", "neg", 1850)
TEx_pos_last_df = to_dataframe(TEx_pos_last, "M2", "pos", 2090)
TEx_neg_last_df = to_dataframe(TEx_neg_last, "M2", "neg", 2090)
TEx_clima_first_df = to_dataframe(TEx_clima_first, "M2", "clima", 1850)
TEx_clima_last_df = to_dataframe(TEx_clima_last, "M2", "clima", 2090)
TEx_dfs = [
    TEx_pos_first_df,
    TEx_neg_first_df,
    TEx_pos_last_df,
    TEx_neg_last_df,
    TEx_clima_first_df,
    TEx_clima_last_df,
]
TEx_dfs = pd.concat(TEx_dfs, axis=0)
# %%
transient_dfs = [
    Tdivphi_dfs,
    Tdiv_p_dfs,
    TEx_dfs,
]
# merge
transient_dfs = [
    df.reset_index(drop=True) if isinstance(df, pd.DataFrame) else df
    for df in transient_dfs
]
transient_dfs = pd.concat(transient_dfs, axis=1)
# remove duplicated columns
transient_dfs = transient_dfs.loc[:, ~transient_dfs.columns.duplicated()]
transient_dfs = transient_dfs[
    ["event", "time", "plev", "phase", "decade", "M2", "N", "P"]
]


# %%
# Steady eddies
Sdivphi_pos_first = to_dataframe(Sdivphi_pos_first, "N", "pos", 1850)
Sdivphi_neg_first = to_dataframe(Sdivphi_neg_first, "N", "neg", 1850)
Sdivphi_pos_last = to_dataframe(Sdivphi_pos_last, "N", "pos", 2090)
Sdivphi_neg_last = to_dataframe(Sdivphi_neg_last, "N", "neg", 2090)
Sdivphi_clima_first = to_dataframe(Sdivphi_clima_first, "N", "clima", 1850)
Sdivphi_clima_last = to_dataframe(Sdivphi_clima_last, "N", "clima", 2090)

# join Sdivphi dataframes
Sdivphi_dfs = [
    Sdivphi_pos_first,
    Sdivphi_neg_first,
    Sdivphi_pos_last,
    Sdivphi_neg_last,
    Sdivphi_clima_first,
    Sdivphi_clima_last,
]
Sdivphi_dfs = pd.concat(Sdivphi_dfs, axis=0)

# %%
Sdiv_p_pos_first = to_dataframe(Sdiv_p_pos_first, "P", "pos", 1850)
Sdiv_p_neg_first = to_dataframe(Sdiv_p_neg_first, "P", "neg", 1850)
Sdiv_p_pos_last = to_dataframe(Sdiv_p_pos_last, "P", "pos", 2090)
Sdiv_p_neg_last = to_dataframe(Sdiv_p_neg_last, "P", "neg", 2090)
Sdiv_p_clima_first = to_dataframe(Sdiv_p_clima_first, "P", "clima", 1850)
Sdiv_p_clima_last = to_dataframe(Sdiv_p_clima_last, "P", "clima", 2090)

# join Sdiv_p dataframes
Sdiv_p_dfs = [
    Sdiv_p_pos_first,
    Sdiv_p_neg_first,
    Sdiv_p_pos_last,
    Sdiv_p_neg_last,
    Sdiv_p_clima_first,
    Sdiv_p_clima_last,
]
Sdiv_p_dfs = pd.concat(Sdiv_p_dfs, axis=0)

# %%
SEx_pos_first_df = to_dataframe(SEx_pos_first, "M2", "pos", 1850)
SEx_neg_first_df = to_dataframe(SEx_neg_first, "M2", "neg", 1850)
SEx_pos_last_df = to_dataframe(SEx_pos_last, "M2", "pos", 2090)
SEx_neg_last_df = to_dataframe(SEx_neg_last, "M2", "neg", 2090)
SEx_clima_first_df = to_dataframe(SEx_clima_first, "M2", "clima", 1850)
SEx_clima_last_df = to_dataframe(SEx_clima_last, "M2", "clima", 2090)

SEx_dfs = [
    SEx_pos_first_df,
    SEx_neg_first_df,
    SEx_pos_last_df,
    SEx_neg_last_df,
    SEx_clima_first_df,
    SEx_clima_last_df,
]
SEx_dfs = pd.concat(SEx_dfs, axis=0)
# %%

# %%
steady_dfs = [
    Sdivphi_dfs,
    Sdiv_p_dfs,
    SEx_dfs,
]

# Merge steady eddy dataframes
steady_dfs = [
    df.reset_index(drop=True) if isinstance(df, pd.DataFrame) else df
    for df in steady_dfs
]
steady_dfs = pd.concat(steady_dfs, axis=1)
# Remove duplicated columns
steady_dfs = steady_dfs.loc[:, ~steady_dfs.columns.duplicated()]
steady_dfs = steady_dfs[["event", "time", "plev", "phase", "decade", "M2", "N", "P"]]

# %%
transient_dfs["M2_N"] = transient_dfs["M2"] + transient_dfs["N"]
steady_dfs["M2_N"] = steady_dfs["M2"] + steady_dfs["N"]

transient_dfs["M2_N_P"] = transient_dfs["M2_N"] + transient_dfs["P"]
steady_dfs["M2_N_P"] = steady_dfs["M2_N"] + steady_dfs["P"]
# %%
transient_dfs_clima = transient_dfs[transient_dfs["phase"] == "clima"]
steady_dfs_clima = steady_dfs[steady_dfs["phase"] == "clima"]


# %%
# select time from -20, 10

transient_dfs = transient_dfs[
    (transient_dfs["time"].between(-20, 10)) & (transient_dfs["phase"] != "clima")
]
steady_dfs = steady_dfs[
    (steady_dfs["time"].between(-20, 10)) & (steady_dfs["phase"] != "clima")
]
# %%
sum_dfs = transient_dfs.copy()
for col in ["M2", "N", "P"]:
    sum_dfs[col] = transient_dfs[col] + steady_dfs[col]
# %%
sum_dfs_clima = transient_dfs_clima.copy()
for col in ["M2", "N", "P"]:
    sum_dfs_clima[col] = transient_dfs_clima[col] + steady_dfs_clima[col]
# %%
fig, axes = plt.subplots(2, 3, figsize=(10, 10), sharex=False, sharey="row")
# first row: 250 hPa, sum of M2 and N
# first col: sum of transient and steady

# Use black for 1850, red for 2090
custom_palette = {1850: "black", 2090: "red"}

sns.lineplot(
    data=sum_dfs[sum_dfs["plev"] == 25000],
    x="time",
    y="N",
    style="phase",
    hue="decade",
    ax=axes[0, 0],
    palette=custom_palette,
    errorbar=("ci", 95),
)

# plot the climatological data
first_color = "black"
second_color = "red"
axes[0, 0].axhline(
    y=sum_dfs_clima[
        (sum_dfs_clima["plev"] == 25000) & (sum_dfs_clima["decade"] == 1850)
    ]["N"].values[0],
    color=first_color,
    linestyle="dotted",
    label="first-clima",
)
# climatological data for 2090
axes[0, 0].axhline(
    y=sum_dfs_clima[
        (sum_dfs_clima["plev"] == 25000) & (sum_dfs_clima["decade"] == 2090)
    ]["N"].values[0],
    color=second_color,
    linestyle="dotted",
    label="last-clima",
)

# second col: transient
sns.lineplot(
    data=transient_dfs[transient_dfs["plev"] == 25000],
    x="time",
    y="N",
    style="phase",
    hue="decade",
    ax=axes[0, 1],
    palette=custom_palette,
    errorbar=("ci", 95),
)

# add climatological data for transient
axes[0, 1].axhline(
    y=transient_dfs_clima[
        (transient_dfs_clima["plev"] == 25000) & (transient_dfs_clima["decade"] == 1850)
    ]["N"].values[0],
    color=first_color,
    linestyle="dotted",
    label="first-clima",
)
axes[0, 1].axhline(
    y=transient_dfs_clima[
        (transient_dfs_clima["plev"] == 25000) & (transient_dfs_clima["decade"] == 2090)
    ]["N"].values[0],
    color=second_color,
    linestyle="dotted",
    label="last-clima",
)

# third col: steady
sns.lineplot(
    data=steady_dfs[steady_dfs["plev"] == 25000],
    x="time",
    y="N",
    style="phase",
    hue="decade",
    ax=axes[0, 2],
    palette=custom_palette,
    errorbar=("ci", 95),
)
# add climatological data for steady
axes[0, 2].axhline(
    y=steady_dfs_clima[
        (steady_dfs_clima["plev"] == 25000) & (steady_dfs_clima["decade"] == 1850)
    ]["N"].values[0],
    color=first_color,
    linestyle="dotted",
    label="first-clima",
)
axes[0, 2].axhline(
    y=steady_dfs_clima[
        (steady_dfs_clima["plev"] == 25000) & (steady_dfs_clima["decade"] == 2090)
    ]["N"].values[0],
    color=second_color,
    linestyle="dotted",
    label="last-clima",
)

# second row: 850 hPa, sum of M2, N and P
sns.lineplot(
    data=sum_dfs[sum_dfs["plev"]==70000],
    x="time",
    y="P",
    style="phase",
    hue="decade",
    ax=axes[1, 0],
    palette=custom_palette,
    errorbar=("ci", 95),
)

# climatological data for 850 hPa
axes[1, 0].axhline(
    y=sum_dfs_clima[
        (sum_dfs_clima["plev"]==70000) & (sum_dfs_clima["decade"] == 1850)
    ]["P"].values[0],
    color=first_color,
    linestyle="dotted",
    label="first-clima",
)
axes[1, 0].axhline(
    y=sum_dfs_clima[
        (sum_dfs_clima["plev"]==70000) & (sum_dfs_clima["decade"] == 2090)
    ]["P"].values[0],
    color=second_color,
    linestyle="dotted",
    label="last-clima",
)

# second col: transient
sns.lineplot(
    data=transient_dfs[transient_dfs["plev"]==70000],
    x="time",
    y="P",
    style="phase",
    hue="decade",
    ax=axes[1, 1],
    palette=custom_palette,
    errorbar=("ci", 95),
)
# add climatological data for transient
axes[1, 1].axhline(
    y=transient_dfs_clima[
        (transient_dfs_clima["plev"]==70000) & (transient_dfs_clima["decade"] == 1850)
    ]["P"].values[0],
    color=first_color,
    linestyle="dotted",
    label="first-clima",
)
axes[1, 1].axhline(
    y=transient_dfs_clima[
        (transient_dfs_clima["plev"]==70000) & (transient_dfs_clima["decade"] == 2090)
    ]["P"].values[0],
    color=second_color,
    linestyle="dotted",
    label="last-clima",
)
# third col: steady
sns.lineplot(
    data=steady_dfs[steady_dfs["plev"]==70000],
    x="time",
    y="P",
    style="phase",
    hue="decade",
    ax=axes[1, 2],
    palette=custom_palette,
    errorbar=("ci", 95),
)
# add climatological data for steady
axes[1, 2].axhline(
    y=steady_dfs_clima[
        (steady_dfs_clima["plev"]==70000) & (steady_dfs_clima["decade"] == 1850)
    ]["P"].values[0],
    color=first_color,
    linestyle="dotted",
    label="first-clima",
)
axes[1, 2].axhline(
    y=steady_dfs_clima[
        (steady_dfs_clima["plev"]==70000) & (steady_dfs_clima["decade"] == 2090)
    ]["P"].values[0],
    color=second_color,
    linestyle="dotted",
    label="last-clima",
)

# Only add legend to axes[1, 2], remove all others
# Remove all legends first
for ax in axes.flat:
    ax.get_legend().remove()

# Custom legend handles

# Decade legend (colors)
decade_handles = [
    Line2D([0], [0], color="black", lw=2, label="1850s"),
    Line2D([0], [0], color="red", lw=2, label="2090s"),
]

# Phase legend (styles)
phase_handles = [
    Line2D([0], [0], color="black", lw=2, linestyle="-", label="pos NAO"),
    Line2D([0], [0], color="black", lw=2, linestyle="--", label="neg NAO"),
    Line2D([0], [0], color="black", lw=2, linestyle="dotted", label="climatology"),
]

# Place legends: first col for decade, second for phase
decade_legend = axes[1, 2].legend(
    handles=decade_handles,
    title="decade",
    loc="upper left",
    bbox_to_anchor=(0.1, 1),
    frameon=False,
)
phase_legend = axes[1, 2].legend(
    handles=phase_handles,
    title="phase",
    loc="upper left",
    bbox_to_anchor=(0.5, 1),
    frameon=False,
)
axes[1, 2].add_artist(decade_legend)


for ax in axes[0, :].flat:
    ax.set_xlabel("")

for ax in axes[1, :].flat:
    ax.set_xlabel("Days relative to extreme onset")

axes[0, 0].set_ylabel(
    "",
)
axes[1, 0].set_ylabel(
    r"$\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta'}}{\overline{\theta}_p} \right)$ [m $s^{-1}$ day $^{-1}$]",
)

# remove top and right spines
for ax in axes.flat:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # Add grid lines only at x=0 and y=0
    ax.axvline(0, color="k", linestyle="-", lw=0.5, zorder=0)
plt.tight_layout()

# add a, b, c
for i, ax in enumerate(axes.flat):
    ax.text(
        -0.06,
        0.96,
        chr(97 + i),
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        va="bottom",
        ha="right",
    )


# # save figure
# plt.savefig(
#     "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0main_text/vpqp_eddy_flux_line.pdf",
#     bbox_inches="tight",
#     dpi=300,
#     transparent=True,
#     metadata={"Creator": __file__},
# )

#%%


# %%

phi_sum_levels = np.arange(-0.3, 0.31, 0.1)
phi_trans_levels = np.arange(-0.15, 0.16, 0.05)
phi_steady_levels = np.arange(-0.15, 0.16, 0.05)



#%%

fig, axes = plt.subplots(3, 3, figsize=(12, 12), sharex=False, sharey="row")

# first row momentum fluxes Phi positive
cf_phi_sum = (div_phi_pos_first_anomaly).plot.contourf(
    ax=axes[0, 0],
    levels=phi_sum_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend='both',
    xlim=(0, 90),
    ylim=(100000, 10000),
    
)
contour_levels = [l for l in phi_sum_levels if l != 0]
(div_phi_pos_last_anomaly).plot.contour(
    ax=axes[0, 0],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_phi_trans = (Tdiv_phi_pos_first_anomaly).plot.contourf(
    ax=axes[0, 1],
    levels=phi_trans_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend='both',
    xlim=(0, 90),
    ylim=(100000, 10000),
    
)
contour_levels = [l for l in phi_trans_levels if l != 0]
(Tdiv_phi_pos_last_anomaly).plot.contour(
    ax=axes[0, 1],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_phi_steady = (Sdivphi_pos_first_anomaly).plot.contourf(
    ax=axes[0, 2],
    levels=phi_steady_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend='both',
    xlim=(0, 90),
    ylim=(100000, 10000),
    
)
contour_levels = [l for l in phi_steady_levels if l != 0]
(Sdivphi_pos_last_anomaly).plot.contour(
    ax=axes[0, 2],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

# second row momentum fluxes Phi (negative phase)
cf_phi_sum = (div_phi_neg_first_anomaly).plot.contourf(
    ax=axes[1, 0],
    levels=phi_sum_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend='both',
    xlim=(0, 90),
    ylim=(100000, 10000),
    
)
contour_levels = [l for l in phi_sum_levels if l != 0]
(div_phi_neg_last_anomaly).plot.contour(
    ax=axes[1, 0],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_phi_trans = (Tdiv_phi_neg_first_anomaly).plot.contourf(
    ax=axes[1, 1],
    levels=phi_trans_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend='both',
    xlim=(0, 90),
    ylim=(100000, 10000),
    
)
contour_levels = [l for l in phi_trans_levels if l != 0]
(Tdiv_phi_neg_last_anomaly).plot.contour(
    ax=axes[1, 1],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_phi_steady = (Sdivphi_neg_first_anomaly).plot.contourf(
    ax=axes[1, 2],
    levels=phi_steady_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend='both',
    xlim=(0, 90),
    ylim=(100000, 10000),
    
)
contour_levels = [l for l in phi_steady_levels if l != 0]
(Sdivphi_neg_last_anomaly).plot.contour(
    ax=axes[1, 2],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,    
    xlim=(0, 90),
    ylim=(100000, 10000)
)

# third row line plots

# Use black for 1850, red for 2090
custom_palette = {1850: "black", 2090: "red"}

# first ten years
sum_first_ano = sum_dfs[(sum_dfs["plev"] == 25000) & (sum_dfs['decade'] == 1850)]
# remove the clima data
sum_first_ano.loc[:, 'N'] = sum_first_ano['N'] - sum_dfs_clima[
        (sum_dfs_clima["plev"] == 25000) & (sum_dfs_clima["decade"] == 1850)
    ]["N"].values


# last ten years
sum_last_ano = sum_dfs[(sum_dfs["plev"] == 25000) & (sum_dfs['decade'] == 2090)]
# remove the clima data
sum_last_ano.loc[:, 'N'] = sum_last_ano['N'] - sum_dfs_clima[
        (sum_dfs_clima["plev"] == 25000) & (sum_dfs_clima["decade"] == 2090)
    ]["N"].values


sns.lineplot(
    data=sum_first_ano,
    x="time",
    y="N",
    style="phase",
    color = 'black',
    ax=axes[2, 0],
    errorbar=("ci", 95),
)

sns.lineplot(
    data=sum_last_ano,
    x="time",
    y="N",
    style="phase",
    color = 'red',
    ax=axes[2, 0],
    errorbar=("ci", 95),
)

# second col: transient
transient_first_ano = transient_dfs[(transient_dfs["plev"] == 25000) & (transient_dfs['decade'] == 1850)]
# remove the clima data
transient_first_ano.loc[:, 'N'] = transient_first_ano['N'] - transient_dfs_clima[
        (transient_dfs_clima["plev"] == 25000) & (transient_dfs_clima["decade"] == 1850)
    ]["N"].values


transient_last_ano = transient_dfs[(transient_dfs["plev"] == 25000) & (transient_dfs['decade'] == 2090)]
# remove the clima data
transient_last_ano.loc[:, 'N'] = transient_last_ano['N'] - transient_dfs_clima[
        (transient_dfs_clima["plev"] == 25000) & (transient_dfs_clima["decade"] == 2090)
    ]["N"].values
sns.lineplot(
    data=transient_first_ano,
    x="time",
    y="N",
    style="phase",
    color = 'black',    
    ax=axes[2, 1],
    errorbar=("ci", 95),
)
sns.lineplot(
    data=transient_last_ano,
    x="time",
    y="N",
    style="phase",
    color = 'red',
    ax=axes[2, 1],
    errorbar=("ci", 95),
)

# third col: steady
steady_first_ano = steady_dfs[(steady_dfs["plev"] == 25000) & (steady_dfs['decade'] == 1850)]
# remove the clima data
steady_first_ano.loc[:, 'N'] = steady_first_ano['N'] - steady_dfs_clima[
        (steady_dfs_clima["plev"] == 25000) & (steady_dfs_clima["decade"] == 1850)
    ]["N"].values

steady_last_ano = steady_dfs[(steady_dfs["plev"] == 25000) & (steady_dfs['decade'] == 2090)]
# remove the clima data
steady_last_ano.loc[:, 'N'] = steady_last_ano['N'] - steady_dfs_clima[
        (steady_dfs_clima["plev"] == 25000) & (steady_dfs_clima["decade"] == 2090)
    ]["N"].values

sns.lineplot(
    data=steady_first_ano,
    x="time",
    y="N",
    style="phase",
    color = 'black',
    ax=axes[2,2],
    errorbar=("ci", 95),
)
sns.lineplot(
    data=steady_last_ano,
    x="time",
    y="N",
    style="phase",
    color = 'red',
    ax=axes[2,2],
    errorbar=("ci", 95),
)


# add the colorbar at the bottom of the second row
# Add colorbars with reduced number of ticks to avoid overlapping ticklabels


cbar_sum = fig.colorbar(
    cf_phi_sum,
    ax=axes[:2, 0],
    orientation="horizontal",
    fraction=0.02,
    pad=0.1,
    aspect=30,
    shrink=0.8,
    label = r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m $s^{-1}$ day $^{-1}$]",
)


cbar_transient = fig.colorbar(
    cf_phi_trans,
    ax=axes[:2, 1],
    orientation="horizontal",
    fraction=0.02,
    pad=0.1,
    aspect=30,
    shrink=0.8,
    label = r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m $s^{-1}$ day $^{-1}$]",
)
cbar_transient.set_ticks([-0.1, 0.0, 0.1])

cbar_steady = fig.colorbar(
    cf_phi_steady,  
    ax=axes[:2, 2],
    orientation="horizontal",
    fraction=0.02,
    pad=0.1,
    aspect=30,
    shrink=0.8,
    label = r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m $s^{-1}$ day $^{-1}$]",
)
cbar_steady.set_ticks([-0.1, 0.0, 0.1])

# Only show legend on last col, remove from others
for ax in axes[2, :-1]:
    ax.get_legend().remove()

# Custom legend handles
decade_handles = [
    Line2D([0], [0], color="black", lw=2, label="1850"),
    Line2D([0], [0], color="red", lw=2, label="2090"),
]
phase_handles = [
    Line2D([0], [0], color="black", lw=2, linestyle="-", label="pos NAO"),
    Line2D([0], [0], color="black", lw=2, linestyle="--", label="neg NAO"),
]
decade_legend = axes[2, 2].legend(
    handles=decade_handles,
    title="decade",
    loc="upper left",
    bbox_to_anchor=(0., 0.3),
    frameon=False,
)
phase_legend = axes[2, 2].legend(
    handles=phase_handles,
    title="phase",
    loc="upper left",
    bbox_to_anchor=(0.4, 0.3),
    frameon=False,
)
axes[2, 2].add_artist(decade_legend)
axes[2, 2].add_artist(phase_legend)

axes[2, 2].set_ylabel("")

for ax in axes[:, 1:].flat:
    ax.set_ylabel("")
axes[2, 0].set_ylabel(
r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m $s^{-1}$ day $^{-1}$]")


# for the first column, set y-label for eddy momentum flux (Pa to hPa)
for ax in axes[:2, 0].flat:
    ax.set_ylabel("Pressure [hPa]")
    ax.set_yticks([100000, 90000, 80000, 70000, 60000, 50000, 40000, 30000, 20000, 10000])
    ax.set_yticklabels([str(int(tick / 100)) for tick in ax.get_yticks()])  # Convert Pa to hPa
for ax in axes[1, :].flat:
    ax.set_xlabel("lat [°N]")
for ax in axes[0, :].flat:
    ax.set_xlabel("")

for ax in axes[2, :].flat:
    ax.set_xlabel("Days relative to extreme onset")

# remove top and right spines
for ax in axes[2, :].flat:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # Add grid lines only at x=0 and y=0
    ax.axvline(0, color="k", linestyle="-", lw=0.5, zorder=0)

# add a,b,c
for i, ax in enumerate(axes.flat):
    ax.text(
        -0.06,
        1.02,
        chr(97 + i),
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        va="bottom",
        ha="right",
    )

# save
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eddy_momentum_together.pdf",
    dpi=300,
    bbox_inches="tight",
    transparent=True,
    metadata={"Creator": __file__},
)


#%%
#%%
# Plot for the p component (thermodynamic eddy flux)

p_sum_levels = np.arange(-4, 4.1, 1)
p_trans_levels = np.arange(-2, 2.1, 0.5)
p_steady_levels = np.arange(-2, 2.1, 0.5)

fig, axes = plt.subplots(3, 3, figsize=(12, 12), sharex=False, sharey="row")

# first row: positive phase
cf_p_sum = (div_p_pos_first_anomaly).plot.contourf(
    ax=axes[0, 0],
    levels=p_sum_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend='both',
    xlim=(0, 90),
    ylim=(100000, 10000),
)
contour_levels = [l for l in p_sum_levels if l != 0]
(div_p_pos_last_anomaly).plot.contour(
    ax=axes[0, 0],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_p_trans = (Tdiv_p_pos_first_anomaly).plot.contourf(
    ax=axes[0, 1],
    levels=p_trans_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend='both',
    xlim=(0, 90),
    ylim=(100000, 10000),
)
contour_levels = [l for l in p_trans_levels if l != 0]
(Tdiv_p_pos_last_anomaly).plot.contour(
    ax=axes[0, 1],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_p_steady = (Sdiv_p_pos_first_anomaly).plot.contourf(
    ax=axes[0, 2],
    levels=p_steady_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend='both',
    xlim=(0, 90),
    ylim=(100000, 10000),
)
contour_levels = [l for l in p_steady_levels if l != 0]
(Sdiv_p_pos_last_anomaly).plot.contour(
    ax=axes[0, 2],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,
    xlim=(0, 90),
    ylim=(100000, 10000)
)

# second row: negative phase
cf_p_sum = (div_p_neg_first_anomaly).plot.contourf(
    ax=axes[1, 0],
    levels=p_sum_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend='both',
    xlim=(0, 90),
    ylim=(100000, 10000),
)
contour_levels = [l for l in p_sum_levels if l != 0]
(div_p_neg_last_anomaly).plot.contour(
    ax=axes[1, 0],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_p_trans = (Tdiv_p_neg_first_anomaly).plot.contourf(
    ax=axes[1, 1],
    levels=p_trans_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend='both',
    xlim=(0, 90),
    ylim=(100000, 10000),
)
contour_levels = [l for l in p_trans_levels if l != 0]
(Tdiv_p_neg_last_anomaly).plot.contour(
    ax=axes[1, 1],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,
    xlim=(0, 90),
    ylim=(100000, 10000)
)

cf_p_steady = (Sdiv_p_neg_first_anomaly).plot.contourf(
    ax=axes[1, 2],
    levels=p_steady_levels,
    cmap="RdBu_r",
    add_colorbar=False,
    extend='both',
    xlim=(0, 90),
    ylim=(100000, 10000),
)
contour_levels = [l for l in p_steady_levels if l != 0]
(Sdiv_p_neg_last_anomaly).plot.contour(
    ax=axes[1, 2],
    levels=contour_levels,
    colors='k',
    linewidths=1,
    add_colorbar=False,
    xlim=(0, 90),
    ylim=(100000, 10000)
)

# third row: line plots

# Use black for 1850, red for 2090
custom_palette = {1850: "black", 2090: "red"}

# first ten years
sum_first_ano = sum_dfs[(sum_dfs["plev"]==70000) & (sum_dfs['decade'] == 1850)]
sum_first_ano = sum_first_ano.copy()
sum_first_ano.loc[:, 'P'] = sum_first_ano['P'] - sum_dfs_clima[
    (sum_dfs_clima["plev"]==70000) & (sum_dfs_clima["decade"] == 1850)
]["P"].values

# last ten years
sum_last_ano = sum_dfs[(sum_dfs["plev"]==70000) & (sum_dfs['decade'] == 2090)]
sum_last_ano = sum_last_ano.copy()
sum_last_ano.loc[:, 'P'] = sum_last_ano['P'] - sum_dfs_clima[
    (sum_dfs_clima["plev"]==70000) & (sum_dfs_clima["decade"] == 2090)
]["P"].values

sns.lineplot(
    data=sum_first_ano,
    x="time",
    y="P",
    style="phase",
    color='black',
    ax=axes[2, 0],
    errorbar=("ci", 95),
)
sns.lineplot(
    data=sum_last_ano,
    x="time",
    y="P",
    style="phase",
    color='red',
    ax=axes[2, 0],
    errorbar=("ci", 95),
)

# second col: transient
transient_first_ano = transient_dfs[(transient_dfs["plev"]==70000) & (transient_dfs['decade'] == 1850)]
transient_first_ano = transient_first_ano.copy()
transient_first_ano.loc[:, 'P'] = transient_first_ano['P'] - transient_dfs_clima[
    (transient_dfs_clima["plev"]==70000) & (transient_dfs_clima["decade"] == 1850)
]["P"].values

transient_last_ano = transient_dfs[(transient_dfs["plev"]==70000) & (transient_dfs['decade'] == 2090)]
transient_last_ano = transient_last_ano.copy()
transient_last_ano.loc[:, 'P'] = transient_last_ano['P'] - transient_dfs_clima[
    (transient_dfs_clima["plev"]==70000) & (transient_dfs_clima["decade"] == 2090)
]["P"].values

sns.lineplot(
    data=transient_first_ano,
    x="time",
    y="P",
    style="phase",
    color='black',
    ax=axes[2, 1],
    errorbar=("ci", 95),
)
sns.lineplot(
    data=transient_last_ano,
    x="time",
    y="P",
    style="phase",
    color='red',
    ax=axes[2, 1],
    errorbar=("ci", 95),
)

# third col: steady
steady_first_ano = steady_dfs[(steady_dfs["plev"]==70000) & (steady_dfs['decade'] == 1850)]
steady_first_ano = steady_first_ano.copy()
steady_first_ano.loc[:, 'P'] = steady_first_ano['P'] - steady_dfs_clima[
    (steady_dfs_clima["plev"]==70000) & (steady_dfs_clima["decade"] == 1850)
]["P"].values

steady_last_ano = steady_dfs[(steady_dfs["plev"]==70000) & (steady_dfs['decade'] == 2090)]
steady_last_ano = steady_last_ano.copy()
steady_last_ano.loc[:, 'P'] = steady_last_ano['P'] - steady_dfs_clima[
    (steady_dfs_clima["plev"]==70000) & (steady_dfs_clima["decade"] == 2090)
]["P"].values

sns.lineplot(
    data=steady_first_ano,
    x="time",
    y="P",
    style="phase",
    color='black',
    ax=axes[2, 2],
    errorbar=("ci", 95),
)
sns.lineplot(
    data=steady_last_ano,
    x="time",
    y="P",
    style="phase",
    color='red',
    ax=axes[2, 2],
    errorbar=("ci", 95),
)

# Add colorbars
cbar_sum = fig.colorbar(
    cf_p_sum,
    ax=axes[:2, 0],
    orientation="horizontal",
    fraction=0.02,
    pad=0.1,
    aspect=30,
    shrink=0.8,
    label=r"$-\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta'}}{\overline{\theta}_p} \right)$ [m $s^{-1}$ day $^{-1}$]",
)
cbar_transient = fig.colorbar(
    cf_p_trans,
    ax=axes[:2, 1],
    orientation="horizontal",
    fraction=0.02,
    pad=0.1,
    aspect=30,
    shrink=0.8,
    label=r"$-\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta'}}{\overline{\theta}_p} \right)$ [m $s^{-1}$ day $^{-1}$]",
)
# cbar_transient.set_ticks([-1, 0.0, 1])
cbar_steady = fig.colorbar(
    cf_p_steady,
    ax=axes[:2, 2],
    orientation="horizontal",
    fraction=0.02,
    pad=0.1,
    aspect=30,
    shrink=0.8,
    label=r"$-\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta'}}{\overline{\theta}_p} \right)$ [m $s^{-1}$ day $^{-1}$]",
)
# cbar_steady.set_ticks([-1, 0.0, 1])

# Only show legend on last col, remove from others
for ax in axes[2, :-1]:
    ax.get_legend().remove()

# Custom legend handles
decade_handles = [
    Line2D([0], [0], color="black", lw=2, label="1850"),
    Line2D([0], [0], color="red", lw=2, label="2090"),
]
phase_handles = [
    Line2D([0], [0], color="black", lw=2, linestyle="-", label="pos NAO"),
    Line2D([0], [0], color="black", lw=2, linestyle="--", label="neg NAO"),
]
decade_legend = axes[2, 2].legend(
    handles=decade_handles,
    title="decade",
    loc="upper left",
    bbox_to_anchor=(0., 0.3),
    frameon=False,
)
phase_legend = axes[2, 2].legend(
    handles=phase_handles,
    title="phase",
    loc="upper left",
    bbox_to_anchor=(0.4, 0.3),
    frameon=False,
)
axes[2, 2].add_artist(decade_legend)
axes[2, 2].add_artist(phase_legend)

axes[2, 2].set_ylabel("")

for ax in axes[:, 1:].flat:
    ax.set_ylabel("")
axes[2, 0].set_ylabel(
    r"$-\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta'}}{\overline{\theta}_p} \right)$ [m $s^{-1}$ day $^{-1}$]"
)

# for the first column, set y-label for eddy thermodynamic flux (Pa to hPa)
for ax in axes[:2, 0].flat:
    ax.set_ylabel("Pressure [hPa]")
    ax.set_yticks([100000, 90000, 80000, 70000, 60000, 50000, 40000, 30000, 20000, 10000])
    ax.set_yticklabels([str(int(tick / 100)) for tick in ax.get_yticks()])
for ax in axes[1, :].flat:
    ax.set_xlabel("lat [°N]")
for ax in axes[0, :].flat:
    ax.set_xlabel("")
for ax in axes[2, :].flat:
    ax.set_xlabel("Days relative to extreme onset")

# remove top and right spines
for ax in axes[2, :].flat:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.axvline(0, color="k", linestyle="-", lw=0.5, zorder=0)

# add a,b,c
for i, ax in enumerate(axes.flat):
    ax.text(
        -0.06,
        1.02,
        chr(97 + i),
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        va="bottom",
        ha="right",
    )

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eddy_heat_together.pdf",
    dpi=300,
    bbox_inches="tight",
    transparent=True,
    metadata={"Creator": __file__},
)
# %%
