# %%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import logging

logging.basicConfig(level=logging.INFO)
import seaborn as sns

import matplotlib.pyplot as plt


# %%
def _jet_stream_anomaly(ens, period, jet_speed_clim, jet_loc_clim):
    # Load data
    jet_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_{period}/"
    jet_file = glob.glob(f"{jet_path}*r{ens}i1p1f1*.nc")[0]

    jet = xr.open_dataset(jet_file).ua
    # drop dim lon
    jet = jet.isel(lon=0)

    # maximum westerly wind speed of the resulting profile is then identified and this is defined as the jet speed.
    jet_speed = jet.max(dim="lat")
    jet_speed_ano = jet_speed.groupby("time.month") - jet_speed_clim

    # The jet latitude is defined as the latitude at which this maximum is found.
    jet_loc = jet.lat[jet.argmax(dim="lat")]

    jet_loc_ano = jet_loc.groupby("time.month") - jet_loc_clim

    if jet_loc_ano.min() < -50:
        logging.warning(
            f"Jet latitude anomaly is below -40 for ens {ens} in period {period}\n"
        )

    return jet_speed_ano, jet_loc_ano


# %%
def jet_stream_anomaly(period):

    # climatology only use the first10 years
    jet_speed_clim = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_speed_climatology_first10.nc"
    ).ua
    jet_loc_clim = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_first10.nc"
    ).lat

    jet_speed_ano = []
    jet_loc_ano = []

    for ens in range(1, 51):
        speed_ano, loc_ano = _jet_stream_anomaly(
            ens, period, jet_speed_clim, jet_loc_clim
        )
        speed_ano["ens"] = ens
        loc_ano["ens"] = ens

        jet_speed_ano.append(speed_ano)
        jet_loc_ano.append(loc_ano)

    jet_speed_ano = xr.concat(jet_speed_ano, dim="ens")
    jet_loc_ano = xr.concat(jet_loc_ano, dim="ens")

    return jet_speed_ano, jet_loc_ano


# %%

jet_speed_first10_ano, jet_loc_first10_ano = jet_stream_anomaly("first10")

# %%
jet_speed_last10_ano, jet_loc_last10_ano = jet_stream_anomaly("last10")
# %%
# jet location anomaly
sns.histplot(
    jet_loc_first10_ano.values.flatten(),
    label="first10",
    color="b",
    bins=np.arange(-30, 31, 2),
    stat="count",
)
sns.histplot(
    jet_loc_last10_ano.values.flatten(),
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
)
plt.legend()
# %%
sns.histplot(
    jet_speed_first10_ano.values.flatten(),
    label="first10",
    color="b",
    bins=np.arange(-5, 5.2, 0.5),
    stat="density",
)
sns.histplot(
    jet_speed_last10_ano.values.flatten(),
    label="last10",
    color="r",
    bins=np.arange(-5, 5.2, 0.5),
    stat="density",
    alpha=0.5,
)
# %%
def jet_loc_extremeNAO(NAO, jet_loc):
    jet_loc_negs = []
    jet_loc_poss = []

    for ens in range(1, 51):
        NAO_ens = NAO.sel(ens=ens)

        # negative NAO extreme months
        NAO_neg = NAO_ens.where(NAO_ens < -1.5, drop=True)
        jet_loc_neg = jet_loc.sel(
        ens=ens,
        time=(
            jet_loc.time.dt.year.isin(NAO_neg.time.dt.year)
            & jet_loc.time.dt.month.isin(NAO_neg.time.dt.month)
        ),
    )

        NAO_pos = NAO_ens.where(NAO_ens > 1.5, drop=True)
        jet_loc_pos = jet_loc.sel(
        ens=ens,
        time=(
            jet_loc.time.dt.year.isin(NAO_pos.time.dt.year)
            & jet_loc.time.dt.month.isin(NAO_pos.time.dt.month)
        ),
    )

        if jet_loc_neg.time.size == 0:
            continue # empty array
        else:
            jet_loc_negs.append(jet_loc_neg.values)

        if jet_loc_pos.time.size == 0:
            continue
        else:
            jet_loc_poss.append(jet_loc_pos.values)

    # flat the list
    jet_loc_negs = np.concatenate(jet_loc_negs)
    jet_loc_poss = np.concatenate(jet_loc_poss)

    return jet_loc_negs, jet_loc_poss

#%%
NAO_index = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result/troposphere_ind_decade_first_JJA_eof_result.nc"
)
# %%
NAO_index = NAO_index.sel(mode="NAO", plev=50000).pc
NAO_index["ens"] = NAO_index.ens + 1  # start from 1
# %%

NAO_first = NAO_index.sel(time=slice("1850", "1859"))
jet_loc_first_neg, jet_loc_first_pos = jet_loc_extremeNAO(NAO_first, jet_loc_first10_ano)
# %%
NAO_last = NAO_index.sel(time=slice("2091", "2100"))
jet_loc_last_neg, jet_loc_last_pos = jet_loc_extremeNAO(NAO_last, jet_loc_last10_ano)
# %%
fig, axes = plt.subplots(3,1, figsize = (10, 10))

# jet location anomaly
sns.histplot(
    jet_loc_first10_ano.values.flatten(),
    label="first10",
    color="b",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax = axes[0]
)
sns.histplot(
    jet_loc_last10_ano.values.flatten(),
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax = axes[0]
)
axes[0].legend()
axes[0].set_title("Jet location anomaly (all)")
axes[0].set_ylim(0,15000)

# positive NAO extreme jet location
sns.histplot(
    jet_loc_first_pos,
    label="first10",
    color="b",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax = axes[1]
)
sns.histplot(
    jet_loc_last_pos,
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax = axes[1]
)
axes[1].set_ylim(0,2000)
axes[1].set_title("Jet location anomaly (positive NAO)")



# negtive NAO extreme jet location
sns.histplot(
    jet_loc_first_neg,
    label="first10",
    color="b",
    bins=np.arange(-30, 31, 2),
    stat="count",
    ax = axes[2]
)
sns.histplot(
    jet_loc_last_neg,
    label="last10",
    color="r",
    bins=np.arange(-30, 31, 2),
    stat="count",
    alpha=0.5,
    ax = axes[2]
)
axes[2].set_ylim(0,2000)
axes[2].set_title("Jet location anomaly (negative NAO)")


# %%
