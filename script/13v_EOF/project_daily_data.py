#%%
import xarray as xr
from src.index_generate.project_index import project_field_to_pattern
import mpi4py.MPI as MPI
import numpy as np
import sys
import glob
# %%
period = sys.argv[1] # first10 or last10
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
#%%
daily_field_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_MJJAS_{period}/'
files = glob.glob(f'{daily_field_path}*.nc')
save_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vEOF/daily_index/daily_index_{period}/'
eof_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vEOF/montly_pattern/va_eof_{period}.nc'
# %%
files_single = np.array_split(files, size)[rank]  # files on this core
# %%
for i, file in enumerate(files_single):
    print(f"Peirod {period}, Rank {rank}, file {i+1}/{len(files_single)}")

    # get filename
    file_name = file.split('/')[-1]

    daily_field = xr.open_dataset(file).va
    daily_field = daily_field.sel(plev=25000, lat = slice(0, 90))
    eof = xr.open_dataset(eof_path).eof.squeeze()

    projected_pcs = eof.groupby('mode').apply(lambda x: project_field_to_pattern(daily_field, x.squeeze(), standard=False))

    projected_pcs.name = "pc"
    
    projected_pcs.to_netcdf(f"{save_path}{file_name}")
# %%
