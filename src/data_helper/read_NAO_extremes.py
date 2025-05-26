import xarray as xr
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import logging
import re
logging.basicConfig(level=logging.INFO)
from shapely import wkt


def read_NAO_extremes(decade, phase = 'positive', dur_threshold = 5):
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
    extremes = extremes[extremes['extreme_duration'] >= dur_threshold]
    return extremes

def read_NAO_extremes_single_ens(phase,dec, ens, dur_threshold = 5):

    # pos or positive to positive
    if phase == 'pos':
        phase = 'positive'
    elif phase == 'neg':
        phase = 'negative'
    else:
        pass

    base_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/extreme_events_decades/{phase}_extreme_events_decades/'

    file_path = base_dir + f'r{ens}i1p1f1/*{dec}*.csv'
    file = glob.glob(file_path)[0]
    df = pd.read_csv(file)
    df['ens'] = ens

    extremes = df[df['extreme_duration'] >= dur_threshold]
    return extremes

# read NAO for troposphere
def read_NAO_extremes_troposphere(decade, phase = 'pos', dur_threshold = 5):
    base_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/extreme_events_trop_firstlast/neg_extreme_events/neg_extreme_events_{decade}/'
    file_list = glob.glob(base_dir + "*.csv")
    # sort
    # Sort by ensemble number (rXX)
    file_list.sort(key=lambda x: int(re.search(r"_r(\d+)_neg_extremes\.csv", x).group(1)))
    extremes = []

    for ens in range(1, 51):
        filename = glob.glob(base_dir + f"*r{ens}_*.csv")[0]

    
        extreme = pd.read_csv(filename)
        extreme['ens'] = ens
        extremes.append(extreme)

    extremes = pd.concat(extremes)
    extremes = extremes[extremes['extreme_duration'] >= dur_threshold]
    return extremes




def read_NAO_extreme_ERA5(phase = 'pos', dur_threshold = 5):

    exteme_csv = f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/{phase}_extreme_events/NAO_pc_{phase}_extremes.csv"

    extreme = pd.read_csv(exteme_csv, index_col = 0)
    extreme = extreme[extreme['extreme_duration'] >= dur_threshold]
    return extreme

def sel_before_NAO(NAO, data, lag = (-20, 10), var = 'eke'):

    data_before_NAO = []
    for i, event in NAO.iterrows():
        event_ens = int(event.ens)
        event_date = pd.to_datetime(event.extreme_start_time)
        event_date_20before = event_date + pd.Timedelta(days=lag[0])
        event_date_10after = event_date + pd.Timedelta(days=lag[1])

        data_NAO_event = data.sel(time=slice(event_date_20before, event_date_10after), ens = event_ens)

        # change the time as the difference between the event date and the date of the data
        data_NAO_event['time'] =  pd.to_datetime(data_NAO_event['time'].values) - event_date
        # change the difference to days
        data_NAO_event['time'] = data_NAO_event['time'].dt.days


        data_df = xarray_to_df(event, data_NAO_event, var, lag)

        data_before_NAO.append(data_df)

    data_before_NAO = pd.concat(data_before_NAO)

    return data_before_NAO

def xarray_to_df(event, arr_data, var, lag = (-20, 10)):
    

    event = pd.DataFrame(event).transpose()
    data_df = arr_data.to_dataframe().reset_index()[['time','lon',var]]
    data_df = data_df.pivot(index = 'lon', columns = 'time', values = var)

    data_df.columns.name = None
    # add one more multitindex to ratio_df the same index as event
    data_df = pd.concat([data_df]*len(event), keys = event.index)

    # keep id info 
    data_df['ens'] = event['ens'].values[0]
    data_df['extreme_duration'] = event['extreme_duration'].values[0]
    data_df['extreme_start_time'] = event['extreme_start_time'].values[0]

    return data_df
