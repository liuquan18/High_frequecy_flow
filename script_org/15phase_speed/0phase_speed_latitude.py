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

var1 = "ua_prime"
var2 = "va_prime"
var_out = "upvp_phase_speed_spectrum"
# %%

up_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/{var1}_daily/r{ens}i1p1f1/"
vp_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/{var2}_daily/r{ens}i1p1f1/"
up_files = glob.glob(up_path + f"*{decade}*.nc")
vp_files = glob.glob(vp_path + f"*{decade}*.nc")
# %%
# save path
output_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var_out}/r{ens}i1p1f1/"
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
up = xr.open_dataset(up_files[0]).ua
vp = xr.open_dataset(vp_files[0]).va
up = up.sel(plev=plev, lat=slice(0, 90))
vp = vp.sel(plev=plev, lat=slice(0, 90))
# Get unique years and distribute across ranks
years = np.unique(up.time.dt.year.values)
n_years = len(years)
years_per_rank = np.array_split(years, size)
my_years = years_per_rank[rank]

if rank == 0:
    print(f"Total years: {n_years}, MPI size: {size}")
    print(f"Rank {rank}: Processing {len(my_years)} years: {my_years}")


# %%
def process_single_latitude_year(up_lat, vp_lat):
    """
    Process a single latitude for one year - calculate cross-spectra between up and vp.

    Parameters
    ----------
    up_lat : np.ndarray
        Zonal wind perturbation time series (time, lon)
    vp_lat : np.ndarray
        Meridional wind perturbation time series (time, lon)

    Returns
    -------
    P_cp : np.ndarray
        Positive phase speed spectrum (nps,)
    P_cn : np.ndarray
        Negative phase speed spectrum (nps,)
    """
    # Calculate space-time cross-spectra between up and vp
    K_p, K_n, lon_freq, om = calc_spacetime_cross_spec(
        up_lat, vp_lat, dx=1, ts=1, NFFT=NFFT, smooth=1
    )

    # Calculate phase speed spectrum
    P_cp, P_cn, C = calPhaseSpeedSpectrum(
        K_p, K_n, lon_freq, om, cmax=cmax, nps=nps, i1=1, i2=6
    )  # sum over i1 to i2 frequency bins, 1-10 to capture synoptic waves, the sixth corresponds to wavenumber 0.03125*360=11.25  

    return P_cp, P_cn


def vectorized_phase_speed(up_data, vp_data):
    """
    Vectorized computation of cross-spectra across all latitudes using apply_ufunc.

    Parameters
    ----------
    up_data : xr.DataArray
        Zonal wind perturbation (time, lat, lon)
    vp_data : xr.DataArray
        Meridional wind perturbation (time, lat, lon)

    Returns
    -------
    P_cp_all : xr.DataArray
        Positive phase speed spectra (lat, phase_speed)
    P_cn_all : xr.DataArray
        Negative phase speed spectra (lat, phase_speed)
    """

    # Use apply_ufunc to vectorize over latitude dimension
    def compute_cross_spectrum(up_vals, vp_vals):
        """Wrapper function for apply_ufunc - computes cross-spectrum"""
        P_cp, P_cn = process_single_latitude_year(up_vals, vp_vals)
        return P_cp, P_cn

    result = xr.apply_ufunc(
        compute_cross_spectrum,
        up_data,
        vp_data,
        input_core_dims=[
            ["time", "lon"],
            ["time", "lon"],
        ],  # Process each (time, lon) slice
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

    # Select data for this year
    up_year = up.sel(time=str(year))
    vp_year = vp.sel(time=str(year))

    # Vectorized computation of cross-spectra across all latitudes
    P_cp_year, P_cn_year = vectorized_phase_speed(up_year, vp_year)

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
lats = up.lat.values
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
    lats = up.lat.values
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
            "description": f"u'v' cospectra averaged over {n_years} years",
            "level": f"{plev/100:.0f} hPa",
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
            "description": f"u'v' cospectra averaged over {n_years} years",
            "level": f"{plev/100:.0f} hPa",
            "method": "Hayashi (1971) space-time cross-spectrum",
            "cmax": cmax,
            "NFFT": NFFT,
        },
    )

    # Combine into a Dataset
    ds = xr.Dataset({"P_eastward": P_cp_da, "P_westward": P_cn_da})

    # Add global attributes
    ds.attrs["title"] = "Phase Speed Spectrum from u'v' cospectra"
    ds.attrs["source"] = f"MPI-ESM1-2-LR r{ens}i1p1f1"
    ds.attrs["decade"] = str(decade)
    ds.attrs["pressure_level"] = f"{plev/100:.0f} hPa"
    ds.attrs["frequency_filter"] = "2-8 day bandpass"

    # Save to NetCDF
    output_file = f"{output_path}phase_speed_upvp_cospectra_{plev/100:.0f}hPa_{decade}_r{ens}i1p1f1.nc"
    ds.to_netcdf(output_file)
    print(f"Saved dataset to: {output_file}")

    # %%
    # # Create latitude-phase speed plot
    # print("Creating latitude-phase speed plot...")
    # fig = plot_latitude_phasespeed(P_cp_avg, P_cn_avg, phase_speeds_2d, lats)
    # fig.savefig(
    #     f"{output_path}latitude_phasespeed_{plev/100:.0f}hPa_{decade}_r{ens}i1p1f1.png",
    #     dpi=300,
    #     bbox_inches="tight",
    # )
    # print(f"Saved latitude-phase speed plot")
    # plt.close(fig)

    # print("All done!")

# %%
