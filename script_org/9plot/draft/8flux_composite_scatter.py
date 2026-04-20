#%%
from glob import glob

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

from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm, to_hex
from src.plotting.util import map_smooth
import src.plotting.util as util
import metpy.calc as mpcalc
from metpy.units import units
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec
from src.data_helper.read_NAO_extremes import read_NAO_extremes

# %%
data_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0composite_feedback"

def load_composite(name):
    return xr.open_dataarray(os.path.join(data_dir, f"{name}.nc"))

# ---- 1850s and 2090s composite ----
#%%
ua_pos_first = load_composite("ua_hat_pos_1850")
ua_neg_first = load_composite("ua_hat_neg_1850")
ua_pos_last  = load_composite("ua_hat_pos_2090")
ua_neg_last  = load_composite("ua_hat_neg_2090")

ua_pos_first = ua_pos_first.sel(lat = slice(0, 70))
ua_neg_first = ua_neg_first.sel(lat = slice(0, 70))
ua_pos_last  = ua_pos_last.sel(lat = slice(0, 70))
ua_neg_last  = ua_neg_last.sel(lat = slice(0, 70))

#%%
awb_pos_first = load_composite("wb_anticyclonic_pos_1850")
awb_neg_first = load_composite("wb_anticyclonic_neg_1850")
awb_pos_last  = load_composite("wb_anticyclonic_pos_2090")
awb_neg_last  = load_composite("wb_anticyclonic_neg_2090")


#%%
# baroclinic growth rate
baroc_pos_first = load_composite("eady_growth_rate_pos_1850")
baroc_neg_first = load_composite("eady_growth_rate_neg_1850")
baroc_pos_last  = load_composite("eady_growth_rate_pos_2090")
baroc_neg_last  = load_composite("eady_growth_rate_neg_2090")


#%%
zg_hat_pos_first = load_composite("zg_hat_pos_1850")
zg_hat_neg_first = load_composite("zg_hat_neg_1850")
zg_hat_pos_last  = load_composite("zg_hat_pos_2090")
zg_hat_neg_last  = load_composite("zg_hat_neg_2090")


#%%
# eddy driven jet
ua_pos_first = ua_pos_first.sel(plev=slice(92500, 70000)).mean(dim="plev")
ua_neg_first = ua_neg_first.sel(plev=slice(92500, 70000)).mean(dim="plev")
ua_pos_last  = ua_pos_last.sel(plev=slice(92500, 70000)).mean(dim="plev")
ua_neg_last  = ua_neg_last.sel(plev=slice(92500, 70000)).mean(dim="plev")
# select levels
zg_hat_pos_first = zg_hat_pos_first.sel(plev=50000)
zg_hat_neg_first = zg_hat_neg_first.sel(plev=50000)
zg_hat_pos_last  = zg_hat_pos_last.sel(plev=50000)
zg_hat_neg_last  = zg_hat_neg_last.sel(plev=50000)


#%%
# fldmean over
def to_dataframe(ds, var_name, phase, decade, lat_slice = slice(50, 70), ds_clim = None):
    ds = ds.sel(lat=lat_slice)    
    if ds_clim is not None:
        ds_clim = ds_clim.sel(lat=lat_slice)
        ds = ds - ds_clim # anomaly

    # create weights
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"

    ds = ds.weighted(weights).mean(dim = ('lat'))

    df = ds.to_dataframe(var_name).reset_index()
    df["phase"] = phase
    df["decade"] = decade
    return df
#%% calculate the jet location (lat of max ua)
def jet_latitude(ua, phase, decade = None, to_df = True):
    # a limit of jet loc between (25, 70)
    ua = ua.sel(lat=slice(25, 70))
    # average over lon if present, then find lat of max ua
    if "lon" in ua.dims:
        ua = ua.mean(dim="lon")
    if "plev" in ua.dims:
        ua = ua.sel(plev=slice(92500, 70000)).mean(dim="plev") # eddy driven jet
    jet_lat = ua.idxmax(dim="lat")
    if to_df:
        jet_lat_df = jet_lat.to_dataframe("jet_lat").reset_index()
        jet_lat_df["phase"] = phase
        jet_lat_df["decade"] = decade
        return jet_lat_df
    else:
        return jet_lat

#%%
# awb_lat_slice = slice(40, 60)
# cwb_lat_slice = slice(50, 70)
awb_pos_first_df = awb_pos_first.to_dataframe("awb").reset_index()
awb_pos_first_df["phase"] = "pos"
awb_pos_first_df["decade"] = 1850

awb_pos_last_df  = awb_pos_last.to_dataframe("awb").reset_index()
awb_pos_last_df["phase"] = "pos"
awb_pos_last_df["decade"] = 2090

awb_pos_df = pd.concat([awb_pos_first_df, awb_pos_last_df], ignore_index=True)

#%%
jet_lat_pos_first = jet_latitude(ua_pos_first, "pos", 1850)
jet_lat_pos_last  = jet_latitude(ua_pos_last,  "pos", 2090)
jet_lat_pos_df = pd.concat([jet_lat_pos_first, jet_lat_pos_last], ignore_index=True)

pos_df = awb_pos_df.merge(jet_lat_pos_df, on=['event', 'time', 'phase', 'decade'], how='inner')
#%%
baroc_neg_first_df = to_dataframe(baroc_neg_first, "baroclinicity", "neg", 1850,)
baroc_neg_last_df  = to_dataframe(baroc_neg_last,  "baroclinicity", "neg", 2090,)
baroc_neg_df = pd.concat([baroc_neg_first_df, baroc_neg_last_df], ignore_index=True)
baroc_neg_df['baroclinicity'] = baroc_neg_df['baroclinicity'] * 86400 # convert to day^-1   


zg_hat_neg_first_df = to_dataframe(zg_hat_neg_first, "GB_index", "neg", 1850, lat_slice= slice(60, 80))
zg_hat_neg_last_df  = to_dataframe(zg_hat_neg_last,  "GB_index", "neg", 2090, lat_slice= slice(60, 80))
zg_hat_neg_df = pd.concat([zg_hat_neg_first_df, zg_hat_neg_last_df], ignore_index=True)

# drop plev from zg_steady and baroc_neg
zg_hat_neg_df = zg_hat_neg_df.drop(columns=["plev"])
baroc_neg_df = baroc_neg_df.drop(columns=["plev"])

neg_df = baroc_neg_df.merge(zg_hat_neg_df, on=['event', 'time', 'phase', 'decade'], how='inner')

#%%
pos_df = pos_df[pos_df['time'].isin(range(0, 31))]
neg_df = neg_df[neg_df['time'].isin(range(0, 31))]

# %% NAO daily extremes
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


NAO_pos_count, NAO_neg_count = NAO_extremes(False, 5)
NAO_pos_days, NAO_neg_days = NAO_extremes(True, 5)

NAO_pos_days = NAO_pos_days.rename(columns={"count": "days"})
NAO_neg_days = NAO_neg_days.rename(columns={"count": "days"})

NAO_count_merge = pd.merge(
    NAO_pos_count, NAO_neg_count, on="decade", suffixes=("_pos", "_neg")
)
NAO_days_merge = pd.merge(
    NAO_pos_days, NAO_neg_days, on="decade", suffixes=("_pos", "_neg")
)
NAO_merge = pd.merge(NAO_count_merge, NAO_days_merge, on="decade")

NAO_merge["decade"] = NAO_merge["decade"].astype(int)

#%%
# ---- composite for each decade ----
all_dec_dir = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0composite_feedback_alldec/'

def _add_decade_dim(da, decade):
    da = da.expand_dims(decade=[decade])
    return da

def load_composite_decade(var, phase, lat_slice = None):
    decades = np.arange(1850, 2100, 10)
    das = []
    for decade in decades:
        try:
            da = xr.open_dataarray(os.path.join(all_dec_dir, f"{var}_NAO_{phase}_{decade}.nc"))
            da = _add_decade_dim(da, decade)
            das.append(da)
        except FileNotFoundError:
            print(f"File for decade {decade} not found, skipping")
    if len(das) == 0:
        raise ValueError(f"No files found for variable {var} and phase {phase}")
  
    das = xr.concat(das, dim="decade")
    if lat_slice is not None:
        das = das.sel(lat=lat_slice).mean(dim="lat")
    return das

#%%
awb_pos_decades = load_composite_decade("wb_anticyclonic_allisen", "pos", lat_slice=None)
#%%
jet_pos_decades = load_composite_decade("jetloc_", "pos", lat_slice=None) # for jet loc

#%%
baroc_neg_decades = load_composite_decade("eady_growth_rate", "neg", lat_slice=slice(50, 70))
# unit
baroc_neg_decades = baroc_neg_decades * 86400 # convert to day^-1

zg_hat_neg_decades = load_composite_decade("zg_hat", "neg", lat_slice=slice(60, 80))

#%%
# to df
awb_pos_decades_df = awb_pos_decades.to_dataframe("awb").reset_index()
awb_pos_decades_df["phase"] = "pos"
jet_pos_decades_df = jet_pos_decades.to_dataframe("jet_lat").reset_index()
jet_pos_decades_df["phase"] = "pos"


baroc_neg_decades_df = baroc_neg_decades.to_dataframe("baroclinicity").reset_index()
baroc_neg_decades_df["phase"] = "neg"
zg_hat_neg_decades_df = zg_hat_neg_decades.to_dataframe("GB_index").reset_index()
zg_hat_neg_decades_df["phase"] = "neg"

#%%
dec_pos_df = awb_pos_decades_df.merge(jet_pos_decades_df, on=["decade", "phase"], how="inner").merge(NAO_merge[['days_pos', 'decade']], on="decade", how="inner")

dec_neg_df = baroc_neg_decades_df.merge(zg_hat_neg_decades_df, on=["decade", "phase"], how="inner").merge(NAO_merge[['days_neg', 'decade']], on="decade", how="inner")
# %%# ===== Density plots =====
COLOR_1850 = "#4C72B0"
COLOR_2090 = "#DD8452"

# Discrete colormap: one distinct color per decade (25 decades)
# Endpoints are pinned to row-1 colors; vivid teal anchors the middle
_continuous = LinearSegmentedColormap.from_list(
    "_decade_base",
    [COLOR_1850, "#29AB87", COLOR_2090],
    N=256,
)
decades_all = np.arange(1850, 2100, 10)   # 25 decades
_n = len(decades_all)
_colors = [to_hex(_continuous(i / (_n - 1))) for i in range(_n)]
_cmap_decades = ListedColormap(_colors, name="decade_cmap")
_bounds = np.arange(1845, 2100, 10)       # boundaries between decades
_norm_decades = BoundaryNorm(_bounds, _cmap_decades.N)
decade_palette = {int(dec): _colors[i] for i, dec in enumerate(decades_all)}

fig, axes = plt.subplots(2, 2, figsize=(9, 9))

# ----- Plot 1: pos_df, x=jet_lat, y=awb -----
_pos_plot_data = pos_df.groupby(['event', 'phase', 'decade'])[['jet_lat', 'awb']].mean().reset_index()
_pos_plot_data['awb'] = _pos_plot_data['awb'] * 100 # convert to percentage
sns.kdeplot(
    data = _pos_plot_data[_pos_plot_data['decade'] == 1850],
    x = "jet_lat",
    y = "awb",
    alpha = 0.8,
    color = 'k',
    linestyles = 'solid',
    ax = axes[0, 0],
    levels = np.arange(0.0, 1.1, 0.2),
    common_norm=False,
)
sns.kdeplot(
    data = _pos_plot_data[_pos_plot_data['decade'] == 2090],
    x = "jet_lat",
    y = "awb",
    alpha = 0.8,
    color = 'k',
    linestyles = 'dashed',
    ax = axes[0, 0],
    levels = np.arange(0.0, 1.1, 0.2),
    common_norm=False,
)
axes[0, 0].set_ylim(-5, 55)
axes[0, 0].set_xlim(38, 64)

# ----- Plot 2: neg_df, x=GB_index, y=baroclinicity -----
_neg_plot_data = neg_df.groupby(['event', 'phase', 'decade'])[['baroclinicity', 'GB_index']].mean().reset_index()
sns.kdeplot(
    data = _neg_plot_data[_neg_plot_data['decade'] == 1850],
    x = "GB_index",
    y = "baroclinicity",
    alpha = 0.8,
    color = 'k',
    linestyles = 'solid',
    ax = axes[0, 1],
    levels = np.arange(0.0, 1.1, 0.2),
    common_norm=False,
)
sns.kdeplot(
    data = _neg_plot_data[_neg_plot_data['decade'] == 2090],
    x = "GB_index",
    y = "baroclinicity",
    alpha = 0.8,
    color = 'k',
    linestyles = 'dashed',
    ax = axes[0, 1],
    levels = np.arange(0.0, 1.1, 0.2),
    common_norm=False,
)

axes[0, 1].set_ylim(2.5, 5.0)
axes[0, 1].set_xlim(5380, 5700)


# legend for top row: solid=1850, dashed=2090
_kde_legend = [
    Line2D([0], [0], color='k', linestyle='solid', label='1850s'),
    Line2D([0], [0], color='k', linestyle='dashed', label='2090s'),
]
axes[0, 0].legend(handles=_kde_legend, frameon=False, fontsize=9, loc='upper left')
axes[0, 1].legend(handles=_kde_legend, frameon=False, fontsize=9, loc='upper right')

# ----- Plot 3: dec_pos_df, x=jet_lat, y=awb, size=NAO count -----
sns.scatterplot(
    data = dec_pos_df.groupby(['decade', 'phase'])[['jet_lat', 'awb', 'days_pos']].mean().reset_index(),
    x = "jet_lat",
    y = "awb",
    hue = 'decade',
    palette = 'Greys',
    size = "days_pos",
    alpha = 0.8,
    ax = axes[1, 0],
    legend=False,
    sizes = (20, 300),
    edgecolors = 'black',
    linewidths = 0.5,
)

# ----- Plot 4: dec_neg_df, x=GB_index, y=baroclinicity, size=NAO count -----
sns.scatterplot(
    data = dec_neg_df.groupby(['decade', 'phase'])[['baroclinicity', 'GB_index', 'days_neg']].mean().reset_index(),
    x = "GB_index",
    y = "baroclinicity",
    hue = 'decade',
    palette = 'Greys',
    size = "days_neg",
    alpha = 0.8,
    ax = axes[1, 1],
    legend=False,
    sizes = (20, 300),
    edgecolors = 'black',
    linewidths = 0.5,
)


# label 1850 and 2090 points on second row
_pos_dec_mean = dec_pos_df.groupby(['decade', 'phase'])[['jet_lat', 'awb']].mean().reset_index()
for _dec, _label in [(1850, '1850'), (2090, '2090')]:
    _row = _pos_dec_mean[_pos_dec_mean['decade'] == _dec]
    if not _row.empty:
        axes[1, 0].annotate(_label, xy=(_row['jet_lat'].values[0], _row['awb'].values[0]),
                            xytext=(4, 4), textcoords='offset points', fontsize=8)

_neg_dec_mean = dec_neg_df.groupby(['decade', 'phase'])[['GB_index', 'baroclinicity']].mean().reset_index()
for _dec, _label in [(1850, '1850'), (2090, '2090')]:
    _row = _neg_dec_mean[_neg_dec_mean['decade'] == _dec]
    if not _row.empty:
        axes[1, 1].annotate(_label, xy=(_row['GB_index'].values[0], _row['baroclinicity'].values[0]),
                            xytext=(4, 4), textcoords='offset points', fontsize=8)

# remove upper and right spines
for ax in axes.flatten():
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # add a, b, c, d labels to the corners
axes[0, 0].text(-0.08, 1.1, "a", transform=axes[0, 0].transAxes,
                ha="left", va="top", fontsize=12, fontweight="bold")
axes[0, 1].text(-0.08, 1.1, "b", transform=axes[0, 1].transAxes,
                ha="left", va="top", fontsize=12, fontweight="bold")
axes[1, 0].text(-0.08, 1.1, "c", transform=axes[1, 0].transAxes,
                ha="left", va="top", fontsize=12, fontweight="bold")
axes[1, 1].text(-0.08, 1.1, "d", transform=axes[1, 1].transAxes,
                ha="left", va="top", fontsize=12, fontweight="bold")

axes[0, 0].set_xlabel("Jet Latitude (°N)")
axes[0, 0].set_ylabel("AWB probability / $\%$")
axes[0, 1].set_xlabel("GB Index")
axes[0, 1].set_ylabel("Eady growth rate / $day^{-1}$")
axes[1, 0].set_xlabel("Jet Latitude (°N)")
axes[1, 0].set_ylabel("AWB occurrence / day")
axes[1, 1].set_xlabel("GB Index")
axes[1, 1].set_ylabel("Eady growth rate / $day^{-1}$")

plt.tight_layout()
plt.subplots_adjust(bottom=0.22)   # make room for bubble-colorband legend

# ===== Combined bubble-colorband legend =====
# Left panel: colored blocks + bubbles for every decade
# Right panel: reference scale for bubble size (NAO days)

# --- size scaling (match seaborn sizes=(20,300)) ---
_days_pos_dec = NAO_merge.set_index("decade")["days_pos"].reindex(decades_all.astype(int)).values
_days_neg_dec = NAO_merge.set_index("decade")["days_neg"].reindex(decades_all.astype(int)).values
_days_avg = (_days_pos_dec + _days_neg_dec) / 2
_s_vmin, _s_vmax = _days_avg.min(), _days_avg.max()
def _msize(v):
    return 20 + (v - _s_vmin) / (_s_vmax - _s_vmin) * (300 - 20)

# --- colorband axis (color + decade labels only) ---
_grey_colors = sns.color_palette('Greys', n_colors=len(decades_all))

leg_ax = fig.add_axes([0.09, 0.05, 0.7, 0.08])
leg_ax.set_xlim(1843, 2097)
leg_ax.set_ylim(-1.5, 1.2)
leg_ax.axis("off")

# draw colored band (rectangles)
_band_y, _band_h = 0.0, 0.8
for i, dec in enumerate(decades_all):
    leg_ax.add_patch(
        plt.Rectangle((dec - 5, _band_y), 10, _band_h,
                      color=_grey_colors[i], zorder=3, clip_on=False)
    )
# outer border around the entire colorband
leg_ax.add_patch(
    plt.Rectangle((1845, _band_y), 250, _band_h,
                  fill=False, edgecolor='black', linewidth=1., zorder=2, clip_on=False)
)

# decade labels below band (every other decade)
for dec in decades_all[::2]:
    leg_ax.text(dec, _band_y - 0.15, str(int(dec)),
                ha="center", va="top", fontsize=7, rotation=45)

leg_ax.text(0.5, 1.15, "Decade",
            ha="center", va="top", transform=leg_ax.transAxes,
            fontsize=8.5, style="italic")

# --- size reference axis (right) ---
ref_ax = fig.add_axes([0.80, 0.05, 0.16, 0.08])
ref_ax.set_xlim(-0.5, 3.5)
ref_ax.set_ylim(-1.5, 1.2)
ref_ax.axis("off")

_ref_days = [round(_s_vmin), round((_s_vmin + _s_vmax) / 2), round(_s_vmax)]
for j, rd in enumerate(_ref_days):
    ref_ax.scatter(j * 1.1, 0.4, s=_msize(rd), color="grey",
                   edgecolors="white", linewidths=0.4, clip_on=False)
    ref_ax.text(j * 1.1, _band_y - 0.15, str(rd),
                ha="center", va="top", fontsize=7)
ref_ax.text(0.4, 1.15, "NAO extremes/day",
            ha="center", va="top", transform=ref_ax.transAxes,
            fontsize=8.5, style="italic")
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0after_defense/flux_composite_density.pdf")
# %%

# %%
