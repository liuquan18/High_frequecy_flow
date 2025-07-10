#%%
import xarray as xr
import numpy as np
from src.data_helper.read_variable import read_prime_single_ens
import sys
import os
import logging
logging.basicConfig(level=logging.INFO)
# %%
#%%
import mpi4py.MPI as MPI
# %%
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()
# %%
logging.info(f"Rank {rank} of {size} is processing upvp index")
# %%
def project(pattern, field):
    
    # Align datasets to ensure coordinates match
    field, pattern = xr.align(field, pattern)

    # Optional: weight by cosine of latitude for area weighting
    weights = np.cos(np.deg2rad(pattern['lat']))
    weights.name = "weights"

    # Compute the projection index (dot product over lat/lon)
    projection_index = (field * pattern * weights).sum(dim=['lat', 'lon'])

    # Normalize the projection index by the pattern norm
    pattern_norm = np.sqrt((pattern**2 * weights).sum(dim=['lat', 'lon']))
    projection_index /= pattern_norm

    # Save to a new netCDF if needed
    projection_index.name = "phi_index"

    return projection_index
# %%
ens = sys.argv[1]

to_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/Fdiv_phi_steady_index_daily/r{ens}i1p1f1/"
if rank == 0:
    if not os.path.exists(to_path):
        os.makedirs(to_path)

#%%

all_decades = np.arange(1850, 2100, 10)
single_decades = np.array_split(all_decades, size)[rank]

for i, decade in enumerate(single_decades):
    logging.info(f"rank {rank} Processing {i+1}/{len(single_decades)} for decade {decade}")

    # read the field
    field = read_prime_single_ens(decade, ens, 'Fdiv_phi_steady', name='div', suffix='_ano', model_dir='MPI_GE_CMIP6_allplev', plev=25000)
    # read the pattern
    pattern = xr.open_dataset("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/Fdiv_phi_pattern/Fdiv_phi_steady_pattern_1850.nc").div # use the same pattern for all decades

    # project the pattern onto the field
    index = project(pattern, field)
    # save the index
    index.to_netcdf(f"{to_path}/Fdiv_phi_steady_index_{decade}.nc")
    logging.info(f"rank {rank} Finished processing decade {decade}")
