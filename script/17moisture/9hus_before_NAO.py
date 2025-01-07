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
def read_NAO_extremes(decade, phase = 'positive'):
    base_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/extreme_events_decades/{phase}_extreme_events_decades/'
    file_list = glob.glob(base_dir + f'r*i1p1f1/*{decade}*.csv')

    # sort
    file_list.sort(key=lambda x: int(x.split('/')[-2][1:].split('i')[0]))

    extremes = []
    for filename in file_list:
        match = re.search(r"/r(\d+)i1p1f1/", filename)
        if match:
            ens = match.group(1)
    
        extreme = pd.read_csv(filename)
        extreme['ens'] = ens

        extremes.append(extreme)
    extremes = pd.concat(extremes)
    return extremes

#%%
def read_all_data(decade):
    # wave breaking
    NAO_pos = read_NAO_extremes(decade, 'positive')
    NAO_neg = read_NAO_extremes(decade, 'negative')


    tas = read_data("tas", decade, (20,60), False, suffix='_std')
    hus = read_data("hus", decade, (20,60), False, suffix='_std')
    data = xr.Dataset({"tas": tas, "hus": hus*1000})

    return NAO_pos, NAO_neg, data
#%%
def ocean_sector(data):
    box_NAL = [-70, -35, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Atlantic
    box_NPO = [140, -145, 20, 60]  # [lon_min, lon_max, lat_min, lat_max] North Pacific
    data_NAL = data.sel(lon=slice(box_NAL[0], box_NAL[1])).mean(dim=("lon", "lat"))
    data_NPO1 = data.sel(lon=slice(box_NPO[0], 180))
    data_NPO2 = data.sel(lon=slice(-180, box_NPO[1]))
    data_NPO = xr.concat([data_NPO1, data_NPO2], dim="lon").mean(dim=("lon", "lat"))
    return data_NAL, data_NPO
#%%
def merge_event_ratio(event, ratio, lag = (-20, 10)):
    

    event = pd.DataFrame(event).transpose()
    expected_ratio_df = pd.DataFrame(np.nan, index = event.index, columns = np.arange(lag[0], lag[1]+1))
    ratio_df = ratio.to_dataframe(name = 'ratio')[['ratio']].transpose()

    ratio_df.index.name = None
    ratio_df.columns.name = None
    ratio_df.index = event.index

    # fill the value in ratio_df to expected_ratio_df
    expected_ratio_df[ratio_df.columns] = ratio_df

    merged = pd.concat([event, expected_ratio_df], axis = 1)

    return merged


# %%
def sel_before_NAO(NAO, data, lag = (-20, 10)):

    NAL_ratios = []
    NPO_ratios = []

    for i, event in NAO.iterrows():
        event_ens = int(event.ens)
        event_date = pd.to_datetime(event.extreme_start_time)
        event_date_20before = event_date + pd.Timedelta(days=lag[0])
        event_date_10after = event_date + pd.Timedelta(days=lag[1])

        data_NAO_event = data.sel(time=slice(event_date_20before, event_date_10after), ens = event_ens)

        ratio = data_NAO_event.hus / data_NAO_event.tas

        # change the time as the difference between the event date and the date of the data
        ratio['time'] =  pd.to_datetime(ratio['time'].values) - event_date
        # change the difference to days
        ratio['time'] = ratio['time'].dt.days

        NAL_ratio, NPO_ratio = ocean_sector(ratio)

        NAL_df = merge_event_ratio(event, NAL_ratio, lag)
        NPO_df = merge_event_ratio(event, NPO_ratio, lag)

        NAL_ratios.append(NAL_df)
        NPO_ratios.append(NPO_df)

    NAL_ratios = pd.concat(NAL_ratios)
    NPO_ratios = pd.concat(NPO_ratios)


    return NAL_ratios, NPO_ratios

#%%
def process_data(decade):
    # read data
    NAO_pos, NAO_neg, data = read_all_data(decade)

    # select the data before NAO
    NAO_pos_NAL, NAO_pos_NPO = sel_before_NAO(NAO_pos, data)
    NAO_neg_NAL, NAO_neg_NPO = sel_before_NAO(NAO_neg, data)


    # save the data
    NAO_pos_NAL.to_csv(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_pos_NAL/NAO_pos_NAL_{decade}.csv')
    NAO_pos_NPO.to_csv(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_pos_NPO/NAO_pos_NPO_{decade}.csv')

    NAO_neg_NAL.to_csv(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_neg_NAL/NAO_neg_NAL_{decade}.csv')
    NAO_neg_NPO.to_csv(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_NAO_neg_NPO/NAO_neg_NPO_{decade}.csv')

    
#%%
decades_all = np.arange(1850, 2100, 10)
decade_single = np.array_split(decades_all, size)[rank]

for decade in decade_single:
    logging.info(f"rank {rank} is processing decade {decade} \n")
    process_data(decade)
# %%
