#%%
from easyclimate.core.eddy import calc_eady_growth_rate
# %%
import xarray as xr
import numpy as np
import logging
import os
import sys
import glob

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# %%
simulations = sys.argv[1] # 'vco2_4xco2_land', 'vco2_4xco2_ocean', 'vco2_4xco2_all'
# %%
#%%
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
all_ens = [f"{i:02d}" for i in range(1, 25)]
ens_core = np.array_split(all_ens, size)[rank]


#%%
for i, member in enumerate(ens_core):
    logging.info(f"rank {rank} Processing ensemble member {member} {i+1}/{len(ens_core)}")

    ua_path = f"/scratch/m/m300883/{simulations}/u_monmean/ens_{member}/"
    zg_path = f"/scratch/m/m300883/{simulations}/geopoth_monmean/ens_{member}/"
    ta_path = f"/scratch/m/m300883/{simulations}/t_monmean/ens_{member}/"


    eddy_growth_rate_path = f"/scratch/m/m300883/{simulations}/eady_growth_rate_monmean/ens_{member}/"

    if 'mlo' in simulations:
        ua_path = f"/scratch/m/m300883/{simulations}/u_monmean/mlo_{member}/"
        zg_path = f"/scratch/m/m300883/{simulations}/geopoth_monmean/mlo_{member}/"
        ta_path = f"/scratch/m/m300883/{simulations}/t_monmean/mlo_{member}/"
        eddy_growth_rate_path = f"/scratch/m/m300883/{simulations}/eady_growth_rate_monmean/mlo_{member}/"

        
    if not os.path.exists(eddy_growth_rate_path):
        os.makedirs(eddy_growth_rate_path)

    # read data
    logging.info(f"   reading data for {member}...")
    ua_file = glob.glob(ua_path + "*.nc")
    zg_file = glob.glob(zg_path + "*.nc")
    ta_file = glob.glob(ta_path + "*.nc")

    ua = xr.open_dataset(ua_file[0]).u
    zg = xr.open_dataset(zg_file[0]).geopoth
    ta = xr.open_dataset(ta_file[0]).t

    logging.info("   calculating eady growth rate...")
    egr = calc_eady_growth_rate(
        u_daily_data=ua,
        z_daily_data=zg,
        temper_daily_data=ta,
        vertical_dim='plev',
        vertical_dim_units='Pa',
        lat_dim='lat',
        g = 9.81,
    )

    egr = egr.eady_growth_rate

    # save
    logging.info(f"   saving data for {member}...")
    egr.to_netcdf(os.path.join(eddy_growth_rate_path, f"eddy_growth_rate_r{member}i1p1f1.nc"))
# %%
