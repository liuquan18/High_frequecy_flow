#%%
import xarray as xr
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.extremes.extreme_read import read_extremes
import src.composite.composite as comp


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
    if valid_geometries.shape[0] < gdf.shape[0]:
        logging.warning(f"Removed {gdf.shape[0] - valid_geometries.shape[0]} invalid geometries")

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


# %%
def lag_lead_composite(NAO, WB):
    '''
    calculate the occurrence of WB as a function of days relative to NAO onset day

    Parameters
    ----------
    NAO : pandas.DataFrame
        NAO extremes
    WB : pandas.DataFrame
        WB array
    '''

    NAO_range = comp.lead_lag_30days(NAO, base_plev=25000)
    WB_composite = comp.date_range_composite(WB, NAO_range)

    WB_composite = WB_composite.sum(dim = 'event')

    return WB_composite

#%%
def NAO_WB(period, fldmean = True):
    NAO_pos_AWB = []
    NAO_neg_AWB = []

    NAO_pos_CWB = []
    NAO_neg_CWB = []

    for ens in range(1, 51):
        AWB = read_wb(period, ens, 'AWB', fldmean)
        CWB = read_wb(period, ens, 'CWB', fldmean)

        NAO_pos, NAO_neg = read_extremes(period, 8, ens, 25000)
        if not NAO_pos.empty:
            NAO_pos_AWB.append(lag_lead_composite(NAO_pos, AWB))
            NAO_pos_CWB.append(lag_lead_composite(NAO_pos, CWB))
            
        if not NAO_neg.empty:
            NAO_neg_AWB.append(lag_lead_composite(NAO_neg, AWB))
            NAO_neg_CWB.append(lag_lead_composite(NAO_neg, CWB))


    NAO_pos_AWB = xr.concat(NAO_pos_AWB, dim = 'ens').sum(dim = 'ens')
    NAO_neg_AWB = xr.concat(NAO_neg_AWB, dim = 'ens').sum(dim = 'ens')
    NAO_pos_CWB = xr.concat(NAO_pos_CWB, dim = 'ens').sum(dim = 'ens')
    NAO_neg_CWB = xr.concat(NAO_neg_CWB, dim = 'ens').sum(dim = 'ens')

    return NAO_pos_AWB, NAO_neg_AWB, NAO_pos_CWB, NAO_neg_CWB
#%%
def smooth(arr, days = 5):
    arr_smooth = arr.rolling(time = days).mean(dim = 'time')
    return arr_smooth

