# %%
import xarray as xr
import matplotlib.pyplot as plt
from src.composite.composite_NAO_WB import smooth, NAO_WB

#%%
first_NAO_pos_AWB, first_NAO_neg_AWB, first_NAO_pos_CWB, first_NAO_neg_CWB = NAO_WB('first10')
last_NAO_pos_AWB, last_NAO_neg_AWB, last_NAO_pos_CWB, last_NAO_neg_CWB = NAO_WB('last10')
# %%
fig, axes = plt.subplots(1,2,figsize = (12,8))
first_NAO_pos_AWB.plot(ax = axes[0], alpha = 0.5,  color = 'b', label = 'first10')
last_NAO_pos_AWB.plot(ax = axes[0], alpha = 0.5, color = 'r', label = 'last10')

first_NAO_neg_CWB.plot(ax = axes[1], alpha = 0.5, color = 'b')
last_NAO_neg_CWB.plot(ax = axes[1], alpha = 0.5,  color = 'r')

smooth(first_NAO_pos_AWB).plot(ax = axes[0], color = 'b', linewidth = 3, label = 'first10 5day-mean')
smooth(last_NAO_pos_AWB).plot(ax = axes[0], color = 'r', linewidth = 3, label = 'last10 5day-mean')

smooth(first_NAO_neg_CWB).plot(ax = axes[1], color = 'b', linewidth = 3, label = 'first10')
smooth(last_NAO_neg_CWB).plot(ax = axes[1], color = 'r', linewidth = 3, label = 'last10')

axes[0].set_title("AWB occurrence during NAO positive")
axes[1].set_title("CWB occurrence during NAO negative")

axes[0].set_xlim(-21,21)
axes[1].set_xlim(-21, 21)

axes[0].set_ylim(10, 32)
axes[1].set_ylim(0, 10)


axes[0].set_ylabel("WB occurrence", fontsize = 14)
axes[0].set_ylabel("")
axes[1].set_xlabel("days relative to onset of NAO extremes", fontsize = 14)
axes[0].set_xlabel("days relative to onset of NAO extremes", fontsize = 14)

axes[0].legend()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/skader_WB/pos_AWB_neg_CWB_occurrence_fldmean.png", dpi = 300)

# %%
# pos NAO - CWB, neg NAO - AWB
fig, axes = plt.subplots(1,2,figsize = (12,8))
first_NAO_pos_CWB.plot(ax = axes[0], alpha = 0.5,  color = 'b', label = 'first10')
last_NAO_pos_CWB.plot(ax = axes[0], alpha = 0.5, color = 'r', label = 'last10')

first_NAO_neg_AWB.plot(ax = axes[1], alpha = 0.5, color = 'b')
last_NAO_neg_AWB.plot(ax = axes[1], alpha = 0.5,  color = 'r')

smooth(first_NAO_pos_CWB).plot(ax = axes[0], color = 'b', linewidth = 3, label = 'first10 5day-mean')
smooth(last_NAO_pos_CWB).plot(ax = axes[0], color = 'r', linewidth = 3, label = 'last10 5day-mean')

smooth(first_NAO_neg_AWB).plot(ax = axes[1], color = 'b', linewidth = 3, label = 'first10')
smooth(last_NAO_neg_AWB).plot(ax = axes[1], color = 'r', linewidth = 3, label = 'last10')

axes[0].set_title("CWB occurrence during NAO positive")
axes[1].set_title("AWB occurrence during NAO negative")

axes[0].set_xlim(-21,21)
axes[1].set_xlim(-21, 21)

axes[0].set_ylim(0,15)
axes[1].set_ylim(0,15)

axes[0].set_ylabel("WB occurrence", fontsize = 14)
axes[0].set_ylabel("")
axes[1].set_xlabel("days relative to onset of NAO extremes", fontsize = 14)
axes[0].set_xlabel("days relative to onset of NAO extremes", fontsize = 14)

axes[0].legend()
plt.savefig("/work/mh0033/m300883/High_frequecy_flow/docs/plots/skader_WB/pos_CWB_neg_AWB_occurrence_fldmean.png", dpi = 300)
# %%
