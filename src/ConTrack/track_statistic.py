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
def read_NAO_WB(period, ens, plev, extreme_type, wave_type = 'AWB'):
    NAO_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{extreme_type}_extreme_events/{extreme_type}_extreme_events_{period}/"
    NAO_file = glob.glob(f"{NAO_path}troposphere_{extreme_type}_*_r{ens}.csv")[0]

    WB_path = f"/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/{wave_type}_events/{wave_type}_events_{period}/"
    WB_file = glob.glob(f"{WB_path}WB_MPI-ESM1-2-LR*_r{ens}i1p1f1_gn_*.csv")[0]

    NAO = pd.read_csv(NAO_file)
    WB = pd.read_csv(WB_file)

    #select NAO extremes duration > 7 days
    NAO = NAO[NAO['plev'] == plev]
    NAO = er.sel_event_above_duration(NAO, 7)

    # convert "18500501_12" to datetime
    WB['Date'] = pd.to_datetime(WB['Date'], format='%Y%m%d_%H')
    return NAO,WB


#%%
# Extract year from 'Date' column in WB
def select_WB_before_NAO(NAO, WB):
    WB['Year'] = WB['Date'].dt.year

    # Extract year from 'extreme_end_time' in NAO
    NAO['Year'] = NAO['extreme_end_time'].dt.year


    # Create a dictionary to store the max 'extreme_end_time' for each year in NAO
    nao_years = NAO['Year'].unique()

    # Define a function to filter WB rows
    def WB_before_nao(group):
        
        year = group['Year'].iloc[0]
        WB_sels = []
        if year in nao_years:
            for i, nao in NAO[NAO['Year'] == year].iterrows(): # there may be multiple NAO events in a year
                lag_days = group['Date'].iloc[-1] - nao['extreme_start_time'] # > 0 if WB end time is before the NAO start time
                group['lag_days'] = lag_days.days
                WB_sels.append(group[group['lag_days'] < 0])
            if WB_sels:
                return pd.concat(WB_sels)
            else:
                return pd.DataFrame()
        else:
            return pd.DataFrame()  # Return an empty DataFrame if the year isn't in NAO

    # Apply the filter function to WB, grouped by 'Flag' and 'Year'
    filtered_WB = WB.groupby(['Flag', 'Year', 'ens'])[WB.columns].apply(WB_before_nao).reset_index(drop=True)

    if not filtered_WB.empty:
        # Remove the temporary 'Year' column if you don't need it
        filtered_WB = filtered_WB.drop('Year', axis=1)
        return filtered_WB
    else:
        return pd.DataFrame()

#%%
def select_WB_during_NAO(NAO, WB):
    WB['Year'] = WB['Date'].dt.year

    # Extract year from 'extreme_end_time' in NAO
    NAO['Year'] = NAO['extreme_end_time'].dt.year

    # Create a dictionary to store the max 'extreme_end_time' for each year in NAO
    nao_years = NAO['Year'].unique()

    # Define a function to filter WB rows
    def WB_during_nao(group):
        
        year = group['Year'].iloc[0]
        WB_sels = []
        if year in nao_years:
            for i, nao in NAO[NAO['Year'] == year].iterrows(): # there may be multiple NAO events in a year
                WB_lead_days = group['Date'].iloc[-1] - nao['extreme_start_time'] # > 0 if WB start time is before the NAO start time
                WB_lag_days = group['Date'].iloc[-1] - nao['extreme_end_time'] # > 0 if WB end time is before the NAO end time
                group['lead_days'] = WB_lead_days.days
                group['lag_days'] = WB_lag_days.days

                WB_sels.append(group[(group['lead_days'] >=0 ) & (group['lag_days'] <= 0)])
            if WB_sels:
                return pd.concat(WB_sels)
            else:
                return pd.DataFrame()
        else:
            return pd.DataFrame()  # Return an empty DataFrame if the year isn't in NAO

    # Apply the filter function to WB, grouped by 'Flag' and 'Year'
    filtered_WB = WB.groupby(['Flag', 'Year','ens'])[WB.columns].apply(WB_during_nao).reset_index(drop=True)

    if not filtered_WB.empty:
        # Remove the temporary 'Year' column if you don't need it
        filtered_WB = filtered_WB.drop('Year', axis=1)
        return filtered_WB
    else:
        return pd.DataFrame()



#%%
def get_color_map(lag_days):
    # Normalize the lag_days to a 0-1 range
    normalized = (lag_days - (-128)) / (0 - (-128))
    
    # Create a colormap - you can experiment with different colormaps
    cmap = plt.cm.get_cmap('RdBu_r')  # Yellow-Orange-Red colormap
    
    # Return the RGB color values
    return cmap(normalized)

#%%
def plot_tracks(WB_df, ax):
    ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
    ax.coastlines()

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
        ax.scatter(lons[0],lats[0],s=10,c='m', zorder=10, edgecolor='black', transform=ccrs.PlateCarree())
