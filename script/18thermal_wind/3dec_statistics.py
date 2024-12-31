#%%
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from src.moisture.longitudinal_contrast import read_data
import logging
import sys
import os
logging.basicConfig(level=logging.INFO)
# %%
def frequency(block):
    return (xr.where(block['flag']>1,1,0).sum(dim=('time','ens'))/(block.time.size*block.ens.size)*100)

def extreme_freq(decade):
    logging.info(f"Processing decade {decade}")

    vt_extremes_pos = read_data("vt", decade, (20, 60), False, suffix='_extremes_pos')
    vt_extremes_neg = read_data("vt", decade, (20, 60), False, suffix='_extremes_neg')

    pos_freq = frequency(vt_extremes_pos)
    neg_freq = frequency(vt_extremes_neg)

    freq = (pos_freq + neg_freq)/2
    return freq

def decade_mean(data):
    return data.mean(dim = ('time', 'ens'))
#%%
# nodes for different decades
node = sys.argv[1]

try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # [0,1,2,3,4,5,6,7,8,9]
    size = comm.Get_size()  # 10
except:
    logging.warning("::: Warning: Proceeding without mpi4py! :::")
    rank = 0
    size = 1
#%%

decade = int(node)

#%%
logging.info(f"processing decade {decade}")

if rank == 0:
    logging.info("processing vt extremes pos")
    frequency_dec = extreme_freq(decade)
    to_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vt_daily_extremes_decade_freq/"
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    frequency_dec.to_netcdf(to_path + f"vt_extreme_dec_{decade}.nc")

if rank == 1:
    logging.info("processing tas")
    tas = read_data("tas", decade, (20, 60), meridional_mean=False)
    tas_dec = decade_mean(tas)
    to_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_daily_std_extremes_decade_freq/"
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    tas_dec.to_netcdf(to_path + f"tas_std_dec_{decade}.nc")

if rank == 2:
    logging.info("processing hus")
    hus = read_data("hus", decade, (20, 60), meridional_mean=False)
    hus_dec = decade_mean(hus)
    to_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_daily_std_extremes_decade_freq/"
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    hus_dec.to_netcdf(to_path + f"hus_std_dec_{decade}.nc")

if rank == 3:
    logging.info("processing va")
    va = read_data("va", decade, (20, 60), meridional_mean=False)
    va_dec = decade_mean(va)
    to_path = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_extremes_decade_freq/"
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    va_dec.to_netcdf(to_path + f"va_extreme_dec_{decade}.nc")