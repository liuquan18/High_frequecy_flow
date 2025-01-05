#%%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import src.composite.composite as comp
import wavebreaking as wbtool

import geopandas as gpd
from shapely import wkt
import shapely.affinity
from shapely.geometry import box


# %%
def read_wb(dec, type, NAO_region = False):

    av_dir = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/av_daily_ano/'
    base_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/WB_{type}_daily/'

    wb_arrs = []
    for ens in range(1, 51,1):
        # wb files
        file_path = base_dir + f'r{ens}i1p1f1/*{dec}*.csv'
        file = glob.glob(file_path)[0]
        df = pd.read_csv(file)
        df["geometry"] = df["geometry"].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(df, geometry="geometry")

        av_path = av_dir + f'r{ens}i1p1f1/*{dec}*.nc'
        av = xr.open_dataset(glob.glob(av_path)[0]).AV

        wb_arr = wbtool.to_xarray(av, gdf)
        wb_arrs.append(wb_arr)

    wb = xr.concat(wb_arrs, dim='ens')

    if NAO_region:
        # lonlatbox, -90,40,30,60
        # change longitude to -180,180
        wb = wb.assign_coords(lon=(wb.lon+ 180) % 360 - 180)
        wb = wb.sortby(wb.lon)
        wb = wb.sel(lon=slice(-90, 40), lat=slice(20, 80))
    return wb

#%%
def count_wb(wb, stat = 'max'):
    wb_count = wb.where(wb > 0).count(dim=('ens', 'time'))
    if stat == 'max':
        wb_count = wb_count.max(dim=('lat', 'lon')) 
    elif stat == 'mean':
        wb_count = wb_count.mean(dim=('lat', 'lon'))
    return wb_count

def plot_wb_count(wb_count):
    p = wb_count.plot(    subplot_kws=dict(projection=ccrs.Orthographic(-20, 60), facecolor="gray"),
    transform=ccrs.PlateCarree(),
)
    p.axes.set_global()
    p.axes.coastlines()
# %%
awb_counts_dec = []
cwb_counts_dec = []

for dec in range(1850, 2100, 10):
    awb = read_wb(dec, 'awb')
    cwb = read_wb(dec, 'cwb')
    awb_count = count_wb(awb, stat='mean')
    cwb_count = count_wb(cwb, stat='mean')
    awb_counts_dec.append(awb_count)
    cwb_counts_dec.append(cwb_count)

awb_counts_dec = xr.concat(awb_counts_dec, dim='dec')
cwb_counts_dec = xr.concat(cwb_counts_dec, dim='dec')

# %%
awb_counts_dec = awb_counts_dec.assign_coords(dec=np.arange(1850, 2100, 10))
cwb_counts_dec = cwb_counts_dec.assign_coords(dec=np.arange(1850, 2100, 10))
# %%
awb_counts_dec = awb_counts_dec.to_dataframe().reset_index()[['dec','flag']]
cwb_counts_dec = cwb_counts_dec.to_dataframe().reset_index()[['dec','flag']]
# %%
awb_counts_dec.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/awb_NA_counts_dec.csv', index=False)
cwb_counts_dec.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_moisture_variability/cwb_NA_counts_dec.csv', index=False)
# %%
wb_count = pd.DataFrame()
wb_count ['count'] = (awb_counts_dec.flag + cwb_counts_dec.flag)/2
wb_count['dec'] = awb_counts_dec.dec
# %%
fig, ax = plt.subplots()
wb_count.plot(x='dec', y='count', ax=ax)
ax.set_ylabel('Wave breaking event count')
ax.set_xlabel('Decade')
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/moisture/wb_extreme_count.png")
# %%
