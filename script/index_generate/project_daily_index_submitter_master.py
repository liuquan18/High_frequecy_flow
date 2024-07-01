#%%
import os
import numpy as np

#%%
for node in range(2): #0,1
  os.system(f"sbatch ./project_daily_index_submitter.sh {node+1}") # 1,0,4, 2,4,8, 3,8,12
# %%