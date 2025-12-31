# %%
import numpy as np
import scipy.signal as ss
import scipy.interpolate as si
import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend for non-interactive plotting
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

#%%

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

