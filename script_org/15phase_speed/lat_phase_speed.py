# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from src.data_helper.read_variable import read_prime

# %%
phase_speed_first = read_prime(
    decade=1850,
    var="phase_speed_spectrum",
    name=None,
    model_dir="MPI_GE_CMIP6",
    suffix="",
)
# %%
phase_speed_last = read_prime(
    decade=2090,
    var="phase_speed_spectrum",
    name=None,
    model_dir="MPI_GE_CMIP6",
    suffix="",
)
# %%
ua_first = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_monthly_ensmean/ua_monmean_ensmean_185005_185909.nc"
)
ua_first = ua_first["ua"].mean(dim="time").sel(plev=25000).mean(dim="lon")
ua_first = ua_first.sel(lat=slice(0, 90))
# %%
ua_last = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_monthly_ensmean/ua_monmean_ensmean_209005_209909.nc"
)
ua_last = ua_last["ua"].mean(dim="time").sel(plev=25000).mean(dim="lon")
ua_last = ua_last.sel(lat=slice(0, 90))


# %%
lats = phase_speed_first["lat"].values
phase_speeds_2d = phase_speed_first["phase_speed_grid"].values
P_cp_first = phase_speed_first["P_eastward"].mean(dim="ens").values
P_cn_first = phase_speed_first["P_westward"].mean(dim="ens").values

P_cp_last = phase_speed_last["P_eastward"].mean(dim="ens").values
P_cn_last = phase_speed_last["P_westward"].mean(dim="ens").values

# %%
# Use middle latitude for representative phase speeds
mid_lat_idx = len(lats) // 2
phase_speeds_plot = phase_speeds_2d[mid_lat_idx, :]

# Plot phase speed spectrum as a function of latitude
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Eastward (positive) phase speeds
cs1 = axes[0].contourf(
    phase_speeds_plot, lats, P_cp_first, levels=20, cmap="YlOrRd", extend="max"
)
axes[0].set_xlabel("Phase Speed (m/s)", fontsize=12)
axes[0].set_ylabel("Latitude (°N)", fontsize=12)
axes[0].set_title("Eastward Phase Speed Spectrum", fontsize=14)
axes[0].set_xlim(0, phase_speeds_plot.max())
axes[0].grid(True, alpha=0.3)
plt.colorbar(cs1, ax=axes[0], label="Power")

# Westward (negative) phase speeds
cs2 = axes[1].contourf(
    -phase_speeds_plot, lats, P_cn_first, levels=20, cmap="Blues", extend="max"
)
axes[1].set_xlabel("Phase Speed (m/s)", fontsize=12)
axes[1].set_ylabel("Latitude (°N)", fontsize=12)
axes[1].set_title("Westward Phase Speed Spectrum", fontsize=14)
axes[1].set_xlim(-phase_speeds_plot.max(), 0)
axes[1].grid(True, alpha=0.3)
plt.colorbar(cs2, ax=axes[1], label="Power")

plt.tight_layout()


# %%
# Combined plot
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

phase_speeds_combined = np.concatenate([-phase_speeds_plot[::-1], phase_speeds_plot])
P_combined_first = np.concatenate([P_cn_first[:, ::-1], P_cp_first], axis=1)
P_combined_last = np.concatenate([P_cn_last[:, ::-1], P_cp_last], axis=1)

# Define consistent levels excluding zero
levels = np.arange(-1.2, 1.21, 0.1)
levels_line = levels[levels != 0]  # Remove zero level

# First period plot
cs1 = axes[0].contour(
    phase_speeds_combined, lats, P_combined_first, levels=levels_line, colors="black"
)
axes[0].axvline(0, color="gray", linestyle="--", linewidth=1.5, alpha=0.5)
axes[0].set_xlabel("Phase Speed (m/s)", fontsize=12)
axes[0].set_ylabel("Latitude (°N)", fontsize=12)
axes[0].set_title(
    f"Phase Speed Spectrum (1850s)",
    fontsize=14,
)
axes[0].grid(True, alpha=0.3)
ua_first.plot(y="lat", ax=axes[0], color="k", linewidth=3, label="Zonal Wind (250 hPa)")
axes[0].set_xlim(-20, 30)

# Last period plot
cs2 = axes[1].contour(
    phase_speeds_combined, lats, P_combined_last, levels=levels, colors="black"
)
axes[1].axvline(0, color="gray", linestyle="--", linewidth=1.5, alpha=0.5)
axes[1].set_xlabel("Phase Speed (m/s)", fontsize=12)
axes[1].set_ylabel("Latitude (°N)", fontsize=12)
axes[1].set_title(
    f"Phase Speed Spectrum (2090s)",
    fontsize=14,
)
axes[1].grid(True, alpha=0.3)
ua_last.plot(y="lat", ax=axes[1], color="k", linewidth=3, label="Zonal Wind (250 hPa)")
axes[1].set_xlim(-20, 30)


plt.tight_layout()

# %%
# Combined single plot: first as colormap, last as contours + Difference plot
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

phase_speeds_combined = np.concatenate([-phase_speeds_plot[::-1], phase_speeds_plot])
P_combined_first = np.concatenate([P_cn_first[:, ::-1], P_cp_first], axis=1)
P_combined_last = np.concatenate([P_cn_last[:, ::-1], P_cp_last], axis=1)

# Define consistent levels excluding zero
levels = np.arange(-1.21, 1.21, 0.1)
levels_line = levels[levels != 0]  # Remove zero level

# Left plot: first as colormap, last as contours
cs_fill = axes[0].contourf(
    phase_speeds_combined,
    lats,
    P_combined_first,
    levels=levels,
    cmap="RdBu_r",
    extend="both",
)

cs_line = axes[0].contour(
    phase_speeds_combined,
    lats,
    P_combined_last,
    levels=levels,
    colors="black",
    linewidths=1.5,
)

axes[0].axvline(0, color="gray", linestyle="--", linewidth=1.5, alpha=0.5)
axes[0].set_xlabel("Phase Speed (m/s)", fontsize=12)
axes[0].set_ylabel("Latitude (°N)", fontsize=12)
axes[0].set_title(
    f"Phase Speed Spectrum: 1850s (shading) vs 2090s (contours)",
    fontsize=14,
)
axes[0].grid(True, alpha=0.3)

ua_first.plot(
    y="lat", ax=axes[0], color="k", linewidth=3, linestyle="-", label="Zonal Wind 1850s"
)
ua_last.plot(
    y="lat",
    ax=axes[0],
    color="k",
    linewidth=3,
    linestyle="--",
    label="Zonal Wind 2090s",
)
axes[0].set_xlim(-20, 30)
axes[0].legend(fontsize=10)

# Right plot: Difference
P_combined_diff = P_combined_last - P_combined_first

levels_diff = np.arange(-0.4, 0.41, 0.04)
levels_diff = levels_diff[levels_diff != 0]  # Remove zero level

cs_diff = axes[1].contourf(
    phase_speeds_combined,
    lats,
    P_combined_diff,
    levels=levels_diff,
    cmap="RdBu",
    extend="both",
)

axes[1].axvline(0, color="gray", linestyle="--", linewidth=1.5, alpha=0.5)
axes[1].set_xlabel("Phase Speed (m/s)", fontsize=12)
axes[1].set_ylabel("Latitude (°N)", fontsize=12)
axes[1].set_title(
    f"Phase Speed Spectrum Difference (2090s - 1850s)",
    fontsize=14,
)
axes[1].grid(True, alpha=0.3)

ua_diff = ua_last - ua_first
ua_diff.plot(y="lat", ax=axes[1], color="k", linewidth=3, label="Zonal Wind Change")
axes[1].set_xlim(-20, 30)
axes[1].legend(fontsize=10)

plt.colorbar(cs_fill, ax=axes[0], label="Power (1850s)")
plt.colorbar(cs_diff, ax=axes[1], label="Power Difference")
plt.tight_layout()

# %%
