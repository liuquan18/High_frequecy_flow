# %%
import importlib.readers
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.plotting.util import erase_white_line
from src.plotting.util import lon2x
from matplotlib.ticker import ScalarFormatter
from src.plotting.prime_data import vert_integrate

import matplotlib.colors as mcolors
import cartopy
import glob

# %%
import src.plotting.util as util
import src.moisture.longitudinal_contrast as lc

import importlib

importlib.reload(util)
# %%
from src.plotting.prime_data import read_composite_MPI  # noqa: E402
from src.plotting.prime_data import read_MPI_GE_uhat
#%%
def read_climatology(var, decade, **kwargs):

    name = kwargs.get("name", var)  # default name is the same as var
    if var == "uhat":
        data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/*{decade}*.nc"

    elif var == "upvp":
        data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/upvp_monthly_ensmean/upvp_monmean_ensmean_{decade}*.nc"
    elif var == "usvs":
        data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/usvs_monthly_ensmean/usvs_monmean_ensmean_{decade}*.nc"
    elif var == "vpetp":
        data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vpetp_monthly_ensmean/vpetp_monmean_ensmean_{decade}*.nc"
    elif var == "vptp":
        data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vptp_monthly_ensmean/vptp_monmean_ensmean_{decade}*.nc"

    file = glob.glob(data_path)
    if len(file) == 0:
        raise ValueError(f"no file found for {var} in {decade}")
    data = xr.open_dataset(file[0])
    data = data[name]

    if "time" in data.dims:
        data = data.mean(dim="time")

    return erase_white_line(data)

#%%
def read_composite_ano(var, decade, phase, **kwargs):

    name = kwargs.get("name", var)  # default name is the same as var
    if var == 'uhat':
        composite_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/composite/"
        if decade == 1850:
            if phase == 'pos':
                composite_path += "jetstream_MJJAS_first10_pos.nc"
            elif phase == 'neg':
                composite_path += "jetstream_MJJAS_first10_neg.nc"
        elif decade == 2090:
            if phase == 'pos':
                composite_path += "jetstream_MJJAS_last10_pos.nc"
            elif phase == 'neg':
                composite_path += "jetstream_MJJAS_last10_neg.nc"

        composite_ano = xr.open_dataarray(composite_path)

    # 5-0 days before
    elif var == "upvp":
        upvp = read_composite_MPI("upvp", "ua", decade = decade, before = "5_0", return_as = phase)
        try:
            composite_ano = upvp.sel(plev = 25000)
        except KeyError:
            composite_ano = upvp
    elif var == "usvs":
        usvs = read_composite_MPI("usvs", "usvs", decade = decade, before = "5_0", return_as = phase)
        try:
            composite_ano = usvs.sel(plev = 25000)
        except KeyError:
            composite_ano = usvs
    
    # -15 - 5 days before
    elif var == "vpetp":
        vpetp = read_composite_MPI("vpetp", "vpetp",decade = decade, before = "15_5", return_as = phase)
        composite_ano = vpetp.sel(plev = 85000)
    elif var == "vptp":
        vptp = read_composite_MPI("vptp", "vptp", decade = decade, before = "15_5", return_as = phase)
        composite_ano = vptp.sel(plev = 85000)

    return erase_white_line(composite_ano)

    
#%%

##### climatology ######
# %%
uhat_first = read_climatology("uhat", 1850, name="ua")
uhat_last = read_climatology("uhat", 2091, name="ua") # 2090 

# eddy driven jet
uhat_first = uhat_first.sel(plev = slice(100000, 85000)).mean(dim = "plev")
uhat_last = uhat_last.sel(plev = slice(100000, 85000)).mean(dim = "plev")

#%%
upvp_first = read_climatology("upvp", 1850, name="ua")
upvp_last = read_climatology("upvp", 2090, name="ua")
#%%
usvs_first = read_climatology("usvs", 1850, name="usvs")
usvs_last = read_climatology("usvs", 2090, name="usvs")
#%%
upvp_first = upvp_first.sel(plev = 25000)
upvp_last = upvp_last.sel(plev = 25000)
#%%
vpetp_first = read_climatology("vpetp", 1850, name="vpetp")
vpetp_last = read_climatology("vpetp", 2090, name="vpetp")
#%%
vpetp_first = vpetp_first.sel(plev = 85000)
vpetp_last = vpetp_last.sel(plev = 85000)
#%%
###### pos anomaly ######
uhat_first_pos = read_composite_ano("uhat", 1850, "pos", name="ua")
uhat_last_pos = read_composite_ano("uhat", 2090, "pos", name="ua")

upvp_first_pos = read_composite_ano("upvp", 1850, "pos", name="ua")
upvp_last_pos = read_composite_ano("upvp", 2090, "pos", name="ua")

vpetp_first_pos = read_composite_ano("vpetp", 1850, "pos", name="vpetp")
vpetp_last_pos = read_composite_ano("vpetp", 2090, "pos", name="vpetp")
####### neg anomaly ######
uhat_first_neg = read_composite_ano("uhat", 1850, "neg", name="ua")
uhat_last_neg = read_composite_ano("uhat", 2090, "neg", name="ua")

upvp_first_neg = read_composite_ano("upvp", 1850, "neg", name="ua")
upvp_last_neg = read_composite_ano("upvp", 2090, "neg", name="ua")

vpetp_first_neg = read_composite_ano("vpetp", 1850, "neg", name="vpetp")
vpetp_last_neg = read_composite_ano("vpetp", 2090, "neg", name="vpetp")




# %%
temp_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/temp_seq.txt"
)
temp_cmap_seq = mcolors.ListedColormap(temp_cmap_seq, name="temp_div")

temp_cmap_div = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/temp_div.txt"
)
temp_cmap_div = mcolors.ListedColormap(temp_cmap_div, name="temp_div")

prec_cmap_seq = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_seq.txt"
)
prec_cmap_seq = mcolors.ListedColormap(prec_cmap_seq, name="prec_div")

prec_cmap_div = np.loadtxt(
    "/work/mh0033/m300883/High_frequecy_flow/data/colormaps-master/continuous_colormaps_rgb_0-1/prec_div.txt"
)
prec_cmap_div = mcolors.ListedColormap(prec_cmap_div, name="prec_div")

# %%
uhat_levels_div = np.arange(-12, 13, 2)
upvp_levels = np.arange(-40, 41, 5)
upvp_levels_div = np.arange(-20, 21, 5)
vptp_levels = np.arange(-20, 21, 5)
vptp_levels_div = np.arange(-1.2, 1.3, 0.4)

scale_div = 0.5

#%%

# plot uhat, first row first10 years, second row last10 years
# first col climatology, second col pos, third col neg 
# #%%
fig, axes = plt.subplots(
    2, 3, figsize=(12, 10), subplot_kw={"projection": ccrs.Orthographic(-30, 90)}
)

# plot climatology
uhat_first.plot.contourf(
    ax=axes[0, 0],
    levels=uhat_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
uhat_clim = uhat_last.plot.contourf(
    ax=axes[1, 0],
    levels=uhat_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

# plot pos
uhat_first_pos.plot.contourf(
    ax=axes[0, 1],
    levels=uhat_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
uhat_pos = uhat_last_pos.plot.contourf(
    ax=axes[1, 1],
    levels=uhat_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)


# plot neg
uhat_first_neg.plot.contourf(
    ax=axes[0, 2],
    levels=uhat_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)
uhat_neg = uhat_last_neg.plot.contourf(
    ax=axes[1, 2],
    levels=uhat_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
)

# add colorbar at the bottom of each column
cbar_ax1 = fig.add_axes([0.07, 0.05, 0.2, 0.02])  # [left, bottom, width, height]
cbar_ax2 = fig.add_axes([0.4, 0.05, 0.2, 0.02])
cbar_ax3 = fig.add_axes([0.73, 0.05, 0.2, 0.02])

fig.colorbar(uhat_clim, cax=cbar_ax1, orientation="horizontal", label=r"$\overline{u} / m s^{-1}$")
fig.colorbar(uhat_pos, cax=cbar_ax2, orientation="horizontal", label=r"$\overline{u} / m s^{-1}$")
fig.colorbar(uhat_neg, cax=cbar_ax3, orientation="horizontal", label=r"$\overline{u} / m s^{-1}$")

for ax in axes.flatten():
    ax.coastlines()
    # add gidlines at lat every 20 degree, and lon every 60 degree
    ax.gridlines(draw_labels=False, linewidth=0.5, linestyle="dotted")
    ax.set_global()

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")

    axes[0, 0].set_title('climatology')
    axes[0, 1].set_title('NAO pos anomaly')
    axes[0, 2].set_title('NAO neg anomaly')

# add a, b, c
for i, ax in enumerate(axes.flatten()):
    ax.text(
        0.02,
        0.95,
        f"{chr(97+i)}",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
    )

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/climatology_anomaly/uhat_clim_ano.pdf", dpi=300, bbox_inches="tight")

# %%
# plot upvp, first row first10 years, second row last10 years
# first col climatology, second col pos, third col neg 
# #%%
fig, axes = plt.subplots(
    2, 3, figsize=(12, 10), subplot_kw={"projection": ccrs.Orthographic(-30, 90)}
)

# plot climatology
upvp_first.plot.contourf(
    ax=axes[0, 0],
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend='both',
)
upvp_clim = upvp_last.plot.contourf(
    ax=axes[1, 0],
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend='both',
)

# plot pos
upvp_first_pos.plot.contourf(
    ax=axes[0, 1],
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend='both',
)
upvp_pos = upvp_last_pos.plot.contourf(
    ax=axes[1, 1],
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend='both',
)


# plot neg
upvp_first_neg.plot.contourf(
    ax=axes[0, 2],
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend='both',
)
upvp_neg = upvp_last_neg.plot.contourf(
    ax=axes[1, 2],
    levels=upvp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend='both',
)

# add colorbar at the bottom of each column
cbar_ax1 = fig.add_axes([0.07, 0.05, 0.2, 0.02])  # [left, bottom, width, height]
cbar_ax2 = fig.add_axes([0.4, 0.05, 0.2, 0.02])
cbar_ax3 = fig.add_axes([0.73, 0.05, 0.2, 0.02])

fig.colorbar(upvp_clim, cax=cbar_ax1, orientation="horizontal", label=r"$\overline{u'v'} / m^2 s^{-2}$")
fig.colorbar(upvp_pos, cax=cbar_ax2, orientation="horizontal", label=r"$\overline{u'v'} / m^2 s^{-2}$")
fig.colorbar(upvp_neg, cax=cbar_ax3, orientation="horizontal", label=r"$\overline{u'v'} / m^2 s^{-2}$")

for ax in axes.flatten():
    ax.coastlines()
    # add gidlines at lat every 20 degree, and lon every 60 degree
    ax.gridlines(draw_labels=False, linewidth=0.5, linestyle="dotted")
    ax.set_global()

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")

    axes[0, 0].set_title('climatology')
    axes[0, 1].set_title('NAO pos anomaly')
    axes[0, 2].set_title('NAO neg anomaly')

# add a, b, c
for i, ax in enumerate(axes.flatten()):
    ax.text(
        0.02,
        0.95,
        f"{chr(97+i)}",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
    )

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/climatology_anomaly/upvp_clim_ano.pdf", dpi=300, bbox_inches="tight")

# %%
fig, axes = plt.subplots(
    2, 3, figsize=(12, 10), subplot_kw={"projection": ccrs.Orthographic(-30, 90)}
)

# plot climatology
vpetp_first.plot.contourf(
    ax=axes[0, 0],
    levels=vptp_levels,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend='both',
)
vpetp_clim = vpetp_last.plot.contourf(
    ax=axes[1, 0],
    levels=vptp_levels,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend='both',
)

# plot pos
vpetp_first_pos.plot.contourf(
    ax=axes[0, 1],
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend='both',
)
vpetp_pos = vpetp_last_pos.plot.contourf(
    ax=axes[1, 1],
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend='both',
)


# plot neg
vpetp_first_neg.plot.contourf(
    ax=axes[0, 2],
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend='both',
)
vpetp_neg = vpetp_last_neg.plot.contourf(
    ax=axes[1, 2],
    levels=vptp_levels_div,
    cmap=temp_cmap_div,
    add_colorbar=False,
    transform=ccrs.PlateCarree(),
    extend='both',
)

# add colorbar at the bottom of each column
cbar_ax1 = fig.add_axes([0.07, 0.05, 0.2, 0.02])  # [left, bottom, width, height]
cbar_ax2 = fig.add_axes([0.4, 0.05, 0.2, 0.02])
cbar_ax3 = fig.add_axes([0.73, 0.05, 0.2, 0.02])

fig.colorbar(vpetp_clim, cax=cbar_ax1, orientation="horizontal", label=r"$\overline{v'\theta_e'} / K m s^{-1}$")
fig.colorbar(vpetp_pos, cax=cbar_ax2, orientation="horizontal", label=r"$\overline{v'\theta_e'} / K m s^{-1}$")
fig.colorbar(vpetp_neg, cax=cbar_ax3, orientation="horizontal", label=r"$\overline{v'\theta_e'} / K m s^{-1}$")

for ax in axes.flatten():
    ax.coastlines()
    # add gidlines at lat every 20 degree, and lon every 60 degree
    ax.gridlines(draw_labels=False, linewidth=0.5, linestyle="dotted")
    ax.set_global()

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")

    axes[0, 0].set_title('climatology')
    axes[0, 1].set_title('NAO pos anomaly')
    axes[0, 2].set_title('NAO neg anomaly')

# add a, b, c
for i, ax in enumerate(axes.flatten()):
    ax.text(
        0.02,
        0.95,
        f"{chr(97+i)}",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
    )

plt.tight_layout()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/climatology_anomaly/vpetp_clim_ano.pdf", dpi=300, bbox_inches="tight")

# %%
