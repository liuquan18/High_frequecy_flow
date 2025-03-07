# %%
import xarray as xr
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

import os
import sys
import glob
import logging

logging.basicConfig(level=logging.INFO)

from src.frequency.coherence import coherence_analy, sector

# %%
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
var1 = sys.argv[1]  # 'hus_std' 'hus_tas'
var2 = sys.argv[2] if len(sys.argv) > 2 else "va"  # 'va'

# true if split the var1 into NAL and NPC
split_basin = sys.argv[3].lower() == "true" if len(sys.argv) > 3 else True

pixel_wise = sys.argv[4].lower() == "true" if len(sys.argv) > 4 else True


# %%

if var1 == "vt":
    logging.error("vt is not calculated yet")

elif var1 == "hus":  # no ano because to calculate std, the mean is subtracted
    var1_path = (
        "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/hus_daily_std_mergeyear/"
    )

elif var1 == "tas":
    var1_path = (
        "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/tas_daily_std_mergeyear/"
    )

if var2 == "va":
    var2_path = (
        "/work/mh0033/m300883/High_frequecy_flow/data/ERA5/va_daily_rm_trend_mergeyear/"
    )
elif var2 == "vt":
    logging.error("vt is not calculated yet")

else:
    logging.error("Second variable is not va")

if pixel_wise:
    coherence_path = f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/{var1}_{var2}_coherence_pixelwise/"
else:
    coherence_path = (
        f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/{var1}_{var2}_coherence/"
    )

# %%
if rank == 0:
    if not os.path.exists(coherence_path):
        os.makedirs(coherence_path)


# %%
years = np.arange(1979, 2025)

years_single = np.array_split(years, size)[rank]
# %%
for i, year in enumerate(years_single):
    logging.info(f"rank {rank} Processing {year} {i+1}/{len(years_single)}")

    var1_files = glob.glob(var1_path + f"*{year}*.nc")[0]
    var2_files = glob.glob(var2_path + f"*{year}*.nc")[0]

    var1_da = xr.open_dataset(var1_files, chunks={"time": -1, "lat": -1, "lon": -1})
    var2_da = xr.open_dataset(var2_files, chunks={"time": -1, "lat": -1, "lon": -1})

    if var1 == "hus":
        var_code = "var133"
        var1_da = var1_da[var_code]

    if var1 == "tas":
        var_code = "var130"
        var1_da = var1_da[var_code]

    if var2 == "va":
        var_code = "var131"
        var2_da = var2_da[var_code]

    # merge to dataset
    var_da = xr.merge([var1_da, var2_da])

    if split_basin:
        var_da_NAL, var_da_NPC = sector(var_da, split_basin=True)

        coherence_NAL = coherence_analy(var_da_NAL, pixel_wise=pixel_wise)
        coherence_NAL.to_netcdf(
            f"{coherence_path}coherence_NAL_{var1}_{var2}_{year}.nc"
        )

        coherence_NPC = coherence_analy(var_da_NPC, pixel_wise=pixel_wise)
        coherence_NPC.to_netcdf(
            f"{coherence_path}coherence_NPC_{var1}_{var2}_{year}.nc"
        )

    else:
        var_da = sector(var_da, split_basin=False)

        coherence = coherence_analy(var_da, pixel_wise=pixel_wise)
        coherence.to_netcdf(f"{coherence_path}coherence_{var1}_{var2}_{year}.nc")


# # %%
# f = coherence_NAL.frequency.values
# Cxy = coherence_NAL.mean(dim = ('time', 'lat','lon')).values

# fig, ax1 = plt.subplots()

# ax1.plot(1/f, Cxy)
# ax1.set_xlabel('period (days)')
# ax1.set_ylabel('Coherence')


# ax1.set_xlim(0, 30)
# plt.show()


# %%
