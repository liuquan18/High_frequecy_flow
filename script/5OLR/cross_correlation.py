#%%
import xarray as xr
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import statsmodels.api as sm
import glob
import seaborn as sns
import pandas as pd
#%%
def read_data(period,ens, plev = 25000):
    OLR_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/{period}_OLR_daily_ano/'
    OLR_file = glob.glob(OLR_dir+f'*r{ens}i1p1f1*.nc')[0]
    OLR = xr.open_dataset(OLR_file).rlut

    # field mean 
    OLR = OLR.sel(lon = slice(50,100)).mean(dim = ['lat','lon'])

    NAO_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_{period}/'
    NAO_file = glob.glob(NAO_dir+f'*r{ens}.nc')[0]
    NAO = xr.open_dataset(NAO_file).pc.sel(plev = plev)

    # select the same time period
    NAO = NAO.sel(time = OLR.time)

    # to dataframe
    OLR = OLR.to_dataframe().reset_index()[['time','rlut']].set_index('time')
    NAO = NAO.to_dataframe().reset_index()[['time','pc']].set_index('time')


    return OLR, NAO

#%%
# function to calculate cross correlation
def ccf(OLR,NAO):

    # combine two dataframes 
    ds = OLR.join(NAO, how = 'inner')
    # groupy by year and calculate cross correlation
    CCF = ds.groupby(ds.index.year)[['rlut','pc']].apply(lambda x: sm.tsa.stattools.ccf(ds['pc'],ds['rlut'], adjusted = True))
    # convert to dataframe
    CCF = pd.DataFrame()
    return CCF

#%%


# %%
OLR = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/tmp/Indo_OLR_recon.nc")
# %%
NAO = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_first10/troposphere_pc_MJJAS_ano_1850_1859_r1.nc")
# %%
OLR = OLR.TP_OLR_reconstructed.squeeze()
NAO = NAO.pc.sel(plev = 50000)
# %%

NAO = NAO.sel(time = "1850")
OLR = OLR.sel(time ="1850")

NAO = NAO.sel(time = OLR.time)
# %%
OLR = OLR.to_dataframe().reset_index()[['time','TP_OLR_reconstructed']]
# %%
NAO = NAO.to_dataframe().reset_index()[['time','pc']]
# %%
OLR = OLR.set_index('time')
NAO = NAO.set_index('time')
# %%
# OLR leads NAO
CCF_OLR_lead_NAO = sm.tsa.stattools.ccf(
                                        NAO.pc,
                                        OLR.TP_OLR_reconstructed,
                                        adjusted = True,
                                        )

#%%
# plot
coef = CCF_OLR_lead_NAO[0]
conf = CCF_OLR_lead_NAO[1]
plt.plot(coef)
plt.fill_between(range(len(coef)), conf[:,0], conf[:,1], color='gray', alpha=0.3)
plt.axhline(0, color='black', linestyle='--', linewidth=1)
# plt.xlim(0,60)

# %%
