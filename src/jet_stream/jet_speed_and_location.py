import glob
import xarray as xr
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)


# %%
def jet_stream_anomaly(jet, climatology, stat = 'loc'):

    if stat == 'speed':

        # maximum westerly wind speed of the resulting profile is then identified and this is defined as the jet speed.
        jet_speed = jet.max(dim="lat")
        jet_speed_ano = jet_speed.groupby("time.month") - climatology

        return jet_speed_ano

    elif stat == 'loc':
            
        # The jet latitude is defined as the latitude at which this maximum is found.
        jet_loc = jet.lat[jet.argmax(dim="lat")]

        jet_loc_ano = jet_loc.groupby("time.month") - climatology


        return jet_loc_ano



# %%
def jet_event(jet_locs, events, average = True):
    # change time to tiemstamp
    try:
        jet_locs['time'] = jet_locs.indexes['time'].to_datetimeindex()
    except AttributeError:
        pass
    # iterate over all events
    jet_locs_event = []
    for idx, event in events.iterrows():
        jet_loc = jet_locs.sel(
            time = slice (event.extreme_start_time, event.extreme_end_time),
            ens = event.ens
        )

        if average:
            jet_loc = jet_loc.mean(dim='time')
        # to numpy array
        jet_loc = jet_loc.values
        jet_locs_event.append(jet_loc)
    try:
        jet_locs_event = np.concatenate(jet_locs_event)
    except ValueError:
        jet_locs_event = np.array(jet_locs_event)
    return jet_locs_event