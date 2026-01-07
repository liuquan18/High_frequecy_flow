# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from src.data_helper.read_variable import read_prime
from src.dynamics.theta_on_pv import find_isentrope_at_pv
# %%
phase_speed_first = read_prime(
    decade=1850,
    var="upvp_isent_phase_speed_spectrum",
    name=None,
    model_dir="MPI_GE_CMIP6",
    suffix="",
)
# %%
phase_speed_last = read_prime(
    decade=2090,
    var="upvp_isent_phase_speed_spectrum",
    name=None,
    model_dir="MPI_GE_CMIP6",
    suffix="",
)


# %%
lats = phase_speed_first["lat"].values
phase_speeds_2d = phase_speed_first["phase_speed_ms"].values
P_cp_first = phase_speed_first["P_eastward"].mean(dim="ens").values
P_cn_first = phase_speed_first["P_westward"].mean(dim="ens").values

P_cp_last = phase_speed_last["P_eastward"].mean(dim="ens").values
P_cn_last = phase_speed_last["P_westward"].mean(dim="ens").values

# %%
# Use middle latitude for representative phase speeds
mid_lat_idx = len(lats) // 2
phase_speeds_plot = phase_speeds_2d[mid_lat_idx, :]
# %%
# %%
# Multi-panel plot for all isentropic levels
# Get isentropic levels from the data
isent_levels = phase_speed_first["isentropic_level"].values
n_levels = len(isent_levels)

# Create figure with 2 rows and n_levels columns
fig, axes = plt.subplots(2, n_levels, figsize=(2.5 * n_levels, 8), sharey=True)

# Get data dimensions
lats = phase_speed_first["lat"].values
phase_speeds_2d = phase_speed_first["phase_speed_ms"].values
mid_lat_idx = len(lats) // 2
phase_speeds_plot = phase_speeds_2d[mid_lat_idx, :]

# Combine positive and negative phase speeds
phase_speeds_combined = np.concatenate([-phase_speeds_plot[::-1], phase_speeds_plot])

# Define consistent contour levels
levels = np.arange(-1.21, 1.21, 0.1)
levels_line = levels[levels != 0]  # Remove zero level
levels_diff = np.arange(-0.3, 0.31, 0.03)
levels_diff = levels_diff[levels_diff != 0]

# Loop through each isentropic level
for i, isent_level in enumerate(isent_levels):
    # Extract data for this isentropic level
    P_cp_first_i = (
        phase_speed_first["P_eastward"]
        .sel(isentropic_level=isent_level)
        .mean(dim="ens")
        .values
    )
    P_cn_first_i = (
        phase_speed_first["P_westward"]
        .sel(isentropic_level=isent_level)
        .mean(dim="ens")
        .values
    )

    P_cp_last_i = (
        phase_speed_last["P_eastward"]
        .sel(isentropic_level=isent_level)
        .mean(dim="ens")
        .values
    )
    P_cn_last_i = (
        phase_speed_last["P_westward"]
        .sel(isentropic_level=isent_level)
        .mean(dim="ens")
        .values
    )

    # Combine eastward and westward
    P_combined_first = np.concatenate([P_cn_first_i[:, ::-1], P_cp_first_i], axis=1)
    P_combined_last = np.concatenate([P_cn_last_i[:, ::-1], P_cp_last_i], axis=1)

    # Row 1: First decade (1850s)
    cs1 = axes[0, i].contour(
        phase_speeds_combined,
        lats,
        P_combined_first,
        levels=levels_line,
        colors="black",
        linewidths=1.0,
    )
    axes[0, i].axvline(0, color="gray", linestyle="--", linewidth=1.0, alpha=0.5)
    axes[0, i].set_xlim(-20, 30)
    axes[0, i].grid(True, alpha=0.3)
    axes[0, i].set_title(f"{int(isent_level)} K", fontsize=11)

    if i == 0:
        axes[0, i].set_ylabel("Latitude (°N)", fontsize=11)

    # Row 2: Last decade (2090s)
    cs2 = axes[1, i].contour(
        phase_speeds_combined,
        lats,
        P_combined_last,
        levels=levels_line,
        colors="black",
        linewidths=1.0,
    )
    axes[1, i].axvline(0, color="gray", linestyle="--", linewidth=1.0, alpha=0.5)
    axes[1, i].set_xlim(-20, 30)
    axes[1, i].set_xlabel("Phase Speed (m/s)", fontsize=11)
    axes[1, i].grid(True, alpha=0.3)

    if i == 0:
        axes[1, i].set_ylabel("Latitude (°N)", fontsize=11)

# Add row labels on the left
fig.text(0.005, 0.75, "1850s", fontsize=13, fontweight="bold", rotation=90, va="center")
fig.text(0.005, 0.25, "2090s", fontsize=13, fontweight="bold", rotation=90, va="center")

plt.tight_layout(rect=[0.02, 0, 1, 1])
plt.show()
#%%
# %% Tropopause
pv_1850 = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0climatology/pv_1850.nc"
)
pv_2090 = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0climatology/pv_2090.nc"
)

pv_1850_zm = pv_1850.pv.mean(dim=("lon")) * 1e6
pv_2090_zm = pv_2090.pv.mean(dim=("lon")) * 1e6


trops_1850 = find_isentrope_at_pv(pv_1850_zm)
trops_2090 = find_isentrope_at_pv(pv_2090_zm)

# %%
# New plot: Average over phase speed range (-10, 20) m/s
# Plot isentropic level vs latitude

# Get dimensions
lats = phase_speed_first["lat"].values
isent_levels = phase_speed_first["isentropic_level"].values
phase_speeds_2d = phase_speed_first["phase_speed_ms"].values

# For each latitude, get phase speeds
mid_lat_idx = len(lats) // 2
phase_speeds_plot = phase_speeds_2d[mid_lat_idx, :]

# Create combined phase speed array (negative for westward, positive for eastward)
phase_speeds_combined = np.concatenate([-phase_speeds_plot[::-1], phase_speeds_plot])

# Find indices for phase speed range (-10, 20)
mask = (phase_speeds_combined >= -10) & (phase_speeds_combined <= 20)

# Initialize arrays for averaged power
P_avg_first = np.zeros((len(isent_levels), len(lats)))
P_avg_last = np.zeros((len(isent_levels), len(lats)))

# Loop through isentropic levels and average over phase speed range
for i, isent_level in enumerate(isent_levels):
    # Get power spectra for this isentropic level
    P_cp_first_i = (
        phase_speed_first["P_eastward"]
        .sel(isentropic_level=isent_level)
        .mean(dim="ens")
        .values
    )
    P_cn_first_i = (
        phase_speed_first["P_westward"]
        .sel(isentropic_level=isent_level)
        .mean(dim="ens")
        .values
    )

    P_cp_last_i = (
        phase_speed_last["P_eastward"]
        .sel(isentropic_level=isent_level)
        .mean(dim="ens")
        .values
    )
    P_cn_last_i = (
        phase_speed_last["P_westward"]
        .sel(isentropic_level=isent_level)
        .mean(dim="ens")
        .values
    )

    # Combine eastward and westward
    P_combined_first = np.concatenate([P_cn_first_i[:, ::-1], P_cp_first_i], axis=1)
    P_combined_last = np.concatenate([P_cn_last_i[:, ::-1], P_cp_last_i], axis=1)

    # Average over selected phase speed range
    P_avg_first[i, :] = P_combined_first[:, mask].mean(axis=1)
    P_avg_last[i, :] = P_combined_last[:, mask].mean(axis=1)

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))

# Define contour levels
levels_filled = np.arange(-0.4, 0.41, 0.05)
levels_line = np.arange(-0.4, 0.41, 0.05)
levels_line = levels_line[np.abs(levels_line) > 1e-10]  # Remove zero level

# Plot first decade as filled contours (colormap)
cs_filled = ax.contourf(
    lats, isent_levels, P_avg_first, levels=levels_filled, cmap="RdBu_r", extend="max"
)

# Plot last decade as line contours
cs_line = ax.contour(
    lats,
    isent_levels,
    P_avg_last,
    levels=levels_line,
    colors="black",
    linewidths=1.5,
    alpha=0.8,
)

# Add contour labels for last decade
ax.clabel(cs_line, inline=True, fontsize=9, fmt="%.2f")

# Labels and formatting
ax.set_xlabel("Latitude (°N)", fontsize=12)
ax.set_ylabel("Isentropic Level (K)", fontsize=12)
ax.set_title(
    "Phase Speed Power Averaged over (-10, 20) m/s\n1850s (filled) vs 2090s (blue contours)",
    fontsize=13,
)
ax.grid(True, alpha=0.3)

# Add colorbar
cbar = plt.colorbar(cs_filled, ax=ax, orientation="vertical", pad=0.02)
cbar.set_label("Power (1850s)", fontsize=11)

plt.tight_layout()
plt.savefig("phase_speed_lat_isent_averaged.png", dpi=300, bbox_inches="tight")
plt.show()

# %%
