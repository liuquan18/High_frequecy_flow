# %%
import wavebreaking as wb
import numpy as np
import pandas as pd
import xarray as xr
import metpy.calc as mpcalc
import metpy.units as mpunits
import cartopy.crs as ccrs
from cdo import *  # python version
import os
import sys
import glob
import logging

logging.basicConfig(level=logging.INFO)

# %%
def wavebreaking_1year(avor, mflux):
    # calculate contours
    contours = wb.calculate_contours(
        data=avor,
        contour_levels=[9.4 * 1e-5],
        periodic_add=120,  # optional
        original_coordinates=False,
    )  # optional

    # calculate overturnings index
    overturnings = wb.calculate_overturnings(
        data=avor,
        contour_levels=[9.4 * 1e-5],
        contours=contours,  # optional
        range_group=5,  # optional
        min_exp=5,  # optional
        intensity=mflux,  # optional
        periodic_add=120,
    )  # optional

    # classify
    events = overturnings

    # positive (anticyclonic) as 2, negative (cyclonic) as 1
    events = events.assign(mean_var=(events.intensity > 0).astype(int) + 1)

    return events
# %%
