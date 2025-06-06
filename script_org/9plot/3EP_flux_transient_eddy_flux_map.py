# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from src.dynamics.EP_flux import PlotEPfluxArrows
from src.data_helper import read_composite
from src.plotting.util import erase_white_line, map_smooth
import importlib
from mpl_toolkits.axes_grid1 import make_axes_locatable

importlib.reload(read_composite)

read_EP_flux = read_composite.read_EP_flux


# %%
levels_vq = np.arange(-3, 3.1, 0.5)
levels_uv = np.arange(-1.5, 1.6, 0.5)
levels_vt = np.arange(-3, 3.1, 0.5)
# %%
# read transient EP flux for positive and negative phase
# read data for first decade with region = western
Tphi_pos_first, Tp_pos_first, Tdivphi_pos_first, Tdiv_p_pos_first = read_EP_flux(
    phase="pos",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)
Tphi_neg_first, Tp_neg_first, Tdivphi_neg_first, Tdiv_p_neg_first = read_EP_flux(
    phase="neg",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)


# last decade region
Tphi_pos_last, Tp_pos_last, Tdivphi_pos_last, Tdiv_p_pos_last = read_EP_flux(
    phase="pos",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)
Tphi_neg_last, Tp_neg_last, Tdivphi_neg_last, Tdiv_p_neg_last = read_EP_flux(
    phase="neg",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)
# %%
# read climatological EP flux
Tphi_clima_first, Tp_clima_first, Tdivphi_clima_first, Tdiv_p_clima_first = (
    read_EP_flux(
        phase="clima",
        decade=1850,
        eddy="transient",
        ano=False,
        lon_mean=False,
        region=None,
    )
)
Tphi_clima_last, Tp_clima_last, Tdivphi_clima_last, Tdiv_p_clima_last = read_EP_flux(
    phase="clima",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)
# %%
Tdivphi_pos_first_ano = Tdivphi_pos_first - Tdivphi_clima_first
Tdiv_p_pos_first_ano = Tdiv_p_pos_first - Tdiv_p_clima_first

Tdivphi_neg_first_ano = Tdivphi_neg_first - Tdivphi_clima_first
Tdiv_p_neg_first_ano = Tdiv_p_neg_first - Tdiv_p_clima_first

Tdivphi_pos_last_ano = Tdivphi_pos_last - Tdivphi_clima_last
Tdiv_p_pos_last_ano = Tdiv_p_pos_last - Tdiv_p_clima_last

Tdivphi_neg_last_ano = Tdivphi_neg_last - Tdivphi_clima_last
Tdiv_p_neg_last_ano = Tdiv_p_neg_last - Tdiv_p_clima_last
# %%
# erase white line
Tdivphi_pos_first_ano = erase_white_line(Tdivphi_pos_first_ano)
Tdiv_p_pos_first_ano = erase_white_line(Tdiv_p_pos_first_ano)
Tdivphi_neg_first_ano = erase_white_line(Tdivphi_neg_first_ano)
Tdiv_p_neg_first_ano = erase_white_line(Tdiv_p_neg_first_ano)
Tdivphi_pos_last_ano = erase_white_line(Tdivphi_pos_last_ano)
Tdiv_p_pos_last_ano = erase_white_line(Tdiv_p_pos_last_ano)
Tdivphi_neg_last_ano = erase_white_line(Tdivphi_neg_last_ano)
Tdiv_p_neg_last_ano = erase_white_line(Tdiv_p_neg_last_ano)
#%%
# erase white line for climatology
Tdivphi_clima_first = erase_white_line(Tdivphi_clima_first)
Tdiv_p_clima_first = erase_white_line(Tdiv_p_clima_first)
Tdivphi_clima_last = erase_white_line(Tdivphi_clima_last)
Tdiv_p_clima_last = erase_white_line(Tdiv_p_clima_last)
# %%
# smooth the data
Tdivphi_pos_first_ano = map_smooth(Tdivphi_pos_first_ano, 5, 5)
Tdiv_p_pos_first_ano = map_smooth(Tdiv_p_pos_first_ano, 5, 5)
Tdivphi_neg_first_ano = map_smooth(Tdivphi_neg_first_ano, 5, 5)
Tdiv_p_neg_first_ano = map_smooth(Tdiv_p_neg_first_ano, 5, 5)
Tdivphi_pos_last_ano = map_smooth(Tdivphi_pos_last_ano, 5, 5)
Tdiv_p_pos_last_ano = map_smooth(Tdiv_p_pos_last_ano, 5, 5)
Tdivphi_neg_last_ano = map_smooth(Tdivphi_neg_last_ano, 5, 5)
Tdiv_p_neg_last_ano = map_smooth(Tdiv_p_neg_last_ano, 5, 5)

# %%
# read steady EP flux for positive and negative phase
Sphi_pos_first, Sp_pos_first, Sdivphi_pos_first, Sdiv_p_pos_first = read_EP_flux(
    phase="pos",
    decade=1850,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)
Sphi_neg_first, Sp_neg_first, Sdivphi_neg_first, Sdiv_p_neg_first = read_EP_flux(
    phase="neg",
    decade=1850,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)

# last decade
Sphi_pos_last, Sp_pos_last, Sdivphi_pos_last, Sdiv_p_pos_last = read_EP_flux(
    phase="pos",
    decade=2090,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)
Sphi_neg_last, Sp_neg_last, Sdivphi_neg_last, Sdiv_p_neg_last = read_EP_flux(
    phase="neg",
    decade=2090,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)
# %%
# read climatological EP flux
Sphi_clima_first, Sp_clima_first, Sdivphi_clima_first, Sdiv_p_clima_first = (
    read_EP_flux(
        phase="clima",
        decade=1850,
        eddy="steady",
        ano=False,
        lon_mean=False,
        region=None,
    )
)
Sphi_clima_last, Sp_clima_last, Sdivphi_clima_last, Sdiv_p_clima_last = read_EP_flux(
    phase="clima",
    decade=2090,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)
# %%
# anomaly
Sdivphi_pos_first_ano = Sdivphi_pos_first - Sdivphi_clima_first
Sdiv_p_pos_first_ano = Sdiv_p_pos_first - Sdiv_p_clima_first

Sdivphi_neg_first_ano = Sdivphi_neg_first - Sdivphi_clima_first
Sdiv_p_neg_first_ano = Sdiv_p_neg_first - Sdiv_p_clima_first

Sdivphi_pos_last_ano = Sdivphi_pos_last - Sdivphi_clima_last
Sdiv_p_pos_last_ano = Sdiv_p_pos_last - Sdiv_p_clima_last

Sdivphi_neg_last_ano = Sdivphi_neg_last - Sdivphi_clima_last
Sdiv_p_neg_last_ano = Sdiv_p_neg_last - Sdiv_p_clima_last
# %%
# erase white line
Sdivphi_pos_first_ano = erase_white_line(Sdivphi_pos_first_ano)
Sdiv_p_pos_first_ano = erase_white_line(Sdiv_p_pos_first_ano)
Sdivphi_neg_first_ano = erase_white_line(Sdivphi_neg_first_ano)
Sdiv_p_neg_first_ano = erase_white_line(Sdiv_p_neg_first_ano)
Sdivphi_pos_last_ano = erase_white_line(Sdivphi_pos_last_ano)
Sdiv_p_pos_last_ano = erase_white_line(Sdiv_p_pos_last_ano)
Sdivphi_neg_last_ano = erase_white_line(Sdivphi_neg_last_ano)
Sdiv_p_neg_last_ano = erase_white_line(Sdiv_p_neg_last_ano)
# %%
# erase white line of climatology
Sdivphi_clima_first = erase_white_line(Sdivphi_clima_first)
Sdiv_p_clima_first = erase_white_line(Sdiv_p_clima_first)
Sdivphi_clima_last = erase_white_line(Sdivphi_clima_last)
Sdiv_p_clima_last = erase_white_line(Sdiv_p_clima_last)
# %%
# smooth the data
Sdivphi_pos_first_ano = map_smooth(Sdivphi_pos_first_ano, 5, 5)
Sdiv_p_pos_first_ano = map_smooth(Sdiv_p_pos_first_ano, 5, 5)
Sdivphi_neg_first_ano = map_smooth(Sdivphi_neg_first_ano, 5, 5)
Sdiv_p_neg_first_ano = map_smooth(Sdiv_p_neg_first_ano, 5, 5)
Sdivphi_pos_last_ano = map_smooth(Sdivphi_pos_last_ano, 5, 5)
Sdiv_p_pos_last_ano = map_smooth(Sdiv_p_pos_last_ano, 5, 5)
Sdivphi_neg_last_ano = map_smooth(Sdivphi_neg_last_ano, 5, 5)
Sdiv_p_neg_last_ano = map_smooth(Sdiv_p_neg_last_ano, 5, 5)


# %%
# transient eddies
fig, axes = plt.subplots(
    2,
    3,
    figsize=(12, 9),
    subplot_kw={"projection": ccrs.Orthographic(-30, 70)},
    sharex=True,
    sharey=False,
)
# first row for pos
# contourf for first decade
# contour for last decade
# v'q'
vq_color = (
    (Tdivphi_pos_first_ano + Tdiv_p_pos_first_ano)
    .sel(plev=85000)
    .plot.contourf(
        ax=axes[0, 0],
        levels=levels_vq,
        cmap="RdBu_r",
        add_colorbar=False,
        extend="both",
        transform=ccrs.PlateCarree(),
    )
)


(Tdivphi_pos_last_ano + Tdiv_p_pos_last_ano).sel(plev=85000).plot.contour(
    ax=axes[0, 0],
    levels=[l for l in levels_vq if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# second col for u'v'
uv_color = Tdivphi_pos_first_ano.sel(plev=25000).plot.contourf(
    ax=axes[0, 1],
    levels=levels_uv,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
Tdivphi_pos_last_ano.sel(plev=25000).plot.contour(
    ax=axes[0, 1],
    levels=[l for l in levels_uv if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# third col for v't'
vt_color = Tdiv_p_pos_first_ano.sel(plev=85000).plot.contourf(
    ax=axes[0, 2],
    levels=levels_vt,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
Tdiv_p_pos_last_ano.sel(plev=85000).plot.contour(
    ax=axes[0, 2],
    levels=[l for l in levels_vt if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)
# second row for neg
# first col for v'q'
vq_color_neg = (
    (Tdivphi_neg_first_ano + Tdiv_p_neg_first_ano)
    .sel(plev=85000)
    .plot.contourf(
        ax=axes[1, 0],
        levels=levels_vq,
        cmap="RdBu_r",
        add_colorbar=False,
        extend="both",
        transform=ccrs.PlateCarree(),
    )
)
(Tdivphi_neg_last_ano + Tdiv_p_neg_last_ano).sel(plev=85000).plot.contour(
    ax=axes[1, 0],
    levels=[l for l in levels_vq if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# second col for u'v'
uv_color_neg = Tdivphi_neg_first_ano.sel(plev=25000).plot.contourf(
    ax=axes[1, 1],
    levels=levels_uv,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
Tdivphi_neg_last_ano.sel(plev=25000).plot.contour(
    ax=axes[1, 1],
    levels=[l for l in levels_uv if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# third col for v't'
vt_color_neg = Tdiv_p_neg_first_ano.sel(plev=85000).plot.contourf(
    ax=axes[1, 2],
    levels=levels_vt,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
Tdiv_p_neg_last_ano.sel(plev=85000).plot.contour(
    ax=axes[1, 2],
    levels=[l for l in levels_vt if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)


# add cax under the second row

# Add colorbar axes using fig.add_axes for better alignment with tight_layout

# Get position of the bottom row axes to align colorbars
fig.tight_layout()
fig.subplots_adjust(bottom=0.12)  # leave space for colorbars
# Calculate colorbar axes positions (shrink by 0.8)
width_shrink = axes[1, 0].get_position().width * 0.8
offset = (axes[1, 0].get_position().width - width_shrink) / 2

cax_vq = fig.add_axes([
    axes[1, 0].get_position().x0 + offset,
    0.08,
    width_shrink,
    0.02
])
cax_uv = fig.add_axes([
    axes[1, 1].get_position().x0 + offset,
    0.08,
    width_shrink,
    0.02
])
cax_vt = fig.add_axes([
    axes[1, 2].get_position().x0 + offset,
    0.08,
    width_shrink,
    0.02
])

fig.colorbar(
    vq_color,
    cax=cax_vq,
    orientation="horizontal",
    label=r"$v'q'$ [m$^2$ s$^{-2}$]",
)
fig.colorbar(
    uv_color,
    cax=cax_uv,
    orientation="horizontal",
    label=r"$- \frac{\partial}{\partial y} \overline{u'v'}$ [m$^2$ s$^{-2}$]",
)
fig.colorbar(
    vt_color,
    cax=cax_vt,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial z} (\frac{f_0}{N^2}\overline{v'\theta_e'})$ [m$^2$ s$^{-2}$]",
)

# no y labels from second row on, no x labels at the frist row
for ax in axes[0, :]:
    ax.set_xlabel("")
for ax in axes[:, 0]:
    ax.set_ylabel("Pressure [Pa]")

for ax in axes[:, 1:].flat:
    ax.set_ylabel("")

for ax in axes[1, :]:
    ax.set_xlabel("Latitude [°N]")

for ax in axes.flat:
    ax.coastlines(color="grey", linewidth=1)
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="dotted",
    )
    ax.set_title("")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0EP_flux/transient_flux_component_map.pdf",
    bbox_inches="tight",
    dpi=300,
)
#%%
Slevels_vq = np.arange(-10, 10.1, 2)
Slevels_uv = np.arange(-1.5, 1.6, 0.5)
Slevels_vt = np.arange(-10, 10.1, 2)

#%%
# steady eddies
fig, axes = plt.subplots(
    2,
    3,
    figsize=(12, 9),
    subplot_kw={"projection": ccrs.Orthographic(-30, 70)},
    sharex=True,
    sharey=False,
)
# first row for pos
# v'q'
vq_color = (
    (Sdivphi_pos_first_ano + Sdiv_p_pos_first_ano)
    .sel(plev=85000)
    .plot.contourf(
        ax=axes[0, 0],
        levels=Slevels_vq,
        cmap="RdBu_r",
        add_colorbar=False,
        extend="both",
        transform=ccrs.PlateCarree(),
    )
)
(Sdivphi_pos_last_ano + Sdiv_p_pos_last_ano).sel(plev=85000).plot.contour(
    ax=axes[0, 0],
    levels=[l for l in Slevels_vq if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# u'v'
uv_color = Sdivphi_pos_first_ano.sel(plev=25000).plot.contourf(
    ax=axes[0, 1],
    levels=Slevels_uv,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
Sdivphi_pos_last_ano.sel(plev=25000).plot.contour(
    ax=axes[0, 1],
    levels=[l for l in Slevels_uv if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# v't'
vt_color = Sdiv_p_pos_first_ano.sel(plev=85000).plot.contourf(
    ax=axes[0, 2],
    levels=Slevels_vt,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
Sdiv_p_pos_last_ano.sel(plev=85000).plot.contour(
    ax=axes[0, 2],
    levels=[l for l in Slevels_vt if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)
# second row for neg
# v'q'
vq_color_neg = (
    (Sdivphi_neg_first_ano + Sdiv_p_neg_first_ano)
    .sel(plev=85000)
    .plot.contourf(
        ax=axes[1, 0],
        levels=Slevels_vq,
        cmap="RdBu_r",
        add_colorbar=False,
        extend="both",
        transform=ccrs.PlateCarree(),
    )
)
(Sdivphi_neg_last_ano + Sdiv_p_neg_last_ano).sel(plev=85000).plot.contour(
    ax=axes[1, 0],
    levels=[l for l in Slevels_vq if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# u'v'
uv_color_neg = Sdivphi_neg_first_ano.sel(plev=25000).plot.contourf(
    ax=axes[1, 1],
    levels=Slevels_uv,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
Sdivphi_neg_last_ano.sel(plev=25000).plot.contour(
    ax=axes[1, 1],
    levels=[l for l in Slevels_uv if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# v't'
vt_color_neg = Sdiv_p_neg_first_ano.sel(plev=85000).plot.contourf(
    ax=axes[1, 2],
    levels=Slevels_vt,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
Sdiv_p_neg_last_ano.sel(plev=85000).plot.contour(
    ax=axes[1, 2],
    levels=[l for l in Slevels_vt if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)

fig.tight_layout()
fig.subplots_adjust(bottom=0.12)
width_shrink = axes[1, 0].get_position().width * 0.8
offset = (axes[1, 0].get_position().width - width_shrink) / 2

cax_vq = fig.add_axes([
    axes[1, 0].get_position().x0 + offset,
    0.08,
    width_shrink,
    0.02
])
cax_uv = fig.add_axes([
    axes[1, 1].get_position().x0 + offset,
    0.08,
    width_shrink,
    0.02
])
cax_vt = fig.add_axes([
    axes[1, 2].get_position().x0 + offset,
    0.08,
    width_shrink,
    0.02
])

fig.colorbar(
    vq_color,
    cax=cax_vq,
    orientation="horizontal",
    label=r"$v'q'$ [m$^2$ s$^{-2}$]",
)
fig.colorbar(
    uv_color,
    cax=cax_uv,
    orientation="horizontal",
    label=r"$-\frac{\partial}{\partial y} \overline{u'v'}$ [m$^2$ s$^{-2}$]",
)
fig.colorbar(
    vt_color,
    cax=cax_vt,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial z} (\frac{f_0}{N^2}\overline{v'\theta_e'})$ [m$^2$ s$^{-2}$]",
)

for ax in axes[0, :]:
    ax.set_xlabel("")
for ax in axes[:, 0]:
    ax.set_ylabel("Pressure [Pa]")
for ax in axes[:, 1:].flat:
    ax.set_ylabel("")
for ax in axes[1, :]:
    ax.set_xlabel("Latitude [°N]")

for ax in axes.flat:
    ax.coastlines(color="grey", linewidth=1)
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="dotted",
    )
    ax.set_title("")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0EP_flux/steady_flux_component_map.pdf",
    bbox_inches="tight",
    dpi=300,
)
# %%
levels_vq_clima = np.arange(-30, 30.1, 5)
levels_uv_clima = np.arange(-5, 6, 1)
levels_vt_clima = np.arange(-30, 30.1, 5)

Slevels_vq_clima = np.arange(-50, 50.1, 10)
Slevels_uv_clima = np.arange(-5, 6, 1)
Slevels_vt_clima = np.arange(-50, 50.1, 10)

# %%
# plot the climatology maps (matching the style of previous plots)
fig, axes = plt.subplots(
    2,
    3,
    figsize=(12, 9),
    subplot_kw={"projection": ccrs.Orthographic(-30, 70)},
    sharex=True,
    sharey=False,
)

# v'q' transient
vq_color = (
    (Tdivphi_clima_first + Tdiv_p_clima_first)
    .sel(plev=85000)
    .plot.contourf(
        ax=axes[0, 0],
        levels=levels_vq_clima,
        cmap="RdBu_r",
        add_colorbar=True,
        extend="both",
        transform=ccrs.PlateCarree(),
        cbar_kwargs={
            "orientation": "horizontal",
            "label": r"$v'q'$ [m$^2$ s$^{-2}$]",
            "shrink": 0.8,
            "pad": 0.05,
        },

    )
)
(Tdivphi_clima_last + Tdiv_p_clima_last).sel(plev=85000).plot.contour(
    ax=axes[0, 0],
    levels=[l for l in levels_vq_clima if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# u'v' transient
uv_color = Tdivphi_clima_first.sel(plev=25000).plot.contourf(
    ax=axes[0, 1],
    levels=levels_uv_clima,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={
        "orientation": "horizontal",
        "label": r"$-\frac{\partial}{\partial y} \overline{u'v'}$ [m$^2$ s$^{-2}$]",
        "shrink": 0.8,
        "pad": 0.05,
    },
)
Tdivphi_clima_last.sel(plev=25000).plot.contour(
    ax=axes[0, 1],
    levels=[l for l in levels_uv_clima if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# v't' transient
vt_color = Tdiv_p_clima_first.sel(plev=85000).plot.contourf(
    ax=axes[0, 2],
    levels=levels_vt_clima,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={
        "orientation": "horizontal",
        "label": r"$\frac{\partial}{\partial z} (\frac{f_0}{N^2}\overline{v'\theta_e'})$ [m$^2$ s$^{-2}$]",
        "shrink": 0.8,
        "pad": 0.05,
    },
)
Tdiv_p_clima_last.sel(plev=85000).plot.contour(
    ax=axes[0, 2],
    levels=[l for l in levels_vt_clima if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# v'q' steady
(Sdivphi_clima_first + Sdiv_p_clima_first).sel(plev=85000).plot.contourf(
    ax=axes[1, 0],
    levels=Slevels_vq_clima,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={
        "orientation": "horizontal",
        "label": r"$v'q'$ [m$^2$ s$^{-2}$]",
        "shrink": 0.8,
        "pad": 0.05,
    },
)
(Sdivphi_clima_last + Sdiv_p_clima_last).sel(plev=85000).plot.contour(
    ax=axes[1, 0],
    levels=[l for l in Slevels_vq_clima if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# u'v' steady
Sdivphi_clima_first.sel(plev=25000).plot.contourf(
    ax=axes[1, 1],
    levels=Slevels_uv_clima,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={
        "orientation": "horizontal",
        "label": r"$-\frac{\partial}{\partial y} \overline{u'v'}$ [m$^2$ s$^{-2}$]",
        "shrink": 0.8,
        "pad": 0.05,
    },
)
Sdivphi_clima_last.sel(plev=25000).plot.contour(
    ax=axes[1, 1],
    levels=[l for l in Slevels_uv_clima if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# v't' steady
Sdiv_p_clima_first.sel(plev=85000).plot.contourf(
    ax=axes[1, 2],
    levels=Slevels_vt_clima,
    cmap="RdBu_r",
    add_colorbar=True,
    extend="both",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={
        "orientation": "horizontal",
        "label": r"$\frac{\partial}{\partial z} (\frac{f_0}{N^2}\overline{v'\theta_e'})$ [m$^2$ s$^{-2}$]",
        "shrink": 0.8,
        "pad": 0.05,
    },
)
Sdiv_p_clima_last.sel(plev=85000).plot.contour(
    ax=axes[1, 2],
    levels=[l for l in Slevels_vt_clima if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)



# Axis labels and formatting
for ax in axes[0, :]:
    ax.set_xlabel("")
for ax in axes[:, 0]:
    ax.set_ylabel("Pressure [Pa]")
for ax in axes[:, 1:].flat:
    ax.set_ylabel("")
for ax in axes[1, :]:
    ax.set_xlabel("Latitude [°N]")

for ax in axes.flat:
    ax.coastlines(color="grey", linewidth=1)
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="dotted",
    )
    ax.set_title("")

plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0EP_flux/climatological_flux_component_map.pdf",
    bbox_inches="tight",
    dpi=300,
)

# %%
