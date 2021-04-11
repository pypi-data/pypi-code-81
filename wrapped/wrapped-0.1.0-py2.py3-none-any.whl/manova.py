# %%
import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri

pandas2ri.activate()

# %% Import the necessary R functions
_r_manova = ro.r["manova"]
_r_as_formula = ro.r["as.formula"]
_r_summary = ro.r["summary"]

# %% Give R's MANOVA function a Python wrapper
def manova(formula, data):
    # with ro.conversion.localconverter(ro.default_converter + pandas2ri.converter):

    # Run R's MANOVA
    data = ro.conversion.py2rpy(data)
    formula = _r_as_formula(formula)
    ans = _r_manova(formula, data)
    summary = _r_summary(ans)

    # Package the results as a dataframe
    stats = summary[3][0].reshape(1, -1)
    columns = ["Df", "Pillai", "approx_F", "num_Df", "den_Df", "Pr(>F)"]
    summary = pd.DataFrame(stats, columns=columns)
    return summary


# %% Test on the iris datasets
import numpy as np
from sklearn.datasets import load_iris

# Get the iris dataset in a dataframe
iris = load_iris()
target = iris.target.reshape(-1, 1)
data = np.concatenate([iris.data, target], axis=1)
columns = ["col1", "col2", "col3", "col4", "label"]
df = pd.DataFrame(data, columns=columns)
df["label"] = df["label"].astype(int)
df.head()

# Run through MANOVA
formula = "cbind(col1, col2, col3, col4) ~ label"
summary = manova(formula, df)
summary.head()
