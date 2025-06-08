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
#%%
# read E_div_x

TEx_pos_first, TEy_pos_first = read_E_div(
    phase="pos",
    decade=1850,
    eddy="transient",
)
TEx_neg_first, TEy_neg_first = read_E_div(
    phase="neg",
    decade=1850,
    eddy="transient",
)
TEx_pos_last, TEy_pos_last = read_E_div(
    phase="pos",
    decade=2090,
    eddy="transient",
)
TEx_neg_last, TEy_neg_last = read_E_div(
    phase="neg",
    decade=2090,
    eddy="transient",
)

# read climatological E_div_x
TEx_clima_first, TEy_clima_first = read_E_div(
    phase="clima",
    decade=1850,
    eddy="transient",
)
TEx_clima_last, TEy_clima_last = read_E_div(
    phase="clima",
    decade=2090,
    eddy="transient",
)

#%%
# read E_div_x for steady eddies
SEx_pos_first, SEy_pos_first = read_E_div(
    phase="pos",
    decade=1850,
    eddy="steady",
)
SEx_neg_first, SEy_neg_first = read_E_div(
    phase="neg",
    decade=1850,
    eddy="steady",
)

SEx_pos_last, SEy_pos_last = read_E_div(
    phase="pos",
    decade=2090,
    eddy="steady",
)
SEx_neg_last, SEy_neg_last = read_E_div(
    phase="neg",
    decade=2090,
    eddy="steady",
)
# read climatological E_div_x for steady
SEx_clima_first, SEy_clima_first = read_E_div(
    phase="clima",
    decade=1850,
    eddy="steady",
)
SEx_clima_last, SEy_clima_last = read_E_div(
    phase="clima",
    decade=2090,
    eddy="steady",
)

#%%
# fldmean over [300, 360, 40, 80]
def to_dataframe(ds, var_name, phase, decade):

    ds = ds.sel(lat=slice(40, 80), lon=slice(300, 360))
    # create weights
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"
    ds = ds.weighted(weights)
    
    ds = ds.mean(dim=["lat", "lon"])

    df = ds.to_dataframe(var_name).reset_index()
    df['phase'] = phase
    df['decade'] = decade
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

#%%
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
#%%
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
#%%
transient_dfs = [
    Tdivphi_dfs,
    Tdiv_p_dfs,
    TEx_dfs,
]
#merge
transient_dfs = [df.reset_index(drop=True) if isinstance(df, pd.DataFrame) else df for df in transient_dfs]
transient_dfs = pd.concat(transient_dfs, axis=1)
# remove duplicated columns
transient_dfs = transient_dfs.loc[:, ~transient_dfs.columns.duplicated()]
transient_dfs = transient_dfs[['plev', 'phase', 'decade', 'M2', 'N', 'P']]




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

#%%
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

#%%
steady_dfs = [
    Sdivphi_dfs,
    Sdiv_p_dfs,
    SEx_dfs,
]

# Merge steady eddy dataframes
steady_dfs = [df.reset_index(drop=True) if isinstance(df, pd.DataFrame) else df for df in steady_dfs]
steady_dfs = pd.concat(steady_dfs, axis=1)
# Remove duplicated columns
steady_dfs = steady_dfs.loc[:, ~steady_dfs.columns.duplicated()]
steady_dfs = steady_dfs[['plev', 'phase', 'decade', 'M2', 'N', 'P']]

#%%
fig, axes = plt.subplots(2, 3, figsize=(12, 10), sharex=True, sharey='row')

plevs = [25000, 85000]
phases = ['clima', 'pos', 'neg']
components = ['P', 'N', 'M2']
colors = ['#F8766D', "#189424", '#4C72B0']  # warm to cool: P, N, M2
hatches = [None, '//']  # 1850: no hatch, 2090: dotted hatch

def get_stacked_data(df, plev, decade):
    df_plot = df[(df['decade'] == decade) & (df['plev'] == plev)].copy()
    df_plot['phase'] = pd.Categorical(df_plot['phase'], categories=phases, ordered=True)
    df_long = df_plot.melt(id_vars=['phase'], value_vars=components, var_name='component', value_name='value')
    df_long['component'] = pd.Categorical(df_long['component'], categories=components, ordered=True)
    df_pivot = df_long.pivot_table(index='phase', columns='component', values='value').loc[phases, components]
    return df_pivot

bar_width = 0.2
gap = 0.08  # gap between 1850 and 2090 bars for each phase
x = np.arange(len(phases))

legend_handles = None
legend_labels = None

for row, plev in enumerate(plevs):
    for col, (df, label) in enumerate(zip([transient_dfs, steady_dfs], ["Transient", "Steady"])):
        ax = axes[row, col]
        for j, decade in enumerate([1850, 2090]):
            # Offset: -bar_width/2-gap/2 for 1850, +bar_width/2+gap/2 for 2090
            offset = (-bar_width/2-gap/2) if j == 0 else (bar_width/2+gap/2)
            df_pivot = get_stacked_data(df, plev, decade)
            bottom_pos = np.zeros(len(phases))
            bottom_neg = np.zeros(len(phases))
            for i, comp in enumerate(components):
                vals = df_pivot[comp].values
                pos_vals = np.where(vals > 0, vals, 0)
                neg_vals = np.where(vals < 0, vals, 0)
                # Plot positive stack
                bars_pos = ax.bar(x + offset, pos_vals, bar_width, bottom=bottom_pos, color=colors[i],
                                  label=f"{comp} {decade}" if (row == 0 and j == 0) else None,
                                  hatch=hatches[j], edgecolor='k')
                bottom_pos += pos_vals
                # Plot negative stack
                bars_neg = ax.bar(x + offset, neg_vals, bar_width, bottom=bottom_neg, color=colors[i],
                                  hatch=hatches[j], edgecolor='k')
                bottom_neg += neg_vals
        ax.set_title(f"{label}, plev={plev}")
        if row == 1:
            ax.set_xlabel("Phase")
        if col == 0:
            ax.set_ylabel("div")
        ax.set_xticks(x)
        ax.set_xticklabels(phases)
        if row == 0 and col == 0:
            handles, labels_ = ax.get_legend_handles_labels()
            # Rename component labels
            label_map = {
                "P": r"$\frac{\partial}{\partial z} \left( f_0 \frac{\overline{v'\theta_e'}}{\overline{\theta}_p} \right)$",
                "N": r"$-\frac{\partial}{\partial y} (\overline{u'v'})$",
                "M2": r"$\frac{\partial}{\partial x} (\overline{v'^2 - u'^2})$"
            }
            labels_ = [label_map.get(l.split()[0], l) for l in labels_]
            # Add a legend entry for hatches
            handles += [Patch(facecolor='white', edgecolor='k', hatch=hatches[0], label='1850'),
                        Patch(facecolor='white', edgecolor='k', hatch=hatches[1], label='2090')]
            labels_ += ['1850', '2090']
            legend_handles = handles
            legend_labels = labels_

    # add a thrid column for sum of transient and steady

    ax_sum = axes[row, 2]
    for j, decade in enumerate([1850, 2090]):
        # Offset: -bar_width/2-gap/2 for 1850, +bar_width/2+gap/2 for 2090
        offset = (-bar_width/2-gap/2) if j == 0 else (bar_width/2+gap/2)
        # Sum the two dataframes
        df_sum = transient_dfs.copy()
        df_sum = df_sum.copy()
        df_sum[['P', 'N', 'M2']] = df_sum[['P', 'N', 'M2']].values + steady_dfs[['P', 'N', 'M2']].values
        df_pivot = get_stacked_data(df_sum, plev, decade)
        bottom_pos = np.zeros(len(phases))
        bottom_neg = np.zeros(len(phases))
        for i, comp in enumerate(components):
            vals = df_pivot[comp].values
            pos_vals = np.where(vals > 0, vals, 0)
            neg_vals = np.where(vals < 0, vals, 0)
            bars_pos = ax_sum.bar(x + offset, pos_vals, bar_width, bottom=bottom_pos, color=colors[i],
                                  label=f"{comp} {decade}" if (row == 1 and j == 0) else None,
                                  hatch=hatches[j], edgecolor='k')
            bottom_pos += pos_vals
            bars_neg = ax_sum.bar(x + offset, neg_vals, bar_width, bottom=bottom_neg, color=colors[i],
                                  hatch=hatches[j], edgecolor='k')
            bottom_neg += neg_vals
# add hline at y=0 for all axes
for ax in axes.flat:
    ax.axhline(0, color='k', linewidth=0.5, linestyle='--')

# romove spinelines of top and right axes
for ax in axes.flat:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Move the legend to axes[1,0] lower left
if legend_handles is not None and legend_labels is not None:
    axes[1, 0].legend(legend_handles, legend_labels, title="Component / Decade", loc="lower left")

plt.tight_layout()

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/vq_component_bar_withheat.pdf",
            bbox_inches='tight', dpi=300)


# %%
fig, axes = plt.subplots(2, 3, figsize=(12, 10), sharex=True, sharey='row')

plevs = [25000, 85000]
phases = ['clima', 'pos', 'neg']
components_all = ['P', 'N', 'M2']
colors_all = ['#F8766D', "#189424", '#4C72B0']  # warm to cool: P, N, M2
hatches = [None, '//']  # 1850: no hatch, 2090: dotted hatch

def get_stacked_data(df, plev, decade, components):
    df_plot = df[(df['decade'] == decade) & (df['plev'] == plev)].copy()
    df_plot['phase'] = pd.Categorical(df_plot['phase'], categories=phases, ordered=True)
    df_long = df_plot.melt(id_vars=['phase'], value_vars=components, var_name='component', value_name='value')
    df_long['component'] = pd.Categorical(df_long['component'], categories=components, ordered=True)
    df_pivot = df_long.pivot_table(index='phase', columns='component', values='value').loc[phases, components]
    return df_pivot

bar_width = 0.2
gap = 0.08  # gap between 1850 and 2090 bars for each phase
x = np.arange(len(phases))

legend_handles = None
legend_labels = None

for row, plev in enumerate(plevs):
    # For plev=25000, only show N and M2; for 85000, show all
    if plev == 25000:
        components = ['N', 'M2']
        colors = [colors_all[1], colors_all[2]]
    else:
        components = components_all
        colors = colors_all
    # --- First two columns: transient and steady ---
    for col, (df, label) in enumerate(zip([transient_dfs, steady_dfs], ["Transient", "Steady"])):
        ax = axes[row, col]
        for j, decade in enumerate([1850, 2090]):
            offset = (-bar_width/2-gap/2) if j == 0 else (bar_width/2+gap/2)
            df_pivot = get_stacked_data(df, plev, decade, components)
            bottom_pos = np.zeros(len(phases))
            bottom_neg = np.zeros(len(phases))
            for i, comp in enumerate(components):
                vals = df_pivot[comp].values
                pos_vals = np.where(vals > 0, vals, 0)
                neg_vals = np.where(vals < 0, vals, 0)
                # Plot positive stack
                bars_pos = ax.bar(x + offset, pos_vals, bar_width, bottom=bottom_pos, color=colors[i],
                                  label=f"{comp} {decade}" if (row == 1 and j == 0) else None,
                                  hatch=hatches[j], edgecolor='k')
                bottom_pos += pos_vals
                # Plot negative stack
                bars_neg = ax.bar(x + offset, neg_vals, bar_width, bottom=bottom_neg, color=colors[i],
                                  hatch=hatches[j], edgecolor='k')
                bottom_neg += neg_vals
        ax.set_title(f"{label}, plev={plev}")
        if row == 1:
            ax.set_xlabel("Phase")
        if col == 0:
            ax.set_ylabel("div")
        ax.set_xticks(x)
        ax.set_xticklabels(phases)
        # Only collect legend from the second row (row==1) and first column (col==0)
        if row == 1 and col == 0:
            handles, labels_ = ax.get_legend_handles_labels()
            # Rename component labels
            label_map = {
                "P": r"$\frac{\partial}{\partial z} \left( f_0 \frac{\overline{v'\theta_e'}}{\overline{\theta}_p} \right)$",
                "N": r"$-\frac{\partial}{\partial y} (\overline{u'v'})$",
                "M2": r"$\frac{\partial}{\partial x} (\overline{v'^2 - u'^2})$"
            }
            labels_ = [label_map.get(l.split()[0], l) for l in labels_]
            # Add a legend entry for hatches
            handles += [Patch(facecolor='white', edgecolor='k', hatch=hatches[0], label='1850'),
                        Patch(facecolor='white', edgecolor='k', hatch=hatches[1], label='2090')]
            labels_ += ['1850', '2090']
            legend_handles = handles
            legend_labels = labels_

    # --- Third column: sum of transient and steady ---
    ax_sum = axes[row, 2]
    for j, decade in enumerate([1850, 2090]):
        offset = (-bar_width/2-gap/2) if j == 0 else (bar_width/2+gap/2)
        # Sum the two dataframes
        df_sum = transient_dfs.copy()
        df_sum = df_sum.copy()
        df_sum[['P', 'N', 'M2']] = df_sum[['P', 'N', 'M2']].values + steady_dfs[['P', 'N', 'M2']].values
        df_pivot = get_stacked_data(df_sum, plev, decade, components)
        bottom_pos = np.zeros(len(phases))
        bottom_neg = np.zeros(len(phases))
        for i, comp in enumerate(components):
            vals = df_pivot[comp].values
            pos_vals = np.where(vals > 0, vals, 0)
            neg_vals = np.where(vals < 0, vals, 0)
            bars_pos = ax_sum.bar(x + offset, pos_vals, bar_width, bottom=bottom_pos, color=colors[i],
                                 label=f"{comp} {decade}" if (row == 1 and j == 0) else None,
                                 hatch=hatches[j], edgecolor='k')
            bottom_pos += pos_vals
            bars_neg = ax_sum.bar(x + offset, neg_vals, bar_width, bottom=bottom_neg, color=colors[i],
                                 hatch=hatches[j], edgecolor='k')
            bottom_neg += neg_vals
    ax_sum.set_title(f"Sum, plev={plev}")
    if row == 1:
        ax_sum.set_xlabel("Phase")
    ax_sum.set_xticks(x)
    ax_sum.set_xticklabels(phases)
    # Only set y-label for first column
    if row == 0:
        ax_sum.set_ylabel("")
    # Remove y-tick labels for sum column to indicate different scale
    # Optionally, you can set a different y-limits for the sum column
    # ax_sum.set_ylim(custom_min, custom_max)  # Set as needed

# add hline at y=0 for all axes
for ax in axes.flat:
    ax.axhline(0, color='k', linewidth=0.5, linestyle='--')

# remove spines of top and right axes
for ax in axes.flat:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Move the legend to axes[1,0] lower left
if legend_handles is not None and legend_labels is not None:
    axes[1, 0].legend(legend_handles, legend_labels, title="Component / Decade", loc="lower left")

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/vq_component_bar.pdf",
            bbox_inches='tight', dpi=300)

# %%
