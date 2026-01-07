#%%
import xarray as xr
import numpy as np
import glob
from src.plotting.util import lon360to180
import os
import sys
import logging
logging.basicConfig(level=logging.INFO)
# %%
import mpi4py.MPI as MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#%%
def process_wb_latlonbox(dec, ens):
    
    awb_from = f"/scratch/m/m300883/MPI_GE_CMIP6/wb_anticyclonic_allisen_daily/r{ens}i1p1f1/"
    cwb_from = f"/scratch/m/m300883/MPI_GE_CMIP6/wb_cyclonic_allisen_daily/r{ens}i1p1f1/"
    
    wb_to = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_both_allisen_fldmean_dec/r{ens}i1p1f1/"
    
    if rank == 0:
        if not os.path.exists(wb_to):
            os.makedirs(wb_to)

    awb_file = glob.glob(f"{awb_from}*{dec}*.nc")[0]
    cwb_file = glob.glob(f"{cwb_from}*{dec}*.nc")[0]

    #
    awb_data = xr.open_dataset(awb_file)
    cwb_data = xr.open_dataset(cwb_file)
    #
    awb_data = lon360to180(awb_data['smooth_pv'])
    cwb_data = lon360to180(cwb_data['smooth_pv'])

    # 
    lat_bnds_awb = [40, 60]
    lon_bnds_awb = [-30, 30]

    lat_bnds_cwb = [50, 70]
    lon_bnds_cwb = [-90, -30]
    # 
    awb_fldmean = awb_data.sel(lat=slice(lat_bnds_awb[0], lat_bnds_awb[1]),
                        lon=slice(lon_bnds_awb[0], lon_bnds_awb[1])).mean(dim=['lat', 'lon']).sum(dim = 'time')
    cwb_fldmean = cwb_data.sel(lat=slice(lat_bnds_cwb[0], lat_bnds_cwb[1]),
                        lon=slice(lon_bnds_cwb[0], lon_bnds_cwb[1])).mean(dim=['lat', 'lon']).sum(dim = 'time')
    #
    wb_ds = xr.Dataset({
        'awb_fldmean': awb_fldmean,
        'cwb_fldmean': cwb_fldmean
    })


    logging.info(f"Processed dec {dec} ens {ens}")
    wb_ds.to_netcdf(f"{wb_to}wb_both_allisen_fldmean_dec_{dec}_r{ens}i1p1f1.nc")

#%%
ens = sys.argv[1]
dec_list = np.arange(1850, 2100, 10)
my_list = np.array_split(dec_list, size)[rank]
#%%
for i, dec in enumerate(my_list):
    logging.info (f"rank {rank} processing dec {dec} ens {ens} {i+1} of {len(my_list)}")
    process_wb_latlonbox(dec, ens)