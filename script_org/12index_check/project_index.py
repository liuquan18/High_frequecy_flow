# %%
from eofs.xarray import Eof

import xarray as xr
from src.index_generate.project_index import project_field_to_pattern
import mpi4py.MPI as MPI
import numpy as np
import sys
import os
import logging
import glob
logging.basicConfig(level=logging.INFO)

# %%
# nodes for different ensemble members
# cores for different years

# nodes and cores
node = int(sys.argv[1]) # ensemble members

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()

#%%
start_years = np.arange(1850, 2100, 10)
member=node
logging.info(f"This node is working on ensemble member {member}")

#%%
start_years_single = np.array_split(start_years, size)[rank]  # years on this core
daily_zg_path=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/zg_NA_daily_ano/r{member}i1p1f1/"
eof_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result/plev_50000_decade_mpi_first_JJA_eof_result.nc"
pc_path=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/0NAO_index_eofs/r{member}i1p1f1/"

# mkdir pc_path
if rank == 0:
    if not os.path.exists(pc_path):
        os.makedirs(pc_path)
#%%
for i, start_year in enumerate(start_years_single):
    print(f"Rank {rank}, year {start_year}-{start_year+9} {i}/{len(start_years_single)}")
    daily_file=glob.glob(f"{daily_zg_path}*_{str(start_year)}*.nc")[0]
    daily_field = xr.open_dataset(daily_file).zg
    eof = xr.open_dataset(eof_path).eof.sel(mode = 'NAO', decade = str(start_year)).squeeze()

    field = daily_field.sel(plev=50000)
    # Calculate cosine of latitude weights
    lats = field.lat.values
    coslat = np.cos(np.deg2rad(lats))
    weights = np.sqrt(coslat)[..., np.newaxis]  # shape (lat, 1) for broadcasting
    solver = Eof(field, weights=weights)

    solver.eofs = eof
    # EOFs are divided by the square-root of their eigenvalue
    pc1_proj = solver.projectField(field, neofs=1, eofscaling = 1).isel(mode = 0)

    pc1_proj.to_netcdf(f"{pc_path}NAO_{str(start_year)}-{str(start_year+9)}_r{member}i1p1f1_scaled.nc")