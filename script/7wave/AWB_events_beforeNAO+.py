#%%
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import glob
import logging
import sys
logging.basicConfig(level=logging.WARNING)

#%%
import src.extremes.extreme_read as er

# %%
def read_NAO_AWB(period, ens, plev, extreme_type):
    NAO_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{extreme_type}_extreme_events/{extreme_type}_extreme_events_{period}/"
    NAO_file = glob.glob(f"{NAO_path}troposphere_{extreme_type}_*_r{ens}.csv")[0]

    AWB_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/AWB_events/AWB_events_{period}/"
    AWB_file = glob.glob(f"{AWB_path}WB_MPI-ESM1-2-LR*_r{ens}i1p1f1_gn_*.csv")[0]

    NAO = pd.read_csv(NAO_file)
    AWB = pd.read_csv(AWB_file)

    #select NAO extremes duration > 7 days
    NAO = NAO[NAO['plev'] == plev]
    NAO = er.sel_event_above_duration(NAO, 7)

    # convert "18500501_12" to datetime
    AWB['Date'] = pd.to_datetime(AWB['Date'], format='%Y%m%d_%H')
    return NAO,AWB


#%%
# Extract year from 'Date' column in AWB
def select_AWB_before_NAO(NAO, AWB):
    AWB['Year'] = AWB['Date'].dt.year

    # Extract year from 'extreme_end_time' in NAO
    NAO['Year'] = NAO['extreme_end_time'].dt.year


    # Create a dictionary to store the max 'extreme_end_time' for each year in NAO
    nao_max_times = NAO.groupby('Year')['extreme_end_time'].max().to_dict()

    # Define a function to filter AWB rows
    def awb_before_nao(group):
        year = group['Year'].iloc[0]
        if year in nao_max_times:
            return group[group['Date'] < nao_max_times[year]]
        return pd.DataFrame()  # Return an empty DataFrame if the year isn't in NAO

    # Apply the filter function to AWB, grouped by 'Flag' and 'Year'
    filtered_AWB = AWB.groupby(['Flag', 'Year'])[['Flag','Year','Date','Longitude','Latitude','Intensity','Size']].apply(awb_before_nao).reset_index(drop=True)

    if not filtered_AWB.empty:
        # Remove the temporary 'Year' column if you don't need it
        filtered_AWB = filtered_AWB.drop('Year', axis=1)
        return filtered_AWB
    else:
        return pd.DataFrame()
#%%
def plot_tracks(WB_df, ax):
    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.coastlines()
    ax.coastlines() # add coastlines

    #need to split each blocking track due to longitude wrapping (jumping at map edge)
    for bid in np.unique(np.asarray(WB_df['Flag'])): #select blocking id
        lons = np.asarray(WB_df['Longitude'].iloc[np.where(WB_df['Flag']==bid)])
        lats = np.asarray(WB_df['Latitude'].iloc[np.where(WB_df['Flag']==bid)])

        # cosmetic: sometimes there is a gap near map edge where track is split:
        lons[lons >= 355] = 359.9
        lons[lons <= 3] = 0.1
        segment = np.vstack((lons,lats))

        #move longitude into the map region and split if longitude jumps by more than "threshold"
        lon0 = 0 #center of map
        bleft = lon0-0.
        bright = lon0+360
        segment[0,segment[0]> bright] -= 360
        segment[0,segment[0]< bleft]  += 360
        threshold = 180  # CHANGE HERE
        isplit = np.nonzero(np.abs(np.diff(segment[0])) > threshold)[0]
        subsegs = np.split(segment,isplit+1,axis=+1)

        #plot the tracks
        for seg in subsegs:
            x,y = seg[0],seg[1]
            ax.plot(x ,y,c = 'm',linewidth=1, transform=ccrs.PlateCarree())
        #plot the starting points
        ax.scatter(lons[0],lats[0],s=11,c='m', zorder=10, edgecolor='black', transform=ccrs.PlateCarree())

# %%

first10_pos_AWBs = []
for ens in range(1,51):
    NAO, AWB = read_NAO_AWB('first10', ens, 25000, 'pos')
    first10_pos_AWB = select_AWB_before_NAO(NAO, AWB)
    first10_pos_AWBs.append(first10_pos_AWB)
first10_pos_AWBs = pd.concat(first10_pos_AWBs)



# %%
last10_pos_AWBs = []
for ens in range(1,51):
    NAO, AWB = read_NAO_AWB('last10', ens, 25000, 'pos')
    last10_pos_AWB = select_AWB_before_NAO(NAO, AWB)
    last10_pos_AWBs.append(last10_pos_AWB)

last10_pos_AWBs = pd.concat(last10_pos_AWBs)

# %%
fig, ax = plt.subplots(2, 1, figsize=(10,5), subplot_kw=dict(projection=ccrs.PlateCarree(-120)))
plot_tracks(first10_pos_AWBs, ax[0])
ax[0].set_title('AWB events before NAO+ events in the First 10 years ')

plot_tracks(last10_pos_AWBs, ax[1])
ax[1].set_title('AWB events before NAO+ events in the Last 10 years ')
ax[1].set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
ax[1].set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])
for ax in [ax[0], ax[1]]:
    ax.set_yticks(range(0, 90, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(0, 90, 30)])

plt.savefig('/work/mh0033/m300883/High_frequecy_flow/docs/plots/wave_break/AWB_before_NAO.png')
# %%
last10_pos_AWBs
# %%
