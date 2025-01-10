# %%
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
def read_eke( decade, suffix = '_ano_2060N', plev = 25000, **kwargs):
    var = 'eke'
    time_tag = f"{decade}0501-{decade+9}0930"
    data_path = (
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily{suffix}/"
    )
    files = glob.glob(data_path + "r*i1p1f1/" + f"{var}*{time_tag}*.nc")
    # sort files
    files.sort(key=lambda x: int(x.split('/')[-2][1:].split('i')[0]))

    data = xr.open_mfdataset(
        files, combine="nested", concat_dim="ens",
        chunks = {"ens": -1, "time": -1, "lat": -1, "lon": -1}
    )
    data = data[var]
    data.load()

    data = data.drop_vars(('plev','lat'))

    data['ens'] = range(1, 51)
    # change longitude from 0-360 to -180-180
    data = data.assign_coords(lon=(data.lon + 180) % 360 - 180).sortby("lon")

    return data

    
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
    logging.info("reading NAO extremes")
    # wave breaking
    NAO_pos = read_NAO_extremes(decade, 'positive')
    NAO_neg = read_NAO_extremes(decade, 'negative')

    logging.info("reading eke")
    eke = read_eke( decade)
    

    return NAO_pos, NAO_neg, eke

#%%
def eke_to_df(event, ratio, lag = (-20, 10)):
    

    event = pd.DataFrame(event).transpose()
    ratio_df = ratio.to_dataframe().reset_index()[['time','lon','eke']]
    ratio_df = ratio_df.pivot(index = 'lon', columns = 'time', values = 'eke')

    ratio_df.columns.name = None
    # add one more multitindex to ratio_df the same index as event
    ratio_df = pd.concat([ratio_df]*len(event), keys = event.index)

    # fill the value in ratio_df to expected_ratio_df

 
    ratio_df['ens'] = event['ens'].values[0]
    ratio_df['extreme_duration'] = event['extreme_duration'].values[0]
    ratio_df['extreme_start_time'] = event['extreme_start_time'].values[0]

    return ratio_df


# %%
def sel_before_NAO(NAO, data, lag = (-20, 10)):

    eke_evnets = []
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


        eke_df = eke_to_df(event, data_NAO_event, lag)

        eke_evnets.append(eke_df)

    eke_evnets = pd.concat(eke_evnets)

    return eke_evnets

#%%
def process_data(decade):
    # read data
    NAO_pos, NAO_neg, data = read_all_data(decade)

    # select data before NAO events
    eke_NAO_pos = sel_before_NAO(NAO_pos, data)
    eke_NAO_neg = sel_before_NAO(NAO_neg, data)

    logging.info(f"rank {rank} is saving data for decade {decade} \n")

    eke_NAO_pos.to_csv(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/eke_NAO_pos/eke_NAO_pos_{decade}.csv')
    eke_NAO_neg.to_csv(f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/eke_NAO_neg/eke_NAO_neg_{decade}.csv')
    
#%%
decades_all = np.arange(1850, 2100, 10)
decade_single = np.array_split(decades_all, size)[rank]

for decade in decade_single:
    logging.info(f"rank {rank} is processing decade {decade} \n")
    process_data(decade)

# %%
