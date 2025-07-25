#%%
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
# %%
first = xr.open_mfdataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NAO_pc_1850_trop_nonstd/*nc",
    combine = 'nested',
    concat_dim = 'ens',
)
# %%
last = xr.open_mfdataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NAO_pc_2090_trop_nonstd/*nc",
    combine = 'nested',
    concat_dim = 'ens',
)
# %%
first = first.pc.sel(plev = 50000)
last = last.pc.sel(plev = 50000)
# %%

# %%
first_std = xr.open_mfdataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NAO_pc_1850_trop_std/*nc",
    combine = 'nested',
    concat_dim = 'ens',
)
last_std = xr.open_mfdataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NAO_pc_2090_trop_std/*nc",
    combine = 'nested',
    concat_dim = 'ens',
)
# %%
first_std = first_std.pc.sel(plev = 50000)
last_std = last_std.pc.sel(plev = 50000)
# %%
fig, ax = plt.subplots(1, 2, figsize=(10, 6))

first.plot.hist(
    bins = np.arange(-60000, 60001, 10000),
    ax = ax[0],
    color = 'black',
    label = "1850s",
    alpha = 0.5,
)
last.plot.hist(
    bins = np.arange(-60000, 60001, 10000),
    ax = ax[0],
    color = 'red',
    label = "2090s",
    alpha = 0.5,
)


first_std.plot.hist(
    bins = np.arange(-4, 4.1, 0.5),
    ax = ax[1],
    color = 'black',
    label = "1850s",
    alpha = 0.5,
)
last_std.plot.hist(
    bins = np.arange(-4, 4.1, 0.5),
    ax = ax[1],
    color = 'red',
    label = "2090s",
    alpha = 0.5,
)
# %%
