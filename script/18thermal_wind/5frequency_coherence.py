#%%
import xarray as xr
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

import os
import sys
import glob
import logging
logging.basicConfig(level=logging.INFO)

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

if rank == 0:
    logging.info(f"::: Running on {size} cores :::")


# %%
member=sys.argv[1]
var1 = sys.argv[2] # 'vt', 'hus_std' 'hus_tas'
var2 = sys.argv[3] if len(sys.argv) > 3 else 'va' # 'va'

# true if split teh var1 into NAL and NPO
split_basin = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else False

pixel_wise = sys.argv[5].lower() == 'true' if len(sys.argv) > 5 else False


#%%

if var1 == 'vt':
    var1_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vt_daily_ano/r{member}i1p1f1/'

elif var1 == 'hus_std': # no ano because to calculate std, the mean is subtracted
    var1_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_daily_std/r{member}i1p1f1/'

elif var1 == 'tas_std':
    var1_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_daily_std/r{member}i1p1f1/'

elif var1 == 'hus_tas':
    var1_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_daily_std/r{member}i1p1f1/'

elif var1 == 'vtm':
    var1_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vtm_daily_ano/r{member}i1p1f1/'

if var2 == 'va':
    var2_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_ano_lowlevel/r{member}i1p1f1/'
elif var2 == 'vt':
    var2_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vt_daily_ano/r{member}i1p1f1/'


else:
    logging.error("Second variable is not va")

if pixel_wise:
    coherence_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var1}_{var2}_coherence_pixelwise/r{member}i1p1f1/'
else:
    coherence_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var1}_{var2}_coherence/r{member}i1p1f1/'

#%%
if rank == 0:
    if not os.path.exists(coherence_path):
        os.makedirs(coherence_path)
    logging.info (f"Processing member {member} between {var1} and {var2}")

#%%
def coherence_analy(da, pixel_wise = False):

    """pixel wise for same variable, e.g., vt and va, spatial average for different variables, e.g., vt and hus_std"""

    if pixel_wise:
        da1 = da[list(da.data_vars)[0]]
        da2 = da[list(da.data_vars)[1]]

        # calculate coherence every year, 153 long,segement lenth 76, 50% overlap
        f, Cxy = signal.coherence(da1, da2, fs = 1, nperseg=76, detrend =False, noverlap = 38, axis = 0)
        Cxy = xr.DataArray(Cxy, dims = ['frequency', 'lat', 'lon'], coords = {'frequency': f, 'lat': da1.lat, 'lon': da1.lon})

    else:
        try:
            da = da.mean(dim = ('lat', 'lon'))
        except ValueError:
            logging.warning("No lat lon dimension, skipping spatial average")
            pass

        da1 = da[list(da.data_vars)[0]]
        da2 = da[list(da.data_vars)[1]]

        # calculate coherence every year, 153 long,segement lenth 76, 50% overlap
        f, Cxy = signal.coherence(da1, da2, fs = 1, nperseg=76, detrend =False, noverlap = 38, axis = 0)

        Cxy = xr.DataArray(Cxy, dims = ['frequency'], coords = {'frequency': f})

    Cxy.name = 'coherence'

    return Cxy
#%%
def sector(data, split_basin = True):
    # change lon from 0-360 to -180-180
    data = data.assign_coords(lon=(data.lon + 180) % 360 - 180).sortby("lon")
    data = data.sel(lat = slice(20, 60))
    if split_basin:
            
        box_NAL = [-70, -35, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Atlantic
        box_NPO = [140, -145, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Pacific

        data_NAL = data.sel(lon=slice(box_NAL[0], box_NAL[1]))
        data_NPO1 = data.sel(lon=slice(box_NPO[0], 180))
        data_NPO2 = data.sel(lon=slice(-180, box_NPO[1]))
        data_NPO = xr.concat([data_NPO1, data_NPO2], dim="lon")

        return data_NAL, data_NPO

    else:
        data = data
        return data


#%%
decades = range(1850, 2100, 10)
decades_single = np.array_split(decades, size)[rank]

#%%
for i, decade in enumerate(decades_single):

    logging.info(f"rank {rank} Processing {decade} {i+1}/{len(decades_single)}")
    var1_files = glob.glob(var1_path + f"*{decade}*.nc")[0]
    var2_files = glob.glob(var2_path + f"*{decade}*.nc")[0]

    var1_da = xr.open_dataset(var1_files, chunks = {'time': -1, 'lat': -1, 'lon': -1})
    var2_da = xr.open_dataset(var2_files, chunks = {'time': -1, 'lat': -1, 'lon': -1})

    try:
        var1_da = var1_da[var1]
    except KeyError:
        var1_name = list(var1_da.data_vars)[-1]
        var1_da = var1_da[var1_name]
        logging.warning(f"Variable {var1} not found in the file, using {var1_name} instead")

    try:
        var2_da = var2_da[var2]
    except KeyError:
        var2_name = list(var2_da.data_vars)[-1]
        var2_da = var2_da[var2_name]
        logging.warning(f"Variable {var2} not found in the file, using {var2_name} instead")

    # merge to dataset
    var_da = xr.merge([var1_da, var2_da])


    if split_basin:
        var_da_NAL, var_da_NPO = sector(var_da, split_basin=True)

        coherence_NAL = var_da_NAL.resample(time = '1YE').apply(coherence_analy, pixel_wise = pixel_wise)
        coherence_NAL.to_netcdf(f"{coherence_path}coherence_NAL_{var1}_{var2}_{decade}0501_{decade+9}0931.nc")


        coherence_NPO = var_da_NPO.resample(time = '1YE').apply(coherence_analy, pixel_wise = pixel_wise)
        coherence_NPO.to_netcdf(f"{coherence_path}coherence_NPO_{var1}_{var2}_{decade}0501_{decade+9}0931.nc")

    else:
        var_da = sector(var_da, split_basin=False)

        coherence = var_da.resample(time = '1YE').apply(coherence_analy, pixel_wise = pixel_wise)
        coherence.to_netcdf(f"{coherence_path}coherence_{var1}_{var2}_{decade}0501_{decade+9}0931.nc")



# %%
f = coherence_NAL.frequency.values
Cxy = coherence_NAL.mean(dim = ('time', 'lat','lon')).values

fig, ax1 = plt.subplots()

ax1.plot(1/f, Cxy)
ax1.set_xlabel('period (days)')
ax1.set_ylabel('Coherence')


ax1.set_xlim(0, 30)
plt.show()


# %%
