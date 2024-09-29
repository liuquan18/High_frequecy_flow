#%%
import pandas as pd
import matplotlib.pyplot as plt

#%%
# Step 1: Read the data
file_path = '/work/mh0033/m300883/High_frequecy_flow/data/NAO_monthly_index_ppt/NAO_monthly.txt'
data = pd.read_csv(file_path, delim_whitespace=True, header=None, names=['Year', 'Month', 'Index'])

# Step 2: Process the data
data['Date'] = pd.to_datetime(data[['Year', 'Month']].assign(DAY=1))
data.set_index('Date', inplace=True)

# Step 3: Select the data between 2023 to 2024
data = data.loc['2020':'2024']

#%%
# Step 4: Plot the data
fig, ax = plt.subplots(figsize=(12, 6))

# Set black background
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Plot the NAO index
ax.plot(data.index, data['Index'], color='white', linewidth=2)

# Fill positive with red and negative with blue
ax.fill_between(data.index, data['Index'], 0, where=data['Index'] > 0, interpolate=True, facecolor='#d53e4f')
ax.fill_between(data.index, data['Index'], 0, where=data['Index'] < 0, interpolate=True, facecolor='#3288bd')

# Set axis labels and title color to white
ax.set_xlabel('Date', color='white')
ax.set_ylabel('NAO Index', color='white')
ax.set_title('NAO Monthly Index Time Series', color='white')

# Set tick parameters to white
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

# y ticks only at 0, 1.5 and -1.5
ax.set_yticks([-1.5, 0, 1.5])

# Set the color of the x-axis and y-axis lines to white
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')


# Show the plot
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/imprs_retreat_2024/NAO_index.png", dpi=300)
# %%
