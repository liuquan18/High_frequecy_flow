# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import glob

# %%
base_dir = "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/wb_both_allisen_fldmean_dec/"


# %%
def read_dec(decade):
    wb_dir = f"{base_dir}r*i1p1f1/wb_both_allisen_fldmean_dec_{decade}_r*i1p1f1.nc"
    wb_files = glob.glob(wb_dir)

    wb_data = xr.open_mfdataset(
        wb_files, combine="nested", parallel=True, concat_dim="ens"
    )
    wb_data = wb_data.mean(dim="ens")
    wb_data["decade"] = decade
    return wb_data.compute()


# %%
wbs = []
for dec in range(1850, 2010, 10):
    wb_dec = read_dec(dec)
    wbs.append(wb_dec)
# %%
wb_all = xr.concat(wbs, dim="decade")
# %%
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

wb_all["awb_fldmean"].plot(ax=axes[0], x="decade", y="isen_level", )
axes[0].set_title("AWB Field Mean")

wb_all["cwb_fldmean"].plot(ax=axes[1], x="decade", y="isen_level",)
axes[1].set_title("CWB Field Mean")

plt.tight_layout()
plt.show()
# %%
awb_line = wb_all["awb_fldmean"].sel(isen_level=330)
cwb_line = wb_all["cwb_fldmean"].sel(isen_level=320)
# %%
fig, ax = plt.subplots(figsize=(8, 5))
awb_line.plot(label="AWB 330K", ax=ax)
cwb_line.plot(label="CWB 320K", ax=ax)
ax.set_title("Field Mean Time Series at Specific Isentropic Levels")
ax.set_xlabel("Decade")
ax.set_ylabel("Field Mean Value")
ax.legend()
plt.show()
# %%
