#%%
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%%
def to_dataframe(pc):

    # exclude the data at 1st may to 3rd May, and the data during 28th Sep and 31st Sep
    mask_exclude = (
        (pc["time.month"] == 5) & (pc["time.day"] >= 1) & (pc["time.day"] <= 3)
    ) | ((pc["time.month"] == 9) & (pc["time.day"] >= 28) & (pc["time.day"] <= 30))
    mask_keep = ~mask_exclude

    pc = pc.where(mask_keep, drop=True)

    # convert to dataframe
    pc = pc.to_dataframe().reset_index()[["plev", "time", "pc"]]
    pc["time"] = pd.to_datetime(pc["time"].values)

    return pc

# %%
def read_pc_df(decade):

    projected_pc_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NAO_pc_{decade}_trop_std/"

    pcs = []

    for member in range(1, 51):
        print(f"Decade {decade}, member {member}")
        
        # read pc index
        pc = xr.open_dataset(
            f"{projected_pc_path}/NAO_pc_{decade}_r{member}_std.nc"
        ).pc

        pc = to_dataframe(pc)
        pcs.append(pc)

        pc['ens'] = member
        pc['decade'] = decade
    pc_df = pd.concat(pcs, ignore_index=True)
    return pc_df

# %%
pc_first = read_pc_df('1850')
# %%
pc_last = read_pc_df('2090')
# %%
pc = pd.concat([pc_first, pc_last], ignore_index=True)

# %%
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(
    data = pc,
    x = 'pc',
    hue = 'decade',
    hue_order = ['1850', '2090'],
    palette=["#1f77b4", "#ff7f0e"],
    multiple="dodge",
    shrink=0.6,
    bins=np.arange(-4, -3, 0.5),
    ax=ax,
    stat = 'density',
)
# %%
