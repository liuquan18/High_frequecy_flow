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
# Initialize MPI
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
except:
    logging.warning("::: Warning: Proceeding without mpi4py! :::")
    rank = 0
    size = 1

# %%
# Parse command line arguments
node = sys.argv[1]
ens = int(node)
decade = sys.argv[2]

# %%
if rank == 0:
    logging.info(f"MPI rank {rank} of {size} initialized.")
    logging.info(f"Processing ensemble {ens} for decade {decade}")
    logging.info("Computing space-time cross-spectra...")

# %%
# Parameters
NFFT = 128  # FFT length
plev = 25000  # pressure level in Pa

# %%
# Load data paths
up_path = f"/scratch/m/m300883/ua_prime_isentropic_daily/r{ens}i1p1f1/"
vp_path = f"/scratch/m/m300883/va_prime_isentropic_daily/r{ens}i1p1f1/"
up_files = glob.glob(up_path + f"*{decade}*.nc")
vp_files = glob.glob(vp_path + f"*{decade}*.nc")

# %%
# Output path
output_path = (
    f"/scratch/m/m300883/upvp_space_time_spectra_daily/r{ens}i1p1f1/dec_{decade}/"
)
if rank == 0:
    if not os.path.exists(output_path):
        os.makedirs(output_path)

# %%
# Load data
up = xr.open_dataset(up_files[0]).__xarray_dataarray_variable__
vp = xr.open_dataset(vp_files[0]).__xarray_dataarray_variable__
up.name = "ua"
vp.name = "va"
up = up.sel(lat=slice(0, 90))
vp = vp.sel(lat=slice(0, 90))

# Get unique years and distribute across ranks
years = np.unique(up.time.dt.year.values)
n_years = len(years)
years_per_rank = np.array_split(years, size)
my_years = years_per_rank[rank]

if rank == 0:
    print(f"Total years: {n_years}, MPI size: {size}")
print(f"Rank {rank}: Processing {len(my_years)} years: {my_years}")


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
    lon_freq : np.ndarray
        Wavenumber array
    om : np.ndarray
        Frequency array
    """
    K_p, K_n, lon_freq, om = calc_spacetime_cross_spec(
        up_lat, vp_lat, dx=1, ts=1, NFFT=NFFT, smooth=1
    )
    return K_p, K_n, lon_freq, om


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
    # Compute for first latitude to get dimensions
    test_up = up_data.isel(lat=0).values
    test_vp = vp_data.isel(lat=0).values
    K_p_test, K_n_test, lon_freq, om = compute_spacetime_spectra_single_lat(
        test_up, test_vp
    )
    n_freq = len(om)
    n_wavenumber = len(lon_freq)

    # Use apply_ufunc to vectorize over latitude
    result = xr.apply_ufunc(
        compute_spacetime_spectra_single_lat,
        up_data,
        vp_data,
        input_core_dims=[["time", "lon"], ["time", "lon"]],
        output_core_dims=[
            ["freq", "wavenumber"],
            ["freq", "wavenumber"],
            ["wavenumber"],
            ["freq"],
        ],
        exclude_dims=set(["time", "lon"]),
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float, float, float, float],
        output_sizes={"freq": n_freq, "wavenumber": n_wavenumber},
    )

    K_p_all = result[0]
    K_n_all = result[1]

    return K_p_all, K_n_all, lon_freq, om


# %%
# Process each year assigned to this rank
for year_idx, year in enumerate(my_years):
    print(f"Rank {rank}: Processing year {year} ({year_idx+1}/{len(my_years)})")

    # Select data for this year
    up_year = up.sel(time=str(year))
    vp_year = vp.sel(time=str(year))

    # Compute space-time cross-spectra
    K_p_year, K_n_year, lon_freq, om = vectorized_spacetime_spectra(up_year, vp_year)

    # Get latitude values
    lats = up_year.lat.values

    # Create DataArrays with proper coordinates
    K_p_da = xr.DataArray(
        K_p_year.values,
        coords={
            "lat": lats,
            "freq": om,
            "wavenumber": lon_freq,
        },
        dims=["lat", "freq", "wavenumber"],
        name="K_positive",
        attrs={
            "long_name": "Positive frequency cross-spectrum",
            "description": "u'v' cross-spectrum for eastward propagating waves",
            "method": "Hayashi (1971) space-time cross-spectrum",
            "NFFT": NFFT,
            "level": f"{plev/100:.0f} hPa",
            "year": year,
        },
    )

    K_n_da = xr.DataArray(
        K_n_year.values,
        coords={
            "lat": lats,
            "freq": om,
            "wavenumber": lon_freq,
        },
        dims=["lat", "freq", "wavenumber"],
        name="K_negative",
        attrs={
            "long_name": "Negative frequency cross-spectrum",
            "description": "u'v' cross-spectrum for westward propagating waves",
            "method": "Hayashi (1971) space-time cross-spectrum",
            "NFFT": NFFT,
            "level": f"{plev/100:.0f} hPa",
            "year": year,
        },
    )

    # Combine into Dataset
    ds = xr.Dataset(
        {
            "K_p": K_p_da,
            "K_n": K_n_da,
        }
    )

    # Add global attributes
    ds.attrs["title"] = "Space-time cross-spectra between u' and v'"
    ds.attrs["source"] = f"MPI-ESM1-2-LR r{ens}i1p1f1"
    ds.attrs["decade"] = str(decade)
    ds.attrs["year"] = year
    ds.attrs["pressure_level"] = f"{plev/100:.0f} hPa"
    ds.attrs["frequency_filter"] = "2-8 day bandpass"

    # Save to NetCDF
    output_file = (
        f"{output_path}spacetime_spectra_upvp_{plev/100:.0f}hPa_{year}_r{ens}i1p1f1.nc"
    )
    ds.to_netcdf(output_file)
    print(f"Rank {rank}: Saved {output_file}")

print(f"Rank {rank}: All done!")

# %%
