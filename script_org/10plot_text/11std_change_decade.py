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

#%%
jet = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/ua_decmean_ensmean_25000hPa.nc")
baroclinic = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/eady_growth_rate_decmean_ensmean_85000hPa.nc")

transient_momentum = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/Fdiv_phi_transient_decmean_ensmean_25000hPa.nc")
steady_momentum = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/Fdiv_phi_steady_decmean_ensmean_25000hPa.nc")

sum_momentum = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/Fdiv_phi_transient_Fdiv_phi_steady_sum_decmean_ensmean_25000hPa.nc")

transient_heat = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/transient_eddy_heat_dy_decmean_ensmean_85000hPa.nc")
steady_heat = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/steady_eddy_heat_dy_decmean_ensmean_85000hPa.nc")

#%%
def to_dataframe(ds, var_name, base=None):
    """Convert xarray dataset to pandas DataFrame."""
    df = ds['std'].squeeze().to_dataframe(var_name).reset_index()
    df['decade'] = (df['time'].dt.year // 10) * 10

    if base is None:
        # use the same
        base = df[df['decade'] == 1850][var_name].values[0]
    else:
        base = base['std'].squeeze().to_dataframe(var_name).reset_index()
        base['decade'] = (base['time'].dt.year // 10) * 10
        base = base[base['decade'] == 1850][var_name].values[0]

    # standardize the var_name coloumn name
    df[var_name] = df[var_name] / base
    return df

#%%
jet = to_dataframe(jet, 'jet_stream')
baroclinic = to_dataframe(baroclinic, 'baroclinic')
transient_heat = to_dataframe(transient_heat, 'heat_flux')
steady_heat = to_dataframe(steady_heat, 'heat_flux')

#%%
transient_momentum = to_dataframe(transient_momentum, 'momentum_flux')
steady_momentum = to_dataframe(steady_momentum, 'momentum_flux')
sum_momentum = to_dataframe(sum_momentum, 'momentum_flux_sum')


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
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

# NAO
sns.lineplot(
    data=NAO_merge,
    x="decade",
    y="days_pos",
    ax=axes[0, 0],
    label="pos NAO",
    color="k",
    linewidth=2,
)
sns.lineplot(
    data=NAO_merge,
    x="decade",
    y="days_neg",
    ax=axes[0, 0],
    label="neg NAO",
    color="k",
    linestyle="--",
    linewidth=2,
)

# jet and baroclinic
sns.lineplot(
    data=jet,
    x="decade",
    y="jet_stream",
    ax=axes[0, 1],
    label="jet stream",
    color="k",
    linewidth=2,
)
sns.lineplot(
    data=baroclinic,
    x="decade",
    y="baroclinic",
    ax=axes[0, 1],
    label="baroclinic",
    color="k",
    linestyle="--",
    linewidth=2,
)

# momentum flux
sns.lineplot(
    data=transient_momentum,
    x="decade",
    y="momentum_flux",
    ax=axes[1, 0],
    label="transient",
    color='k',
    linewidth=2,
)
sns.lineplot(
    data=steady_momentum,
    x="decade",
    y="momentum_flux",
    ax=axes[1, 0],
    label="stationary",
    color='k',
    linestyle="--",
    linewidth=2,
)
# sum
sns.lineplot(
    data=sum_momentum,
    x="decade",
    y="momentum_flux_sum",
    ax=axes[1, 0],
    label="sum",
    color='k',
    linestyle=":",
    linewidth=2,
)


# heat flux
sns.lineplot(
    data=transient_heat,
    x="decade",
    y="heat_flux",
    ax=axes[1, 1],
    label="transient",
    color='k',
    linewidth=2,
)
sns.lineplot(
    data=steady_heat,
    x="decade",
    y="heat_flux",
    ax=axes[1, 1],
    label="stationary",
    color='k',
    linestyle="--",
    linewidth=2,
)

for ax in axes.flat:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis='both', labelsize=16)
    ax.set_xlabel(ax.get_xlabel(), fontsize=16)
    # Set legend font size if legend exists
    leg = ax.get_legend()
    if leg is not None:
        for text in leg.get_texts():
            text.set_fontsize(16)

# add a, b, c
for i, ax in enumerate(axes.flat):
    ax.text(
        -0.1,
        1.05,
        f"{chr(97+i)}",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
    )

axes[0, 0].set_ylabel("extreme NAO days", fontsize=16)
axes[0, 1].set_ylabel("jet stream / baroclinic std", fontsize=16)
axes[1, 0].set_ylabel(r"$-\partial \overline{u'v'}/\partial y$ std", fontsize=16)
axes[1, 1].set_ylabel(r"$-\partial \overline{v'\theta'}/\partial y$ std", fontsize=16)
plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/std_change_dec.pdf", dpi=300, bbox_inches="tight", transparent=True)
# %%