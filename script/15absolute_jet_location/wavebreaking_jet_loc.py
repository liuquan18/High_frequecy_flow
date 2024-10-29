#%%
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import seaborn as sns
#%%
from src.composite.composite_NAO_WB import read_wb, lag_lead_composite
import src.composite.composite as comp
from src.extremes.extreme_read import read_extremes # NAO extremes

# %%
def jet_location_abs(period, ens):

    # Load data
    jet_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_{period}/"
    jet_file = glob.glob(f"{jet_path}*r{ens}i1p1f1*.nc")[0]

    jet = xr.open_dataset(jet_file).ua
    # drop dim lon
    jet = jet.isel(lon=0)

    jet_loc = jet.lat[jet.argmax(dim="lat")]

    jet_loc["ens"] = ens

    jet_loc['time'] = jet_loc.indexes['time'].to_datetimeindex()

    return jet_loc
#%%
def composite_NAO_jet(NAO, jet):
    NAO_jet_composites = []
    for event_id, event in NAO.iterrows():

        NAO_jet_comp = jet.sel(time=slice(event['extreme_start_time'], 
                                          event['extreme_end_time'])).mean(dim="time")

        # tag the composite with the start time and ensemble number, named as 'event'
        NAO_jet_comp['event'] = event_id
        NAO_jet_composites.append(NAO_jet_comp)

    NAO_jet_composites = xr.concat(NAO_jet_composites, dim="event")
    NAO_jet_composites = NAO_jet_composites.to_dataframe('jet_loc')
    return NAO_jet_composites[['jet_loc']]

#%%
def composite_NAO_WB(NAO, WB, lag_days = -10, WB_type = 'AWB'):
    NAO_wb_composites = []

    for event_id, event in NAO.iterrows():
        on_set_day = event['extreme_start_time']

        WB_comp = WB.sel(time=slice(on_set_day + pd.Timedelta(days = lag_days),
                                    on_set_day+pd.Timedelta(days = -1))).mean(dim="time")
        
        WB_comp['event'] = event_id
        NAO_wb_composites.append(WB_comp)

    NAO_wb_composites = xr.concat(NAO_wb_composites, dim="event")
    NAO_wb_composites = NAO_wb_composites.to_dataframe(WB_type)
    return NAO_wb_composites[[WB_type]]


# %%
def event_composite(period):

    NAO_pos_composites = []
    NAO_neg_composites = []


    for ens in range(1,51):

        jet_loc = jet_location_abs(period, ens)
        NAO_pos, NAO_neg = read_extremes(period, 8, ens, 25000)

        AWB = read_wb(period, ens, 'AWB', True)
        CWB = read_wb(period, ens, 'CWB', True)


        if not NAO_pos.empty:

            NAO_pos.index.name = 'event'
            NAO_pos['ens'] = ens
            
            NAO_pos_jet = composite_NAO_jet(NAO_pos, jet_loc)
            NAO_pos_AWB = composite_NAO_WB(NAO_pos, AWB, WB_type = 'AWB')
            NAO_pos_CWB = composite_NAO_WB(NAO_pos, CWB, WB_type = 'CWB')

            NAO_pos_composite = NAO_pos.join(NAO_pos_jet, on = 'event').join(NAO_pos_AWB, on = 'event').join(NAO_pos_CWB, on = 'event')
            NAO_pos_composites.append(NAO_pos_composite)


        if not NAO_neg.empty:
            
            NAO_neg.index.name = 'event'
            NAO_neg['ens'] = ens

            NAO_neg_jet = composite_NAO_jet(NAO_neg, jet_loc)
            NAO_neg_AWB = composite_NAO_WB(NAO_neg, AWB, WB_type = 'AWB')
            NAO_neg_CWB = composite_NAO_WB(NAO_neg, CWB, WB_type = 'CWB')

            NAO_neg_composite = NAO_neg.join(NAO_neg_jet, on = 'event').join(NAO_neg_AWB, on = 'event').join(NAO_neg_CWB, on = 'event')
            NAO_neg_composites.append(NAO_neg_composite)

    
    NAO_pos_composites = pd.concat(NAO_pos_composites, axis = 0)
    NAO_neg_composites = pd.concat(NAO_neg_composites, axis = 0)

    return NAO_pos_composites, NAO_neg_composites

# %%
first_NAO_pos, first_NAO_neg = event_composite('first10')
# %%
