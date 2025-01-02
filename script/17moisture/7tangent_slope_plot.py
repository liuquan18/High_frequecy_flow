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
fig, ax = plt.subplots(1, 2, figsize=(10, 5))

# Update the region labels
df["region"] = df["region"].replace({
    "EAA": "Eurasia_North_Africa",
    "NAM": "North_America",
    "NAL": "North_Atlantic",
    "NPO": "North_Pacific"
})

sns.lineplot(
    data=df[df["region"].isin(["Eurasia_North_Africa", "North_America"])],
    x="decade",
    y="hus",
    hue="region",
    ax=ax[0],
    palette = [sns.color_palette()[1], sns.color_palette()[3]]
)
sns.lineplot(
    data=df[df["region"].isin(["Eurasia_North_Africa", "North_America"])],
    x="decade",
    y="hussat",
    hue="region",
    ax=ax[0],
    linestyle="dotted",
    legend=False,
    palette = [sns.color_palette()[1], sns.color_palette()[3]]
)

sns.lineplot(
    data=df[df["region"].isin(["North_Atlantic", "North_Pacific"])],
    x="decade",
    y="hus",
    hue="region",
    ax=ax[1],
    palette = [sns.color_palette()[0], sns.color_palette()[-1]]
)
sns.lineplot(
    data=df[df["region"].isin(["North_Atlantic", "North_Pacific"])],
    x="decade",
    y="hussat",
    hue="region",
    ax=ax[1],
    linestyle="dotted",
    legend=False,
    palette = [sns.color_palette()[0], sns.color_palette()[-1]]
)

ax[0].set_title("Continent")
ax[1].set_title("Ocean")

ax[0].set_ylabel(r"$\Delta$ moisture / $\Delta$ tas (g/kg/K)")
ax[1].set_ylabel(r"$\Delta$ moisture / $\Delta$ tas (g/kg/K)")

# create custom legend, solid line for 'hus' and dashed line for 'hussat'
handles, labels = ax[0].get_legend_handles_labels()
lines = [
    plt.Line2D([0], [0], color="grey", lw=2),
    plt.Line2D([0], [0], color="grey", lw=2, linestyle="dotted"),
]
custom_labels = ["hus", "hussat"]
ax[0].legend(handles + lines, labels + custom_labels, loc="upper left")

handles, labels = ax[1].get_legend_handles_labels()
ax[1].legend(handles + lines, labels + custom_labels, loc="upper left")

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/mosit_get_mosit_dec.png")
# %%
