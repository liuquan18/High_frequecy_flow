#%%
import pandas as pd
import numpy as np
import seaborn as sns
from src.extremes.extreme_statistics import sel_event_above_duration
import matplotlib.pyplot as plt
# %%
period = 'first10'
duration = 5
#%%
def sel_event_allens(period, duration = 5):
    pos_extreme_path = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/pos_extreme_events/'
    neg_extreme_path = '/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/neg_extreme_events/'

    tags = {'first10': '1850_1859', 'last10': '2091_2100'}
    tag = tags[period]

    pos_extremes = []
    neg_extremes = []


    for i in range(50):
        pos_extreme = pd.read_csv(f'{pos_extreme_path}pos_extreme_events_{period}/pos_extreme_events_{tag}_r{i+1}.csv')
        neg_extreme = pd.read_csv(f'{neg_extreme_path}neg_extreme_events_{period}/neg_extreme_events_{tag}_r{i+1}.csv')

        pos_extreme = sel_event_above_duration(pos_extreme, duration=duration)
        neg_extreme = sel_event_above_duration(neg_extreme, duration=duration)


        pos_extremes.append(pos_extreme)
        neg_extremes.append(neg_extreme)

    pos_extremes = pd.concat(pos_extremes, axis=0)
    neg_extremes = pd.concat(neg_extremes, axis=0)
    return pos_extremes, neg_extremes

#%%
def combine_events(df, duration = 13):
    """
    combine the events which durates more than 13 days
    """
    # Step 1: Split the dataframe
    df_up_to_13 = df[df.index <= duration]
    df_above_13 = df[df.index > duration]

    # Step 2: Sum the "duration" for rows > 13
    count_above_13 = df_above_13['count'].sum()
    mean_above_13 = np.average(df_above_13['mean'], weights=df_above_13.index) # weighted average

    # Step 3: Create a new row and append it to df_up_to_13
    combine_row = pd.DataFrame({'mean':[mean_above_13],
                            'count': [count_above_13],
                            'note': [f'above_{str(duration)}']}, index=[duration+1]) # should be ">duration" in plots
    
    df_final = pd.concat([df_up_to_13, combine_row])

    return df_final


# %%
first10_pos_extremes, first10_neg_extremes = sel_event_allens(period, duration=duration)
last10_pos_extremes, last10_neg_extremes = sel_event_allens('last10', duration=duration)

# %%
first10_pos = first10_pos_extremes.groupby('duration')['mean'].agg(['mean','count'])
first10_neg = first10_neg_extremes.groupby('duration')['mean'].agg(['mean','count'])
# %%
last10_pos = last10_pos_extremes.groupby('duration')['mean'].agg(['mean','count'])
last10_neg = last10_neg_extremes.groupby('duration')['mean'].agg(['mean','count'])

#%%
first10_pos = combine_events(first10_pos, duration = 7)
first10_neg = combine_events(first10_neg, duration = 7)
last10_pos = combine_events(last10_pos, duration = 7)
last10_neg = combine_events(last10_neg, duration = 7)


# %%
def plot_extreme_stat(first10_pos, first10_neg, last10_pos, last10_neg, stat = 'count', duration_lim = 7):
    # Get the union of all durations

    all_durations = sorted(set(first10_pos.index) | set(last10_pos.index) | 
                       set(first10_neg.index) | set(last10_neg.index))

    # Reindex all DataFrames to include all durations, filling missing values with 0
    first10_pos = first10_pos.reindex(all_durations, fill_value=0)
    last10_pos = last10_pos.reindex(all_durations, fill_value=0)
    first10_neg = first10_neg.reindex(all_durations, fill_value=0)
    last10_neg = last10_neg.reindex(all_durations, fill_value=0)

    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 8))

    # Set the width of each bar and the positions of the bars
    width = 0.35
    x = np.arange(len(all_durations))

    # Plot positive values
    ax.bar(x - width/2, first10_pos[stat], width, label='First 10 years (positive)', color='black', alpha=0.7)
    ax.bar(x + width/2, last10_pos[stat], width, label='Last 10 years (positive)', color='red', alpha=0.7)

    # Plot negative values
    if stat == 'count':
        ax.bar(x - width/2, -first10_neg[stat], width, label='First 10 years (negative)', color='black', alpha=0.3)
        ax.bar(x + width/2, -last10_neg[stat], width, label='Last 10 years (negative)', color='red', alpha=0.3)
    elif stat == 'mean':
        ax.bar(x - width/2, first10_neg[stat], width, label='First 10 years (negative)', color='black', alpha=0.3)
        ax.bar(x + width/2, last10_neg[stat], width, label='Last 10 years (negative)', color='red', alpha=0.3)

    # Set labels and title
    ax.set_xlabel('Duration')
    ax.set_ylabel(stat)
    ax.set_title('Count Distribution by Duration')

    # Set x-axis ticks
    ax.set_xticks(x)
    ax.set_xticklabels(all_durations, rotation=45)

    # Add legend
    ax.legend()

    # Add a horizontal line at y=0
    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    
    # change the x-label "11" to ">10"
    labels = [item.get_text() for item in ax.get_xticklabels()]
    labels[-1] = f'>{duration_lim}'
    ax.set_xticklabels(labels)


    # Adjust layout and display the plot
    plt.tight_layout()
    return fig, ax

# %%
fig, ax = plot_extreme_stat(first10_pos, first10_neg, last10_pos, last10_neg, stat='count')
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/extremes_statistics/count_distribution.png")
# %%
fig, ax = plot_extreme_stat(first10_pos, first10_neg, last10_pos, last10_neg, stat='mean')
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/extremes_statistics/mean_distribution.png")
# %%
