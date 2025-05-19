# %%
import xarray as xr
import numpy as np
from src.dynamics.theta_on_pv import theta_on_2pvu

# %%
from src.plotting.prime_data import read_climatology

# %%
import importlib
import src.dynamics.theta_on_pv


# %%
def theta2UPV(
    decade,
    equiv_theta=False,
):
    if equiv_theta:
        theta = read_climatology(
            "equiv_theta",
            decade,
            name="etheta",
        )
    else:
        theta = read_climatology(
            "theta",
            decade,
            name="theta",
        )
    uwnd = read_climatology(
        "ua",
        decade,
        name="ua",
    )

    vwnd = read_climatology(
        "va",
        decade,
        name="va",
    )

    # calculate theta on 2PVU
    theta_pv = theta_on_2pvu(theta, uwnd, vwnd)

    return theta_pv


# %%
first_clima = theta2UPV(
    1850,
    equiv_theta=False,
)
last_clima = theta2UPV(
    2090,
    equiv_theta=False,
)
#%%
first_clima.name = "theta2UPV"
last_clima.name = "theta2UPV"
# %%
first_clima.to_netcdf(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0climatology/theta2UPV_1850.nc"
)
last_clima.to_netcdf(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0climatology/theta2UPV_2090.nc"
)
# %%
