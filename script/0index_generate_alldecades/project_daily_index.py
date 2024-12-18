# %%
import xarray as xr
from src.index_generate.project_index import project_field_to_pattern
import mpi4py.MPI as MPI
import numpy as np
import sys
import os

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
#%%
start_years_single = np.array_split(start_years, size)[rank]  # years on this core
daily_zg_path=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/daily/zg_MJJAS_ano_decade/r{member}i1p1f1/"
eof_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result/plev_50000_decade_mpi_first_JJA_eof_result.nc"
pc_path=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/daily/projected_pc_decade_nonstd/r{member}i1p1f1/"

# mkdir pc_path
if not os.path.exists(pc_path):
    os.makedirs(pc_path)

#%%
for i, start_year in enumerate(start_years_single):
    print(f"Rank {rank}, year {start_year}-{start_year+9} {i}/{len(start_years_single)}")
    daily_file=f"{daily_zg_path}zg_day_MPI-ESM1-2-LR_r{member}i1p1f1_gn_{str(start_year)}0501-{str(start_year+9)}0930_ano.nc"

    daily_field = xr.open_dataset(daily_file).zg
    eof = xr.open_dataset(eof_path).eof.sel(mode = 'NAO', decade = str(start_year)).squeeze()

    projected_pcs = project_field_to_pattern(daily_field, eof, standard=False, plev = 50000)
    projected_pcs.name = "pc"
    projected_pcs.to_netcdf(f"{pc_path}NAO_{str(start_year)}-{str(start_year+9)}_r{member}i1p1f1_nonstd.nc")
