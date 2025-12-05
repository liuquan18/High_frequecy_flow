# High Frequency Flow Analysis - AI Coding Agent Instructions

## Project Overview
Climate science research analyzing extreme North Atlantic Oscillation (NAO) events using MPI Grand Ensemble CMIP6 and ERA5 reanalysis data. Focus on summertime atmospheric dynamics, jet streams, wave breaking, and their response to climate warming.

## Data Architecture

### Data Organization
- **Base path**: `/work/mh0033/m300883/High_frequecy_flow/data/`
- **Primary datasets**: `MPI_GE_CMIP6/`, `MPI_GE_CMIP6_allplev/`, `ERA5/`, `ERA5_allplev/`
- **Scratch storage**: `/scratch/m/m300883/` for intermediate processing
- **Time periods**: "first10" (1850-1859) vs "last10" (2091-2100) for climate change analysis
- **Ensemble members**: 50 members (r1-r50) in MPI-GE simulations

### Period Conventions
- `first10`: Historical baseline (1850s, May-September MJJAS season)
- `last10`: Future warming (2090s, MJJAS season)
- Time tags: `"18500501-18590930"` and `"20910501-21000930"` in filenames

### Coordinate Systems
- **Longitude**: Data often stored as 0-360°, convert to -180 to 180° using `util.lon360to180()`
- **Regional focus**: North Atlantic (-120° to 60°E, 0-90°N)
- **Pressure levels**: Standard levels in Pa (e.g., 25000=250hPa jet stream, 85000=850hPa baroclinicity)

## Core Workflows

### 1. Composite Analysis Pattern
The fundamental analysis approach throughout the codebase:

```python
from src.data_helper.read_composite import read_comp_var
from src.extremes.extreme_read import read_extremes

# Read composite data for NAO extremes
ua_pos = read_comp_var("ua", "pos", 1850, time_window=(-10, 5))
ua_neg = read_comp_var("ua", "neg", 1850, time_window=(-10, 5))
ua_diff = ua_pos - ua_neg  # Composite difference (Pos - Neg)
```

**Key parameters**:
- `time_window=(-10, 5)`: Days relative to NAO event onset
- `phase`: "pos" or "neg" for NAO polarity
- `decade`: 1850 or 2090 for period selection
- `method`: "mean", "sum", or "no_stat"

### 2. Extreme Event Extraction
NAO extremes pre-computed and stored as CSV files:

```python
pos_extreme, neg_extreme = read_extremes(
    period="first10",  # or "last10"
    start_duration=8,  # minimum event duration in days
    ens=1,            # ensemble member
    plev=25000        # optional pressure level filter
)
```

Events have columns: `extreme_start_time`, `extreme_duration`, `plev`, `ens`

### 3. Data Loading Functions
Import hierarchy: `src.data_helper.read_composite` → `src.data_helper.read_variable`

Common functions:
- `read_comp_var()`: Composite means/differences
- `read_climatology()`: Ensemble mean climatologies
- `read_prime()`: High-frequency filtered (2-8 day bandpass) data
- `read_EP_flux()`: Eliassen-Palm flux diagnostics

### 4. SLURM Job Processing
All preprocessing uses SLURM on HPC cluster:

```bash
#!/bin/bash
#SBATCH --account=mh0033
#SBATCH --partition=compute
#SBATCH --mem=200G
#SBATCH --time=01:30:00

module load cdo/2.5.0-gcc-11.2.0
module load parallel

# Process in parallel using GNU parallel or srun
seq -f "%02g" 1 24 | parallel --jobs 4 process_member {}
```

Use CDO operators for NetCDF manipulation: `cdo mergetime`, `cdo selmonth`, `cdo monsub`

## Code Conventions

### Import Patterns
Always use absolute imports from `src/`:

```python
import src.composite.composite as comp
from src.extremes.extreme_read import read_extremes
import src.plotting.util as util
```

Reload modules during development:
```python
import importlib
importlib.reload(comp)
```

### Plotting Standards
- **Jet stream (UA)**: levels `np.arange(-30, 31, 5)` m/s at 250 hPa
- **Baroclinicity**: `np.arange(-8, 8.1, 1)` day⁻¹ at 850 hPa (convert s⁻¹ × 86400)
- **Map projection**: `ccrs.PlateCarree(180)` for Atlantic-centered maps
- **Regions**: Use `util.clip_map()` for North Atlantic sector plots
- **Smoothing**: Apply `util.map_smooth(ds, lon_win=25, lat_win=3)` before plotting
- **White line fix**: Use `util.erase_white_line()` to handle dateline artifacts

### Axis Alignment for Dual-Scale Plots
When overlaying different scales (absolute values + differences):

```python
# Scale bar data by 2x, then format labels as half
ax_bar.barh(lat, ua_change * 2, ...)
ax_bar.set_xlim(axes.get_xlim())  # Match limits exactly
ax_bar.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x/2:.1f}"))
```

This ensures tick alignment while displaying proportional relationships.

### Composite Lag Analysis
Standard lag composite workflow in `src/composite/composite.py`:

```python
# Find time ranges for lag composite (-30 to +30 days)
date_range = comp.find_lead_lag_30days(extremes, base_plev=25000)
composite = comp.date_range_composite(variable, date_range)
```

Results have dimensions: `(event, time, plev, lat, lon)` where `time` is lag days

### Zonal Mean Calculations
Common pattern for Atlantic sector averages:

```python
ua_zm = ua.sel(lon=slice(-120, 60)).mean(dim="lon")  # Jet stream
baroc_zm = baroc.sel(lon=slice(-120, 0)).mean(dim="lon")  # Baroclinicity
```

Northern Hemisphere only: `.sel(lat=slice(0, 90))`

## Module Structure

- **`src/composite/`**: Composite analysis core (`composite.py`, `composite_plot.py`)
- **`src/extremes/`**: Event detection and reading
- **`src/data_helper/`**: Data I/O abstraction layer
- **`src/dynamics/`**: Physical diagnostics (EP flux, wave breaking)
- **`src/plotting/`**: Cartographic utilities and visualization
- **`script/`**: Active analysis scripts (numbered workflow)
- **`script_org/`**: Organized scripts for publication figures
- **`docs/`**: Research notes with plot references

## Development Environment

**Setup**:
```bash
conda env create -f environment.yml
conda activate air_sea
```

**Key dependencies**: xarray, dask, cartopy, metpy, pandas, matplotlib

**Testing**: Limited test coverage in `test/`, focus on integration testing via scripts

## Common Patterns

### Variable Naming
- `ua`/`u`: Zonal wind
- `zg`: Geopotential height
- `uhat`/`hat`: Jet stream maximum
- `prime`: High-frequency (2-8 day) filtered
- `ano`: Anomaly from climatology
- `zm`: Zonal mean
- `pos`/`neg`: Positive/negative NAO phase

### File Naming in Data Directories
- Composites: `{var}_NAO_{phase}_{decade}.nc`
- Extremes: `{troposphere}_{phase}_extreme_events_{tag}_r{ens}.csv`
- Monthly means: `{var}_monmean_ensmean_{start_tag}_{end_tag}.nc`

### Debugging Data Issues
1. Check longitude range: Use `util.lon360to180()` if needed
2. Verify time coordinate: Convert to pandas datetime with `pd.to_datetime(..., format="ISO8601")`
3. Compute lazy arrays before plotting: `.compute()` on dask arrays
4. Check for empty composites: Filter `None` values after ensemble concatenation

## Performance Notes

- Use `chunks='auto'` when opening large NetCDF files
- For ensemble operations: loop, collect, concat, then compute statistics
- Parallel processing: GNU parallel for embarrassingly parallel tasks
- Dask clusters: See `src/compute/slurm_cluster.py` for distributed computation

## Research Context

**Hypothesis**: NAO+ and NAO- extremes respond differently to climate warming due to distinct physical drivers (tropical forcing vs. in-situ development).

**Key diagnostics**: Jet stream position/strength, baroclinicity, wave breaking (AWB/CWB), EP flux, eddy momentum fluxes
