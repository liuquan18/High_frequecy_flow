#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import glob

# %%
def read_momean(var, decade, suffix = '_mon'):
    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/{var}_daily_ano_monmean{suffix}/"

    files = glob.glob(base_dir + f"r*i1p1f1/*{decade}*.nc")

    data = xr.open_mfdataset(files, combine='nested', concat_dim='ens')

    return data.squeeze().load()

#%%
# SMILEs
def read_eof_decade(model, fixed_pattern="decade_mpi"):
    """read eofs that is decomposed by decade"""
    odir = f"/work/mh0033/m300883/Tel_MMLE/data/{model}/EOF_result/"
    filename = f"plev_50000_{fixed_pattern}_first_JJA_eof_result.nc"
    ds = xr.open_dataset(odir + filename)
    ds = ds.sel(mode="NAO")
    return ds


def split_first_last(eof_result):
    times = eof_result.time
    years = np.unique(times.dt.year)
    first_years = years[:10]
    last_years = years[-10:]

    eof_first = eof_result.isel(decade=0).sel(
        time=eof_result["time.year"].isin(first_years)
    )
    eof_last = eof_result.isel(decade=-1).sel(
        time=eof_result["time.year"].isin(last_years)
    )
    return eof_first, eof_last


# %%
upvp_first = read_momean("Fdiv_phi_transient", "1850", '_mon')
upvp_last = read_momean("Fdiv_phi_transient", "2090", '_mon')
# %%
vsts_first = read_momean("steady_eddy_heat_d2y2", "1850")
vsts_last = read_momean("steady_eddy_heat_d2y2", "2090")
# %%
eofs = read_eof_decade("MPI_GE_CMIP6")
eof_first, eof_last = split_first_last(eofs)
# %%
upvp_first = upvp_first['div']
upvp_last = upvp_last['div']
#%%
# standardize
std = upvp_first.std(dim=('time', 'ens'))
upvp_first = upvp_first / std
upvp_last = upvp_last / std
# %%
vsts_first = vsts_first['eddy_heat_d2y2']
vsts_last = vsts_last['eddy_heat_d2y2']
#%%
# standardize
std = vsts_first.std(dim=('time', 'ens'))
vsts_first = vsts_first / std
vsts_last = vsts_last / std
# %%
eof_first = eof_first['pc']
eof_last = eof_last['pc']
# %%
fig, axes = plt.subplots(1, 3, figsize=(10, 5), sharex=True, sharey=True,)

# NAO index distribution
eof_first.plot.hist(
    ax=axes[0],
    bins=np.arange(-4, 4.1, 0.5),
    color='k',
    alpha=0.5,
    label='1850s',
    density=True  # Normalize the histogram
)
eof_last.plot.hist(
    ax=axes[0],
    bins=np.arange(-4, 4.1, 0.5),
    color='r',
    alpha=1.0,
    label='2090s',
    histtype='step',
    linewidth=2,
    density=True  # Normalize the histogram
)

# Momentum flux convergence distribution
upvp_first.plot.hist(
    ax=axes[1],
    bins=np.arange(-4, 4.1, 0.5),
    color='k',
    alpha=0.5,
    label='1850s',
    density=True  # Normalize the histogram
)
upvp_last.plot.hist(
    ax=axes[1],
    bins=np.arange(-4, 4.1, 0.5),
    color='r',
    alpha=1.0,
    label='2090s',
    histtype='step',
    linewidth=2,
    density=True  # Normalize the histogram
)

# Steady eddy heat flux distribution
vsts_first.plot.hist(
    ax=axes[2],
    bins=np.arange(-4, 4.1, 0.5),
    color='k',
    alpha=0.5,
    label='1850s',
    density=True  # Normalize the histogram
)
vsts_last.plot.hist(
    ax=axes[2],
    bins=np.arange(-4, 4.1, 0.5),
    color='r',
    alpha=1.0,
    label='2090s',
    histtype='step',
    linewidth=2,
    density=True  # Normalize the histogram
)

for i, ax in enumerate(axes):
    # vline at x = 1.5, and x = -1.5
    ax.axvline(1.5, color='k', linestyle='dotted', linewidth=1)
    ax.axvline(-1.5, color='k', linestyle='dotted', linewidth=1)
    ax.set_xlabel('Standardized Value')

    ax.set_title("")

    # a, b, c labels
    ax.text(0.05, 0.95, chr(97 + i), fontsize=14, fontweight='bold',
            transform=ax.transAxes, va='top', ha='left')
    
    # remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

axes[0].set_ylabel('Density')
axes[0].legend()

axes[0].set_xlabel('std NAO Index')
axes[1].set_xlabel('std momentum forcing')
axes[2].set_xlabel('std thermal forcing')

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0main_text/NAO_momentum_thermal_distribution.png", dpi=300)
# %%
