# %%
import numpy as np
import xarray as xr
import intake
import os

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
)
# %%
save_path = (
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly"
)

# %%
############## first 10 years ################
# "mon" frequency "historical" experiment, "rlut" variable
cat_hist_daily = cat_MPI_GE_CMIP6.search(
    frequency="day",
    variable_id=["tas", "hur"],
    experiment_id="historical",
)


#%%
cat_hist_daily = cat_hist_daily.search(
    member_id = [
        member_id for member_id in cat_hist_daily.df.member_id.unique() if member_id != 'r1i2000p1f1'
    ],
)
#%%
cat_hist_daily_first10 = cat_hist_daily.search(
    path = [
        path for path in cat_hist_daily.df.path.unique() if "18500101-18691231.nc" in path
    ],
)




#%%
dataset_dict = cat_hist_daily_first10.to_dataset_dict(
    cdf_kwargs={"chunks": {"time": 1, "plev":1}},
)

#%%








#%%
daily_files = cat_hist_tas_daily[["path"]]


# only select path with name ending with  "185001-186912.nc"
first10_daily_files = daily_files.loc[daily_files.path.str.contains("18500101-18691231.nc")]






#%%
cat_hist_hur_daily = cat_MPI_GE_CMIP6.search(
    frequency="day",
    variable_id="hur",
    experiment_id="historical",
)
cat_hist_hur_daily = cat_hist_hur_daily.df[cat_hist_hur_daily.df['member_id'] != 'r1i2000p1f1']

#%%
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
last10_month_files1.to_csv("/work/mh0033/m300883/High_frequecy_flow/script/pre_process/OLR/last10_month_files1.csv", index=False, header=False)
last10_month_files2.to_csv("/work/mh0033/m300883/High_frequecy_flow/script/pre_process/OLR/last10_month_files2.csv", index=False, header=False)

# %%
