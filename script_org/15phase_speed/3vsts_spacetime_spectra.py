# %%
"""
Script 1: Compute space-time cross-spectra between u' and v'
Saves K_p and K_n for each year independently for parallel processing
"""
import numpy as np
import xarray as xr
from src.spectrum.phase_speed_spectral import calc_spacetime_cross_spec
from mpi4py import MPI
import sys
import os
import glob
import logging

logging.basicConfig(level=logging.INFO)

# %%
# Parse command line arguments (do this before MPI initialization)
node = sys.argv[1]
ens = int(node)
decade = sys.argv[2]

# %%
# Initialize MPI
comm = None
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
except Exception:
    logging.warning("::: Warning: Proceeding without mpi4py! :::")
    rank = 0
    size = 1

# %%
if rank == 0:
    logging.info(f"MPI rank {rank} of {size} initialized.")
    logging.info(f"Processing ensemble {ens} for decade {decade}.")

# %%
# Parameters
NFFT = 128  # FFT length

# %%
# Load data paths
vs_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/va_steady_daily/r{ens}i1p1f1/"
ts_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/theta_steady_daily/r{ens}i1p1f1/"
vs_files = glob.glob(vs_path + f"*{decade}*.nc")
ts_files = glob.glob(ts_path + f"*{decade}*.nc")

# %%
# Output path
output_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/vsts_space_time_spectra_daily/r{ens}i1p1f1/dec_{decade}/"
if rank == 0:
    os.makedirs(output_path, exist_ok=True)
if comm is not None:
    comm.Barrier()

# %%
# Get unique years and distribute across ranks
years = np.arange(int(decade), int(decade) + 10)
n_years = len(years)
years_per_rank = np.array_split(years, size)
my_years = years_per_rank[rank]

if rank == 0:
    print(f"    Total years: {n_years}, MPI size: {size}")
logging.info(f"Rank {rank}: Processing {len(my_years)} years: {my_years}")


# %%
def compute_spacetime_spectra_single_lat(up_lat, vp_lat):
    """
    Compute space-time cross-spectra for a single latitude.

    Parameters
    ----------
    up_lat : np.ndarray
        Zonal wind perturbation (time, lon)
    vp_lat : np.ndarray
        Meridional wind perturbation (time, lon)

    Returns
    -------
    K_p : np.ndarray
        Positive frequency spectra (freq, wavenumber)
    K_n : np.ndarray
        Negative frequency spectra (freq, wavenumber)
    """
    K_p, K_n, lon_freq, om = calc_spacetime_cross_spec(
        up_lat, vp_lat, dx=1, ts=1, NFFT=NFFT, smooth=1
    )
    return K_p, K_n


def vectorized_spacetime_spectra(up_data, vp_data):
    """
    Vectorized computation of space-time cross-spectra across all latitudes.

    Parameters
    ----------
    up_data : xr.DataArray
        Zonal wind perturbation (time, lat, lon)
    vp_data : xr.DataArray
        Meridional wind perturbation (time, lat, lon)

    Returns
    -------
    K_p_all : xr.DataArray
        Positive frequency spectra (lat, freq, wavenumber)
    K_n_all : xr.DataArray
        Negative frequency spectra (lat, freq, wavenumber)
    lon_freq : np.ndarray
        Wavenumber array
    om : np.ndarray
        Frequency array
    """
    # Compute for first latitude to get dimensions and coordinate arrays
    # Ensure we have 2D arrays (time, lon)
    test_up = up_data.isel(lat=0).values
    test_vp = vp_data.isel(lat=0).values

    # Verify shape is 2D
    if test_up.ndim != 2:
        raise ValueError(
            f"Expected 2D data (time, lon), got shape {test_up.shape} with {test_up.ndim} dimensions"
        )

    K_p_test, K_n_test, lon_freq, om = calc_spacetime_cross_spec(
        test_up, test_vp, dx=1, ts=1, NFFT=NFFT, smooth=1
    )

    # lon_freq from frequeny to wavenumber (cycles/degree to cycles/360degree)
    lon_freq = lon_freq * 360.0  # cycles/360degree

    n_freq = len(om)
    n_wavenumber = len(lon_freq)

    # Use apply_ufunc to vectorize over latitude (only returns K_p and K_n)
    result = xr.apply_ufunc(
        compute_spacetime_spectra_single_lat,
        up_data,
        vp_data,
        input_core_dims=[["time", "lon"], ["time", "lon"]],
        output_core_dims=[
            ["freq", "wavenumber"],
            ["freq", "wavenumber"],
        ],
        exclude_dims=set(["time", "lon"]),
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float, float],
        output_sizes={"freq": n_freq, "wavenumber": n_wavenumber},
    )

    K_p_all = result[0]
    K_n_all = result[1]

    # Assign coordinates to the output DataArrays
    K_p_all = K_p_all.assign_coords(freq=om, wavenumber=lon_freq)
    K_n_all = K_n_all.assign_coords(freq=om, wavenumber=lon_freq)

    return K_p_all, K_n_all


# %%
# Process each year assigned to this rank
for year_idx, year in enumerate(my_years):
    logging.info(
        f"     Rank {rank}: Processing year {year} ({year_idx+1}/{len(my_years)})"
    )

    # Load data for this year
    vs_file = glob.glob(vs_path + f"*{decade}*.nc")
    ts_file = glob.glob(ts_path + f"*{decade}*.nc")

    if len(vs_file) == 0 or len(ts_file) == 0:
        logging.warning(
            f"     Rank {rank}: No data files found for decade {decade}, skipping..."
        )
        continue

    logging.info(f"     Rank {rank}: Loading data for decade {decade}...")
    vs = xr.open_dataset(vs_file[0]).va
    ts = xr.open_dataset(ts_file[0]).theta

    vs = vs.sel(lat=slice(0, 90), plev=85000, time=vs.time.dt.year == int(year))
    ts = ts.sel(lat=slice(0, 90), plev=85000, time=ts.time.dt.year == int(year))

    # Compute space-time cross-spectra for all latitudes
    logging.info(f"     Rank {rank}: Computing spectra for year {year}...")
    K_p_da, K_n_da = vectorized_spacetime_spectra(vs, ts)

    # only keep the first 10 wavenumbers to reduce file size
    K_p_da = K_p_da.isel(wavenumber=slice(0, 10))
    K_n_da = K_n_da.isel(wavenumber=slice(0, 10))

    # Add attributes
    K_p_da.name = "K_positive"
    K_p_da.attrs = {
        "long_name": "Positive frequency cross-spectrum",
        "description": "v'theta' cross-spectrum for eastward propagating waves",
        "method": "Hayashi (1971) space-time cross-spectrum",
        "NFFT": NFFT,
        "units": "power",
        "year": int(year),
    }

    K_n_da.name = "K_negative"
    K_n_da.attrs = {
        "long_name": "Negative frequency cross-spectrum",
        "description": "v'theta' cross-spectrum for westward propagating waves",
        "method": "Hayashi (1971) space-time cross-spectrum",
        "NFFT": NFFT,
        "units": "power",
        "year": int(year),
    }

    # Combine into Dataset
    ds = xr.Dataset({"K_p": K_p_da, "K_n": K_n_da})

    # Add global attributes
    ds.attrs["title"] = "Space-time cross-spectra between v' and theta'"
    ds.attrs["source"] = f"MPI-ESM1-2-LR r{ens}i1p1f1"
    ds.attrs["decade"] = str(decade)
    ds.attrs["year"] = int(year)
    ds.attrs["frequency_filter"] = "2-8 day bandpass"

    # Add coordinate attributes
    ds["lat"].attrs["units"] = "degrees_north"
    ds["lat"].attrs["long_name"] = "Latitude"
    ds["freq"].attrs["units"] = "cycles/day"
    ds["freq"].attrs["long_name"] = "Frequency"
    ds["wavenumber"].attrs["units"] = "cycles/degree"
    ds["wavenumber"].attrs["long_name"] = "Zonal wavenumber"

    # Save to NetCDF (each rank saves independently)
    output_file = f"{output_path}spacetime_spectra_vtheta_{year}_r{ens}i1p1f1.nc"
    ds.to_netcdf(output_file)
    logging.info(f"     Rank {rank}: Saved {output_file}")

logging.info(f"Rank {rank}: All done!")
# %%
