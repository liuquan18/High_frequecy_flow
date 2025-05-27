# %%
import pandas as pd
import numpy as np
import xarray as xr
from src.extremes.extreme_read import read_extremes_allens
from src.dynamics.jet_speed_and_location import jet_event

# %%

################ old jet, should be updated #############


##### jet stream
def read_anomaly(period, same_clim=True, eddy=True):

    # anomaly
    ano_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/loc_anomaly/"
    clima_label = "sameclima" if same_clim else "diffclima"
    eddy_label = "eddy" if eddy else "noneddy"

    ano_path = f"{ano_dir}jet_stream_anomaly_{eddy_label}_{clima_label}_{period}.nc"

    loc_ano = xr.open_dataset(ano_path).lat_ano

    return loc_ano


same_clim = False
eddy = True

first10_ano = read_anomaly("first10", same_clim=same_clim, eddy=eddy)
last10_ano = read_anomaly("last10", same_clim=same_clim, eddy=eddy)


first10_pos_events, first10_neg_events = read_extremes_allens("first10", 8)
last10_pos_events, last10_neg_events = read_extremes_allens("last10", 8)


# select 250 hPa only
first10_pos_events = first10_pos_events[first10_pos_events["plev"] == 25000]
first10_neg_events = first10_neg_events[first10_neg_events["plev"] == 25000]

last10_pos_events = last10_pos_events[last10_pos_events["plev"] == 25000]
last10_neg_events = last10_neg_events[last10_neg_events["plev"] == 25000]


jet_loc_first10_pos = jet_event(first10_ano, first10_pos_events)
jet_loc_first10_neg = jet_event(first10_ano, first10_neg_events)

jet_loc_last10_pos = jet_event(last10_ano, last10_pos_events)
jet_loc_last10_neg = jet_event(last10_ano, last10_neg_events)
# %%
# save jet location
# to dataframe
jet_loc_first10_pos_df = pd.DataFrame(
    {
        "jet_loc": jet_loc_first10_pos,
    }
)
jet_loc_first10_neg_df = pd.DataFrame(
    {
        "jet_loc": jet_loc_first10_neg,
    }
)
jet_loc_last10_pos_df = pd.DataFrame(
    {
        "jet_loc": jet_loc_last10_pos,
    }
)
jet_loc_last10_neg_df = pd.DataFrame(
    {
        "jet_loc": jet_loc_last10_neg,
    }
)
# save to csv
jet_loc_first10_pos_df.to_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_distribution/jet_loc_first10_pos.csv",
    index=False,
)
jet_loc_first10_neg_df.to_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_distribution/jet_loc_first10_neg.csv",
    index=False,
)
jet_loc_last10_pos_df.to_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_distribution/jet_loc_last10_pos.csv",
    index=False,
)
jet_loc_last10_neg_df.to_csv(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0composite_distribution/jet_loc_last10_neg.csv",
    index=False,
)   

# %%
