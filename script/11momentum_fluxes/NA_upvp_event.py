#  %%
import xarray as xr
import numpy as np
import pandas as pd
# %%
import eventextreme.eventextreme as ee

# %%
import sys
import glob
import logging

logging.basicConfig(level=logging.WARNING)



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
members_all = np.arange(1,51)
members_single = np.array_split(members_all, size)[rank]
# %%
period = str(sys.argv[1])
#%%
base_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_{period}/'
AWB_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_AWB/AWB_{period}/'
CWB_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_CWB/CWB_{period}/'
# %%
def to_dataframe(pc):

    # exclude the data at 1st may to 3rd May, and the data during 28th Sep and 31st Sep
    mask_exclude = (
        (pc["time.month"] == 5) & (pc["time.day"] >= 1) & (pc["time.day"] <= 3)
    ) | ((pc["time.month"] == 9) & (pc["time.day"] >= 28) & (pc["time.day"] <= 30))
    mask_keep = ~mask_exclude

    pc = pc.where(mask_keep, drop=True)

    # convert to dataframe
    pc = pc.to_dataframe().reset_index()[["time", "ua"]]
    pc["time"] = pd.to_datetime(pc["time"].values)

    return pc
# %%
for i, member in enumerate(members_single):
    print(" Period ", period, " member ", member)

    # read the data
    file=glob.glob(base_dir+f'*r{member}i*.nc')[0]
    upvp = xr.open_dataset(file).ua.squeeze()
    upvp['time'] = upvp.indexes['time'].to_datetimeindex()

    df = to_dataframe(upvp)

    # read the threshold
    AWB_threshold = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_threshold/AWB_threshold_first10_allens.csv")
    CWB_threshold = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_threshold/CWB_threshold_first10_allens.csv")



    # extract extremes
    extremes = ee.EventExtreme(df, 'ua')

    # set thresholds
    extremes.set_positive_threshold(AWB_threshold)
    extremes.set_negative_threshold(CWB_threshold)



    # extract extremes
    AWB_extremes = extremes.extract_positive_extremes
    CWB_extremes = extremes.extract_negative_extremes


    # save the data
    AWB_extremes.to_csv(AWB_dir+f'AWB_{period}_r{member}.csv', index = False)
    CWB_extremes.to_csv(CWB_dir+f'CWB_{period}_r{member}.csv', index = False)
