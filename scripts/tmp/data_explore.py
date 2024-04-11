#%%
import xarray as xr
import intake
import numpy as np
import intake_esm
# %%
import pandas as pd

pd.set_option("max_colwidth", None)  # makes the tables render better

import intake

try:
    import outtake
except:
    import sys

    print(
        """Could not load outtake - tape downloads might not work. Try adding

module use /work/k20200/k202134/hsm-tools/outtake/module
module load hsm-tools/unstable

to your ~./kernel_env file""",
        file=sys.stderr,
    )

# %%
def get_from_cat(catalog, columns):
    """A helper function for inspecting an intake catalog.

    Call with the catalog to be inspected and a list of columns of interest."""
    import pandas as pd

    pd.set_option("max_colwidth", None)  # makes the tables render better

    if type(columns) == type(""):
        columns = [columns]
    return (
        catalog.df[columns]
        .drop_duplicates()
        .sort_values(columns)
        .reset_index(drop=True)
    )
# %%
catalog_file = "/pool/data/CMIP6/main.yaml"
cat = intake.open_esm_datastore(catalog_file)
cat
# %%
