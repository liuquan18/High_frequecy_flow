# %%
import xarray as xr
import numpy as np
from src.dynamics.theta_on_pv import theta_on_2pvu

# %%
from src.data_helper.prime_data import read_composite_MPI

# %%
import importlib
import src.dynamics.theta_on_pv
#%%
time_window = "12_6"

# %%
def theta2UPV(
    decade,
    phase="pos",
    equiv_theta=False,
    time_window = "10_0",
):
    if equiv_theta:
        theta = read_composite_MPI(
            "equiv_theta",
            "etheta",
            decade,
            before=time_window,
            return_as=phase,
            ano=False,
        )
    else:
        theta = read_composite_MPI(
            "theta",
            "theta",
            decade,
            before=time_window,
            return_as=phase,
            ano=False,
        )
    uwnd = read_composite_MPI(
        "ua",
        "ua",
        decade,
        before=time_window,
        return_as=phase,
        ano=False,
    )

    vwnd = read_composite_MPI(
        "va",
        "va",
        decade,
        before=time_window,
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
    time_window = time_window,
)
# %%
neg_first = theta2UPV(
    1850,
    phase="neg",
    equiv_theta=False,
    time_window = time_window,
)

# %%
pos_last = theta2UPV(
    2090,
    phase="pos",
    equiv_theta=False,
    time_window = time_window,
)

neg_last = theta2UPV(
    2090,
    phase="neg",
    equiv_theta=False,
    time_window = time_window,
)

#%%
pos_first.name = "theta2PVU"
neg_first.name = "theta2PVU"
pos_last.name = "theta2PVU"
neg_last.name = "theta2PVU"
# %%
# save the data
pos_first.to_netcdf(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results_without_ano/theta2PVU_NAO_pos_{time_window}_mean_1850.nc"
)

neg_first.to_netcdf(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results_without_ano/theta2PVU_NAO_neg_{time_window}_mean_1850.nc"
)
# %%
pos_last.to_netcdf(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results_without_ano/theta2PVU_NAO_pos_{time_window}_mean_2090.nc"
)
neg_last.to_netcdf(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results_without_ano/theta2PVU_NAO_neg_{time_window}_mean_2090.nc"
)

# %%
