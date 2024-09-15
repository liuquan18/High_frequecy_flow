#%%
import xarray as xr
import pandas as pd
import numpy as np
import sys
import logging
logging.basicConfig(level=logging.WARNING)
import glob

# Any import of metpy will activate the accessors
import metpy.calc as mpcalc
from metpy.units import units

# %%
try:
    node = int(sys.argv[1])
except ValueError:
    logging.warning("no node number provided, using default node 0")
    node = 0

# %%
# nodes and cores
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # [0,1,2,3,4,5,6,7,8,9]
    size = comm.Get_size()  # 10
except:
    logging.warning("::: Warning: Proceeding without mpi4py! :::")
    rank = 0
    size = 1

# %%
periods = ["first10", "last10"]
period = periods[node]

tags = ["1850_1859", "2091_2100"]
tag = tags[node]

# %%
frequency_tag = 'prime'
uprime_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_ano_{period}_{frequency_tag}/"
vprime_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_MJJAS_ano_{period}_{frequency_tag}/"

div_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_div_daily_global/E_div_MJJAS_ano_{period}_{frequency_tag}/"
# %%
members_all = list(range(1, 51))  # all members
members_single = np.array_split(members_all, size)[rank]  # members on this core

# %%
def divergence(u,v):
    """
    Calculate the divergence of a vector field.
    
    Parameters
    ----------
    u : xarray.DataArray
        The x component of the vector field
    v : xarray.DataArray
        The y component of the vector field
    
    Returns
    -------
    div : xarray.DataArray
        The divergence of the vector field
    """
    # units
    u = u * units('m/s')
    v = v * units('m/s')

    # smoothing the data
    u = mpcalc.smooth_gaussian(u, 5)
    v = mpcalc.smooth_gaussian(v, 5)

    # calcualte the divergence
    div = mpcalc.divergence(u, v)

    return div.metpy.dequantify()
# %%
for i, ens in enumerate(members_single):
    logging.info (f" period {period}, member {ens} {i+1}/{len(members_single)}")

    ufile = glob.glob(f"{uprime_dir}/ua_*r{ens}*.nc")[0]
    vfile = glob.glob(f"{vprime_dir}/va_*r{ens}*.nc")[0]

    u = xr.open_dataset(ufile).ua.sel(plev = 25000)
    v = xr.open_dataset(vfile).va.sel(plev = 25000)

    div = divergence(u,v)

    div.to_netcdf(f"{div_dir}/E_div_MJJAS_ano_{period}_{frequency_tag}_r{ens}.nc")

