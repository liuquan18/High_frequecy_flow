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

importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var

from src.data_helper.read_variable import read_climatology
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
Tdivphi_clima_first = read_climatology("Fdiv_phi_transient", decade=1850, name = 'div')
# %%
Tdivphi_clima_last = read_climatology("Fdiv_phi_transient", decade=2090, name = 'div')
#%%
Tdivp_clima_first = read_climatology("Fdiv_p_transient", decade=1850, name = 'div2')
# %%
Tdivp_clima_last = read_climatology("Fdiv_p_transient", decade=2090, name = 'div2')
# %%
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
# read climatology for steady EP flux
Sdivphi_clima_first = read_climatology("Fdiv_phi_steady", decade=1850, name = 'div')
Sdivphi_clima_last = read_climatology("Fdiv_phi_steady", decade=2090, name = 'div')
# %%
Sdivp_clima_first = read_climatology("Fdiv_p_steady", decade=1850, name = 'div2')
Sdivp_clima_last = read_climatology("Fdiv_p_steady", decade=2090, name = 'div2')
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
# %%
def ano_df(ds, ds_clima, name = 'div', plev = None, lat_slice = slice(40, 70)):
    """
    Calculate the anomaly of a dataset with respect to a climatology.
    """
    # average over time
    ds = ds.sel(time = slice(-10, 5)).mean(dim=('time','lon'))
    ds_clima = ds_clima.mean(dim=('lon'))
    anomaly = ds - ds_clima

    if plev is not None:
        anomaly = anomaly.sel(plev=plev)

    anomaly.load()

    # select latitude slice if specified
    if lat_slice is not None:
            # create weights
        weights = np.cos(np.deg2rad(anomaly.lat))
        weights.name = "weights"
        anomaly = anomaly.weighted(weights)
        anomaly = anomaly.sel(lat=lat_slice).mean(dim='lat')
    df = anomaly.to_dataframe(name).reset_index()

    return df

# %%
Tdiv_phi_pos_first_anomaly = ano_df(Tdivphi_pos_first, Tdivphi_clima_first, 'div_phi', plev = 25000)
Tdiv_phi_neg_first_anomaly = ano_df(Tdivphi_neg_first, Tdivphi_clima_first, 'div_phi', plev = 25000)
Tdiv_phi_pos_last_anomaly = ano_df(Tdivphi_pos_last, Tdivphi_clima_last, 'div_phi', plev = 25000)
Tdiv_phi_neg_last_anomaly = ano_df(Tdivphi_neg_last, Tdivphi_clima_last, 'div_phi', plev = 25000)

# %%
Tdiv_p_pos_first_anomaly = ano_df(Tdiv_p_pos_first, Tdivp_clima_first, 'div_p', plev = 70000)
Tdiv_p_neg_first_anomaly = ano_df(Tdiv_p_neg_first, Tdivp_clima_first, 'div_p', plev = 70000)
Tdiv_p_pos_last_anomaly = ano_df(Tdiv_p_pos_last, Tdivp_clima_last, 'div_p', plev = 70000)
Tdiv_p_neg_last_anomaly = ano_df(Tdiv_p_neg_last, Tdivp_clima_last, 'div_p', plev = 70000)
# %%
Sdiv_phi_pos_first_anomaly = ano_df(Sdivphi_pos_first, Sdivphi_clima_first, 'div_phi', plev = 25000)
Sdiv_phi_neg_first_anomaly = ano_df(Sdivphi_neg_first, Sdivphi_clima_first, 'div_phi', plev = 25000)
Sdiv_phi_pos_last_anomaly = ano_df(Sdivphi_pos_last, Sdivphi_clima_last, 'div_phi', plev = 25000)
Sdiv_phi_neg_last_anomaly = ano_df(Sdivphi_neg_last, Sdivphi_clima_last, 'div_phi', plev = 25000)
# %%
Sdiv_p_pos_first_anomaly = ano_df(Sdiv_p_pos_first, Sdivp_clima_first, 'div_p', plev = 70000)
Sdiv_p_neg_first_anomaly = ano_df(Sdiv_p_neg_first, Sdivp_clima_first, 'div_p', plev = 70000)
Sdiv_p_pos_last_anomaly = ano_df(Sdiv_p_pos_last, Sdivp_clima_last, 'div_p', plev = 70000)
Sdiv_p_neg_last_anomaly = ano_df(Sdiv_p_neg_last, Sdivp_clima_last, 'div_p', plev = 70000)


#%%
# sum of transient and steady anomalies
div_phi_pos_first_anomaly = Tdiv_phi_pos_first_anomaly.copy()
div_phi_pos_first_anomaly['div_phi'] += Sdiv_phi_pos_first_anomaly['div_phi']
div_phi_neg_first_anomaly = Tdiv_phi_neg_first_anomaly.copy()
div_phi_neg_first_anomaly['div_phi'] += Sdiv_phi_neg_first_anomaly['div_phi']
div_phi_pos_last_anomaly = Tdiv_phi_pos_last_anomaly.copy()
div_phi_pos_last_anomaly['div_phi'] += Sdiv_phi_pos_last_anomaly['div_phi']
div_phi_neg_last_anomaly = Tdiv_phi_neg_last_anomaly.copy()
div_phi_neg_last_anomaly['div_phi'] += Sdiv_phi_neg_last_anomaly['div_phi']



# %%
# transient
# sum (transient + steady)
fig, axes = plt.subplots(
    3, 2, figsize=(10, 10), sharex=True, sharey=True,
)

# Top row: sum of transient and steady anomalies
sns.histplot(
    data=div_phi_pos_first_anomaly,
    x="div_phi",
    ax=axes[0, 0],
    bins=np.arange(-2, 2.1, 0.1),
    color='C1',
    label='pos NAO'
)
sns.histplot(
    data=div_phi_neg_first_anomaly,
    x="div_phi",
    ax=axes[0, 0],
    bins=np.arange(-2, 2.1, 0.1),
    color='C0',
    label='neg NAO'
)
sns.histplot(
    data=div_phi_pos_last_anomaly,
    x="div_phi",
    ax=axes[0, 1],
    bins=np.arange(-2, 2.1, 0.1),
    color='C1',
    label='pos'
)
sns.histplot(
    data=div_phi_neg_last_anomaly,
    x="div_phi",
    ax=axes[0, 1],
    bins=np.arange(-2, 2.1, 0.1),
    color='C0',
    label='neg'
)

# transient (middle row, swapped)
sns.histplot(
    data=Tdiv_phi_pos_first_anomaly,
    x="div_phi",
    ax=axes[1, 0],
    bins=np.arange(-2, 2.1, 0.1),
    color='C1'
)
sns.histplot(
    data=Tdiv_phi_neg_first_anomaly,
    x="div_phi",
    ax=axes[1, 0],
    bins=np.arange(-2, 2.1, 0.1),
    color='C0'
)
sns.histplot(
    data=Tdiv_phi_pos_last_anomaly,
    x="div_phi",
    ax=axes[1, 1],
    bins=np.arange(-2, 2.1, 0.1),
    color='C1'
)
sns.histplot(
    data=Tdiv_phi_neg_last_anomaly,
    x="div_phi",
    ax=axes[1, 1],
    bins=np.arange(-2, 2.1, 0.1),
    color='C0'
)

# steady (bottom row, swapped)
sns.histplot(
    data=Sdiv_phi_pos_first_anomaly,
    x="div_phi",
    ax=axes[2, 0],
    bins=np.arange(-2, 2.1, 0.1),
    color='C1'
)
sns.histplot(
    data=Sdiv_phi_neg_first_anomaly,
    x="div_phi",
    ax=axes[2, 0],
    bins=np.arange(-2, 2.1, 0.1),
    color='C0'
)
sns.histplot(
    data=Sdiv_phi_pos_last_anomaly,
    x="div_phi",
    ax=axes[2, 1],
    bins=np.arange(-2, 2.1, 0.1),
    color='C1'
)
sns.histplot(
    data=Sdiv_phi_neg_last_anomaly,
    x="div_phi",
    ax=axes[2, 1],
    bins=np.arange(-2, 2.1, 0.1),
    color='C0'
)

# plot the vline at mean
axes[0, 0].axvline(div_phi_pos_first_anomaly['div_phi'].mean(), color='C1', linestyle='--', linewidth=2)
axes[0, 0].axvline(div_phi_neg_first_anomaly['div_phi'].mean(), color='C0', linestyle='--', linewidth=2)
axes[0, 1].axvline(div_phi_pos_last_anomaly['div_phi'].mean(), color='C1', linestyle='--', linewidth=2)
axes[0, 1].axvline(div_phi_neg_last_anomaly['div_phi'].mean(), color='C0', linestyle='--', linewidth=2)

axes[1, 0].axvline(Tdiv_phi_pos_first_anomaly['div_phi'].mean(), color='C1', linestyle='--', linewidth=2)
axes[1, 0].axvline(Tdiv_phi_neg_first_anomaly['div_phi'].mean(), color='C0', linestyle='--', linewidth=2)
axes[1, 1].axvline(Tdiv_phi_pos_last_anomaly['div_phi'].mean(), color='C1', linestyle='--', linewidth=2)
axes[1, 1].axvline(Tdiv_phi_neg_last_anomaly['div_phi'].mean(), color='C0', linestyle='--', linewidth=2)

axes[2, 0].axvline(Sdiv_phi_pos_first_anomaly['div_phi'].mean(), color='C1', linestyle='--', linewidth=2)
axes[2, 0].axvline(Sdiv_phi_neg_first_anomaly['div_phi'].mean(), color='C0', linestyle='--', linewidth=2)
axes[2, 1].axvline(Sdiv_phi_pos_last_anomaly['div_phi'].mean(), color='C1', linestyle='--', linewidth=2)
axes[2, 1].axvline(Sdiv_phi_neg_last_anomaly['div_phi'].mean(), color='C0', linestyle='--', linewidth=2)




# Optionally, add titles or labels for clarity
axes[0, 0].set_title('Sum: First Decade')
axes[0, 1].set_title('Sum: Last Decade')
axes[1, 0].set_title('Transient: First Decade')
axes[1, 1].set_title('Transient: Last Decade')
axes[2, 0].set_title('Steady: First Decade')
axes[2, 1].set_title('Steady: Last Decade')

axes[0, 0].legend()

plt.tight_layout()

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eddy_momentum_div_pdf.pdf",
            bbox_inches='tight', dpi=300)

# %%
# Plot PDF for div_p (sum, transient, steady)
fig, axes = plt.subplots(
    3, 2, figsize=(10, 10), sharex=True, sharey=True,
)

# Top row: sum of transient and steady anomalies
sns.histplot(
    data=Tdiv_p_pos_first_anomaly.assign(div_p=Tdiv_p_pos_first_anomaly['div_p'] + Sdiv_p_pos_first_anomaly['div_p']),
    x="div_p",
    ax=axes[0, 0],
    bins=np.arange(-8, 8.1, 1),
    color='C1',
    label='pos NAO'
)
sns.histplot(
    data=Tdiv_p_neg_first_anomaly.assign(div_p=Tdiv_p_neg_first_anomaly['div_p'] + Sdiv_p_neg_first_anomaly['div_p']),
    x="div_p",
    ax=axes[0, 0],
    bins=np.arange(-8, 8.1, 1),
    color='C0',
    label='neg NAO'
)
sns.histplot(
    data=Tdiv_p_pos_last_anomaly.assign(div_p=Tdiv_p_pos_last_anomaly['div_p'] + Sdiv_p_pos_last_anomaly['div_p']),
    x="div_p",
    ax=axes[0, 1],
    bins=np.arange(-8, 8.1, 1),
    color='C1',
    label='pos'
)
sns.histplot(
    data=Tdiv_p_neg_last_anomaly.assign(div_p=Tdiv_p_neg_last_anomaly['div_p'] + Sdiv_p_neg_last_anomaly['div_p']),
    x="div_p",
    ax=axes[0, 1],
    bins=np.arange(-8, 8.1, 1),
    color='C0',
    label='neg'
)

# Middle row: transient only
sns.histplot(
    data=Tdiv_p_pos_first_anomaly,
    x="div_p",
    ax=axes[1, 0],
    bins=np.arange(-8, 8.1, 1),
    color='C1'
)
sns.histplot(
    data=Tdiv_p_neg_first_anomaly,
    x="div_p",
    ax=axes[1, 0],
    bins=np.arange(-8, 8.1, 1),
    color='C0'
)
sns.histplot(
    data=Tdiv_p_pos_last_anomaly,
    x="div_p",
    ax=axes[1, 1],
    bins=np.arange(-8, 8.1, 1),
    color='C1'
)
sns.histplot(
    data=Tdiv_p_neg_last_anomaly,
    x="div_p",
    ax=axes[1, 1],
    bins=np.arange(-8, 8.1, 1),
    color='C0'
)

# Bottom row: steady only
sns.histplot(
    data=Sdiv_p_pos_first_anomaly,
    x="div_p",
    ax=axes[2, 0],
    bins=np.arange(-8, 8.1, 1),
    color='C1'
)
sns.histplot(
    data=Sdiv_p_neg_first_anomaly,
    x="div_p",
    ax=axes[2, 0],
    bins=np.arange(-8, 8.1, 1),
    color='C0'
)
sns.histplot(
    data=Sdiv_p_pos_last_anomaly,
    x="div_p",
    ax=axes[2, 1],
    bins=np.arange(-8, 8.1, 1),
    color='C1'
)
sns.histplot(
    data=Sdiv_p_neg_last_anomaly,
    x="div_p",
    ax=axes[2, 1],
    bins=np.arange(-8, 8.1, 1),
    color='C0'
)


# plot the vline at mean
axes[0, 0].axvline((Tdiv_p_pos_first_anomaly['div_p'] + Sdiv_p_pos_first_anomaly['div_p']).mean(), color='C1', linestyle='--', linewidth=2)
axes[0, 0].axvline((Tdiv_p_neg_first_anomaly['div_p'] + Sdiv_p_neg_first_anomaly['div_p']).mean(), color='C0', linestyle='--', linewidth=2)
axes[0, 1].axvline((Tdiv_p_pos_last_anomaly['div_p'] + Sdiv_p_pos_last_anomaly['div_p']).mean(), color='C1', linestyle='--', linewidth=2)
axes[0, 1].axvline((Tdiv_p_neg_last_anomaly['div_p'] + Sdiv_p_neg_last_anomaly['div_p']).mean(), color='C0', linestyle='--', linewidth=2)

axes[1, 0].axvline(Tdiv_p_pos_first_anomaly['div_p'].mean(), color='C1', linestyle='--', linewidth=2)
axes[1, 0].axvline(Tdiv_p_neg_first_anomaly['div_p'].mean(), color='C0', linestyle='--', linewidth=2)
axes[1, 1].axvline(Tdiv_p_pos_last_anomaly['div_p'].mean(), color='C1', linestyle='--', linewidth=2)
axes[1, 1].axvline(Tdiv_p_neg_last_anomaly['div_p'].mean(), color='C0', linestyle='--', linewidth=2)

axes[2, 0].axvline(Sdiv_p_pos_first_anomaly['div_p'].mean(), color='C1', linestyle='--', linewidth=2)
axes[2, 0].axvline(Sdiv_p_neg_first_anomaly['div_p'].mean(), color='C0', linestyle='--', linewidth=2)
axes[2, 1].axvline(Sdiv_p_pos_last_anomaly['div_p'].mean(), color='C1', linestyle='--', linewidth=2)
axes[2, 1].axvline(Sdiv_p_neg_last_anomaly['div_p'].mean(), color='C0', linestyle='--', linewidth=2)

axes[0, 0].set_title('Sum: First Decade')
axes[0, 1].set_title('Sum: Last Decade')
axes[1, 0].set_title('Transient: First Decade')
axes[1, 1].set_title('Transient: Last Decade')
axes[2, 0].set_title('Steady: First Decade')
axes[2, 1].set_title('Steady: Last Decade')

axes[0, 0].legend()

plt.tight_layout()
# %%
