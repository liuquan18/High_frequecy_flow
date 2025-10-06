# %%
import cdsapi

# %%
dataset = "reanalysis-era5-pressure-levels"
years = ["2025"]
months = ["06", "07", "08", "09"]
days = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
]
pressure_levels = ["500", "250"]

client = cdsapi.Client()

for month in months:
    request = {
        "product_type": ["reanalysis"],
        "variable": ["geopotential"],
        "year": years,
        "month": [month],
        "day": days,
        "pressure_level": pressure_levels,
        "data_format": "grib",
        "download_format": "unarchived",
    }
    out_path = f"/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_daily/era5_zg_daily-{month}_129.grb"
    client.retrieve(dataset, request).download(out_path)

# %%
