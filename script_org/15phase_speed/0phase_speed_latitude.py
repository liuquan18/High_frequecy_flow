# %%
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from src.spectrum.phase_speed_spectral import (
    calc_spacetime_cross_spec,
    calPhaseSpeedSpectrum,
)
from mpi4py import MPI
import sys
import os
import glob
import logging

logging.basicConfig(level=logging.INFO)

# %%
# Initialize MPI

# %%
node = sys.argv[1]
ens = int(node)
decade = sys.argv[2]
logging.info(f"Processing ensemble {ens} for decade {decade}")
# %%
# %%
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # [0,1,2,3,4,5,6,7,8,9]
    size = comm.Get_size()  # 10
except:
    logging.warning("::: Warning: Proceeding without mpi4py! :::")
    rank = 0
    size = 1

# %%
# Load data
if rank == 0:
    logging.info("Loading data...")


upvp_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/upvp_daily/r{ens}i1p1f1/"
upvp_file = glob.glob(upvp_path + f"*{decade}.nc")
# %%
# save path
output_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/phase_speed_spectrum_daily/r{ens}i1p1f1/"
if rank == 0:
    if not os.path.exists(output_path):
        os.makedirs(output_path)
# %%
# Parameters
earth_radius = 6371000  # meters
deg_to_m = 2 * np.pi * earth_radius / 360  # meters per degree longitude at equator
cmax = 50  # maximum phase speed in grid units (deg/day)
nps = 50  # number of phase speed bins
NFFT = 128  # FFT length, total days 153, this gives two segments with 25% overlap
plev = 25000  # pressure level in Pa

# %%
upvp = xr.open_dataset(upvp_file[0]).upvp
upvp = upvp.sel(plev=plev, lat=slice(0, 90))
# Get unique years and distribute across ranks
years = np.unique(upvp.time.dt.year.values)
n_years = len(years)
years_per_rank = np.array_split(years, size)
my_years = years_per_rank[rank]

if rank == 0:
    print(f"Total years: {n_years}, MPI size: {size}")
    print(f"Rank {rank}: Processing {len(my_years)} years: {my_years}")


# %%
def process_single_latitude_year(upvp_lat, lat_value):
    """
    Process a single latitude for one year.

    Parameters
    ----------
    upvp_lat : np.ndarray
        Momentum flux time series (time, lon)
    lat_value : float
        Latitude value for phase speed conversion

    Returns
    -------
    P_cp : np.ndarray
        Positive phase speed spectrum (nps,)
    P_cn : np.ndarray
        Negative phase speed spectrum (nps,)
    """
    # Calculate space-time cross-spectra
    K_p, K_n, lon_freq, om = calc_spacetime_cross_spec(
        upvp_lat, upvp_lat, dx=1, ts=1, NFFT=NFFT, smooth=1
    )

    # Calculate phase speed spectrum
    P_cp, P_cn, C = calPhaseSpeedSpectrum(
        K_p, K_n, lon_freq, om, cmax=cmax, nps=nps, i1=1, i2=10
    ) # sum over i1 to i2 frequency bins, 1-10 to capture synoptic waves

    return P_cp, P_cn


def vectorized_phase_speed(upvp_data):
    """
    Vectorized computation across all latitudes using apply_ufunc.

    Parameters
    ----------
    upvp_data : xr.DataArray
        Momentum flux (time, lat, lon)

    Returns
    -------
    P_cp_all : xr.DataArray
        Positive phase speed spectra (lat, phase_speed)
    P_cn_all : xr.DataArray
        Negative phase speed spectra (lat, phase_speed)
    """
    n_lats = len(upvp_data.lat)

    # Initialize output arrays
    P_cp_all = np.zeros((n_lats, nps))
    P_cn_all = np.zeros((n_lats, nps))

    # Use apply_ufunc to vectorize over latitude dimension
    def compute_spectrum(upvp_vals):
        """Wrapper function for apply_ufunc"""
        P_cp, P_cn = process_single_latitude_year(
            upvp_vals, 0
        )  # lat_value not used in calculation
        return P_cp, P_cn

    result = xr.apply_ufunc(
        compute_spectrum,
        upvp_data,
        input_core_dims=[["time", "lon"]],  # Process each (time, lon) slice
        output_core_dims=[["phase_speed"], ["phase_speed"]],  # Output dimensions
        exclude_dims=set(["time", "lon"]),  # Dimensions being reduced
        vectorize=True,  # Apply function to each latitude separately
        dask="parallelized",  # Enable dask parallelization if data is chunked
        output_dtypes=[float, float],
        output_sizes={"phase_speed": nps},
    )

    P_cp_all = result[0]
    P_cn_all = result[1]

    return P_cp_all, P_cn_all


# %%
# Initialize arrays to store results for this rank
P_cp_rank = None
P_cn_rank = None

# Loop over years assigned to this rank
for year_idx, year in enumerate(my_years):
    print(f"Rank {rank}: Processing year {year} ({year_idx+1}/{len(my_years)})")

    # Calculate momentum flux
    upvp_year = upvp.sel(time=str(year))

    # Vectorized computation across all latitudes
    P_cp_year, P_cn_year = vectorized_phase_speed(upvp_year)

    # Accumulate for this rank's years
    if P_cp_rank is None:
        P_cp_rank = P_cp_year.values
        P_cn_rank = P_cn_year.values
    else:
        P_cp_rank += P_cp_year.values
        P_cn_rank += P_cn_year.values

# Average over years processed by this rank
if P_cp_rank is not None:
    P_cp_rank /= len(my_years)
    P_cn_rank /= len(my_years)

print(f"Rank {rank}: Completed processing {len(my_years)} years")

# %%
# Calculate phase speeds in physical units (only once at rank 0)
lats = upvp.lat.values
lat_factors = np.cos(np.deg2rad(lats))
C = np.linspace(0.0, cmax, nps)
phase_speeds_physical = (
    C * deg_to_m * lat_factors[:, np.newaxis] / (24 * 3600)
)  # (n_lat, nps)

# Gather results from all ranks to rank 0
P_cp_all = comm.gather(P_cp_rank, root=0)
P_cn_all = comm.gather(P_cn_rank, root=0)

# Rank 0 combines and plots
if rank == 0:
    print("\nRank 0: Combining results from all ranks...")

    # Filter out None values and average
    P_cp_all = [p for p in P_cp_all if p is not None]
    P_cn_all = [p for p in P_cn_all if p is not None]

    P_cp_avg = np.mean(P_cp_all, axis=0)
    P_cn_avg = np.mean(P_cn_all, axis=0)

    print(f"Rank 0: Averaged over {n_years} years. Creating datasets...")

    # Create xarray DataArrays for saving
    lats = upvp.lat.values
    C = np.linspace(0.0, cmax, nps)

    # Calculate phase speeds in physical units for each latitude
    lat_factors = np.cos(np.deg2rad(lats))
    deg_to_m = 2 * np.pi * 6371000 / 360
    phase_speeds_2d = (
        C[np.newaxis, :] * deg_to_m * lat_factors[:, np.newaxis] / (24 * 3600)
    )

    # Create DataArrays
    P_cp_da = xr.DataArray(
        P_cp_avg,
        coords={
            "lat": lats,
            "phase_speed_grid": (["lat", "ps_bin"], phase_speeds_2d),
            "ps_bin": np.arange(nps),
        },
        dims=["lat", "ps_bin"],
        name="eastward_phase_speed_power",
        attrs={
            "long_name": "Eastward phase speed power spectrum",
            "units": "power",
            "description": f"u'v' cospectra averaged over {n_years} years (1850-1859)",
            "level": "250 hPa",
            "method": "Hayashi (1971) space-time cross-spectrum",
            "cmax": cmax,
            "NFFT": NFFT,
        },
    )

    P_cn_da = xr.DataArray(
        P_cn_avg,
        coords={
            "lat": lats,
            "phase_speed_grid": (["lat", "ps_bin"], phase_speeds_2d),
            "ps_bin": np.arange(nps),
        },
        dims=["lat", "ps_bin"],
        name="westward_phase_speed_power",
        attrs={
            "long_name": "Westward phase speed power spectrum",
            "units": "power",
            "description": f"u'v' cospectra averaged over {n_years} years (1850-1859)",
            "level": "250 hPa",
            "method": "Hayashi (1971) space-time cross-spectrum",
            "cmax": cmax,
            "NFFT": NFFT,
        },
    )

    # Combine into a Dataset
    ds = xr.Dataset({"P_eastward": P_cp_da, "P_westward": P_cn_da})

    # Add global attributes
    ds.attrs["title"] = "Phase Speed Spectrum from u-v cospectra"
    ds.attrs["source"] = "MPI-ESM1-2-LR r1i1p1f1"
    ds.attrs["period"] = "1850-1859 (first10)"
    ds.attrs["pressure_level"] = "250 hPa"
    ds.attrs["frequency_filter"] = "2-8 day bandpass"

    # Save to NetCDF
    output_file = f"{output_path}phase_speed_upvp_cospectra_250hPa_{decade}.nc"
    ds.to_netcdf(output_file)
    print(f"Saved dataset to: {output_file}")


#     # %%
#     # Use middle latitude for representative phase speeds
#     mid_lat_idx = len(lats) // 2
#     phase_speeds_plot = phase_speeds_2d[mid_lat_idx, :]

#     # Plot phase speed spectrum as a function of latitude
#     fig, axes = plt.subplots(1, 2, figsize=(14, 6))

#     # Eastward (positive) phase speeds
#     cs1 = axes[0].contourf(
#         phase_speeds_plot, lats, P_cp_avg, levels=20, cmap="YlOrRd", extend="max"
#     )
#     axes[0].set_xlabel("Phase Speed (m/s)", fontsize=12)
#     axes[0].set_ylabel("Latitude (°N)", fontsize=12)
#     axes[0].set_title("Eastward Phase Speed Spectrum", fontsize=14)
#     axes[0].set_xlim(0, phase_speeds_plot.max())
#     axes[0].grid(True, alpha=0.3)
#     plt.colorbar(cs1, ax=axes[0], label="Power")

#     # Westward (negative) phase speeds
#     cs2 = axes[1].contourf(
#         -phase_speeds_plot, lats, P_cn_avg, levels=20, cmap="Blues", extend="max"
#     )
#     axes[1].set_xlabel("Phase Speed (m/s)", fontsize=12)
#     axes[1].set_ylabel("Latitude (°N)", fontsize=12)
#     axes[1].set_title("Westward Phase Speed Spectrum", fontsize=14)
#     axes[1].set_xlim(-phase_speeds_plot.max(), 0)
#     axes[1].grid(True, alpha=0.3)
#     plt.colorbar(cs2, ax=axes[1], label="Power")

#     plt.tight_layout()
#     plt.savefig("phase_speed_eastward_westward.png", dpi=300, bbox_inches="tight")
#     print("Saved: phase_speed_eastward_westward.png")
#     plt.close()

#     # %%
#     # Combined plot
#     fig, ax = plt.subplots(figsize=(12, 6))

#     phase_speeds_combined = np.concatenate(
#         [-phase_speeds_plot[::-1], phase_speeds_plot]
#     )
#     P_combined = np.concatenate([P_cn_avg[:, ::-1], P_cp_avg], axis=1)

#     cs = ax.contourf(
#         phase_speeds_combined, lats, P_combined, levels=20, cmap="RdBu_r", extend="max"
#     )
#     ax.axvline(
#         0, color="black", linestyle="--", linewidth=1.5, label="Zero phase speed"
#     )
#     ax.set_xlabel("Phase Speed (m/s)", fontsize=12)
#     ax.set_ylabel("Latitude (°N)", fontsize=12)
#     ax.set_title(
#         f"Phase Speed Spectrum (u'v' cospectra, 250 hPa, {n_years} years avg)",
#         fontsize=14,
#     )
#     ax.grid(True, alpha=0.3)
#     ax.legend(fontsize=10)
#     plt.colorbar(cs, ax=ax, label="Power")

#     plt.tight_layout()
#     plt.savefig("phase_speed_combined.png", dpi=300, bbox_inches="tight")
#     print("Saved: phase_speed_combined.png")
#     plt.close()

#     print("All done!")

# # %%

# %%
