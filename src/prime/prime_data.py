import xarray as xr
import numpy as np
import glob

def read_prime( decade, var='eke', **kwargs):
    """
    read high frequency data
    """
    
    name = kwargs.get('name', var) # default name is the same as var
    plev = kwargs.get('plev', None)
    suffix = kwargs.get('suffix', '_ano')

    time_tag = f"{decade}0501-{decade+9}0930"
    data_path = (
        f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{var}_daily{suffix}/"
    )
    files = glob.glob(data_path + "r*i1p1f1/" + f"*{time_tag}*.nc")
    # sort files
    files.sort(key=lambda x: int(x.split('/')[-2][1:].split('i')[0]))

    data = xr.open_mfdataset(
        files, combine="nested", concat_dim="ens",
        chunks = {"ens": 1, "time": -1, "lat": -1, "lon": -1, "plev": 1},
        parallel=True,
    )
    data = data[name]
    if plev is not None:
        data = data.sel(plev = plev)

    data['ens'] = range(1, 51)

    return data

def read_prime_ERA5(var = 'eke', model = 'ERA5_allplev', **kwargs):

    name = kwargs.get('name', var) # default name is the same as var
    plev = kwargs.get('plev', None)
    suffix = kwargs.get('suffix', '_ano')

    data_path = f"/work/mh0033/m300883/High_frequecy_flow/data/{model}/{var}_daily{suffix}/"

    files = glob.glob(data_path + "*.nc")

    files.sort()

    data = xr.open_mfdataset(
        files, combine = 'by_coords',
        chunks = {"time": 10, "lat": -1, "lon": -1, "plev": 1},
        parallel = True
    )
    data = data[name]
    if plev is not None:
        data = data.sel(plev = plev)

    return data