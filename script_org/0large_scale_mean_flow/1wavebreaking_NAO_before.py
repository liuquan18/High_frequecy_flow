#%%
# import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import logging
import re
import os

from src.data_helper.read_NAO_extremes import read_NAO_extremes
from src.composite.composite_NAO_WB import read_wb
# %%
def read_all_data(decade, **kwargs):
    logging.info("reading NAO extremes")
    # wave breaking
    NAO_pos = read_NAO_extremes(decade, 'positive')
    NAO_neg = read_NAO_extremes(decade, 'negative')

    logging.info("reading wave breaking data")

    AWB = read_wb(decade, 'cwb', NAO_region=False)
    CWB = read_wb(decade, 'cwb', NAO_region=False)
    

    return NAO_pos, NAO_neg, AWB, CWB
# %%
