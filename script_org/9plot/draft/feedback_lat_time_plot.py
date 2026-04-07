# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import cmocean
import os
import matplotlib
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, FuncFormatter

from src.plotting.util import map_smooth
import src.plotting.util as util
import metpy.calc as mpcalc
from metpy.units import units

# %%
data_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0composite_feedback"

def _load(name):
    return xr.open_dataarray(os.path.join(data_dir, f"{name}.nc"))

# Jet stream
ua_pos_first = _load("ua_pos_1850")
ua_neg_first = _load("ua_neg_1850")
ua_pos_last  = _load("ua_pos_2090")
ua_neg_last  = _load("ua_neg_2090")

# Convergence of eddy momentum flux
momentum_pos_first = _load("Fdiv_phi_transient_pos_1850")
momentum_neg_first = _load("Fdiv_phi_transient_neg_1850")
momentum_pos_last  = _load("Fdiv_phi_transient_pos_2090")
momentum_neg_last  = _load("Fdiv_phi_transient_neg_2090")


# %%# upvp
upvp_pos_first = _load("upvp_pos_1850")
upvp_neg_first = _load("upvp_neg_1850")
upvp_pos_last  = _load("upvp_pos_2090")
upvp_neg_last  = _load("upvp_neg_2090")


# %%
ua_pos_first=ua_pos_first.sel(plev = 25000)
ua_neg_first=ua_neg_first.sel(plev = 25000)
ua_pos_last=ua_pos_last.sel(plev = 25000)
ua_neg_last=ua_neg_last.sel(plev = 25000)

#%%
upvp_pos_first=upvp_pos_first.sel(plev = 25000)
upvp_neg_first=upvp_neg_first.sel(plev = 25000)
upvp_pos_last=upvp_pos_last.sel(plev = 25000)
upvp_neg_last=upvp_neg_last.sel(plev = 25000)

# %% Prepare: average over event dim, compute diffs, scale baroclinicity
def _em(da):
    return da.mean(dim="event").sel(lat=slice(0, 90))
#%%
ua_p1 = _em(ua_pos_first);  ua_n1 = _em(ua_neg_first)
ua_p2 = _em(ua_pos_last);   ua_n2 = _em(ua_neg_last)
ua_d1 = ua_p1 - ua_n1;      ua_d2 = ua_p2 - ua_n2

uv_p1 = _em(upvp_pos_first);  uv_n1 = _em(upvp_neg_first)
uv_p2 = _em(upvp_pos_last);   uv_n2 = _em(upvp_neg_last)
uv_d1 = uv_p1 - uv_n1;      uv_d2 = uv_p2 - uv_n2

mom_p1 = _em(momentum_pos_first);  mom_n1 = _em(momentum_neg_first)
mom_p2 = _em(momentum_pos_last);   mom_n2 = _em(momentum_neg_last)
mom_d1 = mom_p1 - mom_n1;          mom_d2 = mom_p2 - mom_n2


#%%
jet_loc_first = 47.56392575
jet_loc_last = 49.4291537

# +/- 10 degrees around the jet location
lat_min_first = jet_loc_first - 10
lat_max_first = jet_loc_first + 10
lat_min_last = jet_loc_last - 10
lat_max_last = jet_loc_last + 10


# %% Meridional gradient of ua (∂ua/∂y, units: s⁻¹ = m s⁻¹ per meter)
def _ua_meridional_grad(da):
    """Compute ∂ua/∂y in s⁻¹. Converts lat degrees → meters (R·Δlat·π/180)
    then applies np.gradient along the lat axis."""
    R = 6371229.0  # Earth radius in metres
    lat_rad = np.deg2rad(da.lat.values)   # radians
    y_m = R * lat_rad                     # metres along meridian
    grad_vals = np.gradient(da.values, y_m, axis=da.dims.index('lat'))
    return xr.DataArray(grad_vals, coords=da.coords, dims=da.dims)

uag_p1 = _ua_meridional_grad(ua_p1)*86400;  uag_n1 = _ua_meridional_grad(ua_n1)*86400
uag_p2 = _ua_meridional_grad(ua_p2)*86400;  uag_n2 = _ua_meridional_grad(ua_n2)*86400
uag_d1 = uag_p1 - uag_n1
uag_d2 = uag_p2 - uag_n2

# %% Plot – difference only: ua, ua_grad, upvp
ua_dlev   = np.arange(-12, 13, 2)
uag_dlev   = np.arange(-2, 2.1, 0.4)   # day⁻¹ (×86400 from s⁻¹)
uv_dlev   = np.arange(-20, 21, 4)
mom_dlev  = np.arange(-3, 3.1, 0.5)    # m/s/day


diff_rows = [
    (ua_d1,  ua_d2,  ua_dlev,  "$\Delta u$ / m s$^{-1}$"),
    (uag_d1, uag_d2, uag_dlev,  "$\\Delta(\\partial_y u)$ / day$^{-1}$"),
    (uv_d1,  uv_d2,  uv_dlev,  "$\Delta(u'v')$ / m$^2$ s$^{-2}$"),
    (mom_d1, mom_d2, mom_dlev,  "$\Delta(\\partial_y u'v')$ / m s$^{-1}$ day$^{-1}$"),
]

fig2, axes2 = plt.subplots(
    nrows=4, ncols=3,
    figsize=(10, 9),
    constrained_layout=False,
    sharey=True,
    sharex=True,
)
fig2.subplots_adjust(left=0.09, right=0.83, top=0.93, bottom=0.08, wspace=0.08, hspace=0.22)


for row_idx, (d1, d2, dlvl, label) in enumerate(diff_rows):
    t   = d1.time.values
    lat = d1.lat.values
    dd  = d2 - d1  # change between decades
    ddlv = dlvl / 2  # half levels for the difference column

    for col_idx, (data, lvl) in enumerate([(d1, dlvl), (d2, dlvl), (dd, ddlv)]):
        ax = axes2[row_idx, col_idx]
        cf = ax.contourf(t, lat, data.values.T, levels=lvl, cmap="RdBu_r", extend="both")
        ax.contour(t, lat, data.values.T,
                   levels=[l for l in lvl if l != 0], colors="k", linewidths=0.5)
        if col_idx == 0:
            cf_main = cf  # capture for colorbar base (dlvl scale)

    # Dual-axis colorbar: left ticks = dlvl (cols 0&1), right ticks = ddlv (col 2)
    bbox = axes2[row_idx, 2].get_position()
    cax2 = fig2.add_axes([bbox.x1 + 0.04, bbox.y0, 0.016, bbox.height])
    cb2 = fig2.colorbar(cf_main, cax=cax2, orientation="vertical", extend="both")
    cb2.set_ticks(dlvl)
    cb2.ax.tick_params(labelsize=7)
    cb2.ax.yaxis.set_ticks_position("left")
    cb2.ax.yaxis.set_label_position("left")
    cb2.ax.set_title(label, fontsize=7, pad=4)

    pmin, pmax = float(dlvl[0]), float(dlvl[-1])
    dmin, dmax = float(ddlv[0]), float(ddlv[-1])
    ax_sec = cax2.secondary_yaxis(
        "right",
        functions=(lambda x, pm=pmin, pm2=pmax, dm=dmin, dm2=dmax:
                       dm + (x - pm) * (dm2 - dm) / (pm2 - pm),
                   lambda x, pm=pmin, pm2=pmax, dm=dmin, dm2=dmax:
                       pm + (x - dm) * (pm2 - pm) / (dm2 - dm)),
    )
    ax_sec.set_yticks(ddlv)
    ax_sec.tick_params(labelsize=7)

    # For uag row: no special formatter needed (values now in day⁻¹)
    if row_idx == 1:
        pass

# axis labels and panel letters
for i, ax in enumerate(axes2.flatten()):
    if i >= 9:
        ax.set_xlabel("Lag (days)", fontsize=8)
    if i % 3 == 0:
        ax.set_ylabel("Latitude (°N)", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.text(0.02, 0.98, chr(97 + i), transform=ax.transAxes,
            fontsize=9, fontweight="bold", va="top", ha="left")
    ax.set_xlim(-5, 20)
    # dotted vertical line at lag=0
    ax.axvline(0, color="k", linestyle=":", linewidth=0.5)

titles = ["1850s", "2090s", "2090s - 1850s"]
for ax, title in zip(axes2[0, :], titles):
    ax.set_title(title, fontsize=8)

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0after_defense/feedback_diff_ua_grad_upvp.pdf",
    dpi=300,
)

# %%
