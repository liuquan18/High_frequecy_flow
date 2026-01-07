# %%
"""
Script 2: Read space-time cross-spectra (K_p, K_n), average over years,
and compute phase speed spectrum
"""
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from src.spectrum.phase_speed_spectral import calPhaseSpeedSpectrum
import sys
import os
import glob
import logging

logging.basicConfig(level=logging.INFO)


# %%
def compute_phase_speed_single_lat(K_p_lat, K_n_lat, lon_freq, om):
    """
    Compute phase speed spectrum for a single latitude from space-time spectra.

    Parameters
    ----------
    K_p_lat : np.ndarray
        Positive frequency spectrum (freq, wavenumber)
    K_n_lat : np.ndarray
        Negative frequency spectrum (freq, wavenumber)
    lon_freq : np.ndarray
        Wavenumber array
    om : np.ndarray
        Frequency array

    Returns
    -------
    P_cp : np.ndarray
        Positive phase speed spectrum (nps,)
    P_cn : np.ndarray
        Negative phase speed spectrum (nps,)
    """
    # Calculate phase speed spectrum
    P_cp, P_cn, C = calPhaseSpeedSpectrum(
        K_p_lat, K_n_lat, lon_freq, om, cmax=cmax, nps=nps, i1=1, i2=10
    )  # sum over wavenumber bins 1-10 to capture synoptic waves

    return P_cp, P_cn


def vectorized_phase_speed_from_spectra(K_p_data, K_n_data, lon_freq, om):
    """
    Vectorized computation of phase speed spectrum across all latitudes.

    Parameters
    ----------
    K_p_data : xr.DataArray
        Positive frequency spectra (lat, freq, wavenumber)
    K_n_data : xr.DataArray
        Negative frequency spectra (lat, freq, wavenumber)
    lon_freq : np.ndarray
        Wavenumber array
    om : np.ndarray
        Frequency array

    Returns
    -------
    P_cp_all : xr.DataArray
        Positive phase speed spectra (lat, phase_speed)
    P_cn_all : xr.DataArray
        Negative phase speed spectra (lat, phase_speed)
    """

    # Wrapper for apply_ufunc
    def compute_wrapper(K_p_vals, K_n_vals):
        P_cp, P_cn = compute_phase_speed_single_lat(K_p_vals, K_n_vals, lon_freq, om)
        return P_cp, P_cn

    result = xr.apply_ufunc(
        compute_wrapper,
        K_p_data,
        K_n_data,
        input_core_dims=[["freq", "wavenumber"], ["freq", "wavenumber"]],
        output_core_dims=[["phase_speed"], ["phase_speed"]],
        exclude_dims=set(["freq", "wavenumber"]),
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float, float],
        output_sizes={"phase_speed": nps},
    )

    P_cp_all = result[0]
    P_cn_all = result[1]

    return P_cp_all, P_cn_all


# %%
# Parameters
earth_radius = 6371000  # meters
deg_to_m = 2 * np.pi * earth_radius / 360  # meters per degree longitude at equator
cmax = 50  # maximum phase speed in grid units (deg/day)
nps = 50  # number of phase speed bins
plev = 25000  # pressure level in Pa

# %%

def process_ensemble_decade(ens, decade):
    logging.info(f"Processing ensemble {ens} for decade {decade}")
    logging.info("Reading space-time cross-spectra and computing phase speeds...")


    # Input path for space-time spectra
    spectra_path = (
        f"/scratch/m/m300883/upvp_space_time_spectra_daily/r{ens}i1p1f1/dec_{decade}/"
    )
    spectra_files = sorted(glob.glob(spectra_path + "*.nc"))

    # Output path
    output_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/upvp_isent_phase_speed_spectrum_daily/r{ens}i1p1f1/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Read all space-time spectra files
    if len(spectra_files) == 0:
        raise FileNotFoundError(f"No space-time spectra files found in {spectra_path}")

    print(f"Found {len(spectra_files)} space-time spectra files")

    ds = xr.open_mfdataset(spectra_files, combine="nested", concat_dim="year")

    ds = ds.mean(dim="year")

    n_years = 10
    lats = ds.lat.values
    lon_freq = ds.wavenumber.values / 360
    om = ds.freq.values

    print(f"Shape: lat={len(lats)}, freq={len(om)}, wavenumber={len(lon_freq)}")


    # Compute phase speed spectra from averaged space-time spectra
    K_p_avg = ds.K_p
    K_n_avg = ds.K_n
    print("Computing phase speed spectra...")
    P_cp_avg, P_cn_avg = vectorized_phase_speed_from_spectra(K_p_avg, K_n_avg, lon_freq, om)


    # Calculate phase speeds in physical units for each latitude (m/s)
    C = np.linspace(0.0, cmax, nps)
    lat_factors = np.cos(np.deg2rad(lats))
    phase_speeds_2d = C[np.newaxis, :] * deg_to_m * lat_factors[:, np.newaxis] / (24 * 3600)


    # Assign physical phase speeds as 2D coordinate (latitude-dependent)
    P_cp_avg = P_cp_avg.assign_coords(
        phase_speed_ms=(["lat", "phase_speed"], phase_speeds_2d)
    )
    P_cn_avg = P_cn_avg.assign_coords(
        phase_speed_ms=(["lat", "phase_speed"], phase_speeds_2d)
    )

    # Add attributes to the data arrays
    P_cp_avg.attrs.update(
        {
            "long_name": "Eastward phase speed power spectrum",
            "units": "power",
            "description": f"u'v' cospectra averaged over {n_years} years",
            "level": f"{plev/100:.0f} hPa",
            "method": "Hayashi (1971) space-time cross-spectrum to phase speed",
        }
    )

    P_cn_avg.attrs.update(
        {
            "long_name": "Westward phase speed power spectrum",
            "units": "power",
            "description": f"u'v' cospectra averaged over {n_years} years",
            "level": f"{plev/100:.0f} hPa",
            "method": "Hayashi (1971) space-time cross-spectrum to phase speed",
        }
    )

    # Combine into a Dataset
    ds = xr.Dataset({"P_eastward": P_cp_avg, "P_westward": P_cn_avg})

    # Add global attributes
    ds.attrs["title"] = "Phase Speed Spectrum from u'v' cospectra (decade average)"
    ds.attrs["source"] = f"MPI-ESM1-2-LR r{ens}i1p1f1"
    ds.attrs["decade"] = str(decade)
    ds.attrs["n_years"] = n_years
    ds.attrs["pressure_level"] = f"{plev/100:.0f} hPa"
    ds.attrs["frequency_filter"] = "2-8 day bandpass"

    # Save to NetCDF
    output_file = f"{output_path}phase_speed_upvp_cospectra_{plev/100:.0f}hPa_dec{decade}_r{ens}i1p1f1.nc"
    ds.to_netcdf(output_file)
    print(f"Saved dataset to: {output_file}")

#%%
for ens in range(1, 51, 1):
    print(f"Processing ensemble member r{ens}i1p1f1")
    process_ensemble_decade(ens, "1850")
    process_ensemble_decade(ens, "2090")
# %%
