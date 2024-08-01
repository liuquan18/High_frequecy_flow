import numpy as np
import matplotlib.pyplot as plt

def plot_stacked_events(first10_df, last10_df, ax, vmin=15, vmax=85,xmin = 25, xmax = 50):

    # Define color maps
    # Custom normalization class
    blue_cmap = plt.cm.Blues
    orange_cmap = plt.cm.Oranges

    # set the color as 'none' between [0-0.2]
    # Define a function to map values to colors
    def value_to_color(value, cmap, vmin=15, vmax=85):
        if value < vmin:
            return "none"
        elif value > vmax:
            return cmap(1.0)
        else:
            return cmap((value - vmin) / (vmax - vmin))

    # Get the pressure levels and lag days
    pressure_levels = first10_df.index
    lag_days = first10_df.columns

    # Plot the data
    for i, level in enumerate(pressure_levels):
        for j, lag in enumerate(lag_days):
            
            # Add text annotations
            if j in range(xmin+1, xmax, 1):
                first10_value = first10_df.loc[level, lag]
                first10_color = value_to_color(first10_value, blue_cmap, vmin, vmax)
                
                # Plot first10 years data (lower bar)
                ax.bar(
                    j,
                    0.4,
                    bottom=i - 0.1,
                    width=1.0,
                    color=first10_color,
                    edgecolor="grey",
                    linewidth=0.3,
                )

                # Plot last10 years data (upper bar)
                last10_value = last10_df.loc[level, lag]
                last10_color = value_to_color(last10_value, orange_cmap, vmin, vmax)
                ax.bar(
                    j,
                    0.4,
                    bottom=i + 0.3,
                    width=1.0,
                    color=last10_color,
                    edgecolor="grey",
                    linewidth=0.3,
                )

                # Add text annotations (first10 lower)
                ax.text(
                    j,
                    i + 0.1,
                    str(first10_df.loc[level, lag]),
                    ha="center",
                    va="center",
                    fontsize=8,
                )

                # Add text annotations (last10 upper)
                ax.text(
                    j,
                    i + 0.5,
                    str(last10_df.loc[level, lag]),
                    ha="center",
                    va="center",
                    fontsize=8,
                )

    # Customize the plot
    ax.set_ylabel("Pressure Levels / hPa")

    # Set tick labels
    ax.set_xticks(range(len(lag_days)))
    ax.set_xticklabels(lag_days, rotation=45, ha="right")
    ax.set_yticks(np.arange(len(pressure_levels)) + 0.3)
    ax.set_yticklabels((pressure_levels.values / 100).astype(int))
    ax.set_xlim(xmin, xmax)
    # reverse the y-axis
    if pressure_levels[0] < pressure_levels[-1]:
        ax.invert_yaxis()

