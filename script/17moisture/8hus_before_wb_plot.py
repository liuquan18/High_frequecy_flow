# %%
import xarray as xr
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# %%
first_awb_NAL = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_awb_NAL/awb_NAL_1850.csv",
    index_col=0,
)
first_awb_NPC = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_awb_NPC/awb_NPC_1850.csv",
    index_col=0,
)

first_cwb_NAL = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_cwb_NAL/cwb_NAL_1850.csv",
    index_col=0,
)
first_cwb_NPC = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_cwb_NPC/cwb_NPC_1850.csv",
    index_col=0,
)
# %%
last_awb_NAL = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_awb_NAL/awb_NAL_2090.csv",
    index_col=0,
)
last_awb_NPC = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_awb_NPC/awb_NPC_2090.csv",
    index_col=0,
)

last_cwb_NAL = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_cwb_NAL/cwb_NAL_2090.csv",
    index_col=0,
)
last_cwb_NPC = pd.read_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_cwb_NPC/cwb_NPC_2090.csv",
    index_col=0,
)

# %%
first_awb_NAL["type"] = "AWB"
first_awb_NPC["type"] = "AWB"

first_cwb_NAL["type"] = "CWB"
first_cwb_NPC["type"] = "CWB"

last_awb_NAL["type"] = "AWB"
last_awb_NPC["type"] = "AWB"

last_cwb_NAL["type"] = "CWB"
last_cwb_NPC["type"] = "CWB"

# %%
lag = range(-10, -5)
lag_columns = [str(i) for i in lag]

# %%
first_awb_NAL["lag_mean"] = first_awb_NAL[lag_columns].mean(axis=1)
first_awb_NPC["lag_mean"] = first_awb_NPC[lag_columns].mean(axis=1)

first_cwb_NAL["lag_mean"] = first_cwb_NAL[lag_columns].mean(axis=1)
first_cwb_NPC["lag_mean"] = first_cwb_NPC[lag_columns].mean(axis=1)

last_awb_NAL["lag_mean"] = last_awb_NAL[lag_columns].mean(axis=1)
last_awb_NPC["lag_mean"] = last_awb_NPC[lag_columns].mean(axis=1)

last_cwb_NAL["lag_mean"] = last_cwb_NAL[lag_columns].mean(axis=1)
last_cwb_NPC["lag_mean"] = last_cwb_NPC[lag_columns].mean(axis=1)


# %%
first_awb_NAL = first_awb_NAL.reset_index()[["date", "ens", "type", "dec", "lag_mean"]]
first_awb_NPC = first_awb_NPC.reset_index()[["lag_mean"]]

first_awb_NAL.rename(columns={"lag_mean": "NAL"}, inplace=True)
first_awb_NPC.rename(columns={"lag_mean": "NPC"}, inplace=True)

first_awb = first_awb_NAL.join(first_awb_NPC)
# %%
first_cwb_NAL = first_cwb_NAL.reset_index()[["date", "ens", "type", "dec", "lag_mean"]]
first_cwb_NPC = first_cwb_NPC.reset_index()[["lag_mean"]]

first_cwb_NAL.rename(columns={"lag_mean": "NAL"}, inplace=True)
first_cwb_NPC.rename(columns={"lag_mean": "NPC"}, inplace=True)

first_cwb = first_cwb_NAL.join(first_cwb_NPC)
# %%
last_awb_NAL = last_awb_NAL.reset_index()[["date", "ens", "type", "dec", "lag_mean"]]
last_awb_NPC = last_awb_NPC.reset_index()[["lag_mean"]]
last_awb_NAL.rename(columns={"lag_mean": "NAL"}, inplace=True)
last_awb_NPC.rename(columns={"lag_mean": "NPC"}, inplace=True)
last_awb = last_awb_NAL.join(last_awb_NPC)

# %%
last_cwb_NAL = last_cwb_NAL.reset_index()[["date", "ens", "type", "dec", "lag_mean"]]
last_cwb_NPC = last_cwb_NPC.reset_index()[["lag_mean"]]
last_cwb_NAL.rename(columns={"lag_mean": "NAL"}, inplace=True)
last_cwb_NPC.rename(columns={"lag_mean": "NPC"}, inplace=True)

last_cwb = last_cwb_NAL.join(last_cwb_NPC)

# %%
awb_df = pd.concat([first_awb, last_awb])
cwb_df = pd.concat([first_cwb, last_cwb])
# %%
# drop the row when either of 'NAL' or 'NPC' is NaN
awb_df = awb_df.dropna(subset=["NAL", "NPC"])
cwb_df = cwb_df.dropna(subset=["NAL", "NPC"])

# %%
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
sns.kdeplot(data=awb_df, x="NAL", y="NPC", hue="dec", ax=axes[0], common_norm=True)


sns.kdeplot(
    data=cwb_df, x="NAL", y="NPC", hue="dec", ax=axes[1], common_norm=True, fill=False
)
# plot the 1:1 line
for ax in axes:
    x = np.linspace(0, 1.2, 100)
    y = x
    ax.plot(x, y, "k", linestyle="dotted")
    ax.set_ylim(0.3, 1.3)
    ax.set_xlim(0.3, 1.3)


# %%
