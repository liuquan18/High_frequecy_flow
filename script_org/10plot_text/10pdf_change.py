#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd
from src.data_helper.read_variable import read_prime, read_prime_decmean
# %%
transient_first = read_prime(1850, var = 'Fdiv_phi_transient', name = 'div', suffix = '_ano', model_dir = 'MPI_GE_CMIP6_allplev', plev = 25000)
# %%
transient_last = read_prime(2090, var = 'Fdiv_phi_transient', name = 'div', suffix = '_ano', model_dir = 'MPI_GE_CMIP6_allplev', plev = 25000)
# %%
steady_first = read_prime(1850, var = 'Fdiv_phi_steady', name = 'div', suffix = '_ano', model_dir = 'MPI_GE_CMIP6_allplev', plev = 25000)
steady_last = read_prime(2090, var = 'Fdiv_phi_steady', name = 'div', suffix = '_ano', model_dir = 'MPI_GE_CMIP6_allplev', plev = 25000)
# %%
def fldmean(ds, lat_slice = (50, 70)):
    ds = ds.sel(lat=slice(*lat_slice))
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"
    ds = ds.weighted(weights).mean(dim=["lon", "lat"])
    return ds
# %%
transient_first = fldmean(transient_first)
transient_last = fldmean(transient_last)
steady_first = fldmean(steady_first)
steady_last = fldmean(steady_last)
# %%
sum_first = transient_first.copy(data = transient_first.values + steady_first.values)
sum_last = transient_last.copy(data = transient_last.values + steady_last.values)
#%%
# read the std change
sum_std = read_prime_decmean(var='Fdiv_phi_transient_Fdiv_phi_steady_sum_std', name='div', plev=25000)
transient_std = read_prime_decmean(var='Fdiv_phi_transient_std', name='div', plev=25000)
steady_std = read_prime_decmean(var='Fdiv_phi_steady_std', name='div', plev=25000)
#%%
# adjust the year of the std change
sum_std['year'] = sum_std['year'] - 9
transient_std['year'] = transient_std['year'] - 9
steady_std['year'] = steady_std['year'] - 9

#%%
# load data
transient_first = transient_first.compute()
transient_last = transient_last.compute()
steady_first = steady_first.compute()
steady_last = steady_last.compute()

transient_std = transient_std.compute()
steady_std = steady_std.compute()
sum_std = sum_std.compute()
# %%
# to dataframe
transient_first_df = transient_first.to_dataframe('div_phi').reset_index()
transient_last_df = transient_last.to_dataframe('div_phi').reset_index()
steady_first_df = steady_first.to_dataframe('div_phi').reset_index()
steady_last_df = steady_last.to_dataframe('div_phi').reset_index()
sum_first_df = sum_first.to_dataframe('div_phi').reset_index()
sum_last_df = sum_last.to_dataframe('div_phi').reset_index()
#%%
sum_std_df = sum_std['std'].to_dataframe('div_phi').reset_index()
transient_std_df = transient_std['std'].to_dataframe('div_phi').reset_index()
steady_std_df = steady_std['std'].to_dataframe('div_phi').reset_index()
#%%
sum_std_df['div_phi'] = np.sqrt(sum_std_df['div_phi'])
transient_std_df['div_phi'] = np.sqrt(transient_std_df['div_phi'])
steady_std_df['div_phi'] = np.sqrt(steady_std_df['div_phi'])
#%%
# save the dataframes
dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0eddy_momentum_pdf/"
transient_first_df.to_csv(dir+'transient_first_df.csv', index=False)
transient_last_df.to_csv(dir+'transient_last_df.csv', index=False)
steady_first_df.to_csv(dir+'steady_first_df.csv', index=False)
steady_last_df.to_csv(dir+'steady_last_df.csv', index=False)
sum_first_df.to_csv(dir+'sum_first_df.csv', index=False)
sum_last_df.to_csv(dir+'sum_last_df.csv', index=False)
transient_std_df.to_csv(dir+'transient_std_df.csv', index=False)
steady_std_df.to_csv(dir+'steady_std_df.csv', index=False)
sum_std_df.to_csv(dir+'sum_std_df.csv', index=False)


# %%
fig, axes = plt.subplots(2, 3, figsize=(15, 10), sharey=False, sharex=False)
# Plot PDF for sum
sns.histplot(sum_first_df['div_phi'], bins=np.arange(-5.0, 5.1, 0.1), ax=axes[0,0], color='black', label='1850', stat='density', kde=False, alpha=0.5)
sns.histplot(sum_last_df['div_phi'], bins=np.arange(-5.0, 5.1, 0.1), ax=axes[0,0], color='red', label='2090', stat='density', kde=False, alpha=0.5)
axes[0,0].set_title('Sum')
axes[0,0].legend()

# Plot PDF for transient
sns.histplot(transient_first_df['div_phi'], bins=np.arange(-5.0, 5.1, 0.1), ax=axes[0,1], color='black', label='1850', stat='density', kde=False, alpha=0.5)
sns.histplot(transient_last_df['div_phi'], bins=np.arange(-5.0, 5.1, 0.1), ax=axes[0,1], color='red', label='2090', stat='density', kde=False, alpha=0.5)
axes[0,1].set_title('Transient')
axes[0,1].legend()

# Plot PDF for steady
sns.histplot(steady_first_df['div_phi'], bins=np.arange(-5.0, 5.1, 0.1), ax=axes[0,2], color='black', label='1850', stat='density', kde=False, alpha=0.5)
sns.histplot(steady_last_df['div_phi'], bins=np.arange(-5.0, 5.1, 0.1), ax=axes[0,2], color='red', label='2090', stat='density', kde=False, alpha=0.5)
axes[0,2].set_title('Steady')
axes[0,2].legend()

for ax in axes[0,:]:
    ax.set_ylim(0, 1.3)



# plot the std as lines
sns.lineplot(data = sum_std_df, x='year', y='div_phi', ax=axes[1,0], label='Sum Std', color='black')
sns.lineplot(data = transient_std_df, x='year', y='div_phi', ax=axes[1,1], label='Transient Std', color='blue')
sns.lineplot(data = steady_std_df, x='year', y='div_phi', ax=axes[1,2], label='Steady Std', color='green')

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eddy_flux_pdf.pdf", dpi=300, bbox_inches='tight')
# %%
