# %%
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from src.data_helper.read_variable import read_climatology, read_climatology_decmean

# %%
from src.plotting.util import map_smooth


# %%
def calc_land_ocean_contrast(
    theta_dec,
    lat_slice=slice(50, 70),
    lon_land=slice(60, 120),
    lon_ocean=slice(300, 360),
    lon_win=7,
    lat_win=3,
):
    theta_dec_ano = theta_dec - theta_dec.mean(dim="lon")
    theta_dec_ano = map_smooth(theta_dec_ano, lon_win=lon_win, lat_win=lat_win)
    theta_dec_ano = theta_dec_ano.sel(lat=lat_slice).mean(dim="lat")
    contrast = theta_dec_ano.sel(lon=lon_land).mean(dim="lon") - theta_dec_ano.sel(
        lon=lon_ocean
    ).mean(dim="lon")
    return contrast


# %%
zg_first = read_climatology("zg_steady", 1850, plev=25000, name="zg")
zg_last = read_climatology("zg_steady", 2090, plev=25000, name="zg")
# %%
# smooth the data
zg_first = map_smooth(zg_first, lon_win=7, lat_win=3)
zg_last = map_smooth(zg_last, lon_win=7, lat_win=3)

# %%
theta_first = read_climatology(
    "theta_hat", 1850, plev=85000, name="theta"
)  # remove zonal mean to get zonal anomaly
theta_last = read_climatology("theta_hat", 2090, plev=85000, name="theta")
# %%
theta_first = map_smooth(theta_first, lon_win=7, lat_win=3)
theta_last = map_smooth(theta_last, lon_win=7, lat_win=3)
# %%
theta_first = theta_first - theta_first.mean(dim="lon")
theta_last = theta_last - theta_last.mean(dim="lon")
# %%
etheta_first = read_climatology("equiv_theta_hat", 1850, plev=85000, name="etheta")
etheta_last = read_climatology("equiv_theta_hat", 2090, plev=85000, name="etheta")
# %%
etheta_first = map_smooth(etheta_first, lon_win=7, lat_win=3)
etheta_last = map_smooth(etheta_last, lon_win=7, lat_win=3)

etheta_first = etheta_first - etheta_first.mean(dim="lon")
etheta_last = etheta_last - etheta_last.mean(dim="lon")
# %%
steady_heat = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0std_change/steady_eddy_heat_d2y2_decmean_ensmean_85000hPa.nc"
)
steady_heat = steady_heat["std"].squeeze()
# %%
# theta land-ocean contrast
theta_dec = read_climatology_decmean("theta_hat", plev=85000, NAL=False, name="theta")
theta_dec_contrast = calc_land_ocean_contrast(theta_dec)
# %%
# to pandas
theta_dec_contrast_df = (
    theta_dec_contrast["theta"].to_dataframe("contrast").reset_index()
)
theta_dec_contrast_df["decade"] = theta_dec_contrast_df["year"] - 9
steady_heat_df = steady_heat.to_dataframe("steady_heat").reset_index()
steady_heat_df["decade"] = steady_heat_df["time"].dt.year - 9
# divide the steady heat by the value at 1850s
steady_heat_df["steady_heat"] = (
    steady_heat_df["steady_heat"]
    / steady_heat_df.loc[steady_heat_df["decade"] == 1850, "steady_heat"].values[0]
)
steady_heat_df = steady_heat_df[["decade", "steady_heat"]]
theta_dec_contrast_df = theta_dec_contrast_df[["decade", "contrast"]]
# merge the two dataframes
merged_df = pd.merge(steady_heat_df, theta_dec_contrast_df, on="decade", how="outer")


# %%
# extremes only
# %%
# meridional mean
def meri_mean(zg_first, zg_last, lat_slice=slice(50, 70)):
    zg_first_mm = zg_first.sel(lat=lat_slice).mean(dim="lat")
    zg_last_mm = zg_last.sel(lat=lat_slice).mean(dim="lat")

    # change the longitude from 0-360 to -180 to 180
    zg_first_mm = zg_first_mm.assign_coords(lon=((zg_first_mm.lon + 180) % 360) - 180)
    zg_last_mm = zg_last_mm.assign_coords(lon=((zg_last_mm.lon + 180) % 360) - 180)

    # sort the longitude
    zg_first_mm = zg_first_mm.sortby("lon")
    zg_last_mm = zg_last_mm.sortby("lon")
    return zg_first_mm, zg_last_mm


# %%
zg_first_mm, zg_last_mm = meri_mean(zg_first, zg_last)
theta_first_mm, theta_last_mm = meri_mean(theta_first, theta_last)
etheta_first_mm, etheta_last_mm = meri_mean(etheta_first, etheta_last)


# %%
fig, axes = plt.subplots(1, 2, figsize=(8, 4))  # 1 row, 2 columns

# theta at 850 hPa (axes[0])
theta_first_mm.plot.line(
    ax=axes[0],
    x="lon",
    color="k",
    label="1850s",
    linewidth=1.5,
)
theta_last_mm.plot.line(
    ax=axes[0],
    x="lon",
    linestyle="--",
    color="k",
    label="2090s",
    linewidth=1.5,
)

# scatter plot (axes[1])
sns.scatterplot(
    data=merged_df,
    x="contrast",
    y="steady_heat",
    ax=axes[1],
    hue="decade",
    palette="Greys",
    s=150,
)

# Set titles and labels for only the used axes
axes[0].set_title("")
axes[0].set_ylabel(r"$\overline{\theta^*}$ at 850 hPa (K)")
axes[1].set_title("")
axes[1].set_ylabel(r"std of $\partial^2 \overline{v^*\theta^*}/\partial y^2$")
axes[1].legend(loc="lower right")

# Remove the top and right spines, set x-labels, legends, and panel labels for only the used axes
axes[0].spines["top"].set_visible(False)
axes[0].spines["right"].set_visible(False)
axes[0].set_xlabel("Longitude")
axes[0].legend(loc="lower right", fontsize=10)

axes[0].set_xticks(np.arange(-180, 181, 90))

axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)
axes[1].set_xlabel(r"land-ocean contrast [K]")


# vertical text "North Atlantic" at x = -50 on the first subplot
axes[0].text(
    0.27,
    0.4,
    "North America",
    transform=axes[0].transAxes,
    fontsize=10,
    va="center",
    ha="right",
    rotation=90,
)

axes[0].text(
    0.43,
    0.7,
    "North Atlantic",
    transform=axes[0].transAxes,
    fontsize=10,
    va="center",
    ha="right",
    rotation=90,
)
axes[0].text(
    0.73,
    0.4,
    "Eurasia",
    transform=axes[0].transAxes,
    fontsize=10,
    va="center",
    ha="right",
    rotation=90,
)

plt.tight_layout()

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/land_ocean_contrast.png", dpi=500, bbox_inches="tight", metadata={"Creator": __file__})

# %%
