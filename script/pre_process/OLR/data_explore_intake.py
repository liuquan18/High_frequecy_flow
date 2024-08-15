# %%
import intake
import xarray as xr
import dask
import subprocess as sp

# %%
from src.gem_helpers.gem_helpers import *

# %%
uid = getpass.getuser()
image_path = make_tempdir("intake_demo_plots")
data_cache_path = make_tempdir("intake_demo_data")
# %%
catalog_file = "/work/ik1017/Catalogs/dkrz_cmip6_disk.json"
cat = intake.open_esm_datastore(catalog_file)
cat
# %%
cat.df.head()
# %%
# %%
cat_hist_olr_daily = cat.search(
    institution_id="MPI-M",
    frequency="day",
    source_id="MPI-ESM1-2-LR",
    variable_id="rlut",
    experiment_id="historical",
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
get_from_cat(cat_hist_olr_daily, 'path')
# %%
cat_hist_olr_monthly = cat.search(
    institution_id="MPI-M",
    frequency="mon",
    source_id="MPI-ESM1-2-LR",
    variable_id="rlut",
    experiment_id="historical",
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
get_from_cat(cat_hist_olr_monthly, 'path')
# %%
cat_hist_olr_monthly_file_paths = get_from_cat(cat_hist_olr_monthly, 'path')

#%%
# only select path ending with "185001-186912.nc"
cat_hist_olr_monthly_file_paths = cat_hist_olr_monthly_file_paths.loc[
    cat_hist_olr_monthly_file_paths.path.str.contains("185001-186912.nc")
]

#%%
monthly_file_lists = cat_hist_olr_monthly_file_paths.path.tolist()
# remove comma from each element in the list
monthly_file_lists = [x.replace(",", "") for x in monthly_file_lists]
# %%
query = (
    [
        "cdo",
        "-P",
        "8",
        "-selmonth,5/9",
        "-ensmean",
        "-apply,-selyear,1850/1859",
        "[",
    ]
    + cat_hist_olr_monthly_file_paths.path.tolist()[:2]
    + ["]", "/scarch/m/m300883/tmp/olr_monthly_1850_1859.nc"],
)

# %%
sp.run(query)
# %%
