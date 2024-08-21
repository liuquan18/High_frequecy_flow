import glob
import pandas as pd
import src.extremes.extreme_read as er
# %%
def read_extremes(period, member, extreme_type="pos", dur_lim=8):
    """
    Read the NAO and OLR extremes
    """
    NAO_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{extreme_type}_extreme_events/{extreme_type}_extreme_events_{period}/"
    OLR_dir = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_extremes_pos/OLR_extremes_pos_{period}/"  # no extreme_type in the OLR_extremes

    # read NAO positive extremes
    NAO_file = glob.glob(
        f"{NAO_dir}troposphere_{extreme_type}_extreme_events*r{member}.csv"
    )[0]
    NAO_pos = pd.read_csv(NAO_file)
    NAO_pos = NAO_pos[NAO_pos["plev"] == 25000]

    # select extremes based on minimum duration
    NAO_pos = er.sel_event_above_duration(
        NAO_pos, duration=dur_lim, by="extreme_duration"
    )
    # select columns
    NAO_pos = NAO_pos[["sign_start_time", "extreme_duration"]]

    # read OLR extremes
    OLR_file = glob.glob(f"{OLR_dir}OLR_extremes*r{member}.csv")[0]
    OLR = pd.read_csv(OLR_file)
    # select extremes based on minimum duration but not limited in JJA
    OLR = OLR[OLR["extreme_duration"] >= dur_lim]
    # select columns
    OLR = OLR[["sign_start_time", "extreme_duration", "lat", "lon"]]

    return NAO_pos, OLR
