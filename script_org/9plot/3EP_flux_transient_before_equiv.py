# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


from src.dynamics.EP_flux import (
    NPC_mean,
    PlotEPfluxArrows,
    NAL_mean,
)


# %%
def read_EP_flux(
    phase, decade, eddy="transient", ano=False, isentrope=False, region="western"
):
    if isentrope:
        EP_flux_dir = (
            "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0EP_flux_isen/"
        )
    else:
        EP_flux_dir = (
            "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0EP_flux/"
        )

    T_phi = xr.open_dataarray(f"{EP_flux_dir}{eddy}_F_phi_{phase}_{decade}_ano{ano}.nc")
    F_p = xr.open_dataarray(f"{EP_flux_dir}{eddy}_F_p_{phase}_{decade}_ano{ano}.nc")
    div = xr.open_dataarray(f"{EP_flux_dir}{eddy}_div_{phase}_{decade}_ano{ano}.nc")

    if region == "NPC":
        T_phi = NPC_mean(T_phi)
        F_p = NPC_mean(F_p)
        div = NPC_mean(div)

    elif region == "NAL":
        T_phi = NAL_mean(T_phi)
        F_p = NAL_mean(F_p)
        div = NAL_mean(div)
    elif region == "western":
        T_phi = xr.concat(
            [T_phi.sel(lon = slice(240, None)),
            T_phi.sel(lon = slice(0, 60))], dim = "lon"
        )
        F_p = xr.concat(
            [F_p.sel(lon = slice(240, None)),
            F_p.sel(lon = slice(0, 60))], dim = "lon"
        )
        div = xr.concat(
            [div.sel(lon = slice(240, None)),
            div.sel(lon = slice(0, 60))], dim = "lon"
        )
    elif region is None:
        # do nothing, return the data as is
        pass


    return T_phi, F_p, div


# %%
scale = 1e16
scale_div = 1e15
levels = np.arange(-10, 10.1, 1)
levels_div = np.arange(-1.5, 1.6, 0.3)
# %%
# read transient EP flux for positive and negative phase
# read data for first decade without region
T_phi_pos_first, T_p_pos_first, Tdiv_pos_first = read_EP_flux(
    phase="pos", decade=1850, eddy="transient", ano=False, isentrope=False
)

T_phi_neg_first, T_p_neg_first, Tdiv_neg_first = read_EP_flux(
    phase="neg", decade=1850, eddy="transient", ano=False, isentrope=False
)


# last decade without region
T_phi_pos_last, T_p_pos_last, Tdiv_pos_last = read_EP_flux(
    phase="pos", decade=2090, eddy="transient", ano=False, isentrope=False
)

T_phi_neg_last, T_p_neg_last, Tdiv_neg_last = read_EP_flux(
    phase="neg", decade=2090, eddy="transient", ano=False, isentrope=False
)

# -1 * p component because the 'plev' was ascending in the data
T_p_pos_first = -1 * T_p_pos_first
T_p_pos_last = -1 * T_p_pos_last
T_p_neg_first = -1 * T_p_neg_first
T_p_neg_last = -1 * T_p_neg_last
# zonal mean
T_phi_pos_first_zonal = T_phi_pos_first.mean(dim="lon")
T_p_pos_first_zonal = T_p_pos_first.mean(dim="lon")
T_phi_pos_last_zonal = T_phi_pos_last.mean(dim="lon")
T_p_pos_last_zonal = T_p_pos_last.mean(dim="lon")
Tdiv_pos_first_zonal = Tdiv_pos_first.mean(dim="lon")
Tdiv_pos_last_zonal = Tdiv_pos_last.mean(dim="lon")

T_phi_neg_first_zonal = T_phi_neg_first.mean(dim="lon")
T_p_neg_first_zonal = T_p_neg_first.mean(dim="lon")
T_phi_neg_last_zonal = T_phi_neg_last.mean(dim="lon")
T_p_neg_last_zonal = T_p_neg_last.mean(dim="lon")
Tdiv_neg_first_zonal = Tdiv_neg_first.mean(dim="lon")
Tdiv_neg_last_zonal = Tdiv_neg_last.mean(dim="lon")

#%% 
# read steady EP flux for positive and negative phase
S_phi_pos_first, S_p_pos_first, Sdiv_pos_first = read_EP_flux(
    phase="pos", decade=1850, eddy="steady", ano=False, isentrope=False
)
S_phi_neg_first, S_p_neg_first, Sdiv_neg_first = read_EP_flux(
    phase="neg", decade=1850, eddy="steady", ano=False, isentrope=False
)

S_phi_pos_last, S_p_pos_last, Sdiv_pos_last = read_EP_flux(
    phase="pos", decade=2090, eddy="steady", ano=False, isentrope=False
)
S_phi_neg_last, S_p_neg_last, Sdiv_neg_last = read_EP_flux(
    phase="neg", decade=2090, eddy="steady", ano=False, isentrope=False
)
# -1 * p component because the 'plev' was ascending in the data
S_p_pos_first = -1 * S_p_pos_first
S_p_pos_last = -1 * S_p_pos_last
S_p_neg_first = -1 * S_p_neg_first
S_p_neg_last = -1 * S_p_neg_last
# zonal mean
S_phi_pos_first_zonal = S_phi_pos_first.mean(dim="lon")
S_p_pos_first_zonal = S_p_pos_first.mean(dim="lon")
S_phi_pos_last_zonal = S_phi_pos_last.mean(dim="lon")
S_p_pos_last_zonal = S_p_pos_last.mean(dim="lon")
Sdiv_pos_first_zonal = Sdiv_pos_first.mean(dim="lon")
Sdiv_pos_last_zonal = Sdiv_pos_last.mean(dim="lon")
S_phi_neg_first_zonal = S_phi_neg_first.mean(dim="lon")
S_p_neg_first_zonal = S_p_neg_first.mean(dim="lon")
S_phi_neg_last_zonal = S_phi_neg_last.mean(dim="lon")
S_p_neg_last_zonal = S_p_neg_last.mean(dim="lon")
Sdiv_neg_first_zonal = Sdiv_neg_first.mean(dim="lon")
Sdiv_neg_last_zonal = Sdiv_neg_last.mean(dim="lon")


# %%
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
# first row for first decade
Tdiv_pos_first_zonal.plot.contourf(
    ax=axes[0, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)

# for pos
PlotEPfluxArrows(
    x=T_phi_pos_first_zonal.lat[::3],
    y=T_phi_pos_first_zonal.plev,
    ep1=T_phi_pos_first_zonal[:, ::3],
    ep2=T_p_pos_first_zonal[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    ylim=[1000, 200],
    fig=fig,
    ax=axes[0, 0],
)

# for neg
Tdiv_neg_first_zonal.plot.contourf(
    ax=axes[0, 1], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=T_phi_neg_first_zonal.lat[::3],
    y=T_phi_neg_first_zonal.plev,
    ep1=T_phi_neg_first_zonal[:, ::3],
    ep2=T_p_neg_first_zonal[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    ylim=[1000, 200],
    fig=fig,
    ax=axes[0, 1],
)
# third col for difference between positive and negative
Tdiv_diff_first_zonal = Tdiv_pos_first_zonal - Tdiv_neg_first_zonal
Tdiv_diff_first_zonal.plot.contourf(
    ax=axes[0, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=T_phi_pos_first_zonal.lat[::3],
    y=T_phi_pos_first_zonal.plev,
    ep1=(T_phi_pos_first_zonal - T_phi_neg_first_zonal)[:, ::3],
    ep2=(T_p_pos_first_zonal - T_p_neg_first_zonal)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    ylim=[1000, 200],
    fig=fig,
    ax=axes[0, 2],  
    draw_key=True,
    key_loc=(0.7, 0.95),
)

# second row for last decade
map = Tdiv_pos_last_zonal.plot.contourf(
    ax=axes[1, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=T_phi_pos_last_zonal.lat[::3],
    y=T_phi_pos_last_zonal.plev,
    ep1=T_phi_pos_last_zonal[:, ::3],
    ep2=T_p_pos_last_zonal[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    ylim=[1000, 200],
    fig=fig,
    ax=axes[1, 0],
)
Tdiv_neg_last_zonal.plot.contourf(
    ax=axes[1, 1], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=T_phi_neg_last_zonal.lat[::3],
    y=T_phi_neg_last_zonal.plev,
    ep1=T_phi_neg_last_zonal[:, ::3],
    ep2=T_p_neg_last_zonal[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    ylim=[1000, 200],
    fig=fig,
    ax=axes[1, 1],
)
# third col for difference between positive and negative
Tdiv_diff_last_zonal = Tdiv_pos_last_zonal - Tdiv_neg_last_zonal
diff_map = Tdiv_diff_last_zonal.plot.contourf(
    ax=axes[1, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=T_phi_pos_last_zonal.lat[::3],
    y=T_phi_pos_last_zonal.plev,
    ep1=(T_phi_pos_last_zonal - T_phi_neg_last_zonal)[:, ::3],
    ep2=(T_p_pos_last_zonal - T_p_neg_last_zonal)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    ylim=[1000, 200],
    fig=fig,
    ax=axes[1, 2],
    draw_key=True,
    key_loc=(0.7, 0.95),
)

for ax in axes.flatten():
    ax.set_xlabel("")
    ax.set_ylabel("")
for ax in axes[:, 0]:
    ax.set_ylabel("Pressure (hPa)")
for ax in axes[1, :]:
    ax.set_xlabel("Latitude (°N)")

# add colorbar at the bottom
fig.colorbar(
    map,
    ax = axes[:, :2],
    orientation='horizontal',
    label='EP flux divergence (m s$^{-1}$ day$^{-1}$)',
    shrink=0.5,
)
fig.colorbar(
    diff_map,
    ax = axes[:, 2],
    orientation='horizontal',
    label='EP flux divergence (m s$^{-1}$ day$^{-1}$)',
)

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/transient_EP_flux_divergence.pdf", dpi=300)
#%%
fig, axes = plt.subplots(2, 3, figsize=(12, 10))
# first row for first decade (steady eddies)
Sdiv_pos_first_zonal.plot.contourf(
    ax=axes[0, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)

# for pos
PlotEPfluxArrows(
    x=S_phi_pos_first_zonal.lat[::3],
    y=S_phi_pos_first_zonal.plev,
    ep1=S_phi_pos_first_zonal[:, ::3],
    ep2=S_p_pos_first_zonal[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    ylim=[1000, 200],
    fig=fig,
    ax=axes[0, 0],
)

# for neg
Sdiv_neg_first_zonal.plot.contourf(
    ax=axes[0, 1], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=S_phi_neg_first_zonal.lat[::3],
    y=S_phi_neg_first_zonal.plev,
    ep1=S_phi_neg_first_zonal[:, ::3],
    ep2=S_p_neg_first_zonal[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    ylim=[1000, 200],
    fig=fig,
    ax=axes[0, 1],
)
# third col for difference between positive and negative
Sdiv_diff_first_zonal = Sdiv_pos_first_zonal - Sdiv_neg_first_zonal
Sdiv_diff_first_zonal.plot.contourf(
    ax=axes[0, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=S_phi_pos_first_zonal.lat[::3],
    y=S_phi_pos_first_zonal.plev,
    ep1=(S_phi_pos_first_zonal - S_phi_neg_first_zonal)[:, ::3],
    ep2=(S_p_pos_first_zonal - S_p_neg_first_zonal)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    ylim=[1000, 200],
    fig=fig,
    ax=axes[0, 2],  
    draw_key=True,
    key_loc=(0.7, 0.95),
)

# second row for last decade (steady eddies)
Sdiv_pos_last_zonal.plot.contourf(
    ax=axes[1, 0], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=S_phi_pos_last_zonal.lat[::3],
    y=S_phi_pos_last_zonal.plev,
    ep1=S_phi_pos_last_zonal[:, ::3],
    ep2=S_p_pos_last_zonal[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    ylim=[1000, 200],
    fig=fig,
    ax=axes[1, 0],
)
map = Sdiv_neg_last_zonal.plot.contourf(
    ax=axes[1, 1], levels=levels, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=S_phi_neg_last_zonal.lat[::3],
    y=S_phi_neg_last_zonal.plev,
    ep1=S_phi_neg_last_zonal[:, ::3],
    ep2=S_p_neg_last_zonal[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale,
    xlim=[0, 85],
    ylim=[1000, 200],
    fig=fig,
    ax=axes[1, 1],
)
# third col for difference between positive and negative
Sdiv_diff_last_zonal = Sdiv_pos_last_zonal - Sdiv_neg_last_zonal
diff_map = Sdiv_diff_last_zonal.plot.contourf(
    ax=axes[1, 2], levels=levels_div, cmap="RdBu_r", add_colorbar=False
)
PlotEPfluxArrows(
    x=S_phi_pos_last_zonal.lat[::3],
    y=S_phi_pos_last_zonal.plev,
    ep1=(S_phi_pos_last_zonal - S_phi_neg_last_zonal)[:, ::3],
    ep2=(S_p_pos_last_zonal - S_p_neg_last_zonal)[:, ::3],
    xscale="linear",
    yscale="linear",
    scale=scale_div,
    xlim=[0, 85],
    ylim=[1000, 200],
    fig=fig,
    ax=axes[1, 2],
    draw_key=True,
    key_loc=(0.7, 0.95),
)

for ax in axes.flatten():
    ax.set_xlabel("")
    ax.set_ylabel("")
for ax in axes[:, 0]:
    ax.set_ylabel("Pressure (hPa)")
for ax in axes[1, :]:
    ax.set_xlabel("Latitude (°N)")

# add colorbar at the bottom
fig.colorbar(
    map,
    ax = axes[:, :2],
    orientation='horizontal',
    label='EP flux divergence (m s$^{-1}$ day$^{-1}$)',
    shrink=0.5,
)
fig.colorbar(
    diff_map,
    ax = axes[:, 2],
    orientation='horizontal',
    label='EP flux divergence (m s$^{-1}$ day$^{-1}$)',
)
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/eddy_flux/steady_EP_flux_divergence.pdf", dpi=300)
# %%
