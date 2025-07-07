# %%
import xarray as xr
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# %%
# transient div_phi, pos
TPhi_pos = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/transient_div_phi_pos_plev_25000.csv")
# transient div_p, pos
TP_pos = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/transient_div_p_pos_plev_85000.csv")

# transient div_phi, neg
TPhi_neg = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/transient_div_phi_neg_plev_25000.csv")
# transient div_p, neg
TP_neg = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/transient_div_p_neg_plev_85000.csv")
# %%
# steady div_phi, pos
SPhi_pos = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/steady_div_phi_pos_plev_25000.csv")
# steady div_p, pos
SP_pos = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/steady_div_p_pos_plev_85000.csv")
# steady div_phi, neg
SPhi_neg = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/steady_div_phi_neg_plev_25000.csv")
# steady div_p, neg
SP_neg = pd.read_csv("/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/0EP_flux_distribution/steady_div_p_neg_plev_85000.csv")
# %%
sumPhi_pos = TPhi_pos.copy()
sumPhi_pos['div_phi'] = TPhi_pos['div_phi'] + SPhi_pos['div_phi']
# %%
sumP_pos = TP_pos.copy()
sumP_pos['div_p'] = TP_pos['div_p'] + SP_pos['div_p']
# %%
sumPhi_neg = TPhi_neg.copy()
sumPhi_neg['div_phi'] = TPhi_neg['div_phi'] + SPhi_neg['div_phi']
# %%
sumP_neg = TP_neg.copy()
sumP_neg['div_p'] = TP_neg['div_p'] + SP_neg['div_p']
# %%
fig, axes = plt.subplots(2, 3, figsize=(10, 10), sharex=False, sharey="row")

# sumphi pos and neg
sns.lineplot(
    data = sumPhi_pos,
    x = "time",
    y = "div_phi",
    ax = axes[0, 0],
    errorbar=("ci", 95),
    color = 'k',
)

sns.lineplot(
    data = sumPhi_neg,
    x = "time",
    y = "div_phi",
    ax = axes[0, 0],
    errorbar=("ci", 95),
    color = 'k',
    linestyle = '--',
)

# transient phi , pos and neg
sns.lineplot(
    data = TPhi_pos,
    x = "time",
    y = "div_phi",
    ax = axes[0, 1],
    errorbar=("ci", 95),
    color = 'k',
)
sns.lineplot(
    data = TPhi_neg,
    x = "time",
    y = "div_phi",
    ax = axes[0, 1],
    errorbar=("ci", 95),
    color = 'k',
    linestyle = '--',
)

# steady phi, pos and neg
sns.lineplot(
    data = SPhi_pos,
    x = "time",
    y = "div_phi",
    ax = axes[0, 2],
    errorbar=("ci", 95),
    color = 'k',
)
sns.lineplot(
    data = SPhi_neg,
    x = "time",
    y = "div_phi",
    ax = axes[0, 2],
    errorbar=("ci", 95),
    color = 'k',
    linestyle = '--',
)

# second row for p
# sum p pos and neg
sns.lineplot(
    data = sumP_pos,
    x = "time",
    y = "div_p",
    ax = axes[1, 0],
    errorbar=("ci", 95),
    color = 'k',
)
sns.lineplot(
    data = sumP_neg,
    x = "time",
    y = "div_p",
    ax = axes[1, 0],
    errorbar=("ci", 95),
    color = 'k',
    linestyle = '--',
)
# transient p, pos and neg
sns.lineplot(
    data = TP_pos,
    x = "time",
    y = "div_p",
    ax = axes[1, 1],
    errorbar=("ci", 95),
    color = 'k',
)
sns.lineplot(
    data = TP_neg,
    x = "time",
    y = "div_p",
    ax = axes[1, 1],
    errorbar=("ci", 95),
    color = 'k',
    linestyle = '--',
)   
# steady p, pos and neg
sns.lineplot(
    data = SP_pos,
    x = "time",
    y = "div_p",
    ax = axes[1, 2],
    errorbar=("ci", 95),
    color = 'k',
)
sns.lineplot(
    data = SP_neg,
    x = "time",
    y = "div_p",
    ax = axes[1, 2],
    errorbar=("ci", 95),
    color = 'k',
    linestyle = '--',
)

for ax in axes.flat:
    ax.set_xlim(-20, 10)


# %%
