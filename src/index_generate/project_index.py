import xarray as xr
import numpy as np

def cos_lat_weight(lat):
    """Calculate the cosine of latitude for weighting."""
    return np.cos(np.deg2rad(lat))

def project_field_to_pattern(field_data, pattern_data, lat_dim='lat', lon_dim='lon', standard=False):
    """Project field data onto pattern data to get the temporal index, weighted by cos(latitude)."""
    # Extract latitudes and calculate weights
    latitudes = field_data.coords[lat_dim].values
    weights = cos_lat_weight(latitudes)
    
    # Apply weights
    weighted_field = field_data * weights[:, np.newaxis]
    weighted_pattern = pattern_data * weights[:, np.newaxis]
    

    # flat field to [time,lon-lat] or [time,lon-lat,heith]
    field_flat = weighted_field.stack(spatial = ('lon','lat'))

    eof_flat = weighted_pattern.stack(spatial = ('lon','lat'))

    # dorpna
    field_flat = field_flat.dropna(dim='spatial')
    eof_flat = eof_flat.dropna(dim='spatial')

    # for all plevs:
    Projected_pcs = []
    for plev in field_flat.plev:
        field_f = field_flat.sel(plev = plev)
        eof_f = eof_flat.sel(plev = plev)
        projected_pcs = field_f.dot(eof_f.T)
        Projected_pcs.append(projected_pcs)

    Projected_pcs = xr.concat(Projected_pcs, dim = 'plev')

    if standard:
        # standardize the ppc with its std
        mean = Projected_pcs.mean(dim = 'time')
        std = Projected_pcs.std(dim = 'time')
        Projected_pcs = (Projected_pcs - mean) / std

    return Projected_pcs

# %%
def project(x,y):
    projected_pcs = np.dot(x, y.T)
    return projected_pcs