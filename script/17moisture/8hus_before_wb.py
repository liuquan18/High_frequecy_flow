# %%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns

# %%
# wave breaking
awb = pd.read_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wave_breaking_stat/awb_th3_NAO_overlap70.csv', index_col=0)
cwb = pd.read_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wave_breaking_stat/cwb_th3_NAO_overlap70.csv', index_col=0)
# %%
awb_first = awb[awb['dec'] == 1850]
awb_last = awb[awb['dec'] == 2090]
# %%
cwb_first = cwb[cwb['dec'] == 1850]
cwb_last = cwb[cwb['dec'] == 2090]
# %%
