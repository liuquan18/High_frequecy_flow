#%%
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
# %%
first = xr.open_mfdataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0NAO_index_eofs/r*i1p1f1/*1850*.nc",
    combine = 'nested',
    concat_dim = 'ens',
)
# %%
last = xr.open_mfdataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0NAO_index_eofs/r*i1p1f1/*2090*.nc",
    combine = 'nested',
    concat_dim = 'ens',
)
# %%
first_std = first.pseudo_pcs
last_std = last.pseudo_pcs
# %%
fig, ax = plt.subplots(figsize=(10, 6))

first_std.plot.hist(
    bins = np.arange(-4, 4.1, 0.5),
    ax = ax,
    color = 'black',
    label = "1850s",
    alpha = 0.5,
)
last_std.plot.hist(
    bins = np.arange(-4, 4.1, 0.5),
    ax = ax,
    color = 'red',
    label = "2090s",
    alpha = 0.5,
)
# %%
