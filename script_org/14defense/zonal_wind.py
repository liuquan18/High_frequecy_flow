# %%
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# %%
# Load data
ds = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/ua_monthly_mean/ua_monthly_05_09.nc"
)

# %%
# Select 250 hPa level (assuming 'level' is the pressure coordinate)
ua_250 = ds["var131"].sel(plev=25000)

# Average over all times
ua_250_mean = ua_250.mean(dim="time")

# Only Northern Hemisphere
ua_250_mean_nh = ua_250_mean.sel(lat=slice(90, 0))

# %%
# Plot
plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree())

# Define contour levels
levels = np.arange(-40, 41, 5)  # adjust as needed

# Plot positive contours (solid black)
pos_levels = [lvl for lvl in levels if lvl > 0]
ua_250_mean_nh.plot.contour(
    ax=ax,
    transform=ccrs.PlateCarree(),
    levels=pos_levels,
    colors="black",
    linestyles="solid",
    add_colorbar=False,
)

# Plot negative contours (dashed black)
neg_levels = [lvl for lvl in levels if lvl < 0]
ua_250_mean_nh.plot.contour(
    ax=ax,
    transform=ccrs.PlateCarree(),
    levels=neg_levels,
    colors="black",
    linestyles="dashed",
    add_colorbar=False,
)

# Add colorbar for reference (optional, can be removed)
contourf = ua_250_mean_nh.plot.contourf(
    ax=ax,
    transform=ccrs.PlateCarree(),
    levels=levels,
    cmap="coolwarm",
    add_colorbar=True,
    cbar_kwargs={"label": "Zonal wind (m/s)"},
    alpha=0.3,
)

ax.coastlines()
ax.add_feature(cfeature.BORDERS, linewidth=0.5)
ax.set_title("Mean Zonal Wind at 250 hPa (ERA5, May-Sep, NH)")


# add line at y = 50 degrees
ax.axhline(50, color="red", linestyle="--", lw=1)

plt.show()

# %%
# plot the profile of the zonal wind at 50 degrees north
ua_50N = ua_250_mean.sel(lat=50, method="nearest")

# Select longitude range from -150 to 30
ua_50N_subset = ua_50N.sel(lon=slice(-150, 30))

plt.figure(figsize=(10, 5))
plt.plot(ua_50N_subset["lon"], ua_50N_subset, color="blue", lw=1.5)
plt.axhline(0, color="k", lw=0.8)
plt.title("Zonal Wind at 50°N, 250 hPa (ERA5, May-Sep)")
plt.xlabel("Longitude (°)")
plt.ylabel("Zonal Wind (m/s)")
plt.grid(True, ls="--", alpha=0.5)
plt.show()
# %%
ds_50 = ds.sel(lat=50, method="nearest")
# %%
ds_50 = ds_50.mean(dim="time").var131
# %%
data = ds_50
## Shift longitude from [0, 360) → [-180, 180)
lon = data.lon
lon_shifted = ((lon + 180) % 360) - 180
data_shifted = data.assign_coords(lon=lon_shifted)

# Sort by longitude so it goes from -180 → 180
data_shifted = data_shifted.sortby("lon")

# Plot
plt.figure(figsize=(12, 6))
contour = plt.contourf(
    data_shifted.lon, data_shifted.plev, data_shifted, cmap="RdBu_r", levels=21
)

plt.gca().invert_yaxis()  # Pressure: high at bottom, low at top
plt.colorbar(contour, label="Value")

plt.xlabel("Longitude (°)")
plt.ylabel("Pressure level (hPa)")
plt.title("Longitude–Height Cross-Section at 50°N")

# Optional: Add vertical line at Greenwich (0°)
plt.axvline(0, color="k", linestyle="--", lw=0.8)

plt.show()

# %%
# Map of Northern Hemisphere, black background, white coastlines, gray continents, Winkel Tripel projection
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig = plt.figure(figsize=(12, 6.75))
ax = plt.axes(projection=ccrs.PlateCarree())

# Set background color to black
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

# Add continents in gray
ax.add_feature(cfeature.LAND, facecolor="gray", edgecolor="none")
# Add coastlines in white
ax.coastlines(color="gray", linewidth=1.0)

# Limit to Northern Hemisphere
# ax.set_extent([-150, 150, 0, 90], crs=ccrs.PlateCarree())

# plt.title("Northern Hemisphere Map (Robinson)", color="white")
plt.tight_layout()
plt.show()

# %%
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

# Example grid (replace with your own data)
lon = np.linspace(-180, 180, 100)
lat = np.linspace(-90, 90, 50)
Lon, Lat = np.meshgrid(lon, lat)

# Example wind field (synthetic, replace with your data)
u = np.cos(np.deg2rad(Lat)) * np.cos(2 * np.deg2rad(Lon))
v = np.sin(np.deg2rad(Lon))

# Set up figure
fig = plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines(color="lightgray", linewidth=0.8)  # optional: turn off for pure wind

# Streamplot (white lines)
strm = ax.streamplot(
    Lon, Lat, u, v,
    color="white",
    linewidth=1,
    transform=ccrs.PlateCarree(),
    density=2  # controls how many streamlines
)

# Dark background
ax.set_facecolor("black")

# Remove borders etc. for slide aesthetic
ax.outline_patch.set_visible(False)

plt.show()
