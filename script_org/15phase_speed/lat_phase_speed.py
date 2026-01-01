#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from src.data_helper.read_variable import read_prime
# %%
phase_speed_first = read_prime(
    decade = 1850,
    var = 'phase_speed_spectrum',
    name = None,
    model_dir = 'MPI_GE_CMIP6',
    suffix = '',
) 
# %%
ua_first = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_monthly_ensmean/ua_monmean_ensmean_185005_185909.nc")
# %%
ua_first = ua_first['ua'].mean(dim='time').sel(plev = 25000).mean(dim = 'lon')
ua_first = ua_first.sel(lat=slice(0, 90))
# %%
lats = phase_speed_first['lat'].values
phase_speeds_2d = phase_speed_first['phase_speed_grid'].values
P_cp_avg = phase_speed_first['P_eastward'].mean(dim = 'ens').values
P_cn_avg = phase_speed_first['P_westward'].mean(dim = 'ens').values



# %%
# Use middle latitude for representative phase speeds
mid_lat_idx = len(lats) // 2
phase_speeds_plot = phase_speeds_2d[mid_lat_idx, :]

# Plot phase speed spectrum as a function of latitude
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Eastward (positive) phase speeds
cs1 = axes[0].contourf(
    phase_speeds_plot, lats, P_cp_avg, levels=20, cmap="YlOrRd", extend="max"
)
axes[0].set_xlabel("Phase Speed (m/s)", fontsize=12)
axes[0].set_ylabel("Latitude (°N)", fontsize=12)
axes[0].set_title("Eastward Phase Speed Spectrum", fontsize=14)
axes[0].set_xlim(0, phase_speeds_plot.max())
axes[0].grid(True, alpha=0.3)
plt.colorbar(cs1, ax=axes[0], label="Power")

# Westward (negative) phase speeds
cs2 = axes[1].contourf(
    -phase_speeds_plot, lats, P_cn_avg, levels=20, cmap="Blues", extend="max"
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
fig, ax = plt.subplots(figsize=(12, 6))

phase_speeds_combined = np.concatenate(
    [-phase_speeds_plot[::-1], phase_speeds_plot]
)
P_combined = np.concatenate([P_cn_avg[:, ::-1], P_cp_avg], axis=1)

cs = ax.contour(
    phase_speeds_combined, lats, P_combined, levels=20, colors = 'black'
)
ax.axvline(
    0, color="black", linestyle="--", linewidth=1.5, label="Zero phase speed"
)
ax.set_xlabel("Phase Speed (m/s)", fontsize=12)
ax.set_ylabel("Latitude (°N)", fontsize=12)
ax.set_title(
    f"Phase Speed Spectrum (u'v' cospectra, 250 hPa)",
    fontsize=14,
)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
plt.colorbar(cs, ax=ax, label="Power")
# plot the zonal wind profile
ua_first.plot(y = 'lat', ax = ax, color = 'k', linewidth = 2, label = 'Zonal Wind (250 hPa)')
ax.set_xlim(-20, 30)

plt.tight_layout()

# %%
