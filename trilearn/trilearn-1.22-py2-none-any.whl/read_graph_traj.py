import pandas as pd
import networkx as nx
import numpy as np
import networkx as nx                                                  
import matplotlib.pyplot as plt
from pandas.plotting import autocorrelation_plot
import seaborn as sns
 
from trilearn.graph import trajectory
import trilearn.graph.graph as glib
import trilearn.graph.decomposable as dlib
import trilearn.distributions.g_intra_class as gic
import trilearn.auxiliary_functions as aux
from trilearn.distributions import discrete_dec_log_linear as loglin
from trilearn import pgibbs
sns.set_style("whitegrid")

#aw_df = pd.read_csv("sample_data/czech_autoworkers.csv", header=[0, 1])
#np.random.seed(1)                                         
#aw_graph_traj = pgibbs.sample_trajectory_loglin(dataframe=aw_df, n_particles=10, n_samples=300, reset_cache=False)

#df = aw_graph_traj.graph_diff_trajectory_df() 

#df.to_csv("traj.csv", sep=";", index=False)

def edges_str_to_list(str):
    edges_str = str[1:-1].split(",")
    edges = [(int(edge.split("-")[0]), int(edge.split("-")[1])) for edge in edges_str if len(edge.split("-"))==2]
    return edges

df = pd.read_csv("traj.csv", sep=";")


adjmat = None
n_edges = 0
g = nx.Graph()
size = []

for index, row in df.iterrows():
    if row["index"] == 0:
        adjmat = nx.to_numpy_array(g)
    if row["index"] > 0:
        cur_index = df["index"].iloc[index]
        prev_index = df["index"].iloc[index-1]
        reps = cur_index - prev_index        
        adjmat += nx.to_numpy_matrix(g) * reps

    added = edges_str_to_list(row["added"])
    removed = edges_str_to_list(row["removed"])
    g.add_edges_from(added)
    g.remove_edges_from(removed)
    size.append(g.size())

df["size"] = size

print(adjmat / 300)

print(df)


newindex = pd.Series(range(300))
df2 = df[["index","size"]][2:].set_index("index") # removes the two first rows.

df2 = df2.reindex(newindex).reset_index().reindex(columns=df2.columns).fillna(method="ffill")

print(df2)

pd.plotting.autocorrelation_plot(df2["size"])
plt.savefig("autocorr.png")

print(df["index"].iloc[-1])