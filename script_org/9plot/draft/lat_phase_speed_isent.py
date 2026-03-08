# %%
import glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from src.data_helper.read_variable import read_prime

# %%

def read_dec(decade):
    wb_dir = "/scratch/m/m300883/MPI_GE_CMIP6/vsts_space_time_spectra_daily/r*i1p1f1/"

    wb_files = glob.glob(wb_dir)

    wb_data = xr.open_mfdataset(
        wb_files, combine="nested", parallel=True, concat_dim="ens"
    )
    wb_data = wb_data.mean(dim="ens")
    wb_data["decade"] = decade
    return wb_data.compute()


def calc_second_meridional_derivative(data, smooth=True):
    if smooth:
        data = data.rolling(lat=3, center=True).median().dropna("lat")

    r_earth = 6.371e6
    dlat_rad = np.deg2rad(data.lat.values[1] - data.lat.values[0])
    dy = r_earth * dlat_rad

    first_deriv = np.gradient(data.values, axis=1) / dy
    second_deriv = np.gradient(first_deriv, axis=1) / dy

    return xr.DataArray(
        second_deriv,
        coords=data.coords,
        dims=data.dims,
        attrs={"units": "1/m²", "long_name": "Second meridional derivative"},
    )


# %%
# Top-row data: transient eddy momentum flux in latitude-phase speed space
phase_speed_first = read_prime(
    decade=1850,
    var="upvp_isent_phase_speed_spectrum",
    name=None,
    model_dir="MPI_GE_CMIP6",
    suffix="",
)
phase_speed_last = read_prime(
    decade=2090,
    var="upvp_isent_phase_speed_spectrum",
    name=None,
    model_dir="MPI_GE_CMIP6",
    suffix="",
)

lats_phase = phase_speed_first["lat"].values
phase_speeds_2d = phase_speed_first["phase_speed_ms"].values
mid_lat_idx = len(lats_phase) // 2
phase_speeds_plot = phase_speeds_2d[mid_lat_idx, :]
phase_speeds_combined = np.concatenate([-phase_speeds_plot[::-1], phase_speeds_plot])

# average over ensemble and isentropic levels for a single latitude-phase speed map
p_cp_first = phase_speed_first["P_eastward"].mean(dim=("ens", "isentropic_level")).values
p_cn_first = phase_speed_first["P_westward"].mean(dim=("ens", "isentropic_level")).values
p_cp_last = phase_speed_last["P_eastward"].mean(dim=("ens", "isentropic_level")).values
p_cn_last = phase_speed_last["P_westward"].mean(dim=("ens", "isentropic_level")).values

p_combined_first = np.concatenate([p_cn_first[:, ::-1], p_cp_first], axis=1)
p_combined_last = np.concatenate([p_cn_last[:, ::-1], p_cp_last], axis=1)


# %%
# Bottom-row data: quasi-stationary eddy thermal feedback proxy in latitude-wavenumber space
vsts_1850 = read_dec(1850)
vsts_2090 = read_dec(2090)

vsts_1850_sum = vsts_1850.sum(dim="freq").isel(wavenumber=slice(1, None))
vsts_2090_sum = vsts_2090.sum(dim="freq").isel(wavenumber=slice(1, None))

vsts_1850_combined = vsts_1850_sum.K_p + vsts_1850_sum.K_n
vsts_2090_combined = vsts_2090_sum.K_p + vsts_2090_sum.K_n

feedback_1850 = calc_second_meridional_derivative(vsts_1850_combined).compute()
feedback_2090 = calc_second_meridional_derivative(vsts_2090_combined).compute()


# %%
# Combined 2x2 figure: columns = decades, rows = diagnostics
fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharey="row")

# Row 1: latitude vs phase speed (transient momentum flux)
levels_phase = np.arange(-1.2, 1.21, 0.1)
cf_phase_1850 = axes[0, 0].contourf(
    phase_speeds_combined,
    lats_phase,
    p_combined_first,
    levels=levels_phase,
    cmap="RdBu_r",
    extend="both",
)
cf_phase_2090 = axes[0, 1].contourf(
    phase_speeds_combined,
    lats_phase,
    p_combined_last,
    levels=levels_phase,
    cmap="RdBu_r",
    extend="both",
)

for ax in axes[0, :]:
    ax.axvline(0, color="gray", linestyle="--", linewidth=1.0, alpha=0.6)
    ax.set_xlim(-20, 30)
    ax.set_xlabel("Phase speed [m s$^{-1}$]")
    ax.grid(True, alpha=0.3)

axes[0, 0].set_ylabel("Latitude [°N]")
axes[0, 0].set_title("1850s transient momentum flux")
axes[0, 1].set_title("2090s transient momentum flux")

# Row 2: latitude vs wavenumber (quasi-stationary thermal feedback)
levels_feedback = np.arange(-5, 5.1, 1) * 1e-9
cf_fb_1850 = axes[1, 0].contourf(
    feedback_1850.lat,
    feedback_1850.wavenumber,
    feedback_1850.T,
    levels=levels_feedback,
    cmap="RdBu_r",
    extend="both",
)
cf_fb_2090 = axes[1, 1].contourf(
    feedback_2090.lat,
    feedback_2090.wavenumber,
    feedback_2090.T,
    levels=levels_feedback,
    cmap="RdBu_r",
    extend="both",
)

for ax in axes[1, :]:
    ax.set_ylim(2, 8)
    ax.set_xlabel("Latitude [°N]")
    ax.grid(True, alpha=0.3)

axes[1, 0].set_ylabel("Wavenumber")
axes[1, 0].set_title("1850s quasi-stationary thermal feedback")
axes[1, 1].set_title("2090s quasi-stationary thermal feedback")

# panel labels
for i, ax in enumerate(axes.flat):
    ax.text(
        -0.1,
        1.02,
        chr(97 + i),
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="bottom",
        ha="right",
    )

# one colorbar per row
cbar1 = fig.colorbar(
    cf_phase_1850,
    ax=axes[0, :],
    orientation="horizontal",
    fraction=0.06,
    pad=0.12,
)
cbar1.set_label("Transient eddy momentum flux power")

cbar2 = fig.colorbar(
    cf_fb_1850,
    ax=axes[1, :],
    orientation="horizontal",
    fraction=0.06,
    pad=0.2,
)
cbar2.set_label("Quasi-stationary eddy thermal-feedback proxy [1 m$^{-2}$]")

plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/lat_phase_speed_thermal_feedback_2x2.pdf",
    dpi=300,
    bbox_inches="tight",
)
plt.show()
# %%
