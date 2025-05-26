#%%
# %%
import xarray as xr
from src.index_generate.project_index import project_field_to_pattern
import mpi4py.MPI as MPI
import numpy as np
import sys
import logging
import glob
logging.basicConfig(level=logging.INFO)
# %%
decade=sys.argv[1] # 1850
# %%
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()

# %%
logging.info(f"This node is working on decade {decade}")
logging.info(f"Rank {rank} of {size} on {name}")
#%%
daily_field_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_NA_allplev_daily_ano/"

eof_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result/troposphere_ind_decade_first_JJA_eof_result_1850_2090.nc"
save_path=f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NAO_pc_{decade}_trop_nonstd"
members_all = list(range(1, 51))  # all members

# %%
members_single = np.array_split(members_all, size)[rank]  # members on this core

# %%
for i, member in enumerate(members_single):
    print(f"Rank {rank}, member {member}/{members_single[-1]}")
    daily_file=glob.glob(f"{daily_field_path}/r{member}i1p1f1/*{decade}*.nc")[0]
    daily_field = xr.open_dataset(daily_file).zg
    eof = xr.open_dataset(eof_path).eof.sel(mode = 'NAO', decade = str(decade)).squeeze()
    
    projected_pcs = project_field_to_pattern(daily_field, eof, standard=False)

    projected_pcs.name = "pc"

    projected_pcs.to_netcdf(
        f"{save_path}/NAO_pc_{decade}_r{member}_nonstd.nc"
    )
