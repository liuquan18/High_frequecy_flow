#%%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import logging
import re
import os
import wavebreaking as wb


from src.data_helper.read_NAO_extremes import read_NAO_extremes_single_ens
from src.composite.composite import range_NAO_composite
from src.data_helper import read_variable 
from src.data_helper import read_wb 
import importlib
importlib.reload(read_wb)
read_wb_single_ens = read_wb.read_wb_single_ens
read_prime_single_ens = read_variable.read_prime_single_ens

import mpi4py.MPI as MPI
# %%
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()
# %%
def read_all_data(decade,ens, **kwargs):
    logging.info("reading NAO extremes")
    # wave breaking
    NAO_pos = read_NAO_extremes_single_ens('pos', decade, ens)
    NAO_neg = read_NAO_extremes_single_ens('neg', decade, ens )

    logging.info("reading wave breaking data")
    AWB = read_wb_single_ens(decade, ens, 'awb')
    CWB = read_wb_single_ens(decade, ens, 'cwb')

    logging.info("reading AV data")
    AV = read_prime_single_ens(decade, ens, 'av', suffix = '', name = 'AV')
    

    # convert events to arrays
    AWB_array = wb.to_xarray(AV, AWB)
    CWB_array = wb.to_xarray(AV, CWB)


    return NAO_pos, NAO_neg, AWB_array, CWB_array
# %%

# %%
decade = int(sys.argv[1]) if len(sys.argv) > 1 else 1850
logging.info(f"decade: {decade}")
# %%
members = np.arange(1, 51)  # all members
members_single = np.array_split(members, size)[rank]  # members on this core

# %%

pos_AWBs = []
neg_AWBs = []

pos_CWBs = []
neg_CWBs = []

for i, member in enumerate(members_single):
    print(f"Rank {rank}, member {member}/{members_single[-1]}")

    # read data
    NAO_pos, NAO_neg, AWB, CWB = read_all_data(decade, member)

    # select data before NAO events
    pos_AWB, neg_AWB = range_NAO_composite(AWB, NAO_pos, NAO_neg)
    pos_CWB, neg_CWB = range_NAO_composite(CWB, NAO_pos, NAO_neg)

    pos_AWBs.append(pos_AWB)
    neg_AWBs.append(neg_AWB)

    pos_CWBs.append(pos_CWB)
    neg_CWBs.append(neg_CWB)

# combine all members from all cores
pos_AWBs = xr.concat(pos_AWBs, dim="ens").sum(dim="ens")
neg_AWBs = xr.concat(neg_AWBs, dim="ens").sum(dim="ens")
pos_CWBs = xr.concat(pos_CWBs, dim="ens").sum(dim="ens")
neg_CWBs = xr.concat(neg_CWBs, dim="ens").sum(dim="ens")


# concatenate all members
if rank == 0:
    logging.info("combining all members")
    # flatten the gathered lists
    pos_AWBs = [item for sublist in pos_AWBs for item in sublist]
    neg_AWBs = [item for sublist in neg_AWBs for item in sublist]
    pos_CWBs = [item for sublist in pos_CWBs for item in sublist]
    neg_CWBs = [item for sublist in neg_CWBs for item in sublist]
    pos_AWBs = xr.concat(pos_AWB, dim="ens")
    neg_AWBs = xr.concat(neg_AWB, dim="ens")
    pos_CWBs = xr.concat(pos_CWB, dim="ens")
    neg_CWBs = xr.concat(neg_CWB, dim="ens")

    # save data
    logging.info("saving data")

    pos_AWBs.to_netcdf(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_range/AWB_pos_{decade}.nc')
    neg_AWBs.to_netcdf(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_range/AWB_neg_{decade}.nc')
    pos_CWBs.to_netcdf(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_range/CWB_pos_{decade}.nc')
    neg_CWBs.to_netcdf(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_range/CWB_neg_{decade}.nc')

    