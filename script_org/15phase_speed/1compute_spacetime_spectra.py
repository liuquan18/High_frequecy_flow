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
year = sys.argv[2]
decade = (int(year) // 10) * 10

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
if rank == 0:
    logging.info(f"MPI rank {rank} of {size} initialized.")
    logging.info(f"Processing ensemble {ens} for year {year}")
    logging.info("Computing space-time cross-spectra...")

# %%
# Parameters
NFFT = 128  # FFT length

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

# Select isentropic level if it exists in the data
up = up.sel(time=up.time.dt.year == int(year))
vp = vp.sel(time=vp.time.dt.year == int(year))
if rank == 0:
    print(f"Processing year {year}")

up = up.sel(lat=slice(0, 90))
vp = vp.sel(lat=slice(0, 90))


# Get unique isentropic levels and distribute across ranks
isents = np.unique(up.isentropic_level.values)
n_levels = len(isents)
levels_per_rank = np.array_split(isents, size)
my_levels = levels_per_rank[rank]

if rank == 0:
    print(f"Total levels: {n_levels}, MPI size: {size}")
print(f"Rank {rank}: Processing {len(my_levels)} levels: {my_levels}")


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
# Process each isentropic level assigned to this rank
K_p_list = []
K_n_list = []

for level_idx, level in enumerate(my_levels):
    print(f"Rank {rank}: Processing level {level} ({level_idx+1}/{len(my_levels)})")

    # Select data for this level
    up_level = up.sel(isentropic_level=level)
    vp_level = vp.sel(isentropic_level=level)

    # Compute space-time cross-spectra (returns DataArrays with freq and wavenumber coords)
    K_p_level, K_n_level = vectorized_spacetime_spectra(up_level, vp_level)

    # Add isentropic_level as coordinate
    K_p_level = K_p_level.expand_dims(isentropic_level=[level])
    K_n_level = K_n_level.expand_dims(isentropic_level=[level])

    K_p_list.append(K_p_level)
    K_n_list.append(K_n_level)
# Combine all levels for this rank along isentropic_level dimension
if len(K_p_list) > 0:
    K_p_rank = xr.concat(K_p_list, dim="isentropic_level")
    K_n_rank = xr.concat(K_n_list, dim="isentropic_level")
else:
    K_p_rank = None 
    K_n_rank = None

print(f"Rank {rank}: Finished computing {len(my_levels)} levels")

# %%
# Gather all results from all ranks to rank 0
if rank == 0:
    print("Gathering results from all ranks...")

# Gather xarray DataArrays from all ranks
K_p_all_ranks = comm.gather(K_p_rank, root=0)
K_n_all_ranks = comm.gather(K_n_rank, root=0)

# %%
# Rank 0 combines all data into a single dataset
if rank == 0:
    print("Combining data from all ranks...")

    # Filter out None values and concatenate along isentropic_level
    K_p_list_all = [k for k in K_p_all_ranks if k is not None]
    K_n_list_all = [k for k in K_n_all_ranks if k is not None]

    # Concatenate and sort by isentropic level
    K_p_da = xr.concat(K_p_list_all, dim="isentropic_level").sortby("isentropic_level")
    K_n_da = xr.concat(K_n_list_all, dim="isentropic_level").sortby("isentropic_level")

    # only keep the first 10 wavenumbers to reduce file size
    K_p_da = K_p_da.isel(wavenumber=slice(0, 10))
    K_n_da = K_n_da.isel(wavenumber=slice(0, 10))


    # Add attributes
    K_p_da.name = "K_positive"
    K_p_da.attrs = {
        "long_name": "Positive frequency cross-spectrum",
        "description": "u'v' cross-spectrum for eastward propagating waves",
        "method": "Hayashi (1971) space-time cross-spectrum",
        "NFFT": NFFT,
        "units": "power",
        "year": year,
    }

    K_n_da.name = "K_negative"
    K_n_da.attrs = {
        "long_name": "Negative frequency cross-spectrum",
        "description": "u'v' cross-spectrum for westward propagating waves",
        "method": "Hayashi (1971) space-time cross-spectrum",
        "NFFT": NFFT,
        "units": "power",
        "year": year,
    }

    # Combine into Dataset
    ds = xr.Dataset({"K_p": K_p_da, "K_n": K_n_da})

    # Add global attributes
    ds.attrs["title"] = "Space-time cross-spectra between u' and v'"
    ds.attrs["source"] = f"MPI-ESM1-2-LR r{ens}i1p1f1"
    ds.attrs["decade"] = str(decade)
    ds.attrs["year"] = year
    ds.attrs["frequency_filter"] = "2-8 day bandpass"
    ds.attrs["n_isentropic_levels"] = len(K_p_da.isentropic_level)

    # Add coordinate attributes
    ds["isentropic_level"].attrs["units"] = "K"
    ds["isentropic_level"].attrs["long_name"] = "Isentropic level"
    ds["lat"].attrs["units"] = "degrees_north"
    ds["lat"].attrs["long_name"] = "Latitude"
    ds["freq"].attrs["units"] = "cycles/day"
    ds["freq"].attrs["long_name"] = "Frequency"
    ds["wavenumber"].attrs["units"] = "cycles/degree"
    ds["wavenumber"].attrs["long_name"] = "Zonal wavenumber"

    print(f"Combined shape: {K_p_da.shape}")
    print(f"Isentropic levels: {K_p_da.isentropic_level.values}")
    print(f"Dataset dimensions: {ds.dims}")

    # Save to NetCDF
    output_file = (
        f"{output_path}spacetime_spectra_upvp_alllevels_{year}_r{ens}i1p1f1.nc"
    )
    ds.to_netcdf(output_file)
    print(f"Saved combined dataset to: {output_file}")

print(f"Rank {rank}: All done!")

# %%
