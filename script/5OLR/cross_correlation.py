# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
import seaborn as sns
import cartopy.crs as ccrs
from src.cross_correlation.cross_correlation import ens_ccf, plot_ccf, locmimum_index_inbin, composite_mean_OLR

import matplotlib.gridspec as gridspec

from matplotlib.lines import Line2D



# %%
######################### cross correlation #########################
# first 10 years
CCFs_first10_pos_indo, CCFs_first10_pos_natl = ens_ccf("first10", "pos")

# last 10 years
CCFs_last10_pos_indo, CCFs_last10_pos_natl = ens_ccf("last10", "pos")

# %%
fig, axes = plt.subplots(2, 2, figsize=(20, 10))


plot_ccf(CCFs_first10_pos_indo, axes[0, 0])
plot_ccf(CCFs_last10_pos_indo, axes[0, 1])
plot_ccf(CCFs_first10_pos_natl, axes[1, 0])
plot_ccf(CCFs_last10_pos_natl, axes[1, 1])

axes[0, 0].set_title("First 10 years Indo-Pacific")
axes[0, 1].set_title("Last 10 years Indo-Pacific")

axes[1, 0].set_title("First 10 years natlon")
axes[1, 1].set_title("Last 10 years natlon")

# add legend
# black line for 'median'
# red bar for "% of corr < -0.5"
legend_elements = [
    Line2D([0], [0], color="black", lw=1, label="median"),
    Line2D([0], [0], color="red", lw=5, label="% of corr < -0.5", alpha = 0.3),
]

axes[0, 0].legend(handles=legend_elements, loc="upper right")
plt.savefig(
    "/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_composite_e2c/Indo_natl_OLR_NAO_pos_ccf.png"
)


#%%
############################## example ccf plot ##############################
def plot_ccf_exp(CCFs_first10_pos_indo, ax, ind):
    for column in CCFs_first10_pos_indo.columns[[ind]]:
        ax.plot(
        CCFs_first10_pos_indo.index, CCFs_first10_pos_indo[column], color="black"
    )



    # hline at y = 0
    ax.hlines(y=0, xmin=-50, xmax=0, linestyles="dotted", color = 'black')
    ax.hlines(y=-0.5, xmin=-50, xmax=0, linestyles="dotted", color = 'black')

    # vline at x = -16, -6
    ax.vlines(x=-16, ymin=-0.85, ymax=0.86, linestyles="--")
    ax.vlines(x=-6, ymin=-0.85, ymax=0.86, linestyles="--")

    ax.set_xlabel("Lags")
    ax.set_ylabel("Correlation")

    ax.set_xlim(-40, 0)
    ax.set_ylim(-0.85, 0.86)

# example ccf plot
fig, axes = plt.subplots()

plot_ccf_exp(CCFs_first10_pos_indo, axes,9)
plt.savefig('/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_composite_e2c/ccf_example.png')

# %%


# %%
first_indo = locmimum_index_inbin(CCFs_first10_pos_indo)
last_indo = locmimum_index_inbin(CCFs_last10_pos_indo)

first_natl = locmimum_index_inbin(CCFs_first10_pos_natl)
last_natl = locmimum_index_inbin(CCFs_last10_pos_natl)

# %%

# construct dataframe for bar plot
ds_count = pd.DataFrame(data = {'count':[first_indo.size, last_indo.size, first_natl.size, last_natl.size],
                                'peirod':['first','last','first','last'],
                                'region':['Indo-Pacific','Indo-Pacific','North-Atlantic','North-Atlantic']})


# %%
# bar plot, x for Indo and natlon, differnet colors for first and last 10 years
sns.barplot(x = 'region', y = 'count', hue = 'peirod', data = ds_count)
plt.title('Count of local minimum in lag (-16,-6]')
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_composite_e2c/loc_min_count.png")
# %%
# save
# %%
######################## composite of OLR based on different period and region ########################

# %%
first10_pos_indo_comp = composite_mean_OLR(first_indo, "first10")

first10_pos_natl_comp = composite_mean_OLR(first_natl, "first10")

last10_pos_indo_comp = composite_mean_OLR(last_indo, "last10")

last10_pos_natl_comp = composite_mean_OLR(last_natl, "last10")
# %%

def plot_composite(field, ax, levels=np.arange(-10, 11, 1)):
    p = field.plot(
        levels=levels,
        transform=ccrs.PlateCarree(),
        add_colorbar=False,
        ax=ax,
        add_labels=False,
        extend="both",
    )
    ax.coastlines()
    return p


# %%
fig = plt.figure(figsize=(20, 5))
gs = gridspec.GridSpec(2, 2, wspace = 0.1, hspace = 0.1)
levels = np.arange(-12, 13, 2)

ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree(central_longitude=180))
plot_composite(first10_pos_indo_comp, ax1, levels=levels)
ax1.set_title("First 10 years Indo-Pacific")

ax2 = fig.add_subplot(gs[0, 1], projection=ccrs.PlateCarree(central_longitude=180))
plot_composite(last10_pos_indo_comp, ax2, levels=levels)
ax2.set_title("Last 10 years Indo-Pacific")

ax3 = fig.add_subplot(gs[1, 0], projection=ccrs.PlateCarree(central_longitude=180))
plot_composite(first10_pos_natl_comp, ax3, levels=levels)
ax3.set_title("First 10 years North Atlantic")

ax4 = fig.add_subplot(gs[1, 1], projection=ccrs.PlateCarree(central_longitude=180))
plot_composite(last10_pos_natl_comp, ax4, levels=levels)
ax4.set_title("Last 10 years North Atlantic")

# Adjust layout to make space for colorbar
fig.subplots_adjust(bottom=0.15)

# Add cax at the bottom of the plot
cax = fig.add_axes([0.1, 0.05, 0.8, 0.02])

# Add colorbar after layout adjustments
fig.colorbar(ax1.collections[0], cax=cax, orientation="horizontal", aspect=50)
cax.set_title("OLR anomaly (W/m^2)")

# add y-axis labels
for ax in [ax1, ax3]:
    ax.set_yticks(range(-30, 31, 30), crs=ccrs.PlateCarree())
    ax.set_yticklabels([f"{lat}°" for lat in range(-30, 31, 30)])

# add x-axis labels
for ax in [ax3, ax4]:
    ax.set_xticks(range(-180, 180, 60), crs=ccrs.PlateCarree())
    ax.set_xticklabels([f"{lon}°" for lon in range(-180, 180, 60)])


# vlines at x = 50, 120, -70 for axes[0, 0]
ax1.vlines(x=50, ymin = -28, ymax = 28, linestyles="--", transform=ccrs.PlateCarree(),color = 'black')
ax1.vlines(x=120, ymin = -28, ymax = 28, linestyles="--", transform=ccrs.PlateCarree(), color = 'black')
ax1.vlines(x=-80, ymin = -28, ymax = 28, linestyles="--", transform=ccrs.PlateCarree(), color = 'black')
ax1.vlines(x = -10, ymin = -28, ymax = 28, linestyles="--", transform=ccrs.PlateCarree(), color = 'black')

plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/OLR_composite_e2c/loc_min_composite_OLR.png")
# %%# %%
