#%%
import pandas as pd
import numpy as np
import xarray as xr
import glob
import sys
# %%
eddy = sys.argv[1] if len(sys.argv) > 1 else "transient"
div = sys.argv[2] if len(sys.argv) > 2 else "div_phi"
phase = sys.argv[3] if len(sys.argv) > 3 else "pos"
plev = int(sys.argv[4]) if len(sys.argv) > 4 else 25000
# %%
# eddy = 'transient'
# div = 'div_phi'
# phase = 'pos'
# plev = 25000
# %%
def read_EP_flux_ERA5(eddy, div, phase, plev):
    EP_flux_dir = (
        "/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/"
    )
    
    if phase in ["pos", "neg"]:
        F = xr.open_dataarray(f"{EP_flux_dir}{eddy}_{div}_{phase}_anoFalse.nc", chunks = 'auto')
    elif phase == 'clima':
        F = xr.open_dataarray(f"{EP_flux_dir}{eddy}_{div}_clima.nc", chunks = 'auto')
    else:
        raise ValueError("Phase must be 'pos', 'neg', or 'clima'.")
    
    if plev is not None:
        F = F.sel(plev=plev)
    
    return F

def to_dataframe(ds, var_name, phase):

    ds = ds.sel(lat=slice(80, 40), lon=slice(280, 360))
    # create weights
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"
    ds = ds.weighted(weights)

    ds = ds.mean(dim=["lat", "lon"])

    df = ds.to_dataframe(var_name).reset_index()
    df["phase"] = phase
    return df

# %%
ds = read_EP_flux_ERA5(eddy, div, phase, plev)
# %%
div_df = to_dataframe(ds, div, phase)
# %%
# save to csv
output_file = f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/{eddy}_{div}_{phase}_plev_{plev}.csv"
div_df.to_csv(output_file, index=False)
print(f"Saved {output_file}")
# %%
