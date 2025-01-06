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
from shapely.geometry import box, Polygon, MultiPolygon

import logging
logging.basicConfig(level=logging.INFO)

#%%
# Convert coordinates

def convert_geometry(geom):
    """
    Convert geometry coordinates from [0, 360] to [-180, 180] system.
    Handles both Polygon and MultiPolygon geometries.
    
    Args:
        geom: Shapely Polygon or MultiPolygon object
    
    Returns:
        Converted Polygon or MultiPolygon
    """
    if isinstance(geom, Polygon):
        # Handle single Polygon
        exterior_coords = list(geom.exterior.coords)
        new_exterior = [(lon if lon <= 180 else lon - 360, lat) for lon, lat in exterior_coords]
        
        # Handle interior rings (holes) if they exist
        new_interiors = []
        for interior in geom.interiors:
            interior_coords = list(interior.coords)
            new_interior = [(lon if lon <= 180 else lon - 360, lat) for lon, lat in interior_coords]
            new_interiors.append(new_interior)
            
        return Polygon(new_exterior, new_interiors)
        
    elif isinstance(geom, MultiPolygon):
        # Handle MultiPolygon by converting each polygon
        new_polys = []
        for poly in geom.geoms:
            exterior_coords = list(poly.exterior.coords)
            new_exterior = [(lon if lon <= 180 else lon - 360, lat) for lon, lat in exterior_coords]
            
            # Handle interior rings (holes) if they exist
            new_interiors = []
            for interior in poly.interiors:
                interior_coords = list(interior.coords)
                new_interior = [(lon if lon <= 180 else lon - 360, lat) for lon, lat in interior_coords]
                new_interiors.append(new_interior)
                
            new_polys.append(Polygon(new_exterior, new_interiors))
            
        return MultiPolygon(new_polys)
    
    else:
        raise ValueError(f"Unsupported geometry type: {type(geom)}")


def filter_by_overlap_threshold(gdf, region_box, threshold=0.5):
    """
    Filter GeoDataFrame to keep only geometries that overlap with the region box
    above the specified threshold (default 50%).
    
    Args:
        gdf: GeoDataFrame containing the geometries
        region_box: Shapely box geometry defining the region of interest
        threshold: Minimum overlap ratio (0 to 1) required to keep the geometry
        
    Returns:
        GeoDataFrame containing only geometries meeting the overlap threshold
    """

    
    # Calculate intersection areas
    valid_geometries = gdf[gdf.geometry.is_valid]

    # Calculate original and intersection areas
    original_areas = valid_geometries.geometry.area
    intersection_areas = valid_geometries.geometry.intersection(region_box).area

    # Calculate overlap ratio
    overlap_ratios = intersection_areas / original_areas
    
    # Create mask for geometries meeting threshold
    overlap_mask = overlap_ratios >= threshold
    
    # Return filtered GeoDataFrame
    return valid_geometries[overlap_mask]

# %%
def read_wb(dec, type, NAO_region = False, overlap_threshold=0.5):

    base_dir = f'/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/WB_{type}_th3_daily/'

    wbs = []
    for ens in range(1, 51, 1):
        # wb files
        file_path = base_dir + f'r{ens}i1p1f1/*{dec}*.csv'
        file = glob.glob(file_path)[0]
        df = pd.read_csv(file)
        df["geometry"] = df["geometry"].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(df, geometry="geometry")
        # convert coordinates
        gdf.geometry = gdf.geometry.apply(convert_geometry)
        gdf['ens'] = ens
        wbs.append(gdf)
    
    wbs = pd.concat(wbs)
    
    if NAO_region:
        # Create region box (-90,40,20,80)
        region_box = box(-90, 20, 40, 80)
        
    wbs = filter_by_overlap_threshold(wbs, region_box, threshold=overlap_threshold)
    return wbs

#%%
# plot the geopands dataframe 'geometry' column
def plot_examine(awb):
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
    awb.plot(ax=ax, column='ens', cmap='tab20', legend=True)

    ax.coastlines()

    # plot the region box
    region_box = box(-90, 20, 40, 80)
    region_box = convert_geometry(region_box)
    region_box_patch = gpd.GeoSeries(region_box)
    region_box_patch.plot(ax=ax, facecolor='none', edgecolor='red')

    plt.show()

# %%
awb_dec = []
cwb_dec = []
for dec in range(1850, 2100, 10):
    logging.info(f"Processing {dec}")
    awb = read_wb(dec, 'awb', NAO_region=True, overlap_threshold=0.7)
    cwb = read_wb(dec, 'cwb', NAO_region=True, overlap_threshold=0.7)

    awb['dec'] = dec
    cwb['dec'] = dec

    awb_dec.append(awb)
    cwb_dec.append(cwb)

awb_dec = pd.concat(awb_dec)
cwb_dec = pd.concat(cwb_dec)

#%%
awb_dec.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wave_breaking_stat/awb_th3_NAO_overlap70.csv')
cwb_dec.to_csv('/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wave_breaking_stat/cwb_th3_NAO_overlap70.csv')
# %%
awb_count = awb_dec.groupby(['dec']).size().reset_index(name='count')
# %%
cwb_count = cwb_dec.groupby(['dec']).size().reset_index(name='count')
# %%
