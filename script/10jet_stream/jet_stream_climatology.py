#%%
import xarray as xr
import sys
#%%
def jet_stream_climatology(period, allplev = False):
    if allplev:
        jet_path =  f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_allplev_{period}/'
        speed_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_speed_climatology_allplev_{period}.nc"
        loc_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_allplev_{period}.nc"
    else:
        jet_path = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_{period}/'
        speed_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_speed_climatology_{period}.nc"
        loc_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_climatology/jet_loc_climatology_{period}.nc"
    jets = xr.open_mfdataset(f'{jet_path}*.nc', combine = 'nested', concat_dim = 'ens')

    # drop lon dim
    jets = jets.isel(lon = 0).ua

    # load data into memory
    jets = jets.load()
    # maximum westerly wind speed of the resulting profile is then identified and this is defined as the jet speed.
    jet_speeds = jets.max(dim = 'lat')

    # seasonal cycle
    jet_speeds = jet_speeds.groupby('time.month').mean(dim = ('time', 'ens'))

    # save to file
    jet_speeds.to_netcdf(speed_path)

    # The jet latitude is defined as the latitude at which this maximum is found.
    jet_locs = jets.lat[jets.argmax(dim = 'lat')]

    #Smooth seasonal cycles of the jet latitude and speed are defined by averaging over all years and then Fourier filtering, retaining only the mean and the two lowest frequencies.
    jet_locs_clim = jet_locs.groupby('time.month').mean(dim = ('time', 'ens'))

    # save to file
    jet_locs_clim.to_netcdf(loc_path)
# %%
period = sys.argv[1]
allplev = sys.argv[2]
print(f"Calculating jet stream climatology for {period} with all plev = {allplev}")
jet_stream_climatology(period, allplev)

# %%
