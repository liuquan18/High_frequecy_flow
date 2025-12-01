# %%
import numpy as np
import scipy.interpolate as si
import xarray as xr
import scipy.signal as signal
import matplotlib.pyplot as plt


# %%
def calc_hayashi_spectra(data, dt=1.0, dx=1.0, nfft=None, window="hann"):
    """
    Calculates Space-Time Spectra following Hayashi (1971).
    Separates power into Eastward and Westward propagating components.

    Parameters:
        data (np.ndarray): Input array with shape (time, longitude).
        dt (float): Sampling interval in time (e.g., 1 day).
        dx (float): Sampling interval in space (e.g., degrees longitude).
        nfft (int): Length of the FFT for the time dimension (default: length of time).
        window (str): Window function for time-domain FFT (e.g., 'hann').

    Returns:
        wavenumbers (np.ndarray): Zonal wavenumbers.
        frequencies (np.ndarray): Frequencies (cycles per time unit).
        westward_power (np.ndarray): Power spectrum of westward propagating waves.
        eastward_power (np.ndarray): Power spectrum of eastward propagating waves.
    """
    nt, nx = data.shape
    if nfft is None:
        nfft = nt

    # 1. FFT in Space (Longitude)
    # Returns coefficients for wavenumbers 0 to nx/2
    fft_space = np.fft.rfft(data, axis=1) / nx

    # Separate Real (Cosine) and Imaginary (Sine) coefficients
    # shape: (time, n_wavenumbers)
    C_k = fft_space.real
    S_k = fft_space.imag

    wavenumbers = (
        np.fft.rfftfreq(nx, d=dx) * nx
    )  # Convert to integer wavenumbers if dx=1 represents grid spacing

    # Initialize output arrays
    num_freqs = nfft // 2 + 1
    num_waves = C_k.shape[1]

    P_west = np.zeros((num_freqs, num_waves))
    P_east = np.zeros((num_freqs, num_waves))

    # 2. Cross-Spectral Density in Time for each Wavenumber
    # We calculate the cross-spectra between the Cosine and Sine spatial coefficients
    for k in range(num_waves):
        # Calculate auto-spectra (P_CC, P_SS) and cross-spectrum (P_CS)
        # fs = 1/dt (sampling frequency)
        freqs, P_CC = signal.csd(
            C_k[:, k], C_k[:, k], fs=1 / dt, nperseg=nfft, window=window
        )
        _, P_SS = signal.csd(
            S_k[:, k], S_k[:, k], fs=1 / dt, nperseg=nfft, window=window
        )
        _, P_CS = signal.csd(
            C_k[:, k], S_k[:, k], fs=1 / dt, nperseg=nfft, window=window
        )

        # Quadrature spectrum Q_CS is the imaginary part of P_CS
        Q_CS = P_CS.imag

        # 3. Hayashi (1971) Formula regarding East/West separation
        # Westward Power: (P_CC + P_SS + 2*Q_CS) / 2
        # Eastward Power: (P_CC + P_SS - 2*Q_CS) / 2
        # Note: Factor of 4 or 2 depends on normalization. Using standard 1/2 split here.

        P_west[:, k] = (P_CC + P_SS + 2 * Q_CS) / 2
        P_east[:, k] = (P_CC + P_SS - 2 * Q_CS) / 2

    return wavenumbers, freqs, P_west, P_east


#

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
upvp = up * vp


# %%
# 2. Calculate Spectra
k_wn, freq, P_west, P_east = calc_hayashi_spectra(upvp.values, dt=1.0, dx=1.0)
# ----------------------------------------------------
## Plotting and Period Calculation
# ----------------------------------------------------

# ==========================================
# Visualization
# ==========================================
fig, ax = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Convert frequency to period for easier reading (optional)
# Skip zero frequency to avoid inf values
freq_nonzero = freq[1:]
periods = 1 / freq_nonzero
P_west_plot = P_west[1:, :]
P_east_plot = P_east[1:, :]

# Plot Westward Power
# Using pcolormesh. X: Period, Y: Wavenumber
c1 = ax[0].pcolormesh(
    periods, k_wn, P_west_plot.T, shading="auto", cmap="Reds", vmin=0, vmax=0.5
)
ax[0].set_title("Westward Propagating Power\n(Should see Peak at k=4, Period=10)")
ax[0].set_xlabel("Period (Days)")
ax[0].set_ylabel("Zonal Wavenumber")
ax[0].set_xlim(0, 30)
ax[0].set_ylim(0, 10)
plt.colorbar(c1, ax=ax[0])

# Plot Eastward Power
c2 = ax[1].pcolormesh(
    periods, k_wn, P_east_plot.T, shading="auto", cmap="Blues", vmin=0, vmax=0.5
)
ax[1].set_title("Eastward Propagating Power\n(Should see Peak at k=2, Period=5)")
ax[1].set_xlabel("Period (Days)")
ax[1].set_xlim(0, 30)
ax[1].set_ylim(0, 10)
plt.colorbar(c2, ax=ax[1])

plt.suptitle("Hayashi (1971) Space-Time Spectra Analysis", fontsize=16)
plt.show()


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
    P_east, P_west, k_wn, freq, cmax=30, nps=100, i1=1, i2=10
)
# %%

# Plot phase speed spectrum
fig, ax = plt.subplots(figsize=(10, 6))

# Plot positive (eastward) and negative (westward) phase speeds
ax.plot(C, P_cp, label="Eastward (positive)", linewidth=2, color="blue")
ax.plot(-C, P_cn, label="Westward (negative)", linewidth=2, color="red")

# Add vertical line at zero
ax.axvline(0, color="black", linestyle="--", linewidth=1)

# Labels and title
ax.set_xlabel("Phase Speed (m/s)", fontsize=12)
ax.set_ylabel("Power (summed over wavenumbers)", fontsize=12)
ax.set_title("Phase Speed Spectrum: 500 hPa, 60°N", fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)


ax.set_ylim(0, 0.06)

plt.tight_layout()
plt.show()

# %%
#___-------------------------------------------
import numpy as np
import scipy.signal as signal
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def calc_hayashi_spectra(data, dt=1.0, dx=1.0, nfft=None, window='hann'):
    """
    Calculates Space-Time Power Spectra following Hayashi (1971) method.
    This function calculates the power spectrum (A correlated with A).
    
    Parameters:
        data (np.ndarray): Input array with shape (time, longitude).
        dt (float): Sampling interval in time (e.g., 1 day).
        dx (float): Grid spacing in space (e.g., 1 degree longitude).
        nfft (int): Length of the FFT for the time dimension.
        window (str): Window function for time-domain FFT (e.g., 'hann').
        
    Returns:
        wavenumbers (np.ndarray): Zonal wavenumbers (k).
        frequencies (np.ndarray): Frequencies (omega).
        P_west (np.ndarray): Power spectrum of westward propagating waves.
        P_east (np.ndarray): Power spectrum of eastward propagating waves.
    """
    nt, nx = data.shape
    if nfft is None:
        nfft = nt

    # 1. FFT in Space (Longitude)
    # The rfft only returns non-negative wavenumbers (0 to nx/2)
    fft_space = np.fft.rfft(data, axis=1) / nx
    
    C_k = fft_space.real
    S_k = fft_space.imag

    # Zonal wavenumbers (k). Since dx=1 is assumed for grid spacing, k is integer wave number.
    wavenumbers = np.fft.rfftfreq(nx, d=dx) * nx 
    
    num_freqs = nfft // 2 + 1
    num_waves = C_k.shape[1]
    
    P_west = np.zeros((num_freqs, num_waves))
    P_east = np.zeros((num_freqs, num_waves))
    
    # 2. Cross-Spectral Density in Time for each Wavenumber
    # The total power is the sum of the variances of the cosine and sine coefficients.
    for k in range(num_waves):
        # Using Welch's method (csd) for smoothed spectral estimation in time.
        # fs = 1/dt (sampling frequency)
        freqs, P_CC = signal.csd(C_k[:, k], C_k[:, k], fs=1/dt, nperseg=nfft, window=window)
        _,     P_SS = signal.csd(S_k[:, k], S_k[:, k], fs=1/dt, nperseg=nfft, window=window)
        _,     P_CS = signal.csd(C_k[:, k], S_k[:, k], fs=1/dt, nperseg=nfft, window=window)
        
        # Quadrature spectrum Q_CS is the imaginary part of P_CS
        Q_CS = P_CS.imag
        
        # 3. Hayashi (1971) Formula for Power
        # P_total = P_CC + P_SS
        # P_westward = (P_total + 2*Q_CS) / 2
        # P_eastward = (P_total - 2*Q_CS) / 2
        
        P_total = P_CC + P_SS
        
        # NOTE: A factor of 2 is sometimes included here depending on normalization of the 
        # spatial FFT (if using full FFT, it's 2*Q_CS, if using rfft, it's often 4*Q_CS 
        # due to Parseval's theorem on real data). We use the common factor of 2.
        
        P_west[:, k] = (P_total + 2 * Q_CS) / 2
        P_east[:, k] = (P_total - 2 * Q_CS) / 2

    return wavenumbers, freqs, P_west, P_east

def calculate_phase_speed_spectrum(P_p, P_n, wavenumbers, frequencies, cmax=30.0, nps=100, i1=1, i2=None):
    """
    Transforms the (wavenumber, frequency) spectrum into a (phase speed) spectrum 
    by integrating over a specified range of wavenumbers (i1 to i2).

    Parameters:
        P_p (np.ndarray): Eastward Power spectrum (Positive Phase Speed). Shape (frequency, wavenumber).
        P_n (np.ndarray): Westward Power spectrum (Negative Phase Speed). Shape (frequency, wavenumber).
        wavenumbers (np.ndarray): Zonal wavenumbers (k).
        frequencies (np.ndarray): Frequencies (omega).
        cmax (float): Maximum phase speed for the output grid (e.g., 30 m/s).
        nps (int): Number of points in the phase speed grid.
        i1 (int): Lowest zonal wavenumber (inclusive) to integrate over.
        i2 (int): Highest zonal wavenumber (exclusive) to integrate over. Defaults to max wavenumber.

    Returns:
        P_cp_sum (np.ndarray): Summed Eastward (Positive) Phase Speed Spectrum.
        P_cn_sum (np.ndarray): Summed Westward (Negative) Phase Speed Spectrum.
        C (np.ndarray): The phase speed axis (e.g., in deg_lon/day).
    """
    
    # Initialize the integration range for wavenumbers
    if i2 is None:
        i2 = len(wavenumbers)
    
    # Create the Phase Speed (C) axis grid
    C = np.linspace(0.0, cmax, nps)
    
    # Initialize 2D arrays to hold interpolated power for each wavenumber
    # Shape: (Phase Speed, Wavenumber)
    P_cp = np.zeros((nps, len(wavenumbers)))
    P_cn = np.zeros((nps, len(wavenumbers)))
    
    # Iterate through the selected wavenumbers
    # NOTE: Wavenumber 0 (mean) is skipped (starts at i1=1 by default)
    for i in range(i1, min(i2, len(wavenumbers))):
        k = wavenumbers[i]
        
        # Calculate the phase speed grid for the current wavenumber: C_k = omega / k
        # Add a tiny value to k to prevent division by zero, though k=0 is skipped by range(i1, i2).
        C_k = frequencies / k 
        
        # Check if C_k contains any finite values (i.e., not division by zero at freq[0])
        finite_mask = np.isfinite(C_k)
        
        if np.any(finite_mask):
            # Create interpolation function: maps C_k to P_p/P_n
            # We must use only finite C_k and corresponding P values for interp1d
            f_p = interp1d(C_k[finite_mask], P_p[finite_mask, i], kind='linear', 
                           bounds_error=False, fill_value=0.0)
            f_n = interp1d(C_k[finite_mask], P_n[finite_mask, i], kind='linear', 
                           bounds_error=False, fill_value=0.0)
            
            # Interpolate the power onto the common Phase Speed grid C
            # We multiply by |k| (wavenumber) as required for the transformation 
            # (d(omega) = |k|dC) to conserve variance in the transformed domain.
            P_cp[:, i] = f_p(C) * k
            P_cn[:, i] = f_n(C) * k

    # Sum over the wavenumber axis (axis=1) to get the final 1D spectrum
    P_cp_sum = np.sum(P_cp[:, i1:i2], axis=1)
    P_cn_sum = np.sum(P_cn[:, i1:i2], axis=1)
    
    return P_cp_sum, P_cn_sum, C

# ==========================================
# Example Usage with Synthetic Data and Visualization
# ==========================================

# 1. Generate Synthetic Data
Nt, Nx = 128, 64  # 128 days, 64 longitude points
time = np.arange(Nt)
lon = np.linspace(0, 360, Nx, endpoint=False)
dt_days = 1.0  # Time step in days
dx_deg = 360.0 / Nx # Longitudinal spacing (64 points cover 360 degrees)

# Westward Propagating Wave (Rossby-like): k=4, Period=10 days
k_west, T_west = 4, 10.0
omega_west = 1 / T_west
# Phase speed C = omega/k = (1/10)/4 = 0.025 cycles/day/wavenumber
data_west = np.cos(k_west * np.radians(lon)[None, :] + 2 * np.pi * omega_west * time[:, None])

# Eastward Propagating Wave (Kelvin-like): k=2, Period=5 days
k_east, T_east = 2, 5.0
omega_east = 1 / T_east
# Phase speed C = omega/k = (1/5)/2 = 0.1 cycles/day/wavenumber
data_east = 0.5 * np.cos(2 * np.radians(lon)[None, :] - 2 * np.pi * omega_east * time[:, None])

data = data_west + data_east + 0.1 * np.random.randn(Nt, Nx)

# 2. Calculate Space-Time Spectra
k_wn, freq, P_west_k_f, P_east_k_f = calc_hayashi_spectra(data, dt=dt_days, dx=1.0, nfft=Nt) # dx=1 for indexing

#%%
# 3. Calculate Phase Speed Spectrum (Integrating over wavenumbers 1 through 10)
CMAX_DEG_PER_DAY = 0.3  # Max phase speed for the grid (cycles/day/wavenumber)
k_start, k_end = 1, 10
P_cp_sum, P_cn_sum, C = calculate_phase_speed_spectrum(
    P_east_k_f, P_west_k_f, 
    k_wn, freq, 
    cmax=CMAX_DEG_PER_DAY, 
    nps=200, 
    i1=k_start, 
    i2=k_end
)

# Convert C (cycles/day/wavenumber) to physical degree/day for interpretation 
# C_physical = C * 360 degrees / (1 cycle)
C_physical = C * 360 

# %%

# 4. Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# --- Left Plot: Phase Speed Spectrum (1D) ---
ax1.plot(C_physical, P_cp_sum, color='blue', label=f'Eastward (Integrated k={k_start}-{k_end})')
ax1.plot(-C_physical, P_cn_sum, color='red', label=f'Westward (Integrated k={k_start}-{k_end})')

# Expected Peaks:
# Eastward: C = 0.1 * 360 = 36 deg/day
# Westward: C = -0.025 * 360 = -9 deg/day
ax1.axvline(36, color='b', linestyle='--', alpha=0.6, label='Expected Eastward Peak')
ax1.axvline(-9, color='r', linestyle='--', alpha=0.6, label='Expected Westward Peak')

ax1.set_title(f"1D Phase Speed Spectrum (Hayashi Method)\nIntegrated over Wavenumbers {k_start} to {k_end}")
ax1.set_xlabel("Phase Speed ($\Delta$Longitude / Day)")
ax1.set_ylabel("Power Density [Units$^2$ $\cdot$ Day $\cdot$ Wavenumber]")
ax1.set_xlim(-C_physical.max(), C_physical.max())
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend()

# --- Right Plot: Wavenumber-Frequency Spectrum (2D) for reference ---
periods = 1 / freq
# periods[0] is inf because freq[0] is zero (DC component).
# We must exclude the zero-frequency/infinite period component (index 0) from plotting.

# Total Power (East + West)
P_total = P_east_k_f + P_west_k_f
vmax_plot = np.percentile(P_total, 95) # Cap the max for better visualization

# FIX: Slice periods and P_total.T to exclude the zero-frequency/infinite period component (index 0).
# periods[1:] excludes inf, P_total.T[:, 1:] excludes the f=0 column.
cax = ax2.pcolormesh(periods[1:], k_wn, P_total.T[:, 1:], shading='auto', cmap='magma', vmin=0, vmax=vmax_plot)

# Define arrays that exclude the DC and K=0 components for dispersion curves
plot_k_wn = k_wn[1:] # Exclude k=0 for dispersion curves

# Add theoretical phase speed lines C = omega/k
# Westward Peak: C = -9 deg/day (or -0.025 cycles/day)
# Eastward Peak: C = 36 deg/day (or 0.1 cycles/day)
# Re-calculate dispersion curves for k > 0
ax2.plot(1 / (plot_k_wn * 0.025), plot_k_wn, 'r--', label='C = -0.025 cycles/day/k') 
ax2.plot(1 / (plot_k_wn * -0.1), plot_k_wn, 'b--', label='C = 0.1 cycles/day/k') 
ax2.set_xlim(0, 30) # Keep the visual limit to 30 days
ax2.set_ylim(1, 10)
ax2.set_title("Total Power: Wavenumber-Period Spectrum")
ax2.set_xlabel("Period (Days)")
ax2.set_ylabel("Zonal Wavenumber")
plt.colorbar(cax, ax=ax2, label="Total Power Density")
ax2.legend()

plt.tight_layout()
plt.show()
# %%
