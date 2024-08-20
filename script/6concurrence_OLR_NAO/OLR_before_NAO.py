# %%
import numpy as np
import pandas as pd
import xarray as xr
import logging
import matplotlib.pyplot as plt
import glob
import cartopy.crs as ccrs

# %%
import src.extremes.extreme_read as er

# %%
logging.basicConfig(level=logging.INFO)


# %%
# %%
def read_extremes(period, member, extreme_type="pos", dur_lim=8):
    """
    Read the NAO and OLR extremes
    """
    NAO_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{extreme_type}_extreme_events/{extreme_type}_extreme_events_{period}/"
    OLR_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_extremes_pos/OLR_extremes_pos_{period}/"  # no extreme_type in the OLR_extremes

    # read NAO positive extremes
    NAO_file = glob.glob(
        f"{NAO_dir}troposphere_{extreme_type}_extreme_events*r{member}.csv"
    )[0]
    NAO_pos = pd.read_csv(NAO_file)
    NAO_pos = NAO_pos[NAO_pos["plev"] == 25000]

    # select extremes based on minimum duration
    NAO_pos = er.sel_event_above_duration(
        NAO_pos, duration=dur_lim, by="extreme_duration"
    )
    # select columns
    NAO_pos = NAO_pos[["sign_start_time", "extreme_duration"]]

    # read OLR extremes
    OLR_file = glob.glob(f"{OLR_dir}OLR_extremes*r{member}.csv")[0]
    OLR = pd.read_csv(OLR_file)
    # select extremes based on minimum duration but not limited in JJA
    OLR = OLR[OLR["extreme_duration"] >= dur_lim]
    # select columns
    OLR = OLR[["sign_start_time", "extreme_duration", "lat", "lon"]]

    return NAO_pos, OLR


# %%
def OLR_before_NAO(OLR, NAO, lag=16):

    # 16 days ahead of OLR time
    OLR["sign_start_time"] = pd.to_datetime(OLR["sign_start_time"])
    OLR["ahead_time"] = OLR["sign_start_time"] + pd.DateOffset(days=lag)

    NAO["sign_start_time"] = pd.to_datetime(NAO["sign_start_time"])

    # for each row of OLR, keep the rows if the "ahead_time" is after the "sign_start_time" of NAO
    OLR_befores = []
    OLR["sign_start_time"] = pd.to_datetime(OLR["sign_start_time"])
    for i, row in OLR.iterrows():
        if any((row["ahead_time"] > NAO["sign_start_time"]) & (
            row["ahead_time"].year == NAO["sign_start_time"].dt.year
        ).values):
            OLR_before = row
        else:
            continue

        OLR_befores.append(OLR_before)

    if OLR_befores:
        OLR_befores = pd.DataFrame(OLR_befores)
        # drop duplicates
        OLR_befores = OLR_befores.drop_duplicates()
        return OLR_befores.reset_index(drop=True)

    else:
        return pd.DataFrame()



# %%
def OLR_before_NAO_all(period, dur_lim=8, extreme_type="pos", lag=-16):
    """
    select OLR extremes that are before the NAO extremes by lag days for all members
    """
    con_xs = []

    for member in range(1, 51):
        logging.info(f"member {member}")
        NAO_pos, OLR = read_extremes(
            period, member, extreme_type=extreme_type, dur_lim=dur_lim
        )
        concurrence = OLR_before_NAO(OLR, NAO_pos, lag=lag)
        if concurrence.empty:
            continue

        concurrence = concurrence[["sign_start_time", "extreme_duration", "lat", "lon"]]
        concurrence = concurrence.set_index(["sign_start_time", "lat", "lon"])
        con_x = concurrence.to_xarray()

        con_xs.append(con_x)
    # if con_xs is empty, return None
    con_xs = xr.concat(con_xs, dim="member")

    return con_xs


# %%
first10_pos = OLR_before_NAO_all("first10")

# %%
last10_pos = OLR_before_NAO_all("last10")


# %%
#
def plot_concurrence(
    extreme_duration, ax, custom_cmap="Blues", levels=np.arange(5, 31, 5)
):
    p = extreme_duration.plot(
        ax=ax,
        # cmap='Blues',
        transform=ccrs.PlateCarree(),
        levels=levels,
        extend="max",
    )
    p.axes.coastlines()
    return p


# %%
fig = plt.figure(figsize=(12, 5))
ax1 = plt.subplot(211, projection=ccrs.PlateCarree(180))

plot_concurrence(
    first10_pos.count(dim=("member", "sign_start_time")).extreme_duration, ax1
)
ax1.set_title("First 10 years")

ax2 = plt.subplot(212, projection=ccrs.PlateCarree(180))
plot_concurrence(
    last10_pos.count(dim=("member", "sign_start_time")).extreme_duration, ax2
)
ax2.set_title("Last 10 years")

for ax in [ax1, ax2]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])

plt.suptitle("Occurrence of extreme OLR 16 days before NAO extremes")
plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_extremes/OLR_before_NAO_concurrence.png")
# %%
