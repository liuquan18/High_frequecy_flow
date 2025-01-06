#%%
# %%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns


# %%
def read_data(decade):
    base_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/husDBtas_hussatDBtas_dec/moist_tas_ratio_{decade}.nc"
    data = xr.open_dataset(base_dir)
    return data


# %%
def sector(data):
    box_EAA = [
        -35,
        140,
        20,
        60,
    ]  # [lon_min, lon_max, lat_min, lat_max] Eurasia and Africa
    box_NAM = [-145, -70, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North America
    box_NAL = [-70, -35, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Atlantic
    box_NPO = [140, -145, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Pacific

    data_EAA = data.sel(lon=slice(box_EAA[0], box_EAA[1])).mean(dim=("lon", "lat"))
    data_NAM = data.sel(lon=slice(box_NAM[0], box_NAM[1])).mean(dim=("lon", "lat"))
    data_NAL = data.sel(lon=slice(box_NAL[0], box_NAL[1])).mean(dim=("lon", "lat"))
    data_NPO1 = data.sel(lon=slice(box_NPO[0], 180))
    data_NPO2 = data.sel(lon=slice(-180, box_NPO[1]))
    data_NPO = xr.concat([data_NPO1, data_NPO2], dim="lon").mean(dim=("lon", "lat"))
    return data_EAA, data_NAM, data_NAL, data_NPO


# %%
dfs = []

for i in range(1850, 2100, 10):
    data = read_data(i)
    EAA, NAM, NAL, NPO = sector(data)

    dfs.append(
        {
            "decade": i,
            "hus": EAA.hus.values.item(),
            "hussat": EAA.hussat.values.item(),
            "region": "EAA",
        }
    )
    dfs.append(
        {
            "decade": i,
            "hus": NAM.hus.values.item(),
            "hussat": NAM.hussat.values.item(),
            "region": "NAM",
        }
    )
    dfs.append(
        {
            "decade": i,
            "hus": NAL.hus.values.item(),
            "hussat": NAL.hussat.values.item(),
            "region": "NAL",
        }
    )
    dfs.append(
        {
            "decade": i,
            "hus": NPO.hus.values.item(),
            "hussat": NPO.hussat.values.item(),
            "region": "NPO",
        }
    )

df = pd.DataFrame(dfs)
# %%
# minus the value of 1850 ['hus', 'hussat'] from all values
df_ano = pd.DataFrame()
df_ano["decade"] = df["decade"]
df_ano["hus"] = df["hus"] - df[df["decade"] == 1850]["hus"].values[0]
df_ano["hussat"] = df["hussat"] - df[df["decade"] == 1850]["hussat"].values[0]
df_ano["region"] = df["region"]
# %%
# wave breaking
awb = pd.read_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wave_breaking_stat/awb_th3_NAO_overlap70.csv', index_col=0)
# %%
cwb = pd.read_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wave_breaking_stat/cwb_th3_NAO_overlap70.csv', index_col=0)
# %%
awb_count = awb.groupby(['dec']).size().reset_index(name='count')
cwb_count = cwb.groupby(['dec']).size().reset_index(name='count')
#%%
# rename 'dec' to 'decade' for merging
awb_count = awb_count.rename(columns={'dec': 'decade'})
cwb_count = cwb_count.rename(columns={'dec': 'decade'})

#%%
# count column divided by 50 (ensemble members)
awb_count['count'] = awb_count['count'] / 50
cwb_count['count'] = cwb_count['count'] / 50
# %%
hus_NAL = df_ano[df_ano["region"] == "NAL"][['decade', 'hus']]
hus_NPO = df_ano[df_ano["region"] == "NPO"][['decade', 'hus']]
# %%
# merge the dataframes awb_count, cwb_count, hus_NAL, hus_NPO on 'decade'
wb_merge = pd.merge(awb_count, cwb_count, on='decade', suffixes=('_awb', '_cwb'))

# %%
moist_merge = pd.merge(hus_NAL,hus_NPO, on='decade', suffixes=('_NAL', '_NPO'))
# %%
final_merge = pd.merge(wb_merge, moist_merge, on='decade')
# %%
# plot
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
sns.lineplot(data=final_merge, x='decade', y='count_awb', ax=ax[1], label='AWB', color = 'k')
sns.lineplot(data=final_merge, x='decade', y='count_cwb', ax=ax[1], label='CWB', color = 'k', linestyle='--')

sns.lineplot(data=final_merge, x='decade', y='hus_NAL', ax=ax[0], label='NAL', color = sns.color_palette()[0])
sns.lineplot(data=final_merge, x='decade', y='hus_NPO', ax=ax[0], label='NPO', color = sns.color_palette()[-1])

ax[0].set_title('humidity')
ax[1].set_title('wave breaking')


ax[0].set_ylabel(r'longitudinal $\Delta$ hus /$\Delta$ tas ($g \cdot kg^{-1}K^{-1}$)')
ax[1].set_ylabel('wavebreaking count (per dec per ens)')
plt.savefig('/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/wb_count_hus_dec.png')
# %%
