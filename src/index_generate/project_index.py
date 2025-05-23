import xarray as xr
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)

def cos_lat_weight(lat):
    """Calculate the cosine of latitude for weighting."""
    return np.cos(np.deg2rad(lat))

def project_field_to_pattern(field_data, pattern_data, lat_dim='lat', lon_dim='lon', standard=False, plev = None):
    """Project field data onto pattern data to get the temporal index, weighted by cos(latitude)."""
    # Extract latitudes and calculate weights
    latitudes = field_data.coords[lat_dim]
    weights = cos_lat_weight(latitudes)
    
    # Apply weights
    weighted_field = field_data * weights
    weighted_pattern = pattern_data * weights
    

    # flat field to [time,lon-lat] or [time,lon-lat,heith]
    field_flat = weighted_field.stack(spatial = ('lon','lat'))

    eof_flat = weighted_pattern.stack(spatial = ('lon','lat'))

    # dorpna
    field_flat = field_flat.dropna(dim='spatial')
    eof_flat = eof_flat.dropna(dim='spatial')
    eof_flat = eof_flat.sortby('plev', ascending = False)

    # for all plevs:
    if plev is None:
        nplev = field_data.plev.size

        if nplev > 1:

            projected_pcs = xr.apply_ufunc(
                lambda x, y: x.dot(y.T),
                field_flat,
                eof_flat,
                input_core_dims=[['spatial'], ['spatial']],
                exclude_dims={'spatial'},
                vectorize=True,
                dask='allowed',
            )


        else:
            Projected_pcs = field_flat.dot(eof_flat.T)
    else:
        field_flat = field_flat.sel(plev = plev)
        try:
            eof_flat = eof_flat.sel(plev = plev)
        except KeyError:
            eof_flat = eof_flat
            logging.warning(f"plev {plev} not found in pattern data, assume it is corresponding to the reference plev")

        Projected_pcs = field_flat.dot(eof_flat.T)


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