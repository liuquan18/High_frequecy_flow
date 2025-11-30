# %%
import numpy as np
import scipy.signal as ss
import scipy.interpolate as si
import matplotlib.pyplot as mm

import xarray as xr


# %%
def calc_spacetime_cross_spec(a, b, dx=1.0, ts=1.0, smooth=1, width=15.0, NFFT=256):
    """
    Calculate space-time co-spectra, following method of Hayashi (1971).

    NOTE: The signature was modified to include 'dx' as an argument, and
    'mm.window_hanning' was replaced with 'np.hanning(NFFT)' for robustness.
    """

    # Use np.hanning(NFFT) as the window array for consistency
    window_hanning_arr = np.hanning(NFFT)

    t, l = np.shape(a)
    lf = l // 2

    # 1. Calculate spatial FFTs
    Fa = np.fft.fft(a, axis=1) / float(l)
    Fb = np.fft.fft(b, axis=1) / float(l)

    # 2. Get positive wavenumbers
    lon_freq = np.fft.fftfreq(l, d=dx)[:lf]

    CFa = Fa[:, :lf].real
    SFa = Fa[:, :lf].imag
    CFb = Fb[:, :lf].real
    SFb = Fb[:, :lf].imag

    tf = NFFT // 2 + 1

    # K_p, K_n arrays
    K_p = np.zeros((tf, lf))
    K_n = np.zeros((tf, lf))

    # 3. Calculate Cross-spectra (CSD) for each wavenumber component
    for i in range(lf):
        # The window argument assumes a Hanning array of length NFFT
        csd_CaCb, om = mm.csd(
            CFa[:, i],
            CFb[:, i],
            Fs=1.0 / ts,
            NFFT=NFFT,
            scale_by_freq=True,
            window=window_hanning_arr,
        )
        csd_SaSb, om = mm.csd(
            SFa[:, i],
            SFb[:, i],
            Fs=1.0 / ts,
            NFFT=NFFT,
            scale_by_freq=True,
            window=window_hanning_arr,
        )
        csd_CaSb, om = mm.csd(
            CFa[:, i],
            SFb[:, i],
            Fs=1.0 / ts,
            NFFT=NFFT,
            scale_by_freq=True,
            window=window_hanning_arr,
        )
        csd_SaCb, om = mm.csd(
            SFa[:, i],
            CFb[:, i],
            Fs=1.0 / ts,
            NFFT=NFFT,
            scale_by_freq=True,
            window=window_hanning_arr,
        )

        # 4. Combine real and imaginary parts into positive (K_p) and negative (K_n) frequency spectra
        # K_p (Eq 4.11 in Hayashi '71, but for positive frequencies)
        K_p[:, i] = csd_CaCb.real + csd_SaSb.real + csd_CaSb.imag - csd_SaCb.imag
        # K_n (Eq 4.12 in Hayashi '71, but for positive frequencies)
        K_n[:, i] = csd_CaCb.real + csd_SaSb.real - csd_CaSb.imag + csd_SaCb.imag

    # 5. Combine for frequency smoothing
    K_combine = np.zeros((tf * 2, lf))
    K_combine[:tf, :] = K_n[::-1, :]  # Negative frequencies
    K_combine[tf:, :] = K_p[:, :]  # Positive frequencies

    if smooth == 1.0:
        x = np.linspace(-tf / 2, tf / 2.0, tf)
        gauss_filter = np.exp(-(x**2) / (2.0 * width**2))
        gauss_filter /= sum(gauss_filter)
        # Apply convolution for frequency smoothing
        for i in range(lf):
            K_combine[:, i] = np.convolve(K_combine[:, i], gauss_filter, "same")

    # 6. Separate back into K_p and K_n (smoothed)
    K_n = K_combine[:tf, :]
    K_p = K_combine[tf:, :]
    K_n = K_n[::-1, :]

    return K_p, K_n, lon_freq, om


# %%
# ----------------------------------------------------
## Data Generation
# ----------------------------------------------------

# %%
up = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/ua_prime_daily/r1i1p1f1/ua_prime_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc"
)
vp = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/va_prime_daily/r1i1p1f1/va_prime_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc"
)

# %%
up = up.sel(plev=500, lat=60, method="nearest").sel(time="1850").ua
vp = vp.sel(plev=500, lat=60, method="nearest").sel(time="1850").va


# %%
# Run the function
K_p, K_n, lon_freq, om = calc_spacetime_cross_spec(
    up, vp, dx=1, ts=1, NFFT=256, smooth=1
)
# %%

# ----------------------------------------------------
## Plotting and Period Calculation
# ----------------------------------------------------

# %%
# Calculate periods from frequencies (exclude zero frequency)
periods = 1.0 / om[1:]  # Convert frequency to period (in days)

# Create combined spectrum for plotting (westward + eastward)
# K_n represents westward propagation, K_p represents eastward propagation
K_combined = np.concatenate([K_n[1:, :10][::-1], K_p[1:, :10]], axis=0)

# Create period axis (westward negative, eastward positive)
periods_combined = np.concatenate([-periods[::-1], periods])

# %%
# Plot the space-time spectrum
fig, ax = mm.subplots(figsize=(12, 6))

# Use contourf for filled contours
levels = np.linspace(K_combined.min(), K_combined.max(), 20)
cf = ax.contour(
    periods_combined, lon_freq[:10], K_combined.T, levels=levels, cmap="RdBu_r"
)

# Set x-axis limits and labels
ax.set_xlim(-30, 30)
ax.set_xlabel("Period (days): Westward (negative) | Eastward (positive)", fontsize=12)
ax.set_ylabel("Zonal Wavenumber", fontsize=12)
ax.set_title("Space-Time Cross-Spectrum: U-V at 500 hPa, 60°N", fontsize=14)

# Add vertical line at zero
ax.axvline(0, color="black", linestyle="--", linewidth=1)

# Set y-axis to show wavenumbers 0-10
ax.set_ylim(0, lon_freq[9])
ax.set_yticks(lon_freq[:10])
ax.set_yticklabels([f"{int(i)}" for i in range(10)])

# Add colorbar
cbar = mm.colorbar(cf, ax=ax)
cbar.set_label("Power", fontsize=12)

# Improve x-axis ticks
ax.set_xticks([-30, -20, -10, 0, 10, 20, 30])

mm.tight_layout()
mm.show()

# %%
# Plot only eastward waves (K_p)
fig, ax = mm.subplots(figsize=(12, 6))

# Use K_p for eastward propagation only
levels = np.linspace(K_p[1:, :10].min(), K_p[1:, :10].max(), 10)
cf = ax.contour(
    periods,
    lon_freq[:10],
    K_p[1:, :10].T,
    levels=levels,
    colors="k",
)

# Set x-axis limits and labels
ax.set_xscale("log")
ax.set_xlim(1, 30)
ax.set_xlabel("Period (days) - Eastward", fontsize=12)
ax.set_ylabel("Zonal Wavenumber", fontsize=12)
ax.set_title(
    "Space-Time Cross-Spectrum: Eastward Waves Only (500 hPa, 60°N)", fontsize=14
)

# Set y-axis to show wavenumbers 0-10
ax.set_ylim(0, lon_freq[9])
ax.set_yticks(lon_freq[:10])
ax.set_yticklabels([f"{int(i)}" for i in range(10)])

# Add colorbar
cbar = mm.colorbar(cf, ax=ax)
cbar.set_label("Power", fontsize=12)

# Improve x-axis ticks
# ax.set_xticks([0, 5, 10, 15, 20, 25, 30])

mm.tight_layout()
mm.show()

# %%


def calPhaseSpeedSpectrum(P_p, P_n, f_lon, om, cmax, nps, i1=1, i2=50):
    """
    Calculate space-time co-spectra, following method of Hayashi (1971)

    Input:
      P_p - spectra for positive phase speeds
      P_n - spectra for negative phase speeds
      f_lon - wavenumbers
      om - frequencies
      cmax - maximum phase speed
      nps - size of phase speed grid
      i1 - lowest wave number to sum over
      i2 - highest wave number to sum over

    Output:
      P_cp - spectra for positive phase speeds
      P_cn - spectra for negative phase speeds
      C * lon_unit / time_unit - phase speeds
    """
    if i2 < i1:
        print("WARNING: highest wavenumber smaller than lowest wavenumber")

    j = len(f_lon)
    t = len(om)

    # Make phase speed grid
    C = np.linspace(0.0, cmax, nps)

    # K_n,c arrays
    P_cp = np.zeros((nps, j))
    P_cn = np.zeros((nps, j))

    # Interpolate
    for i in range(i1, i2):
        # Make interpolation functions c = omega / k
        f1 = si.interp1d(om / f_lon[i], P_p[:, i], "linear")
        f2 = si.interp1d(om / f_lon[i], P_n[:, i], "linear")

        # interp1d doesn't handle requested points outside data range well, so just zero out these points
        k = -1
        for j in range(len(C)):
            if C[j] > max(om) / f_lon[i]:
                k = j
                break
        if k == -1:
            k = len(C)

        ad1 = np.zeros(nps)
        ad1[:k] = f1(C[:k])
        ad2 = np.zeros(nps)
        ad2[:k] = f2(C[:k])

        # Interpolate
        P_cp[:, i] = ad1 * f_lon[i]
        P_cn[:, i] = ad2 * f_lon[i]

        # Sum over all wavenumbers
    return np.sum(P_cp, axis=1), np.sum(P_cn, axis=1), C


# %%
# Example usage of calPhaseSpeedSpectrum
P_cp, P_cn, C = calPhaseSpeedSpectrum(
    K_p, K_n, lon_freq, om, cmax=30, nps=100, i1=1, i2=10
)
#%%
# to physical speed. from longitude point to m/s
earth_radius = 6371000  # meters
deg_to_m = 2 * np.pi * earth_radius / 360  # meters per degree longitude at equator
lat = 60  # degrees
lat_factor = np.cos(np.deg2rad(lat))  # adjust for latitude
C_physical = C * deg_to_m * lat_factor / (24 * 3600)  # convert from deg/day to m/s

# %%

# Plot phase speed spectrum
fig, ax = mm.subplots(figsize=(10, 6))

# Plot positive (eastward) and negative (westward) phase speeds
ax.plot(C_physical, P_cp, label="Eastward (positive)", linewidth=2, color="blue")
ax.plot(-C_physical, P_cn, label="Westward (negative)", linewidth=2, color="red")

# Add vertical line at zero
ax.axvline(0, color="black", linestyle="--", linewidth=1)

# Labels and title
ax.set_xlabel("Phase Speed (m/s)", fontsize=12)
ax.set_ylabel("Power (summed over wavenumbers)", fontsize=12)
ax.set_title("Phase Speed Spectrum: 500 hPa, 60°N", fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

mm.tight_layout()
mm.show()

# %%
