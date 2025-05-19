# %%
import xarray as xr
import numpy as np
from src.dynamics.theta_on_pv import theta_on_2pvu

# %%
from src.plotting.prime_data import read_composite_MPI

# %%
import importlib
import src.dynamics.theta_on_pv


# %%
def theta2UPV(
    decade,
    phase="pos",
    equiv_theta=False,
):
    if equiv_theta:
        theta = read_composite_MPI(
            "equiv_theta",
            "etheta",
            decade,
            before="10_0",
            return_as=phase,
            ano=False,
        )
    else:
        theta = read_composite_MPI(
            "theta",
            "theta",
            decade,
            before="10_0",
            return_as=phase,
            ano=False,
        )
    uwnd = read_composite_MPI(
        "ua",
        "ua",
        decade,
        before="10_0",
        return_as=phase,
        ano=False,
    )

    vwnd = read_composite_MPI(
        "va",
        "va",
        decade,
        before="10_0",
        return_as=phase,
        ano=False,
    )
    # calculate theta on 2PVU
    theta_pv = theta_on_2pvu(theta, uwnd, vwnd)

    return theta_pv


# %%
pos_first = theta2UPV(
    1850,
    phase="pos",
    equiv_theta=False,
)
# %%
neg_first = theta2UPV(
    1850,
    phase="neg",
    equiv_theta=False,
)

# %%
pos_last = theta2UPV(
    2090,
    phase="pos",
    equiv_theta=False,
)

neg_last = theta2UPV(
    2090,
    phase="neg",
    equiv_theta=False,
)
# %%
# save the data
pos_first.to_netcdf(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/theta2UPV_NAO_pos_10_0_mean_1850.nc"
)

neg_first.to_netcdf(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/theta2UPV_NAO_neg_10_0_mean_1850.nc"
)
# %%
pos_last.to_netcdf(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/theta2UPV_NAO_pos_10_0_mean_2090.nc"
)
neg_last.to_netcdf(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/theta2UPV_NAO_neg_10_0_mean_2090.nc"
)

# %%
