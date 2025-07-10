#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd
from src.data_helper.read_variable import read_prime, read_prime_decmean
import glob
import logging
# Set logging level
logging.basicConfig(level=logging.INFO)
# %%
transient_first = read_prime(1850, var = 'Fdiv_phi_transient_index', name = 'phi_index', suffix = '', model_dir = 'MPI_GE_CMIP6_allplev', plev = None)
transient_last = read_prime(2090, var = 'Fdiv_phi_transient_index', name = 'phi_index', suffix = '', model_dir = 'MPI_GE_CMIP6_allplev', plev = None)
# %%
steady_first = read_prime(1850, var = 'Fdiv_phi_steady_index', name = 'phi_index', suffix = '', model_dir = 'MPI_GE_CMIP6_allplev', plev = None)
steady_last = read_prime(2090, var = 'Fdiv_phi_steady_index', name = 'phi_index', suffix = '', model_dir = 'MPI_GE_CMIP6_allplev', plev = None)
# %%
# to dataframe
transient_first_df = transient_first.to_dataframe('phi_index').reset_index()
transient_last_df = transient_last.to_dataframe('phi_index').reset_index()
steady_first_df = steady_first.to_dataframe('phi_index').reset_index()
steady_last_df = steady_last.to_dataframe('phi_index').reset_index()

#%%
std_transient = []
std_steady = []
covariances = []

for decade in range(1850, 2091, 10):
    logging.info(f"Processing decade: {decade}")
    transient = read_prime(decade, var = 'Fdiv_phi_transient_index', name = 'phi_index', suffix = '', model_dir = 'MPI_GE_CMIP6_allplev', plev = None)

    steady = read_prime(decade, var = 'Fdiv_phi_steady_index', name = 'phi_index', suffix = '', model_dir = 'MPI_GE_CMIP6_allplev', plev = None)
    steady['time'] = transient['time']  # align time coordinates

    transient_std = transient.std().compute()
    transient_std['decade'] = decade
    std_transient.append(transient_std)


    steady_std = steady.std().compute()
    steady_std['decade'] = decade
    std_steady.append(steady_std)

    transient_flat = transient.stack(com = ('time', 'ens'))
    steady_flat = steady.stack(com = ('time', 'ens'))
    covariance = xr.cov(transient_flat, steady_flat, dim='com').compute()
    covariances.append(covariance)


std_transient = xr.concat(std_transient, dim='decade')
std_steady = xr.concat(std_steady, dim='decade')
covariances = xr.concat(covariances, dim='decade')


# %%
fig, axes = plt.subplots(2, 3, figsize=(15, 10), sharey=False, sharex=False)

# Plot PDF for transient
sns.histplot(transient_first_df['phi_index'], bins = np.arange(-6000, 6000, 200), ax=axes[0,1], color='black', label='1850', stat='density', kde=False, alpha=0.5)
sns.histplot(transient_last_df['phi_index'],  bins = np.arange(-6000, 6000, 200),ax=axes[0,1], color='red', label='2090', stat='density', kde=False, alpha=0.5)
axes[0,1].set_title('Transient')
axes[0,1].legend()

# Plot PDF for steady
sns.histplot(steady_first_df['phi_index'], bins = np.arange(-6000, 6000, 200), ax=axes[0,2], color='black', label='1850', stat='density', kde=False, alpha=0.5)
sns.histplot(steady_last_df['phi_index'], bins = np.arange(-6000, 6000, 200), ax=axes[0,2], color='red', label='2090', stat='density', kde=False, alpha=0.5)
axes[0,2].set_title('Steady')
axes[0,2].legend()


# Plot standard deviation for transient
axes[1,1].plot(std_transient['decade'], std_transient, marker='o', color='black')
axes[1,1].set_title('Transient Standard Deviation')
axes[1,1].set_xlabel('Decade')
axes[1,1].set_ylabel('Standard Deviation')

# Plot standard deviation for steady
axes[1,2].plot(std_steady['decade'], std_steady, marker='o', color='black')
axes[1,2].set_title('Steady Standard Deviation')
axes[1,2].set_xlabel('Decade')
axes[1,2].set_ylabel('Standard Deviation')

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/eddy_momentum_index_pdf.pdf", bbox_inches='tight', dpi=300)


# %%
