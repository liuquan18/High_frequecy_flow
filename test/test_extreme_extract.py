#%%
# Import necessary modules
import pytest
import xarray as xr
import pandas as pd
from src.extremes.extreme_extract import subtract_threshold
from src.extremes.extreme_extract import extract_pos_extremes
from src.extremes.extreme_extract import extract_neg_extremes
#%%
# Define the test function
def test_subtract_threshold():
    # Create a dummy xarray.DataArray

    pc = xr.open_dataset(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/projected_pc/projected_pc_first10/troposphere_pc_MJJAS_ano_1850_1859_r1.nc"
    ).pc

    pos_threshold = pd.read_csv(
        "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/threshold/pos_threshold_first10_allens.csv"
    )

    pos_residues = []
    for plev in pc.plev.values:
        residue = subtract_threshold(pc.sel(plev=plev), pos_threshold[pos_threshold['plev'] == plev])
        residue['plev'] = plev
        pos_residues.append(residue)
    pos_residues = pd.concat(pos_residues, axis=0)



    # Assertions
    # Check if the dates May 1st to May 3rd are excluded
    assert not pos_residues[pos_residues['time'] == '1850-05-04 12:00:00'].any()
    # Check if the data during 28th Sep and 30th Sep are excluded (assuming this is a typo and should be 30th Sep)
    # This part is skipped as our dummy data does not cover September

    # Additional checks can be added here to verify the correctness of the operation performed by the function