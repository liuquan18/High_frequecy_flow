# %%
import numpy as np
import xarray as xr
import intake
import os

# %%
# %%
from src.gem_helpers.gem_helpers import *

# %%
# some initial setup
uid = getpass.getuser()
image_path = make_tempdir("intake_demo_plots")
data_cache_path = make_tempdir("intake_demo_data")
# %%
# catalog for MPI_GE_CMIP6
catalog_file = "/work/ik1017/Catalogs/dkrz_cmip6_disk.json"
cat = intake.open_esm_datastore(catalog_file)

cat_MPI_GE_CMIP6 = cat.search(
    institution_id="MPI-M",
    source_id="MPI-ESM1-2-LR",
    member_id=[
        "r10i1p1f1",
        "r11i1p1f1",
        "r12i1p1f1",
        "r13i1p1f1",
        "r14i1p1f1",
        "r15i1p1f1",
        "r16i1p1f1",
        "r17i1p1f1",
        "r18i1p1f1",
        "r19i1p1f1",
        "r1i1p1f1",
        "r20i1p1f1",
        "r21i1p1f1",
        "r22i1p1f1",
        "r23i1p1f1",
        "r24i1p1f1",
        "r25i1p1f1",
        "r26i1p1f1",
        "r27i1p1f1",
        "r28i1p1f1",
        "r29i1p1f1",
        "r2i1p1f1",
        "r30i1p1f1",
        "r3i1p1f1",
        "r4i1p1f1",
        "r5i1p1f1",
        "r6i1p1f1",
        "r7i1p1f1",
        "r8i1p1f1",
        "r9i1p1f1",
    ],
)
# %%
save_path = (
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_season_global/"
)

# %%
############## first 10 years ################
# "mon" frequency "historical" experiment, "rlut" variable
cat_hist_olr_monthly = cat_MPI_GE_CMIP6.search(
    frequency="mon",
    variable_id="rlut",
    experiment_id="historical",
)

month_files = get_from_cat(cat_hist_olr_monthly, "path")
# only select path with name ending with  "185001-186912.nc"
first10_month_files = month_files.loc[month_files.path.str.contains("185001-186912.nc")]

# use cdo to calculate the ensemble mean, and save the result to
os.system(
    f"cdo -selyear,1850/1859 -selmon,5/9 -ensmean {first10_month_files.path.str.cat(sep=' ')} {save_path}OLR_monthly_ensmean_185005-185909.nc"
)

# %%

############## last 10 years ################
cat_ssp585_olr_monthly = cat_MPI_GE_CMIP6.search(
    frequency="mon",
    variable_id="rlut",
    experiment_id="ssp585",
)

month_files = get_from_cat(cat_ssp585_olr_monthly, "path")

# select the path with names ending with "207501-209412.nc" and "209501-210012.nc"
last10_month_files1 = month_files.loc[month_files.path.str.contains("207501-209412.nc")]
last10_month_files2 = month_files.loc[month_files.path.str.contains("209501-210012.nc")]
# %%
# use cdo to calculate the ensemble mean, and save the result to

# ensemean for the last10_month_files1
os.system(
    f"cdo -selmon,5/9 -ensmean {last10_month_files1.path.str.cat(sep=' ')} {save_path}OLR_monthly_ensmean_207505-209409.nc"
)

# ensemean for the last10_month_files2
os.system(
    f"cdo -selmon,5/9 -ensmean {last10_month_files2.path.str.cat(sep=' ')} {save_path}OLR_monthly_ensmean_209505-210009.nc"
)


#%%
# merge the two ensemble mean files
os.system(
    f"cdo -selyear,2091/2100 -mergetime {data_cache_path}OLR_monthly_ensmean_207505-209409.nc {data_cache_path}OLR_monthly_ensmean_209505-210009.nc {save_path}OLR_monthly_ensmean_209105-210009.nc"
)
# %%
