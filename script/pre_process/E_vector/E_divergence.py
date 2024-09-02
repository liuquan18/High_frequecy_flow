#%%
import xarray as xr
import pandas as pd
import numpy as np
import sys
import logging
logging.basicConfig(level=logging.WARNING)

# Any import of metpy will activate the accessors
import metpy.calc as mpcalc
from metpy.units import units

# %%
try:
    node = int(sys.argv[1])
except ValueError:
    logging.warning("no node number provided, using default node 0")
    node = 0

# %%
# nodes and cores
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
periods = ["first10", "last10"]
period = periods[node]

tags = ["1850_1859", "2091_2100"]
tag = tags[node]
