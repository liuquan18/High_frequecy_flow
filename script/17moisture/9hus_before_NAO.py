# %%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import logging
from src.moisture.longitudinal_contrast import read_data
from src.data_helper.read_NAO_extremes import read_NAO_extremes, sel_before_NAO

import re
logging.basicConfig(level=logging.INFO)
#%%
# nodes for different decades
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



#%%
def read_all_data(decade):
    # wave breaking
    NAO_pos = read_NAO_extremes(decade, 'positive')
    NAO_neg = read_NAO_extremes(decade, 'negative')


    tas = read_data("tas", decade, (20,60), True, suffix='_std')
    hus = read_data("hus", decade, (20,60), True, suffix='_std')
    data = xr.Dataset({"tas": tas, "hus": hus*1000})
    data_ratio = data.hus / data.tas
    data_ratio.name = 'hus_tas_ratio'
    data_ratio.compute()

    return NAO_pos, NAO_neg, data_ratio


#%%
def process_data(decade):
    # read data
    NAO_pos, NAO_neg, data = read_all_data(decade)

    # select the data before NAO
    ratio_NAO_pos = sel_before_NAO(NAO_pos, data, var = 'hus_tas_ratio')
    ratio_NAO_neg = sel_before_NAO(NAO_neg, data, var = 'hus_tas_ratio')


    # save the data
    ratio_NAO_pos.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_pos/hus_tas_ratio_NAO_pos_" + str(decade) + ".csv")
    ratio_NAO_neg.to_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_neg/hus_tas_ratio_NAO_neg_" + str(decade) + ".csv")   
#%%
decades_all = np.arange(1850, 2100, 10)
decade_single = np.array_split(decades_all, size)[rank]

for decade in decade_single:
    logging.info(f"rank {rank} is processing decade {decade} \n")
    process_data(decade)
# %%
