# %%
import numpy as np
import xarray as xr
import glob
import matplotlib.pyplot as plt
import tqdm
from metpy.calc import first_derivative
from metpy.units import units

# %%
base_dir = "/scratch/m/m300883/MPI_GE_CMIP6/vsts_space_time_spectra_daily/"


# %%
def dec_mean(ens, decade):
    wb_dir = f"{base_dir}r{ens}i1p1f1/dec_{decade}/*.nc"
    wb_files = glob.glob(wb_dir)

    wb_data = xr.open_mfdataset(
        wb_files, combine="nested", parallel=True, concat_dim="year"
    )
    wb_data = wb_data.mean(dim="year")
    save_dir = (
        f"/scratch/m/m300883/MPI_GE_CMIP6/vsts_space_time_spectra_daily/r{ens}i1p1f1/"
    )
    wb_data["ens"] = ens
    wb_data.to_netcdf(f"{save_dir}vsts_kp_kn_dec_{decade}_r{ens}i1p1f1.nc")


# %%
# for ens in tqdm.tqdm(range(1, 51)):
#     dec_mean(ens, 1850)
#     dec_mean(ens, 2090)
# %%
def read_dec(decade):
    wb_dir = f"{base_dir}r*i1p1f1/vsts_kp_kn_dec_{decade}_r*i1p1f1.nc"
    wb_files = glob.glob(wb_dir)

    wb_data = xr.open_mfdataset(
        wb_files, combine="nested", parallel=True, concat_dim="ens"
    )
    wb_data = wb_data.mean(dim="ens")
    wb_data["decade"] = decade
    return wb_data.compute()


# %%
vsts_1850 = read_dec(1850)
vsts_2090 = read_dec(2090)

# %%
vsts_1850_sum = vsts_1850.sum(dim="freq")
vsts_2090_sum = vsts_2090.sum(dim="freq")
#%%
vsts_1850_sum = vsts_1850_sum.isel(wavenumber=slice(1, None))
vsts_2090_sum = vsts_2090_sum.isel(wavenumber=slice(1, None))

# %%
# Combine K_p (eastward) and K_n (westward) for cospectra
vsts_1850_combined = vsts_1850_sum.K_p + vsts_1850_sum.K_n
vsts_2090_combined = vsts_2090_sum.K_p + vsts_2090_sum.K_n
vsts_diff = vsts_2090_combined - vsts_1850_combined

# %%
# Plot cospectra: latitude vs wavenumber
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

# 1850 plot
im1 = axes[0].contourf(
    vsts_1850_combined.lat,
    vsts_1850_combined.wavenumber,
    vsts_1850_combined.T,
    levels=20,
    cmap="RdBu_r",
    extend="both",
)
axes[0].set_xlabel("Latitude (°N)", fontsize=12)
axes[0].set_ylabel("Wavenumber", fontsize=12)
axes[0].set_title("1850s v-t Cospectra", fontsize=14, fontweight="bold")
axes[0].grid(True, alpha=0.3)
plt.colorbar(im1, ax=axes[0], label="Power")

# 2090 plot
im2 = axes[1].contourf(
    vsts_2090_combined.lat,
    vsts_2090_combined.wavenumber,
    vsts_2090_combined.T,
    levels=20,
    cmap="RdBu_r",
    extend="both",
)
axes[1].set_xlabel("Latitude (°N)", fontsize=12)
axes[1].set_title("2090s v-t Cospectra", fontsize=14, fontweight="bold")
axes[1].grid(True, alpha=0.3)
plt.colorbar(im2, ax=axes[1], label="Power")

# Difference plot (2090 - 1850)
im3 = axes[2].contourf(
    vsts_diff.lat,
    vsts_diff.wavenumber,
    vsts_diff.T,
    levels=20,
    cmap="RdBu_r",
    extend="both",
)
axes[2].set_xlabel("Latitude (°N)", fontsize=12)
axes[2].set_title("Change (2090s - 1850s)", fontsize=14, fontweight="bold")
axes[2].grid(True, alpha=0.3)
for ax in axes:
    ax.set_ylim(2, 8)
plt.colorbar(im3, ax=axes[2], label="Power Difference")

plt.tight_layout()
plt.savefig("vsts_cospectra_lat_wavenumber_combined.png", dpi=300, bbox_inches="tight")
plt.show()


# %%
# Calculate meridional derivative using metpy
# Need to add units and then compute derivative
def calc_meridional_derivative(data):
    """
    Calculate meridional derivative using metpy to get physical units (1/m).

    Parameters
    ----------
    data : xr.DataArray
        Data with latitude dimension

    Returns
    -------
    derivative : xr.DataArray
        Meridional derivative in physical units (1/m)
    """
    # Earth radius in meters
    R_earth = 6.371e6  # meters

    # Convert latitude to radians for physical distance calculation
    lat_rad = np.deg2rad(data.lat.values)

    # Calculate dy in meters (R_earth * d(lat_rad))
    # For uniform latitude grid, dy is constant
    dlat_rad = np.deg2rad(data.lat.values[1] - data.lat.values[0])
    dy = R_earth * dlat_rad  # meters

    # Calculate derivative using numpy gradient
    # This gives d(data)/d(lat_index), then divide by dy to get d(data)/dy
    deriv_array = np.gradient(data.values, axis=1) / dy  # 1/m

    # Create new DataArray with same coordinates
    deriv_da = xr.DataArray(
        deriv_array,
        coords=data.coords,
        dims=data.dims,
        attrs={"units": "1/m", "long_name": "Meridional derivative"},
    )

    return deriv_da


# Calculate meridional derivatives
vsts_1850_deriv = calc_meridional_derivative(vsts_1850_combined)
vsts_2090_deriv = calc_meridional_derivative(vsts_2090_combined)

#%%
# convergence of derivative
vsts_1850_deriv = vsts_1850_deriv.compute()
vsts_2090_deriv = vsts_2090_deriv.compute()
vsts_diff_deriv = vsts_2090_deriv - vsts_1850_deriv

# %%
# Plot meridional derivatives: latitude vs wavenumber
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

levels = np.arange(-1.5, 1.6, 0.3)*1e-3


# 1850 derivative plot
im1 = axes[0].contourf(
    vsts_1850_deriv.lat,
    vsts_1850_deriv.wavenumber,
    vsts_1850_deriv.T,
    levels=levels,
    cmap="RdBu_r",
    extend="both",
)
axes[0].set_xlabel("Latitude (°N)", fontsize=12)
axes[0].set_ylabel("Wavenumber", fontsize=12)
axes[0].set_title("1850s ∂(v-t Cospectra)/∂y", fontsize=14, fontweight="bold")
axes[0].grid(True, alpha=0.3)
plt.colorbar(im1, ax=axes[0], label="∂Power/∂y (1/m)")

# 2090 derivative plot
im2 = axes[1].contourf(
    vsts_2090_deriv.lat,
    vsts_2090_deriv.wavenumber,
    vsts_2090_deriv.T,
    levels=levels,
    cmap="RdBu_r",
    extend="both",
)
axes[1].set_xlabel("Latitude (°N)", fontsize=12)
axes[1].set_title("2090s ∂(v-t Cospectra)/∂y", fontsize=14, fontweight="bold")
axes[1].grid(True, alpha=0.3)
plt.colorbar(im2, ax=axes[1], label="∂Power/∂y (1/m)")

# Difference derivative plot (2090 - 1850)
im3 = axes[2].contourf(
    vsts_diff_deriv.lat,
    vsts_diff_deriv.wavenumber,
    vsts_diff_deriv.T,
    levels=levels/3,
    cmap="RdBu_r",
    extend="both",
)
axes[2].set_xlabel("Latitude (°N)", fontsize=12)
axes[2].set_title("Change in ∂/∂y (2090s - 1850s)", fontsize=14, fontweight="bold")
axes[2].grid(True, alpha=0.3)
for ax in axes:
    ax.set_ylim(2, 8)
plt.colorbar(im3, ax=axes[2], label="∂Power/∂y Difference (1/m)")

plt.tight_layout()
plt.savefig("vsts_cospectra_meridional_derivative.png", dpi=300, bbox_inches="tight")
plt.show()

# %%
# New plot: 1850s derivative as colormap, 2090s derivative as contour lines
fig, ax = plt.subplots(1, 1, figsize=(10, 6))

# Plot 1850s as filled contours (colormap)
im = ax.contourf(
    vsts_1850_deriv.lat,
    vsts_1850_deriv.wavenumber,
    vsts_1850_deriv.T,
    levels=20,
    cmap="RdBu_r",
    extend="both",
    alpha=0.8
)

# Overlay 2090s as contour lines
contours = ax.contour(
    vsts_2090_deriv.lat,
    vsts_2090_deriv.wavenumber,
    vsts_2090_deriv.T,
    levels=15,
    colors='black',
    linewidths=1.5,
    alpha=0.7
)

# Add contour labels
ax.clabel(contours, inline=True, fontsize=8, fmt='%.1e')

# Formatting
ax.set_xlabel("Latitude (°N)", fontsize=13)
ax.set_ylabel("Wavenumber", fontsize=13)
ax.set_title("∂(v-t Cospectra)/∂y: 1850s (colormap) vs 2090s (contours)", 
             fontsize=14, fontweight="bold")
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_ylim(2, 8)

# Colorbar
cbar = plt.colorbar(im, ax=ax, label="∂Power/∂y (1/m) - 1850s")
cbar.set_label("∂Power/∂y (1/m) - 1850s", fontsize=12)

# Add legend for contours
from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], color='black', linewidth=1.5, label='2090s contours')]
ax.legend(handles=legend_elements, loc='upper right', fontsize=11)

plt.tight_layout()
plt.savefig("vsts_cospectra_derivative_overlay.png", dpi=300, bbox_inches="tight")
plt.show()

# %%
# %%
# Calculate second meridional derivative
def calc_second_meridional_derivative(data, smooth=True):
    """
    Calculate second meridional derivative using metpy to get physical units (1/m²).

    Parameters
    ----------
    data : xr.DataArray
        Data with latitude dimension

    Returns
    -------
    second_derivative : xr.DataArray
        Second meridional derivative in physical units (1/m²)
    """
    # do meridional smooth by median filter if needed
    if smooth:
        data = data.rolling(lat=3, center=True).median().dropna("lat")

    # Earth radius in meters
    R_earth = 6.371e6  # meters

    # Convert latitude to radians for physical distance calculation
    lat_rad = np.deg2rad(data.lat.values)

    # Calculate dy in meters (R_earth * d(lat_rad))
    # For uniform latitude grid, dy is constant
    dlat_rad = np.deg2rad(data.lat.values[1] - data.lat.values[0])
    dy = R_earth * dlat_rad  # meters

    # Calculate second derivative: d²/dy² = d/dy(d/dy)
    # First derivative
    first_deriv = np.gradient(data.values, axis=1) / dy
    # Second derivative
    second_deriv = np.gradient(first_deriv, axis=1) / dy  # 1/m²

    # Create new DataArray with same coordinates
    second_deriv_da = xr.DataArray(
        second_deriv,
        coords=data.coords,
        dims=data.dims,
        attrs={"units": "1/m²", "long_name": "Second meridional derivative"},
    )

    return second_deriv_da


# Calculate second meridional derivatives
vsts_1850_deriv2 = calc_second_meridional_derivative(vsts_1850_combined)
vsts_2090_deriv2 = calc_second_meridional_derivative(vsts_2090_combined)

# %%
# Compute and calculate difference
vsts_1850_deriv2 = vsts_1850_deriv2.compute()
vsts_2090_deriv2 = vsts_2090_deriv2.compute()
vsts_diff_deriv2 = vsts_2090_deriv2 - vsts_1850_deriv2

# %%
# Plot second meridional derivatives: latitude vs wavenumber
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

levels2 = np.arange(-5, 5.1, 1) * 1e-9

# 1850 second derivative plot
im1 = axes[0].contourf(
    vsts_1850_deriv2.lat,
    vsts_1850_deriv2.wavenumber,
    vsts_1850_deriv2.T,
    levels=levels2,
    cmap="RdBu_r",
    extend="both",
)
axes[0].set_xlabel("Latitude (°N)", fontsize=12)
axes[0].set_ylabel("Wavenumber", fontsize=12)
axes[0].set_title("1850s ∂²(v-t Cospectra)/∂y²", fontsize=14, fontweight="bold")
axes[0].grid(True, alpha=0.3)
plt.colorbar(im1, ax=axes[0], label="∂²Power/∂y² (1/m²)")

# 2090 second derivative plot
im2 = axes[1].contourf(
    vsts_2090_deriv2.lat,
    vsts_2090_deriv2.wavenumber,
    vsts_2090_deriv2.T,
    levels=levels2,
    cmap="RdBu_r",
    extend="both",
)
axes[1].set_xlabel("Latitude (°N)", fontsize=12)
axes[1].set_title("2090s ∂²(v-t Cospectra)/∂y²", fontsize=14, fontweight="bold")
axes[1].grid(True, alpha=0.3)
plt.colorbar(im2, ax=axes[1], label="∂²Power/∂y² (1/m²)")

# Difference second derivative plot (2090 - 1850)
im3 = axes[2].contourf(
    vsts_diff_deriv2.lat,
    vsts_diff_deriv2.wavenumber,
    vsts_diff_deriv2.T,
    levels=levels2 / 3,
    cmap="RdBu_r",
    extend="both",
)
axes[2].set_xlabel("Latitude (°N)", fontsize=12)
axes[2].set_title("Change in ∂²/∂y² (2090s - 1850s)", fontsize=14, fontweight="bold")
axes[2].grid(True, alpha=0.3)
for ax in axes:
    ax.set_ylim(2, 8)
plt.colorbar(im3, ax=axes[2], label="∂²Power/∂y² Difference (1/m²)")

plt.tight_layout()
plt.savefig("vsts_cospectra_second_derivative.png", dpi=300, bbox_inches="tight")
plt.show()

# %%
# Overlay plot: 1850s second derivative as colormap, 2090s as contour lines
fig, ax = plt.subplots(1, 1, figsize=(10, 6))

# Plot 1850s as filled contours (colormap)
im = ax.contourf(
    vsts_1850_deriv2.lat,
    vsts_1850_deriv2.wavenumber,
    vsts_1850_deriv2.T,
    levels=20,
    cmap="RdBu_r",
    extend="both",
    alpha=0.8,
)

# Overlay 2090s as contour lines
contours = ax.contour(
    vsts_2090_deriv2.lat,
    vsts_2090_deriv2.wavenumber,
    vsts_2090_deriv2.T,
    levels=15,
    colors="black",
    linewidths=1.5,
    alpha=0.7,
)

# Add contour labels
ax.clabel(contours, inline=True, fontsize=8, fmt="%.1e")

# Formatting
ax.set_xlabel("Latitude (°N)", fontsize=13)
ax.set_ylabel("Wavenumber", fontsize=13)
ax.set_title(
    "∂²(v-t Cospectra)/∂y²: 1850s (colormap) vs 2090s (contours)",
    fontsize=14,
    fontweight="bold",
)
ax.grid(True, alpha=0.3, linestyle="--")
ax.set_ylim(2, 8)

# Colorbar
cbar = plt.colorbar(im, ax=ax, label="∂²Power/∂y² (1/m²) - 1850s")
cbar.set_label("∂²Power/∂y² (1/m²) - 1850s", fontsize=12)

# Add legend for contours
legend_elements = [
    Line2D([0], [0], color="black", linewidth=1.5, label="2090s contours")
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=11)

plt.tight_layout()
plt.savefig("vsts_cospectra_second_derivative_overlay.png", dpi=300, bbox_inches="tight")
plt.show()

# %%