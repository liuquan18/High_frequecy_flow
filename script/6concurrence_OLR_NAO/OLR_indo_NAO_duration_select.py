#%%
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %%
import src.OLR_NAO.OLR_NAO_association as OLR_NAO
# %%
# read the OLR and NAO extremes
period = 'first10'
member = 2
extreme_type = 'pos'
dur_lim = 8
# %%
def read_extreme_mean(period, member, extreme_type, dur_lim):

    NAO_pos, OLR = OLR_NAO.read_extremes(period, member, extreme_type=extreme_type, limit = False, dur_lim=dur_lim)
    
    NAO_pos['sign_start_time'] = pd.to_datetime(NAO_pos['sign_start_time'])
    OLR['sign_start_time'] = pd.to_datetime(OLR['sign_start_time'])
    
    OLR_x = OLR.set_index(['sign_start_time','lat','lon']).to_xarray()

    
    OLR_indo_x = OLR_x.sel(lon=slice(50,110)).mean(dim = ['lat','lon'])
    
    OLR_indo = OLR_indo_x.to_dataframe().reset_index()

    return OLR_indo, NAO_pos

#%%
OLR_indos = []
NAOs = []

for member in range(1, 51):
    OLR_indo, NAO = read_extreme_mean(period, member, extreme_type, dur_lim)
    OLR_indo['member'] = member
    NAO['member'] = member

    OLR_indos.append(OLR_indo)
    NAOs.append(NAO)
#%%
OLR_indos = pd.concat(OLR_indos)
NAOs = pd.concat(NAOs)

#%%
# plot the hist
fig, ax = plt.subplots()

NAOs[NAOs['extreme_duration']>=8]['extreme_duration'].plot.hist(ax = ax, label = 'NAO', bins = 10)
OLR_indos[OLR_indos['extreme_duration']>=20]['extreme_duration'].plot.hist(ax = ax, alpha = 0.5,label = 'OLR_indo', bins = 10)

plt.legend()
plt.suptitle("duration of the extremes that occur roughly in the same frequency")

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_extremes/OLR_indo_NAO_extreme_duration_hist_sel.png")


#%%
# take annual mean
OLR_indo_summer = OLR_indo.groupby(OLR_indo['sign_start_time'].dt.year)[['extreme_duration']].count()
# %%
NAO_summer = NAO_pos.groupby(NAO_pos['sign_start_time'].dt.year)[['extreme_duration']].count()
# %%
