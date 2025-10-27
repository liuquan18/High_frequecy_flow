# %%
import cdsapi

# %%
dataset = "derived-era5-pressure-levels-daily-statistics"
request = {
    "product_type": "reanalysis",
    "variable": ["geopotential"],
    "year": "2025",
    "month": ["08"],  # changed from "07" to "08"
    "day": [
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
    ],
    "pressure_level": ["50000", "85000"],
    "daily_statistic": "daily_mean",
    "time_zone": "utc+00:00",
    "frequency": "1_hourly",
}
# %%
client = cdsapi.Client()
client.retrieve(dataset, request).download(
    "/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/zg_daily/E5pl00_1D_2025-08_129.nc"  # changed "07" to "08"
)

# %%
