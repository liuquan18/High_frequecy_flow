# %%
import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from src.moisture.longitudinal_contrast import read_data

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
    awb = pd.read_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wave_breaking_stat/awb_th3_NAO_overlap70.csv', index_col=0)
    cwb = pd.read_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wave_breaking_stat/cwb_th3_NAO_overlap70.csv', index_col=0)
    awb_dec = awb[awb.dec == decade]
    cwb_dec = cwb[cwb.dec == decade]


    tas = read_data("tas", decade, (20,60), False, suffix='_std')
    hus = read_data("hus", decade, (20,60), False, suffix='_std')
    data = xr.Dataset({"tas": tas, "hus": hus*1000})

    return awb_dec, cwb_dec, data
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

    expected_ratio_df.columns = ['days ' + str(i) for i in expected_ratio_df.columns]
    merged = pd.concat([event, ratio_df], axis = 1)

    return merged


# %%
def sel_before_wb(wb, data, lag = (-20, 10)):

    NAL_ratios = []
    NPO_ratios = []

    for i, event in wb.iterrows():
        event_ens = event.ens
        event_date = pd.to_datetime(event.date)
        event_date_20before = event_date + pd.Timedelta(days=lag[0])
        event_date_10after = event_date + pd.Timedelta(days=lag[1])

        data_wb_event = data.sel(time=slice(event_date_20before, event_date_10after), ens = event_ens)

        ratio = data_wb_event.hus / data_wb_event.tas

        # change the time as the difference between the event date and the date of the data
        ratio['time'] =  pd.to_datetime(ratio['time'].values) - event_date
        # change the difference to days
        ratio['time'] = ratio['time'].dt.days

        NAL_ratio, NPO_ratio = ocean_sector(ratio)

        NAL_df = merge_event_ratio(event, NAL_ratio)
        NPO_df = merge_event_ratio(event, NPO_ratio)

        NAL_ratios.append(NAL_df)
        NPO_ratios.append(NPO_df)

    NAL_ratios = pd.concat(NAL_ratios)
    NPO_ratios = pd.concat(NPO_ratios)


    return NAL_ratios, NPO_ratios

#%%
def process_data(decade):
    # read data
    awb_dec, cwb_dec, data = read_all_data(decade)

    # select the data before wb
    awb_NAL, awb_NPO = sel_before_wb(awb_dec, data)
    cwb_NAL, cwb_NPO = sel_before_wb(cwb_dec, data)

    # save the data
    awb_NAL.to_csv(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_awb_NAL/awb_NAL_{decade}.csv')
    awb_NPO.to_csv(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_awb_NPO/awb_NPO_{decade}.csv')

    cwb_NAL.to_csv(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_cwb_NAL/cwb_NAL_{decade}.csv')
    cwb_NPO.to_csv(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_ratio_cwb_NPO/cwb_NPO_{decade}.csv')


#%%
decades_all = np.arange(1850, 2100, 10)
decade_single = np.array_split(decades_all, size)[rank]

for decade in decade_single:
    logging.info(f"rank {rank} is processing decade {decade} \n")
    process_data(decade)
# %%
