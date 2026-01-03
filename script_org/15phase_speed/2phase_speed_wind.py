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
# Parse command line arguments
node = sys.argv[1]
ens = int(node)
decade = sys.argv[2]

# %%
logging.info(f"Processing ensemble {ens} for decade {decade}")
logging.info("Reading space-time cross-spectra and computing phase speeds...")

# %%
# Input path for space-time spectra
spectra_path = (
    f"/scratch/m/m300883/upvp_space_time_spectra_daily/r{ens}i1p1f1/dec_{decade}/"
)
spectra_files = sorted(glob.glob(spectra_path + "*.nc"))
# %%
# Output path
output_path = (
    f"/scratch/m/m300883/upvp_phase_speed_spectrum_daily/r{ens}i1p1f1/dec_{decade}/"
)
if not os.path.exists(output_path):
    os.makedirs(output_path)

# %%
# Parameters
earth_radius = 6371000  # meters
deg_to_m = 2 * np.pi * earth_radius / 360  # meters per degree longitude at equator
cmax = 50  # maximum phase speed in grid units (deg/day)
nps = 50  # number of phase speed bins
plev = 25000  # pressure level in Pa

# %%
# Read all space-time spectra files
if len(spectra_files) == 0:
    raise FileNotFoundError(f"No space-time spectra files found in {spectra_path}")

print(f"Found {len(spectra_files)} space-time spectra files")

# Load all files and average
K_p_list = []
K_n_list = []

for file in spectra_files:
    ds = xr.open_dataset(file)
    K_p_list.append(ds["K_p"])
    K_n_list.append(ds["K_n"])
    year = ds.attrs.get("year", "unknown")
    print(f"Loaded year {year}")

# Average over all years
K_p_avg = xr.concat(K_p_list, dim="year").mean(dim="year")
K_n_avg = xr.concat(K_n_list, dim="year").mean(dim="year")

n_years = len(K_p_list)
lats = K_p_avg.lat.values
lon_freq = K_p_avg.wavenumber.values
om = K_p_avg.freq.values

print(f"Averaged space-time spectra over {n_years} years")
print(f"Shape: lat={len(lats)}, freq={len(om)}, wavenumber={len(lon_freq)}")


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
# Compute phase speed spectra from averaged space-time spectra
print("Computing phase speed spectra...")
P_cp_avg, P_cn_avg = vectorized_phase_speed_from_spectra(K_p_avg, K_n_avg, lon_freq, om)

# %%
# Calculate phase speeds in physical units for each latitude
C = np.linspace(0.0, cmax, nps)
lat_factors = np.cos(np.deg2rad(lats))
phase_speeds_2d = C[np.newaxis, :] * deg_to_m * lat_factors[:, np.newaxis] / (24 * 3600)

# %%
# Create DataArrays
P_cp_da = xr.DataArray(
    P_cp_avg.values,
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
        "method": "Hayashi (1971) space-time cross-spectrum to phase speed",
        "cmax": cmax,
        "n_years": n_years,
    },
)

P_cn_da = xr.DataArray(
    P_cn_avg.values,
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
        "method": "Hayashi (1971) space-time cross-spectrum to phase speed",
        "cmax": cmax,
        "n_years": n_years,
    },
)

# Combine into a Dataset
ds = xr.Dataset({"P_eastward": P_cp_da, "P_westward": P_cn_da})

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
