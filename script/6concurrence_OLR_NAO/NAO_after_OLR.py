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

#%%
from src.OLR_NAO.OLR_NAO_association import read_extremes
# %%


# %%
def NAO_after_OLR(OLR, NAO, lag=[-16,-6]):

    # -16 days lag of NAO time
    NAO["sign_start_time"] = pd.to_datetime(NAO["sign_start_time"])
    NAO["lag_start_time"] = NAO["sign_start_time"] + pd.DateOffset(days=lag[0])
    NAO["lag_end_time"] = NAO["sign_start_time"] + pd.DateOffset(days=lag[1])

    # for each row of NAO, find the rows in OLR whose sign_start_time is before the lag_time
    OLR_befores = []
    OLR["sign_start_time"] = pd.to_datetime(OLR["sign_start_time"])
    for i, row in NAO.iterrows():
        lag_start_time = row["lag_start_time"]
        lag_end_time = row["lag_end_time"]
        OLR_sel = OLR[
            (OLR["sign_start_time"] >= lag_start_time)
            &(OLR["sign_start_time"] <= lag_end_time)
            & (OLR["sign_start_time"].dt.year == lag_start_time.year)
        ]

        OLR_befores.append(OLR_sel)
    
    if OLR_befores:
        OLR_before = pd.concat(OLR_befores)
        # drop duplicates
        OLR_before = OLR_before.drop_duplicates(subset=["sign_start_time", "lat", "lon"])

        return OLR_before.reset_index(drop=True)
    else:
        return pd.DataFrame()


# %%
def NAO_after_OLR_all(period,  extreme_type="pos", lag=[-16,-6]):
    """
    select OLR extremes that are before the NAO extremes by lag days for all members
    """
    con_xs = []

    for member in range(1, 51):
        logging.info(f"member {member}")
        NAO_pos, OLR = read_extremes(
            period, member, extreme_type=extreme_type, lim_OLR = 10
        )
        concurrence = NAO_after_OLR(OLR, NAO_pos, lag=lag)
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
first10_pos = NAO_after_OLR_all("first10", lag = [-16,-6])

#%%
last10_pos = NAO_after_OLR_all("last10", lag = [-16,-6])
# %%
# 
def plot_concurrence(
    extreme_duration, ax, custom_cmap="Blues", levels=np.arange(5, 16, 1)
):
    p = extreme_duration.plot(
        ax=ax,
        # cmap='Blues',
        transform=ccrs.PlateCarree(),
        levels=levels,
        extend="max",
        add_colorbar=False,
    )
    p.axes.coastlines()
    p.figure.colorbar(p,label = "count")
    return p


#%%
fig = plt.figure(figsize=(12,5))
ax1 = plt.subplot(211, projection=ccrs.PlateCarree(180))

plot_concurrence(first10_pos.count(dim = ('member','sign_start_time')).extreme_duration, ax1)
ax1.set_title("First 10 years")

ax2 = plt.subplot(212, projection=ccrs.PlateCarree(180))
plot_concurrence(last10_pos.count(dim = ('member','sign_start_time')).extreme_duration, ax2)
ax2.set_title("Last 10 years")

plt.suptitle("Occurrence of extreme OLR 16 days before NAO extremes")
plt.tight_layout()
for ax in [ax1, ax2]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])
    
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_extremes/NAO_pos_after_OLR_concurrence.png")

# %%


# %%
first10_neg = NAO_after_OLR_all("first10", extreme_type="neg", lag = [-16,-6])
last10_neg = NAO_after_OLR_all("last10", extreme_type="neg", lag = [-16,-6])

# %%
fig = plt.figure(figsize=(12,5))
ax1 = plt.subplot(211, projection=ccrs.PlateCarree(180))

plot_concurrence(first10_neg.count(dim = ('member','sign_start_time')).extreme_duration, ax1)
ax1.set_title("First 10 years")

ax2 = plt.subplot(212, projection=ccrs.PlateCarree(180))
plot_concurrence(last10_neg.count(dim = ('member','sign_start_time')).extreme_duration, ax2)
ax2.set_title("Last 10 years")

plt.suptitle("Occurrence of extreme OLR 16 days before NAO extremes")
plt.tight_layout()
for ax in [ax1, ax2]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])
    
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_extremes/NAO_neg_after_OLR_concurrence.png")

# %%
