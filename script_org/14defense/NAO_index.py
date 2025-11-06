# %%
import pandas as pd
import matplotlib.pyplot as plt

# %%
# Read the data
df = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/elevation/NAO_index.txt")

# Combine year, month, day into a datetime
df["date"] = pd.to_datetime(df[["year", "month", "day"]])

# Set datetime as index
df.set_index("date", inplace=True)


# %%
# Calculate linear trend for the selected period
import numpy as np
from scipy.stats import linregress


# %%
# remove the linear trend from the NAO index for each calendar day (across years)
def detrend_series(series):
    x = np.arange(len(series))
    slope, intercept, r_value, p_value, std_err = linregress(x, series)
    trend = slope * x + intercept
    detrended = series - trend
    return detrended


# Apply detrending for each calendar day (month, day) across all years
def detrend_by_calendar_day(df, value_col):
    # Group by month and day
    detrended = []
    for (month, day), group in df.groupby([df.index.month, df.index.day]):
        detrended_values = detrend_series(group[value_col])
        # Assign detrended values back to the group
        group = group.copy()
        group[value_col + "_detrended"] = detrended_values.values
        detrended.append(group)
    # Concatenate all groups back together and sort by date
    df_detrended = pd.concat(detrended).sort_index()
    return df_detrended


# Assuming the NAO index column is named 'aao_index_cdas'
df = detrend_by_calendar_day(df, "aao_index_cdas")

# %%
# Filter data for July 2025
start_date = "2025-07-10"
end_date = "2025-07-30"
df_july2025 = df.loc[start_date:end_date]

# If you want to plot the detrended data for July 2025:
df_july2025 = df.loc[start_date:end_date]


# %%
# Plot the detrended time series
plt.figure(figsize=(8, 4))
plt.plot(
    df_july2025.index,
    df_july2025["aao_index_cdas_detrended"],
    label="NAO Index Detrended",
    color="k",
    lw=2,
)
plt.axhline(0, color="k", linestyle="--", linewidth=1)  # zero line
plt.title("NAO Index in July 2025", fontsize=18)
plt.xlabel("Date", fontsize=16)
plt.ylabel("Standardized NAO Index", fontsize=16)
plt.tick_params(axis="both", which="major", labelsize=12)
# remove top and right spines
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/NAO_index_July2025.png",
    dpi=500,
    bbox_inches="tight",
    metadata={"Creator": __file__},
)


# %%
# Calculate JJA (June, July, August) mean of the NAO index for each year
def calc_jja_mean(df, value_col):
    # Filter for JJA months
    jja = df[df.index.month.isin([6, 7, 8])]
    # Group by year and calculate mean
    jja_mean = jja.groupby(jja.index.year)[value_col].mean()
    return jja_mean


# Calculate JJA mean for the detrended NAO index
jja_mean = calc_jja_mean(df, "aao_index_cdas_detrended")

# %%
# Plot JJA mean for all years
plt.figure(figsize=(8, 4))
plt.plot(jja_mean.index, jja_mean.values, color="k", lw=2)
plt.axhline(0, color="k", linestyle="--", linewidth=1)
plt.title("JJA Mean of Detrended NAO Index (All Years)", fontsize=18)
plt.xlabel("Year", fontsize=16)
plt.ylabel("JJA Mean NAO Index (Detrended)", fontsize=16)
plt.tick_params(axis="both", which="major", labelsize=12)
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/NAO_index_JJA_mean.png",
    dpi=500,
    bbox_inches="tight",
    metadata={"Creator": __file__},
)


# %%
# Calculate monthly mean of the NAO index for each year and month
def calc_monthly_mean(df, value_col):
    # Group by year and month and calculate mean
    monthly_mean = df.groupby([df.index.year, df.index.month])[value_col].mean()
    # Convert to DataFrame with MultiIndex (year, month)
    monthly_mean = monthly_mean.rename_axis(["year", "month"]).reset_index()
    return monthly_mean


# Calculate monthly mean for the detrended NAO index
monthly_mean = calc_monthly_mean(df, "aao_index_cdas_detrended")

# Filter for JJA months (June=6, July=7, August=8)
jja_monthly_mean = monthly_mean[monthly_mean["month"].isin([6, 7, 8])]

# %%
# Plot JJA monthly mean for all years
plt.figure(figsize=(8, 4))
for m, label in zip([6, 7, 8], ["June", "July", "August"]):
    data = jja_monthly_mean[jja_monthly_mean["month"] == m]
    plt.plot(data["year"], data["aao_index_cdas_detrended"], label=label, lw=2)
plt.axhline(0, color="k", linestyle="--", linewidth=1)
plt.title("JJA Monthly Mean of Detrended NAO Index (All Years)", fontsize=18)
plt.xlabel("Year", fontsize=16)
plt.ylabel("Monthly Mean NAO Index (Detrended)", fontsize=16)
plt.tick_params(axis="both", which="major", labelsize=12)
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/NAO_index_JJA_monthly_mean.png",
    dpi=500,
    bbox_inches="tight",
    metadata={"Creator": __file__},
)

# %%
# Plot JJA monthly mean for all years as a single black line, with custom x-axis labels
plt.figure(figsize=(6, 4))

# Sort by year and month to ensure correct order
jja_monthly_mean_sorted = jja_monthly_mean.sort_values(["year", "month"])

# Plot as a single line
plt.plot(
    jja_monthly_mean_sorted.index,
    jja_monthly_mean_sorted["aao_index_cdas_detrended"],
    color="k",
    lw=2,
)
# mark July 2025 with a red dot

plt.title("Summer NAO monthly index 1979-2025", fontsize=16)
plt.xlabel("Year", fontsize=16)
plt.ylabel("standardized NAO index", fontsize=12)
plt.tick_params(axis="both", which="major", labelsize=12)
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

# Custom x-axis labels: for each JJA month, label with 'JJA' above and year below
years = jja_monthly_mean_sorted["year"].unique()
xticks = []
xticklabels = []
# Only label every 10th year (e.g., 1980, 1990, ...)
interval = 10
for y in years:
    if y % interval == 0:
        # Find the index for June of this year (or first JJA month available)
        idxs = jja_monthly_mean_sorted[(jja_monthly_mean_sorted["year"] == y)].index
        if len(idxs) > 0:
            xticks.append(idxs[0])
            xticklabels.append(str(y))
# Set the ticks and labels
plt.xticks(xticks, xticklabels, rotation=0, ha="center", fontsize=10)
# only show y-ticks on 3, 1.5, 0, -1.5, -3
plt.yticks([3, 1.5, 0, -1.5, -3], fontsize=10)
plt.ylim(-3, 3)

xmin, xmax = plt.gca().get_xlim()
plt.axhline(0, color="k", linestyle="--", linewidth=1)
plt.axhline(1.5, color="k", linestyle="dotted", linewidth=1)
plt.axhline(-1.5, color="k", linestyle="dotted", linewidth=1)

plt.tight_layout()
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/0defense/NAO_index_JJA_monthly_mean_1.5.png",
    dpi=500,
    bbox_inches="tight",
    metadata={"Creator": __file__},
)

# %%
# %%
