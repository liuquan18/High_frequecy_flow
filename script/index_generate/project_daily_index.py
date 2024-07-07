# %%
import xarray as xr
from src.index_generate.project_index import project_field_to_pattern
import mpi4py.MPI as MPI
import numpy as np
import sys

# %%
# nodes for different periods
# first10: 1850-1859
# last10: 2091-2100

# nodes and cores
node = int(sys.argv[1])
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()

#%%
period, year_range, tag, date_range = (
    ["first10", "1850_1859", "historical", "18500601-18590831"]
    if node == 1
    else ["last10", "2091_2100", "ssp585", "20910601-21000831"]
)
print(f"Node {node} is working on {period} ({year_range})")

daily_field_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/daily/zg_JJA_ano_{period}"
eof_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/EOF_result/{period[:-2]}_pattern_projected.nc"
members_all = list(range(1, 51))  # all members
# %%
members_single = np.array_split(members_all, size)[rank]  # members on this core
# %%
for i, member in enumerate(members_single):
    print(f"Rank {rank}, member {member}/{members_single[-1]}")
    daily_field = xr.open_dataset(
        f"{daily_field_path}/zg_day_MPI-ESM1-2-LR_{tag}_r{member}i1p1f1_gn_{date_range}_ano.nc"
    )
    daily_field = daily_field.zg.sel(plev=50000).drop_vars("plev")
    eof = xr.open_dataset(eof_path).__xarray_dataarray_variable__

    projected_pcs = project_field_to_pattern(daily_field, eof, standard=False)

    projected_pcs.name = "pc"
    projected_pcs.to_netcdf(
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/daily/projected_pc_{period}_nonstd/zg_JJA_ano_{year_range}_r{member}_nonstd.nc"
    )

# %%
