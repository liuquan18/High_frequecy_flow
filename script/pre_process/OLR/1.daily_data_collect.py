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
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly"
)

# %%
############## first 10 years ################
# "mon" frequency "historical" experiment, "rlut" variable
cat_hist_olr_daily = cat_MPI_GE_CMIP6.search(
    frequency="day",
    variable_id="rlut",
    experiment_id="historical",
)

daily_files = get_from_cat(cat_hist_olr_daily, "path")


# only select path with name ending with  "185001-186912.nc"
first10_daily_files = daily_files.loc[daily_files.path.str.contains("18500101-18691231.nc")]

# save the list of path to a file for read in by bash
first10_daily_files.to_csv("/work/mh0033/m300883/High_frequecy_flow/script/pre_process/OLR/first10_daily_files.csv", index=False, header=False)



# %%

############## last 10 years ################
cat_ssp585_olr_daily = cat_MPI_GE_CMIP6.search(
    frequency="day",
    variable_id="rlut",
    experiment_id="ssp585",
)

day_files = get_from_cat(cat_ssp585_olr_daily, "path")

# select the path with names ending with "207501-209412.nc" and "209501-210012.nc"
last10_month_files1 = day_files.loc[day_files.path.str.contains("20750101-20941231.nc")]
last10_month_files2 = day_files.loc[day_files.path.str.contains("20950101-21001231.nc")]
# %%
last10_month_files1.to_csv("/work/mh0033/m300883/High_frequecy_flow/script/pre_process/OLR/last10_month_files1.csv", index=False)
last10_month_files2.to_csv("/work/mh0033/m300883/High_frequecy_flow/script/pre_process/OLR/last10_month_files2.csv", index=False)

# %%
