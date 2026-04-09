#%%
import xarray as xr
import numpy as np
import os
# %%
from src.data_helper.read_variable import read_climatology

# %%

#%%
def _zonal_mean(da, lon_min=-90, lon_max=40):
    """Zonal mean over [lon_min, lon_max], handling both 0-360 and -180-180 grids."""
    if da.lon.max() > 180:
        # Convert 0-360 to -180-180
        da = da.assign_coords(lon=(da.lon + 180) % 360 - 180).sortby("lon")
    return da.sel(lon=slice(lon_min, lon_max)).mean(dim="lon")

# %%
Fdiv_phi_transient_first = read_climatology("Fdiv_phi_transient", decade="1850", name="div", plev = 25000)
Fdiv_phi_transient_last = read_climatology("Fdiv_phi_transient", decade="2090", name="div", plev = 25000)

Fdiv_phi_steady_first = read_climatology("Fdiv_phi_steady", decade="1850", name="div", plev = 25000)
Fdiv_phi_steady_last = read_climatology("Fdiv_phi_steady", decade="2090", name="div", plev = 25000)

#%%
eke_first = read_climatology("eke", decade="1850", name="eke", plev = 25000, model_dir = "MPI_GE_CMIP6")
eke_last = read_climatology("eke", decade="2090", name="eke", plev = 25000, model_dir = "MPI_GE_CMIP6")

#%%
baroc_first = read_climatology("eady_growth_rate", decade="1850", name="eady_growth_rate", plev = 85000)
baroc_last = read_climatology("eady_growth_rate", decade="2090", name="eady_growth_rate", plev = 85000)

#%%
transient_eddy_heat_d2y2_first = read_climatology("transient_eddy_heat_d2y2", decade="1850", name="eddy_heat_d2y2", plev = 85000)
transient_eddy_heat_d2y2_last = read_climatology("transient_eddy_heat_d2y2", decade="2090", name="eddy_heat_d2y2", plev = 85000)
#%%
steady_eddy_heat_d2y2_first = read_climatology("steady_eddy_heat_d2y2", decade="1850", name="eddy_heat_d2y2", plev = 85000)
steady_eddy_heat_d2y2_last = read_climatology("steady_eddy_heat_d2y2", decade="2090", name="eddy_heat_d2y2", plev = 85000)
                                               
#%%
# save 
save_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0flux_climatology"
os.makedirs(save_dir, exist_ok=True)

_to_save = {
    "Fdiv_phi_transient_first": Fdiv_phi_transient_first,
    "Fdiv_phi_transient_last": Fdiv_phi_transient_last,
    "Fdiv_phi_steady_first": Fdiv_phi_steady_first,
    "Fdiv_phi_steady_last": Fdiv_phi_steady_last,
    "eke_first": eke_first,
    "eke_last": eke_last,
    "baroc_first": baroc_first,
    "baroc_last": baroc_last,
    "transient_eddy_heat_d2y2_first": transient_eddy_heat_d2y2_first,
    "transient_eddy_heat_d2y2_last": transient_eddy_heat_d2y2_last,
    "steady_eddy_heat_d2y2_first": steady_eddy_heat_d2y2_first,
    "steady_eddy_heat_d2y2_last": steady_eddy_heat_d2y2_last,
}

for name, da in _to_save.items():
    _zonal_mean(da).to_netcdf(os.path.join(save_dir, f"{name}.nc"))
# %%
