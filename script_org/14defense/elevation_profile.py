# %%
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# %%
# ----------------------------------------------------------
# 1. Load global topography data (ETOPO1)
# ----------------------------------------------------------
# Download from: https://www.ngdc.noaa.gov/mgg/global/relief/ETOPO1/
# File: ETOPO1_Ice_g_gmt4.grd (NetCDF format)
# Example path:
etopo_path = (
    "/work/mh0033/m300883/High_frequecy_flow/data/elevation/ETOPO1_Ice_g_gmt4.grd"
)

ds = xr.open_dataset(etopo_path)

# %%
# The dataset typically has coords 'x' (longitude), 'y' (latitude), 'z' (elevation)
lon = ds["x"].values
lat = ds["y"].values
elev = ds["z"]

# ----------------------------------------------------------
# 2. Extract elevation profile at 50°N
# ----------------------------------------------------------
target_lat = 50

# Find the nearest latitude index
lat_idx = np.abs(lat - target_lat).argmin()
profile = elev[lat_idx, :].values

# Restrict to longitudes spanning North America → Europe
lon_min, lon_max = -130, 30  # adjust if needed
mask = (lon >= lon_min) & (lon <= lon_max)

lon_profile = lon[mask]
elev_profile = profile[mask]
# %%
# Smooth the elevation profile using running mean (window size 10)
window = 101
elev_profile_smooth = np.convolve(elev_profile, np.ones(window) / window, mode="valid")
lon_profile_smooth = lon_profile[window // 2 : -(window // 2)]

# %%
# ----------------------------------------------------------
# 3. Plot
# ----------------------------------------------------------
plt.figure(figsize=(33 / 2.54, 10 / 2.54))  # width=33cm, height=10cm
plt.plot(lon_profile_smooth, elev_profile_smooth, color="steelblue", lw=1.5)
plt.axhline(0, color="k", lw=0.8)

plt.title("Elevation Profile at 50°N", fontsize=14)
plt.xlabel("Longitude (°)")
plt.ylabel("Elevation (m)")

# Mark approximate regions
plt.text(-110, 4000, "North America", ha="center", fontsize=10)
plt.text(-40, 4000, "North Atlantic", ha="center", fontsize=10)
plt.text(10, 4000, "Europe", ha="center", fontsize=10)

plt.grid(True, ls="--", alpha=0.5)
plt.tight_layout()
plt.show()


# %%
# 3. Plot
# ----------------------------------------------------------
plt.figure(figsize=(33 / 2.54, 12 / 2.54), facecolor="black")  # width=33cm, height=10cm
ax = plt.gca()
ax.set_facecolor("black")
plt.plot(lon_profile_smooth, elev_profile_smooth, color="white", lw=5)
plt.axis("off")
plt.tight_layout()
# plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/elevation_profile_50N.png", dpi=500, bbox_inches="tight", pad_inches=0.1, facecolor="black")
# %%
# -----------------------------------------------------------
# Visualize the elevation data as an image: higher = whiter, black background
# -----------------------------------------------------------
plt.figure(figsize=(12, 6), facecolor="black")
ax = plt.gca()
ax.set_facecolor("black")

# Normalize elevation for display: min = black, max = white
elev_img = elev.values
# Mask ocean (elevation <= 0)
elev_img_land = np.where(elev_img > -10, elev_img, np.nan)
# Optionally, clip to a reasonable range to enhance contrast
vmin_clip = -5000
vmax_clip = 5000
elev_img_land = np.clip(elev_img_land, vmin_clip, vmax_clip)

# Show image: only land (higher = whiter, ocean = transparent)
im = ax.imshow(
    elev_img_land,
    cmap="gray",
    origin="lower",
    extent=[lon.min(), lon.max(), lat.min(), lat.max()],
    vmin=vmin_clip,
    vmax=vmax_clip,
    aspect="auto",
)

# ax.set_xlabel("Longitude (°)", color="white")
# ax.set_ylabel("Latitude (°)", color="white")
# ax.set_title("Global Elevation (Land Only, Higher = Whiter)", color="white")
# ax.tick_params(colors="white")
# plt.tight_layout()
# plt.show()

# %%
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig = plt.figure(figsize=(12, 6.75))
ax = plt.axes(projection=ccrs.PlateCarree())

# Set background color to black
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

# Add continents in gray
# ax.add_feature(cfeature.LAND, facecolor="gray", edgecolor="none")
# Add coastlines in white
# ax.coastlines(color="gray", linewidth=1.0)

# plot the elevation data, only above 100 m
elev_img = elev.values
# Mask ocean (elevation <= 0)
elev_img_land = np.where(elev_img > 500, elev_img, np.nan)
# Optionally, clip to a reasonable range to enhance contrast
vmin_clip = 50
vmax_clip = 3000
elev_img_land = np.clip(elev_img_land, vmin_clip, vmax_clip)
# Show image: only land (higher = whiter, ocean = transparent)
im = ax.imshow(
    elev_img_land,
    cmap="gray",
    origin="lower",
    extent=[lon.min(), lon.max(), lat.min(), lat.max()],
    vmin=vmin_clip,
    vmax=vmax_clip,
    aspect="auto",
)

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
    Lon,
    Lat,
    u,
    v,
    color="white",
    linewidth=0.5,  # thinner lines
    transform=ccrs.PlateCarree(),
    density=4,  # more dense streamlines
)

# Dark background
ax.set_facecolor("black")

# Remove borders etc. for slide aesthetic
ax.outline_patch.set_visible(False)

plt.show()

# %%
