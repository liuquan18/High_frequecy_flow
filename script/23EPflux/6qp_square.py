# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import glob

# %%
qq = xr.open_mfdataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/qpqp_monthly_ensmean/*.nc")
# %%
qq =qq.hus
# %%
qq = qq.sel(plev = 85000)
#%%
qq = qq.rolling(time = 10).mean()
# %%
qq.compute()
# %%
qq_NPC = qq.sel(lon = slice(120, 240), lat = slice(30, 50)).mean(dim = ['lon', 'lat'])
qq_NAL = qq.sel(lon = slice(270, 330), lat = slice(30, 50)).mean(dim = ['lon', 'lat'])
# %%
qq_NPC.plot()
# %%
qq_NAL.plot()

# %%
