# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.path as mpath
import matplotlib.ticker as mticker


from src.dynamics.EP_flux import PlotEPfluxArrows
from src.data_helper import read_composite
from src.plotting.util import erase_white_line, map_smooth
import importlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
from src.data_helper.read_variable import read_climatology
from metpy.units import units
import metpy.calc as mpcalc
import src.plotting.util as util

importlib.reload(read_composite)
importlib.reload(util)

read_EP_flux = read_composite.read_EP_flux
read_E_div = read_composite.read_E_div
read_comp_var = read_composite.read_comp_var
clip_map = util.clip_map


# %%
# read transient EP flux for positive and negative phase
# read data for first decade with region = western
_, _, Tdivphi_pos_first, Tdiv_p_pos_first = read_EP_flux(
    phase="pos",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)
_, _, Tdivphi_neg_first, Tdiv_p_neg_first = read_EP_flux(
    phase="neg",
    decade=1850,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)


# last decade region
_, _, Tdivphi_pos_last, Tdiv_p_pos_last = read_EP_flux(
    phase="pos",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)
_, _, Tdivphi_neg_last, Tdiv_p_neg_last = read_EP_flux(
    phase="neg",
    decade=2090,
    eddy="transient",
    ano=False,
    lon_mean=False,
    region=None,
)
# %%
# read climatological EP flux
_, _, Tdivphi_clima_first, Tdiv_p_clima_first = (
    read_EP_flux(
        phase="clima",
        decade=1850,
        eddy="transient",
        ano=False,
        lon_mean=False,
        region=None,
    )
)
_, _, Tdivphi_clima_last, Tdiv_p_clima_last = read_EP_flux(
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
#%%

TEx_pos_first, _ = read_E_div(
    phase="pos",
    decade=1850,
    eddy="transient",
)
TEx_neg_first, _ = read_E_div(
    phase="neg",
    decade=1850,
    eddy="transient",
)
TEx_pos_last, _ = read_E_div(
    phase="pos",
    decade=2090,
    eddy="transient",
)
TEx_neg_last, _ = read_E_div(
    phase="neg",
    decade=2090,
    eddy="transient",
)

# read climatological E_div_x
TEx_clima_first, _ = read_E_div(
    phase="clima",
    decade=1850,
    eddy="transient",
)
TEx_clima_last, _ = read_E_div(
    phase="clima",
    decade=2090,
    eddy="transient",
)

#%%
TEx_pos_first_ano = TEx_pos_first - TEx_clima_first
TEx_neg_first_ano = TEx_neg_first - TEx_clima_first
TEx_pos_last_ano = TEx_pos_last - TEx_clima_last
TEx_neg_last_ano = TEx_neg_last - TEx_clima_last

# erase white line
TEx_pos_first_ano = erase_white_line(TEx_pos_first_ano)
TEx_neg_first_ano = erase_white_line(TEx_neg_first_ano)
TEx_pos_last_ano = erase_white_line(TEx_pos_last_ano)
TEx_neg_last_ano = erase_white_line(TEx_neg_last_ano)

# erase white line for climatology
TEx_clima_first = erase_white_line(TEx_clima_first)
TEx_clima_last = erase_white_line(TEx_clima_last)

#%%
# smooth the data
TEx_pos_first_ano = map_smooth(TEx_pos_first_ano, 5, 5)
TEx_neg_first_ano = map_smooth(TEx_neg_first_ano, 5, 5)
TEx_pos_last_ano = map_smooth(TEx_pos_last_ano, 5, 5)
TEx_neg_last_ano = map_smooth(TEx_neg_last_ano, 5, 5)

TEx_clima_first = map_smooth(TEx_clima_first, 5, 5)
TEx_clima_last = map_smooth(TEx_clima_last, 5, 5)

# %%
# read steady EP flux for positive and negative phase
_, _, Sdivphi_pos_first, Sdiv_p_pos_first = read_EP_flux(
    phase="pos",
    decade=1850,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)
_, _, Sdivphi_neg_first, Sdiv_p_neg_first = read_EP_flux(
    phase="neg",
    decade=1850,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)

# last decade
_, _, Sdivphi_pos_last, Sdiv_p_pos_last = read_EP_flux(
    phase="pos",
    decade=2090,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)
_, _, Sdivphi_neg_last, Sdiv_p_neg_last = read_EP_flux(
    phase="neg",
    decade=2090,
    eddy="steady",
    ano=False,
    lon_mean=False,
    region=None,
)
# %%
# read climatological EP flux
_, _, Sdivphi_clima_first, Sdiv_p_clima_first = (
    read_EP_flux(
        phase="clima",
        decade=1850,
        eddy="steady",
        ano=False,
        lon_mean=False,
        region=None,
    )
)
_, _, Sdivphi_clima_last, Sdiv_p_clima_last = read_EP_flux(
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
#%%

# read E_div_x for steady eddies
SEx_pos_first, _ = read_E_div(
    phase="pos",
    decade=1850,
    eddy="steady",
)
SEx_neg_first, _ = read_E_div(
    phase="neg",
    decade=1850,
    eddy="steady",
)

SEx_pos_last, _ = read_E_div(
    phase="pos",
    decade=2090,
    eddy="steady",
)
SEx_neg_last, _ = read_E_div(
    phase="neg",
    decade=2090,
    eddy="steady",
)
# read climatological E_div_x for steady
SEx_clima_first, _ = read_E_div(
    phase="clima",
    decade=1850,
    eddy="steady",
)
SEx_clima_last, _ = read_E_div(
    phase="clima",
    decade=2090,
    eddy="steady",
)

#%%
# anomaly
SEx_pos_first_ano = SEx_pos_first - SEx_clima_first
SEx_neg_first_ano = SEx_neg_first - SEx_clima_first

SEx_pos_last_ano = SEx_pos_last - SEx_clima_last
SEx_neg_last_ano = SEx_neg_last - SEx_clima_last
#%%
# erase white line
SEx_pos_first_ano = erase_white_line(SEx_pos_first_ano)
SEx_neg_first_ano = erase_white_line(SEx_neg_first_ano)
SEx_pos_last_ano = erase_white_line(SEx_pos_last_ano)
SEx_neg_last_ano = erase_white_line(SEx_neg_last_ano)

# erase white line for climatology
SEx_clima_first = erase_white_line(SEx_clima_first)
SEx_clima_last = erase_white_line(SEx_clima_last)

#%%
# smooth the data
SEx_pos_first_ano = map_smooth(SEx_pos_first_ano, 5, 5)
SEx_neg_first_ano = map_smooth(SEx_neg_first_ano, 5, 5)
SEx_pos_last_ano = map_smooth(SEx_pos_last_ano, 5, 5)
SEx_neg_last_ano = map_smooth(SEx_neg_last_ano, 5, 5)

SEx_clima_first = map_smooth(SEx_clima_first, 5, 5)
SEx_clima_last = map_smooth(SEx_clima_last, 5, 5)



#%%
# (v'^2 - u'^2) - (u'v') note that the minus sign is already included in the definition of Tdivphi
Txy_pos_first = (TEx_pos_first_ano + Tdivphi_pos_first_ano).sel(plev=25000)
Txy_neg_first = (TEx_neg_first_ano + Tdivphi_neg_first_ano).sel(plev=25000)
Txy_pos_last = (TEx_pos_last_ano + Tdivphi_pos_last_ano).sel(plev=25000)
Txy_neg_last = (TEx_neg_last_ano + Tdivphi_neg_last_ano).sel(plev=25000)
# steady eddies
Sxy_pos_first = (SEx_pos_first_ano + Sdivphi_pos_first_ano).sel(plev=25000)
Sxy_neg_first = (SEx_neg_first_ano + Sdivphi_neg_first_ano).sel(plev=25000)
Sxy_pos_last = (SEx_pos_last_ano + Sdivphi_pos_last_ano).sel(plev=25000)
Sxy_neg_last = (SEx_neg_last_ano + Sdivphi_neg_last_ano).sel(plev=25000)
#%%
# sum of transient and steady eddies
Div_xy_pos_first = Txy_pos_first + Sxy_pos_first
Div_xy_neg_first = Txy_neg_first + Sxy_neg_first

Div_xy_pos_last = Txy_pos_last + Sxy_pos_last
Div_xy_neg_last = Txy_neg_last + Sxy_neg_last

#%%
levels_vq = np.arange(-3, 3.1, 0.5)
levels_uv = np.arange(-4, 5, 1)
levels_vt = np.arange(-10, 10.1, 2)

# %%
# divergence x, y
fig, axes = plt.subplots(
    2,
    3,
    figsize=(12, 9),
    subplot_kw={"projection": ccrs.Orthographic(-30, 70)},
    sharex=True,
    sharey=False,
)
# first row for Div_xy at 25000 Pa
# sum of transient and steady eddies
sum_color = Div_xy_pos_first.plot.contourf(
    ax=axes[0, 0],
    levels=levels_uv,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)

Div_xy_pos_last.plot.contour(
    ax=axes[0, 0],
    levels=[l for l in levels_uv if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# transient
trans_color = Txy_pos_first.plot.contourf(
    ax=axes[0, 1],
    levels=levels_uv,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)

Txy_pos_last.plot.contour(
    ax=axes[0, 1],
    levels=[l for l in levels_uv if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# steady
steady_color = Sxy_pos_first.plot.contourf(
    ax=axes[0, 2],
    levels=levels_uv,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
Sxy_pos_last.plot.contour(
    ax=axes[0, 2],
    levels=[l for l in levels_uv if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# second row for negative phase
sum_color_neg = Div_xy_neg_first.plot.contourf(
    ax=axes[1, 0],
    levels=levels_uv,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
Div_xy_neg_last.plot.contour(
    ax=axes[1, 0],
    levels=[l for l in levels_uv if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

#transient
Txy_xy_neg_first = Txy_neg_first.plot.contourf(
    ax=axes[1, 1],
    levels=levels_uv,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
Txy_neg_last.plot.contour(
    ax=axes[1, 1],
    levels=[l for l in levels_uv if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# steady
Sxy_xy_neg_first = Sxy_neg_first.plot.contourf(
    ax=axes[1, 2],
    levels=levels_uv,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
Sxy_neg_last.plot.contour(
    ax=axes[1, 2],
    levels=[l for l in levels_uv if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# Add colorbar axes using fig.add_axes for better alignment with tight_layout

fig.tight_layout()
fig.subplots_adjust(wspace=-0.03, hspace=-0.5, top=1., bottom=0.15)

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
    sum_color,
    cax=cax_vq,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial x} (\overline{v'^2 - u'^2})-\frac{\partial}{\partial y} (\overline{u'v'})$ [m s$^{-1}$ day$^{-1}$]",
)
fig.colorbar(
    trans_color,
    cax=cax_uv,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial x} (\overline{v'^2 - u'^2})-\frac{\partial}{\partial y} (\overline{u'v'})$ [m s$^{-1}$ day$^{-1}$]",
)
fig.colorbar(
    steady_color,
    cax=cax_vt,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial x} (\overline{v'^2 - u'^2})-\frac{\partial}{\partial y} (\overline{u'v'})$ [m s$^{-1}$ day$^{-1}$]",
)

# no y labels from second row on, no x labels at the first row
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
    ax.set_extent([-180, 180, 20, 90], crs=ccrs.PlateCarree())
    gl.xlocator = mticker.FixedLocator([-180,-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180])
    gl.ylocator = mticker.FixedLocator([10, 30, 50, 70, 90])
    clip_map(ax)

# Add panel labels a, b, c, ...
for i, ax in enumerate(axes.flat):
    ax.text(
        0.1,
        0.5,
        f"{chr(97 + i)}",
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top",
        ha="right",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=0.2),
        zorder=10,
    )

# save
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/transient_div_xy_map.pdf",
    bbox_inches="tight",
    dpi=300,
)
#%%
# vertical compoenent at 85000 Pa
sum_div_p_pos_first = (Tdiv_p_pos_first_ano + Sdiv_p_pos_first_ano).sel(plev=85000)
trans_div_p_pos_first = Tdiv_p_pos_first_ano.sel(plev=85000)
steady_div_p_pos_first = Sdiv_p_pos_first_ano.sel(plev=85000)

sum_div_p_neg_first = (Tdiv_p_neg_first_ano + Sdiv_p_neg_first_ano).sel(plev=85000)
trans_div_p_neg_first = Tdiv_p_neg_first_ano.sel(plev=85000)
steady_div_p_neg_first = Sdiv_p_neg_first_ano.sel(plev=85000)

# last
sum_div_p_pos_last = (Tdiv_p_pos_last_ano + Sdiv_p_pos_last_ano).sel(plev=85000)
trans_div_p_pos_last = Tdiv_p_pos_last_ano.sel(plev=85000)
steady_div_p_pos_last = Sdiv_p_pos_last_ano.sel(plev=85000)

sum_div_p_neg_last = (Tdiv_p_neg_last_ano + Sdiv_p_neg_last_ano).sel(plev=85000)
trans_div_neg_last = Tdiv_p_neg_last_ano.sel(plev=85000)
steady_div_p_neg_last = Sdiv_p_neg_last_ano.sel(plev=85000)
#%%
# read vapor flux
upqp_pos_first = read_comp_var("upqp", phase="pos", decade=1850, time_window=(-10, 5), ano = False).sel(plev = 85000)
upqp_neg_first = read_comp_var("upqp", phase="neg", decade=1850, time_window=(-10, 5), ano = False).sel(plev = 85000)
upqp_pos_last = read_comp_var("upqp", phase="pos", decade=2090, time_window=(-10, 5), ano = False).sel(plev = 85000)
upqp_neg_last = read_comp_var("upqp", phase="neg", decade=2090, time_window=(-10, 5), ano = False).sel(plev = 85000)

#
vpqp_pos_first = read_comp_var("vpqp", phase="pos", decade=1850, time_window=(-10, 5), ano = False).sel(plev = 85000)
vpqp_neg_first = read_comp_var("vpqp", phase="neg", decade=1850, time_window=(-10, 5), ano = False).sel(plev = 85000)
vpqp_pos_last = read_comp_var("vpqp", phase="pos", decade=2090, time_window=(-10, 5), ano = False).sel(plev = 85000)
vpqp_neg_last = read_comp_var("vpqp", phase="neg", decade=2090, time_window=(-10, 5), ano = False).sel(plev = 85000)

# # to flux
qpflux_pos_first = xr.Dataset(
    {"u": upqp_pos_first*1e3, "v": vpqp_pos_first*1e3}
)
qpflux_neg_first = xr.Dataset(
    {"u": upqp_neg_first*1e3, "v": vpqp_neg_first*1e3}
)
qpflux_pos_last = xr.Dataset(
    {"u": upqp_pos_last*1e3, "v": vpqp_pos_last*1e3}
)
qpflux_neg_last = xr.Dataset(
    {"u": upqp_neg_last*1e3, "v": vpqp_neg_last*1e3}
)
#%%
# read climatological vapor flux
upqp_clima_first = read_climatology("upqp", 1850, model_dir = 'MPI_GE_CMIP6').sel(plev = 85000)
upqp_clima_last = read_climatology("upqp", 2090, model_dir = 'MPI_GE_CMIP6').sel(plev = 85000)

vpqp_clima_first = read_climatology("vpqp", 1850, model_dir = 'MPI_GE_CMIP6').sel(plev = 85000)
vpqp_clima_last = read_climatology("vpqp", 2090, model_dir = 'MPI_GE_CMIP6').sel(plev = 85000)

# to flux
qpflux_clima_first = xr.Dataset(
    {"u": upqp_clima_first*1e3, "v": vpqp_clima_first*1e3}
)
qpflux_clima_last = xr.Dataset(
    {"u": upqp_clima_last*1e3, "v": vpqp_clima_last*1e3}
)
#%%
# anomaly
qpflux_pos_first_ano = qpflux_pos_first - qpflux_clima_first
qpflux_neg_first_ano = qpflux_neg_first - qpflux_clima_first
qpflux_pos_last_ano = qpflux_pos_last - qpflux_clima_last
qpflux_neg_last_ano = qpflux_neg_last - qpflux_clima_last


#%%
usqs_pos_first = read_comp_var("usqs", phase="pos", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
usqs_neg_first = read_comp_var("usqs", phase="neg", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)

usqs_pos_last = read_comp_var("usqs", phase="pos", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
usqs_neg_last = read_comp_var("usqs", phase="neg", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)

vsqs_pos_first = read_comp_var("vsqs", phase="pos", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
vsqs_neg_first = read_comp_var("vsqs", phase="neg", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)

vsqs_pos_last = read_comp_var("vsqs", phase="pos", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
vsqs_neg_last = read_comp_var("vsqs", phase="neg", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)

# to flux
qsflux_pos_first = xr.Dataset(
    {"u": usqs_pos_first*1e3, "v": vsqs_pos_first*1e3}
)
qsflux_neg_first = xr.Dataset(
    {"u": usqs_neg_first*1e3, "v": vsqs_neg_first*1e3}
)

qsflux_pos_last = xr.Dataset(
    {"u": usqs_pos_last*1e3, "v": vsqs_pos_last*1e3}
)

qsflux_neg_last = xr.Dataset(
    {"u": usqs_neg_last*1e3, "v": vsqs_neg_last*1e3}
)
#%%
# read climatological vapor flux
usqs_clima_first = read_climatology("usqs", 1850, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
usqs_clima_last = read_climatology("usqs", 2090, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
vsqs_clima_first = read_climatology("vsqs", 1850, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)
vsqs_clima_last = read_climatology("vsqs", 2090, model_dir = 'MPI_GE_CMIP6_allplev').sel(plev = 85000)

# to flux
qsflux_clima_first = xr.Dataset(
    {"u": usqs_clima_first*1e3, "v": vsqs_clima_first*1e3}
)
qsflux_clima_last = xr.Dataset(
    {"u": usqs_clima_last*1e3, "v": vsqs_clima_last*1e3}
)

# anomaly
qsflux_pos_first_ano = qsflux_pos_first - qsflux_clima_first
qsflux_neg_first_ano = qsflux_neg_first - qsflux_clima_first
qsflux_pos_last_ano = qsflux_pos_last - qsflux_clima_last
qsflux_neg_last_ano = qsflux_neg_last - qsflux_clima_last

#%%
qsumflux_pos_first = (qpflux_pos_first + qsflux_pos_first)
qsumflux_neg_first = (qpflux_neg_first + qsflux_neg_first)
qsumflux_pos_last = (qpflux_pos_last + qsflux_pos_last)
qsumflux_neg_last = (qpflux_neg_last + qsflux_neg_last  )
#%%
# anomaly
qsumflux_pos_first_ano = (qpflux_pos_first_ano + qsflux_pos_first_ano)
qsumflux_neg_first_ano = (qpflux_neg_first_ano + qsflux_neg_first_ano)
qsumflux_pos_last_ano = (qpflux_pos_last_ano + qsflux_pos_last_ano)
qsumflux_neg_last_ano = (qpflux_neg_last_ano + qsflux_neg_last_ano)
#%%
levels_vt = np.arange(-12, 13, 3)
levels_vt_prime = np.arange(-4, 5, 1)
qscale_sum = 20
qscale = 10
qscale_steady =20

#%%
fig, axes = plt.subplots(
    2,
    3,
    figsize=(12, 9),
    subplot_kw={"projection": ccrs.NorthPolarStereo(-40, 80)},
    sharex=True,
    sharey=False,
)

plt.subplots_adjust(wspace=-0.2, hspace=-0.2)


sum_color = sum_div_p_pos_first.plot.contourf(
    ax=axes[0, 0],
    levels=levels_vt,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
sum_div_p_pos_last.plot.contour(
    ax=axes[0, 0],
    levels=[l for l in levels_vt if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# quiver for vapor flux anomaly
sum_arrows = axes[0, 0].quiver(
    qsumflux_pos_first_ano.lon.values[::5],
    qsumflux_pos_first_ano.lat.values[::5],
    qsumflux_pos_first_ano.u.values[::5, ::5],
    qsumflux_pos_first_ano.v.values[::5, ::5],
    scale=qscale_sum,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
)

# transient
trans_color = trans_div_p_pos_first.plot.contourf(
    ax=axes[0, 1],
    levels=levels_vt_prime,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
trans_div_p_pos_last.plot.contour(
    ax=axes[0, 1],
    levels=[l for l in levels_vt_prime if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# quiver for vapor flux anomaly
trans_arrows = axes[0, 1].quiver(
    qpflux_pos_first_ano.lon.values[::5],
    qpflux_pos_first_ano.lat.values[::5],
    qpflux_pos_first_ano.u.values[::5, ::5],
    qpflux_pos_first_ano.v.values[::5, ::5],
    scale=qscale,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
)

# steady
steady_color = steady_div_p_pos_first.plot.contourf(
    ax=axes[0, 2],
    levels=levels_vt,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
steady_div_p_pos_last.plot.contour(
    ax=axes[0, 2],
    levels=[l for l in levels_vt if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# quiver for vapor flux anomaly
steady_arrows = axes[0, 2].quiver(
    qsflux_pos_first_ano.lon.values[::5],
    qsflux_pos_first_ano.lat.values[::5],
    qsflux_pos_first_ano.u.values[::5, ::5],
    qsflux_pos_first_ano.v.values[::5, ::5],
    scale=qscale_steady,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
)

# second row for negative phase
sum_color_neg = sum_div_p_neg_first.plot.contourf(
    ax=axes[1, 0],
    levels=levels_vt,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
sum_div_p_neg_last.plot.contour(
    ax=axes[1, 0],
    levels=[l for l in levels_vt if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# quiver for vapor flux anomaly
sum_arrows_neg = axes[1, 0].quiver(
    qsumflux_neg_first_ano.lon.values[::5],
    qsumflux_neg_first_ano.lat.values[::5],
    qsumflux_neg_first_ano.u.values[::5, ::5],
    qsumflux_neg_first_ano.v.values[::5, ::5],
    scale=qscale_sum,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
)

# transient
trans_color = trans_div_neg_last.plot.contourf(
    ax=axes[1, 1],
    levels=levels_vt_prime,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
trans_div_neg_last.plot.contour(
    ax=axes[1, 1],
    levels=[l for l in levels_vt_prime if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# quiver for vapor flux anomaly
trans_arrows_neg = axes[1, 1].quiver(
    qpflux_neg_first_ano.lon.values[::5],
    qpflux_neg_first_ano.lat.values[::5],
    qpflux_neg_first_ano.u.values[::5, ::5],
    qpflux_neg_first_ano.v.values[::5, ::5],
    scale=qscale,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
)

# steady
steady_color = steady_div_p_neg_last.plot.contourf(
    ax=axes[1, 2],
    levels=levels_vt,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
steady_div_p_neg_last.plot.contour(
    ax=axes[1, 2],
    levels=[l for l in levels_vt if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)

steady_arrows_neg = axes[1, 2].quiver(
    qsflux_neg_first_ano.lon.values[::5],
    qsflux_neg_first_ano.lat.values[::5],
    qsflux_neg_first_ano.u.values[::5, ::5],
    qsflux_neg_first_ano.v.values[::5, ::5],
    scale=qscale_steady,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
)

# Add colorbar axes using fig.add_axes for better alignment with tight_layout

# Get position of the bottom row axes to align colorbars
fig.tight_layout()
fig.subplots_adjust(wspace=-0.03, hspace=-0.5, top = 1., bottom = 0.15)

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
    sum_color,
    cax=cax_vq,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta_e'}}{\overline{\theta}_p} \right)$ [m s$^{-1}$ day$^{-1}$]",

)
fig.colorbar(
    trans_color,
    cax=cax_uv,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta_e'}}{\overline{\theta}_p} \right)$ [m s$^{-1}$ day$^{-1}$]",
)
fig.colorbar(
    steady_color,
    cax=cax_vt,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta_e'}}{\overline{\theta}_p} \right)$ [m s$^{-1}$ day$^{-1}$]",
)

# no y labels from second row on, no x labels at the frist row

for ax in axes.flat:
    ax.coastlines(color="grey", linewidth=1)
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="dotted",
    )
    gl.xlocator = mticker.FixedLocator([-180,-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180])
    gl.ylocator = mticker.FixedLocator([10, 30, 50, 70, 90])
    ax.set_title("")
    ax.set_extent([-180, 180, 20, 90], crs=ccrs.PlateCarree())
    clip_map(ax)


# add quiver key for the second row
qk = axes[1, 0].quiverkey(
    sum_arrows_neg,
    0.6,
    -0.05,
    2,
    r"2 $m s^{-1} g kg ^{-1}$",
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 10},
    labelsep=0.05,

)

qk = axes[1, 1].quiverkey(
    trans_arrows_neg,
    0.6,
    -0.05,
    2,
    r"2 $m s^{-1} g kg ^{-1}$",
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 10},
    labelsep=0.05,
)

qk = axes[1, 2].quiverkey(
    steady_arrows_neg,
    0.6,
    -0.05,
    2,
    r"2 $m s^{-1} g kg ^{-1}$",
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 10},
    labelsep=0.05,
)


# Add panel labels a, b, c, ...
for i, ax in enumerate(axes.flat):
    # Place label slightly outside top-left of each subplot
    ax.text(
        0.1,
        0.5,
        f"{chr(97 + i)}",
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top",
        ha="right",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=0.2),
        zorder=10,
    )

# save
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/transient_div_p_map.pdf",
    bbox_inches="tight",
    dpi=300,
)
# %%

#%%
fig, axes = plt.subplots(
    2,
    3,
    figsize=(12, 9),
    subplot_kw={"projection": ccrs.NorthPolarStereo(-40, 80)},
    sharex=True,
    sharey=False,
)

plt.subplots_adjust(wspace=-0.2, hspace=-0.2)

sum_color = sum_div_p_pos_first.plot.contourf(
    ax=axes[0, 0],
    levels=levels_vt,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
sum_div_p_pos_last.plot.contour(
    ax=axes[0, 0],
    levels=[l for l in levels_vt if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# quiver for vapor flux anomaly (last 10 years)
sum_arrows = axes[0, 0].quiver(
    qsumflux_pos_last_ano.lon.values[::5],
    qsumflux_pos_last_ano.lat.values[::5],
    qsumflux_pos_last_ano.u.values[::5, ::5],
    qsumflux_pos_last_ano.v.values[::5, ::5],
    scale=qscale_sum,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
)

# transient
trans_color = trans_div_p_pos_first.plot.contourf(
    ax=axes[0, 1],
    levels=levels_vt_prime,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
trans_div_p_pos_last.plot.contour(
    ax=axes[0, 1],
    levels=[l for l in levels_vt_prime if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# quiver for vapor flux anomaly (last 10 years)
trans_arrows = axes[0, 1].quiver(
    qpflux_pos_last_ano.lon.values[::5],
    qpflux_pos_last_ano.lat.values[::5],
    qpflux_pos_last_ano.u.values[::5, ::5],
    qpflux_pos_last_ano.v.values[::5, ::5],
    scale=qscale,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
)

# steady
steady_color = steady_div_p_pos_first.plot.contourf(
    ax=axes[0, 2],
    levels=levels_vt,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
steady_div_p_pos_last.plot.contour(
    ax=axes[0, 2],
    levels=[l for l in levels_vt if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# quiver for vapor flux anomaly (last 10 years)
steady_arrows = axes[0, 2].quiver(
    qsflux_pos_last_ano.lon.values[::5],
    qsflux_pos_last_ano.lat.values[::5],
    qsflux_pos_last_ano.u.values[::5, ::5],
    qsflux_pos_last_ano.v.values[::5, ::5],
    scale=qscale_steady,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
)

# second row for negative phase
sum_color_neg = sum_div_p_neg_first.plot.contourf(
    ax=axes[1, 0],
    levels=levels_vt,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
sum_div_p_neg_last.plot.contour(
    ax=axes[1, 0],
    levels=[l for l in levels_vt if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# quiver for vapor flux anomaly (last 10 years)
sum_arrows_neg = axes[1, 0].quiver(
    qsumflux_neg_last_ano.lon.values[::5],
    qsumflux_neg_last_ano.lat.values[::5],
    qsumflux_neg_last_ano.u.values[::5, ::5],
    qsumflux_neg_last_ano.v.values[::5, ::5],
    scale=qscale_sum,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
)

# transient
trans_color = trans_div_neg_last.plot.contourf(
    ax=axes[1, 1],
    levels=levels_vt_prime,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
trans_div_neg_last.plot.contour(
    ax=axes[1, 1],
    levels=[l for l in levels_vt_prime if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# quiver for vapor flux anomaly (last 10 years)
trans_arrows_neg = axes[1, 1].quiver(
    qpflux_neg_last_ano.lon.values[::5],
    qpflux_neg_last_ano.lat.values[::5],
    qpflux_neg_last_ano.u.values[::5, ::5],
    qpflux_neg_last_ano.v.values[::5, ::5],
    scale=qscale,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
)

# steady
steady_color = steady_div_p_neg_last.plot.contourf(
    ax=axes[1, 2],
    levels=levels_vt,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
steady_div_p_neg_last.plot.contour(
    ax=axes[1, 2],
    levels=[l for l in levels_vt if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)

steady_arrows_neg = axes[1, 2].quiver(
    qsflux_neg_last_ano.lon.values[::5],
    qsflux_neg_last_ano.lat.values[::5],
    qsflux_neg_last_ano.u.values[::5, ::5],
    qsflux_neg_last_ano.v.values[::5, ::5],
    scale=qscale_steady,
    transform=ccrs.PlateCarree(),
    color="green",
    width=0.005,
)

# Add colorbar axes using fig.add_axes for better alignment with tight_layout
fig.tight_layout()
# Get position of the bottom row axes to align colorbars
fig.subplots_adjust(wspace=-0.03, hspace=-0.5, top = 1., bottom = 0.15)

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
    sum_color,
    cax=cax_vq,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta_e'}}{\overline{\theta}_p} \right)$ [m s$^{-1}$ day$^{-1}$]",

)
fig.colorbar(
    trans_color,
    cax=cax_uv,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta_e'}}{\overline{\theta}_p} \right)$ [m s$^{-1}$ day$^{-1}$]",
)
fig.colorbar(
    steady_color,
    cax=cax_vt,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial p} \left( f_0 \frac{\overline{v'\theta_e'}}{\overline{\theta}_p} \right)$ [m s$^{-1}$ day$^{-1}$]",
)

# no y labels from second row on, no x labels at the frist row

for ax in axes.flat:
    ax.coastlines(color="grey", linewidth=1)
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=1,
        color="grey",
        alpha=0.5,
        linestyle="dotted",
    )
    gl.xlocator = mticker.FixedLocator([-180,-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180])
    gl.ylocator = mticker.FixedLocator([10, 30, 50, 70, 90])
    ax.set_title("")
    ax.set_extent([-180, 180, 20, 90], crs=ccrs.PlateCarree())
    clip_map(ax)

# add quiver key for the second row
qk = axes[1, 0].quiverkey(
    sum_arrows_neg,
    0.6,
    -0.05,
    2,
    r"2 $m s^{-1} g kg ^{-1}$",
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 10},
    labelsep=0.05,

)

qk = axes[1, 1].quiverkey(
    trans_arrows_neg,
    0.6,
    -0.05,
    2,
    r"2 $m s^{-1} g kg ^{-1}$",
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 10},
    labelsep=0.05,
)

qk = axes[1, 2].quiverkey(
    steady_arrows_neg,
    0.6,
    -0.05,
    2,
    r"2 $m s^{-1} g kg ^{-1}$",
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 10},
    labelsep=0.05,
)
# Add panel labels a, b, c, ... with adjusted positions for the subplot layout
for i, ax in enumerate(axes.flat):
    # Place label slightly outside top-left of each subplot
    ax.text(
        0.1,
        0.5,
        f"{chr(97 + i)}",
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top",
        ha="right",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=0.2),
        zorder=10,
    )
# save
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/transient_div_p_map_last_arrow.pdf",
    bbox_inches="tight",
    dpi=300,
)
# %%

#%%
# E_x
sum_Ex_pos_first = (TEx_pos_first_ano + SEx_pos_first_ano).sel(plev=25000)
sum_Ex_neg_first = (TEx_neg_first_ano + SEx_neg_first_ano).sel(plev=25000)

sum_Ex_pos_last = (TEx_pos_last_ano + SEx_pos_last_ano).sel(plev=25000)
sum_Ex_neg_last = (TEx_neg_last_ano + SEx_neg_last_ano).sel(plev=25000)

trans_Ex_pos_first = TEx_pos_first_ano.sel(plev=25000)
trans_Ex_neg_first = TEx_neg_first_ano.sel(plev=25000)

trans_Ex_pos_last = TEx_pos_last_ano.sel(plev=25000)
trans_Ex_neg_last = TEx_neg_last_ano.sel(plev=25000)

steady_Ex_pos_first = SEx_pos_first_ano.sel(plev=25000)
steady_Ex_neg_first = SEx_neg_first_ano.sel(plev=25000)

steady_Ex_pos_last = SEx_pos_last_ano.sel(plev=25000)
steady_Ex_neg_last = SEx_neg_last_ano.sel(plev=25000)
#%%
#E_y
sum_Ey_pos_first = (Tdivphi_pos_first_ano + Sdivphi_pos_first_ano).sel(plev=25000)
sum_Ey_neg_first = (Tdivphi_neg_first_ano + Sdivphi_neg_first_ano).sel(plev=25000)

sum_Ey_pos_last = (Tdivphi_pos_last_ano + Sdivphi_pos_last_ano).sel(plev=25000)
sum_Ey_neg_last = (Tdivphi_neg_last_ano + Sdivphi_neg_last_ano).sel(plev=25000)

trans_Ey_pos_first = Tdivphi_pos_first_ano.sel(plev=25000)
trans_Ey_neg_first  = Tdivphi_neg_first_ano.sel(plev=25000)

trans_Ey_pos_last = Tdivphi_pos_last_ano.sel(plev=25000)
trans_Ey_neg_last = Tdivphi_neg_last_ano.sel(plev=25000)

steady_Ey_pos_first = Sdivphi_pos_first_ano.sel(plev=25000)
steady_Ey_neg_first = Sdivphi_neg_first_ano.sel(plev=25000)

steady_Ey_pos_last = Sdivphi_pos_last_ano.sel(plev=25000)
steady_Ey_neg_last = Sdivphi_neg_last_ano.sel(plev=25000)

#%%
# read ua, va
ua_pos_first = read_comp_var("ua", phase="pos", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
ua_neg_first = read_comp_var("ua", phase="neg", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
ua_pos_last = read_comp_var("ua", phase="pos", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
ua_neg_last = read_comp_var("ua", phase="neg", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)

va_pos_first = read_comp_var("va", phase="pos", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
va_neg_first = read_comp_var("va", phase="neg", decade=1850, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
va_pos_last = read_comp_var("va", phase="pos", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
va_neg_last = read_comp_var("va", phase="neg", decade=2090, time_window=(-10, 5), ano = False, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
#%%
# to flux
wndflux_pos_first = xr.Dataset({
    "u": ua_pos_first,
    "v": va_pos_first,
})
wndflux_neg_first = xr.Dataset({
    "u": ua_neg_first,
    "v": va_neg_first,
})
wndflux_pos_last = xr.Dataset({
    "u": ua_pos_last,
    "v": va_pos_last,
})
wndflux_neg_last = xr.Dataset({
    "u": ua_neg_last,
    "v": va_neg_last,
})

#%%
# climatology
ua_clima_first = read_climatology("ua", 1850, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
ua_clima_last = read_climatology("ua", 2090, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
va_clima_first = read_climatology("va", 1850, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)
va_clima_last = read_climatology("va", 2090, model_dir = 'MPI_GE_CMIP6').sel(plev=25000)

#%%
# to anomaly
ua_pos_first_ano = ua_pos_first - ua_clima_first
ua_neg_first_ano = ua_neg_first - ua_clima_first
ua_pos_last_ano = ua_pos_last - ua_clima_last
ua_neg_last_ano = ua_neg_last - ua_clima_last

va_pos_first_ano = va_pos_first - va_clima_first
va_neg_first_ano = va_neg_first - va_clima_first
va_pos_last_ano = va_pos_last - va_clima_last
va_neg_last_ano = va_neg_last - va_clima_last

# to flux
wndflux_pos_first_ano = xr.Dataset({
    "u": ua_pos_first_ano,
    "v": va_pos_first_ano,
})

wndflux_neg_first_ano = xr.Dataset({
    "u": ua_neg_first_ano,
    "v": va_neg_first_ano,
})
wndflux_pos_last_ano = xr.Dataset({
    "u": ua_pos_last_ano,
    "v": va_pos_last_ano,
})
wndflux_neg_last_ano = xr.Dataset({ 
    "u": ua_neg_last_ano,
    "v": va_neg_last_ano,
})


#%%
levels_Ey = np.arange(-3, 3.1, 0.5)
levels_Ey_prime = np.arange(-1.5, 1.6, 0.5)
wnd_scale = 150
#%%
# plot E_y
fig, axes = plt.subplots(
    2,
    3,
    figsize=(12, 9),
    subplot_kw={"projection": ccrs.NorthPolarStereo(-40, 80)},
    sharex=True,
    sharey=False,
)
# first row for pos
sum_color = sum_Ey_pos_first.plot.contourf(
    ax=axes[0, 0],
    levels=levels_Ey,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
sum_Ey_pos_last.plot.contour(
    ax=axes[0, 0],
    levels=[l for l in levels_Ey if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# quiver for wind anomaly
sum_arrows = axes[0, 0].quiver(
    wndflux_pos_first.lon.values[::7],
    wndflux_pos_first.lat.values[::6],
    wndflux_pos_first.u.values[::6, ::7],
    wndflux_pos_first.v.values[::6, ::7],
    scale=wnd_scale,
    transform=ccrs.PlateCarree(),
    color="purple",
    width=0.005,
)




# transient
trans_color = trans_Ey_pos_first.plot.contourf(
    ax=axes[0, 1],
    levels=levels_Ey_prime,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
trans_Ey_pos_last.plot.contour(
    ax=axes[0, 1],
    levels=[l for l in levels_Ey_prime if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# steady
steady_color = steady_Ey_pos_first.plot.contourf(
    ax=axes[0, 2],  
    levels=levels_Ey,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
steady_Ey_pos_last.plot.contour(
    ax=axes[0, 2],
    levels=[l for l in levels_Ey if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)
# second row for neg
sum_color_neg = sum_Ey_neg_first.plot.contourf(
    ax=axes[1, 0],
    levels=levels_Ey,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
sum_Ey_neg_last.plot.contour(
    ax=axes[1, 0],
    levels=[l for l in levels_Ey if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)

# quiver for wind anomaly
sum_arrows_neg = axes[1, 0].quiver(
    wndflux_neg_first.lon.values[::7],
    wndflux_neg_first.lat.values[::6],
    wndflux_neg_first.u.values[::6, ::7],
    wndflux_neg_first.v.values[::6, ::7],
    scale=wnd_scale,
    transform=ccrs.PlateCarree(),
    color="purple",
    width=0.005,
)

# transient
trans_color = trans_Ey_neg_first.plot.contourf(
    ax=axes[1, 1],
    levels=levels_Ey_prime,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
trans_Ey_neg_last.plot.contour(
    ax=axes[1, 1],
    levels=[l for l in levels_Ey_prime if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# steady
steady_color = steady_Ey_neg_first.plot.contourf(
    ax=axes[1, 2],
    levels=levels_Ey,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
steady_Ey_neg_last.plot.contour(
    ax=axes[1, 2],
    levels=[l for l in levels_Ey if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)


# Add colorbar axes using fig.add_axes for better alignment with tight_layout

# Get position of the bottom row axes to align colorbars
fig.tight_layout()
fig.subplots_adjust(wspace=-0.03, hspace=-0.5, top = 1., bottom = 0.15)

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
    sum_color,
    cax=cax_vq,
    orientation="horizontal",
    label= r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m s$^{-1}$ day$^{-1}$]",

)
fig.colorbar(
    trans_color,
    cax=cax_uv,
    orientation="horizontal",
    label= r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m s$^{-1}$ day$^{-1}$]",
    # ticks label every 2
    ticks = levels_Ey[::2] / 2  # levels_Ey/2 is used for transients
)
fig.colorbar(
    steady_color,
    cax=cax_vt,
    orientation="horizontal",
    label= r"$-\frac{\partial}{\partial y} (\overline{u'v'})$ [m s$^{-1}$ day$^{-1}$]",
)
# add quiver key for the second row
qk = axes[1, 0].quiverkey(
    sum_arrows_neg,
    0.6,
    -0.05,
    10,
    r"10 $m s^{-1}$",
    labelpos="E",
    coordinates="axes",
    fontproperties={"size": 10},
    labelsep=0.05,
)

# no y labels from second row on, no x labels at the frist row
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
    ax.set_extent([-180, 180, 20, 90], crs=ccrs.PlateCarree())
    gl.xlocator = mticker.FixedLocator([-180,-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180])
    gl.ylocator = mticker.FixedLocator([10, 30, 50, 70, 90])
    clip_map(ax)
# Add panel labels a, b, c, ... 
for i, ax in enumerate(axes.flat):
    # Place label slightly outside top-left of each subplot
    ax.text(
        0.1,
        0.5,
        f"{chr(97 + i)}",
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top",
        ha="right",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=0.2),
        zorder=10,
    )
# save
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/transient_Ey_map.pdf",
    bbox_inches="tight",
    dpi=300,
)

# %%

# %%

# %%
levels_Ex = np.arange(-5, 5.1, 1)
# plot E_x
fig, axes = plt.subplots(
    2,
    3,
    figsize=(12, 9),
    subplot_kw={"projection": ccrs.NorthPolarStereo(-40, 80)},
    sharex=True,
    sharey=False,
)

plt.subplots_adjust(wspace=-0.2, hspace=-0.2)

# first row for pos
sum_color = sum_Ex_pos_first.plot.contourf(
    ax=axes[0, 0],
    levels=levels_Ex,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
sum_Ex_pos_last.plot.contour(
    ax=axes[0, 0],
    levels=[l for l in levels_Ex if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# transient
trans_color = trans_Ex_pos_first.plot.contourf(
    ax=axes[0, 1],
    levels=levels_Ex/2,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
trans_Ex_pos_last.plot.contour(
    ax=axes[0, 1],
    levels=[l for l in levels_Ex/2 if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# steady
steady_color = steady_Ex_pos_first.plot.contourf(
    ax=axes[0, 2],  
    levels=levels_Ex,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
steady_Ex_pos_last.plot.contour(
    ax=axes[0, 2],
    levels=[l for l in levels_Ex if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)
# second row for neg
sum_color_neg = sum_Ex_neg_first.plot.contourf(
    ax=axes[1, 0],
    levels=levels_Ex,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
sum_Ex_neg_last.plot.contour(
    ax=axes[1, 0],
    levels=[l for l in levels_Ex if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# transient
trans_color = trans_Ex_neg_first.plot.contourf(
    ax=axes[1, 1],
    levels=levels_Ex/2,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
trans_Ex_neg_last.plot.contour(
    ax=axes[1, 1],
    levels=[l for l in levels_Ex/2 if l != 0],
    colors="k",
    linewidths=0.5,
    extend="both",
    transform=ccrs.PlateCarree(),
)
# steady
steady_color = steady_Ex_neg_first.plot.contourf(
    ax=axes[1, 2],
    levels=levels_Ex,
    cmap="RdBu_r",
    add_colorbar=False,
    extend="both",
    transform=ccrs.PlateCarree(),
)
steady_Ex_neg_last.plot.contour(
    ax=axes[1, 2],
    levels=[l for l in levels_Ex if l != 0],
    colors="k",
    linewidths=0.5,
    transform=ccrs.PlateCarree(),
    extend="both",
)

# Add colorbar axes using fig.add_axes for better alignment with tight_layout
fig.tight_layout()
fig.subplots_adjust(wspace=-0.03, hspace=-0.5, top=1., bottom=0.15)

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
    sum_color,
    cax=cax_vq,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial x} (\overline{v'^2 - u'^2})$ [m s$^{-1}$ day$^{-1}$]",
)
fig.colorbar(
    trans_color,
    cax=cax_uv,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial x} (\overline{v'^2 - u'^2})$ [m s$^{-1}$ day$^{-1}$]",
    ticks=levels_Ex[::2] / 2
)
fig.colorbar(
    steady_color,
    cax=cax_vt,
    orientation="horizontal",
    label=r"$\frac{\partial}{\partial x} (\overline{v'^2 - u'^2})$ [m s$^{-1}$ day$^{-1}$]",
)

# no y labels from second row on, no x labels at the first row
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
    ax.set_extent([-180, 180, 20, 90], crs=ccrs.PlateCarree())
    gl.xlocator = mticker.FixedLocator([-180,-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180])
    gl.ylocator = mticker.FixedLocator([10, 30, 50, 70, 90])
    clip_map(ax)

# Add panel labels a, b, c, ...
for i, ax in enumerate(axes.flat):
    ax.text(
        0.1,
        0.5,
        f"{chr(97 + i)}",
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top",
        ha="right",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=0.2),
        zorder=10,
    )

# save
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0eddy_flux/transient_Ex_map.pdf",
    bbox_inches="tight",
    dpi=300,
)

# %%
