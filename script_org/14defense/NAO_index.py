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
#%%
# standardize the index
df["aao_index_cdas"] = (df["aao_index_cdas"] - df["aao_index_cdas"].mean()) / df["aao_index_cdas"].std()
#%%
# Filter data for July 2025
start_date = "2025-06-01"
end_date = "2025-08-30"
df_july2025 = df.loc[start_date:end_date]

# %%
# Plot the time series
plt.figure(figsize=(12, 5))
plt.plot(
    df_july2025.index, df_july2025["aao_index_cdas"], label="NAO Index", color="navy"
)

plt.axhline(0, color="k", linestyle="--", linewidth=1)  # zero line
plt.title("NAO Index Time Series (2025-07-01 to 2025-07-31)")
plt.xlabel("Date")
plt.ylabel("NAO Index")
plt.legend()
plt.tight_layout()
plt.show()

# %%
