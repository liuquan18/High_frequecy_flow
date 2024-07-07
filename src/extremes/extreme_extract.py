#%%
import xarray as xr
import pandas as pd


#%%
def subtract_threshold(pc, pos_threshold, neg_threshold):
    # xarray exclude the data at 1st may to 3rd May, and the data during 28th Sep and 31st Sep
    # Create a mask for the dates to exclude
    mask_exclude = (
        ((pc['time.month'] == 5) & (pc['time.day'] >= 1) & (pc['time.day'] <= 3)) |
        ((pc['time.month'] == 9) & (pc['time.day'] >= 28) & (pc['time.day'] <= 30))
    )
    mask_keep = ~mask_exclude
    pc = pc.where(mask_keep, drop = True)


    df = pc.to_dataframe()

    G =  df.groupby(df.index.year)['pc']


    # positive extremes all be greater than the positive threshold
    pos_residues = G.transform(lambda x: x - pos_threshold['threshold'].values)
    # negative extremes all be less than the negative threshold
    neg_residues = G.transform(lambda x: x - neg_threshold['threshold'].values)

    return pos_residues.reset_index(), neg_residues.reset_index()