#%%
import xarray as xr
from xmca.xarray import xMCA
import numpy as np
import sys
import os
#%%
import mpi4py.MPI as MPI
# %%
period = str(sys.argv[1]) # first10 or last10
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
#%%
if period == "first10":
    NA_zg_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/daily/zg_MJJAS_ano_first10/"
    TP_OLR_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/first10_OLR_daily_ano/"
    reconstruct_OLR_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_reconstructed/first10_OLR_reconstructed/"
    reconstruct_ZG_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_zg_daily_reconstructed/first10_NA_zg_reconstructed/"

elif period == "last10":
    NA_zg_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/daily/zg_MJJAS_ano_last10/"
    TP_OLR_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/last10_OLR_daily_ano/"
    reconstruct_OLR_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_reconstructed/last10_OLR_reconstructed/"
    reconstruct_ZG_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_zg_daily_reconstructed/last10_NA_zg_reconstructed/"

#%%
# all files to be processed
NA_zg_files = os.listdir(NA_zg_dir)
TP_OLR_files = os.listdir(TP_OLR_dir)

NA_zg_files = [f for f in NA_zg_files if f.endswith('.nc')]
TP_OLR_files = [f for f in TP_OLR_files if f.endswith('.nc')]

# order lists to make ensemble members match
NA_zg_files.sort()
TP_OLR_files.sort()

# files to be processed on this core
NA_zg_single = np.array_split(NA_zg_files, size)[rank]
TP_OLR_single = np.array_split(TP_OLR_files, size)[rank]

# %%
def reconstruct(NA_zg,TP_OLR, lag = 6, nmodes = 50):
    """
    lag: int, default 6, the lag days between the two fields, NA_zg leads
    nmodes: int, default 50, the number of modes to be reconstructed
    """
    # remove the nan values on spatial dimensions
    NA_zg = NA_zg.dropna(dim = ('lon'), how = 'all').dropna(dim = 'lat', how = 'all')
    TP_OLR = TP_OLR.dropna(dim = ('lon'), how = 'all').dropna(dim = 'lat', how = 'all')

    # shift the NA_zg field by -lag days
    NA_zg = NA_zg.shift(time = -lag)
    NA_zg = NA_zg.dropna(dim = 'time', how = 'all')

    # Ensure the time coordinates match
    NA_zg, TP_OLR = xr.align(NA_zg, TP_OLR, join='inner', exclude=['lat', 'lon'])

    # Perform MCA
    mca = xMCA(NA_zg,TP_OLR)
    mca.normalize()
    mca.apply_coslat()
    mca.solve()
    reconstructed = mca.reconstructed_fields(mode = slice (1,nmodes))
    NA_zg_reconstructed = reconstructed['left']
    TP_OLR_reconstructed = reconstructed['right']
    return NA_zg_reconstructed,TP_OLR_reconstructed
# %%
def reconstruct_yearly(NA_zg, TP_OLR):

    # Create a dataset with both variables
    ds = xr.Dataset({'NA_zg': NA_zg, 'TP_OLR': TP_OLR})

    # Group the dataset by year
    grouped = ds.groupby('time.year')

    # Define a function to apply to each year's data
    def apply_reconstruct(group):
        NA_zg_year = group.NA_zg
        TP_OLR_year = group.TP_OLR
        NA_zg_reconstructed, TP_OLR_reconstructed = reconstruct(NA_zg_year, TP_OLR_year)
        return xr.Dataset({
            'NA_zg_reconstructed': NA_zg_reconstructed,
            'TP_OLR_reconstructed': TP_OLR_reconstructed
        })

    # Apply the function to each year's data
    result = grouped.map(apply_reconstruct)
    reconstructed_NA_zg = result['NA_zg_reconstructed'].dropna(dim = ('lon'), how = 'all').dropna(dim = 'lat', how = 'all')
    reconstructed_TP_OLR = result['TP_OLR_reconstructed'].dropna(dim = ('lon'), how = 'all').dropna(dim = 'lat', how = 'all')

    return reconstructed_NA_zg, reconstructed_TP_OLR

#%%
for i, (NA_zg_file, TP_OLR_file) in enumerate(zip(NA_zg_single, TP_OLR_single)):
    print(f"Rank {rank}, file {i}/{len(NA_zg_single)-1}")
    print(NA_zg_file)
    print(NA_zg_file)
    NA_zg = xr.open_dataset(NA_zg_dir + NA_zg_file).zg
    NA_zg = NA_zg.sel(plev = 50000)
    TP_OLR = xr.open_dataset(TP_OLR_dir + TP_OLR_file).rlut
    reconstructed_NA_zg, reconstructed_TP_OLR = reconstruct_yearly(NA_zg, TP_OLR)

    # save the reconstructed
    reconstructed_NA_zg.to_netcdf(reconstruct_ZG_dir + NA_zg_file)
    reconstructed_TP_OLR.to_netcdf(reconstruct_OLR_dir + TP_OLR_file)

